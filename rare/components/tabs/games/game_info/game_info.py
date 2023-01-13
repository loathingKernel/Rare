import os
import platform
import shutil
from logging import getLogger
from pathlib import Path
from typing import Dict, Optional

from PyQt5.QtCore import (
    QRunnable,
    Qt,
    pyqtSignal,
    QThreadPool,
    pyqtSlot,
)
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QMenu,
    QProgressBar,
    QPushButton,
    QWidget,
    QMessageBox,
    QWidgetAction,
)
from legendary.models.game import Game, InstalledGame

from rare.models.game import RareGame
from rare.models.install import InstallOptionsModel
from rare.shared import (
    LegendaryCoreSingleton,
    GlobalSignalsSingleton,
    ArgumentsSingleton,
    ImageManagerSingleton,
)
from rare.shared.image_manager import ImageSize
from rare.shared.workers.verify import VerifyWorker
from rare.ui.components.tabs.games.game_info.game_info import Ui_GameInfo
from rare.utils.misc import get_size
from rare.utils.steam_grades import SteamWorker
from rare.widgets.image_widget import ImageWidget
from .move_game import CopyGameInstallation, MoveGamePopUp, is_game_dir

logger = getLogger("GameInfo")


class GameInfo(QWidget):
    verification_finished = pyqtSignal(InstalledGame)
    uninstalled = pyqtSignal(str)

    def __init__(self, game_utils, parent=None):
        super(GameInfo, self).__init__(parent=parent)
        self.ui = Ui_GameInfo()
        self.ui.setupUi(self)
        self.core = LegendaryCoreSingleton()
        self.signals = GlobalSignalsSingleton()
        self.args = ArgumentsSingleton()
        self.image_manager = ImageManagerSingleton()
        self.game_utils = game_utils

        self.rgame: Optional[RareGame] = None
        # self.game: Optional[Game] = None
        # self.igame: Optional[InstalledGame] = None

        self.image = ImageWidget(self)
        self.image.setFixedSize(ImageSize.Display)
        self.ui.layout_game_info.insertWidget(0, self.image, alignment=Qt.AlignTop)

        if platform.system() == "Windows":
            self.ui.lbl_grade.setVisible(False)
            self.ui.grade.setVisible(False)
        else:
            self.steam_worker: SteamWorker = SteamWorker(self.core)
            self.steam_worker.signals.rating.connect(self.ui.grade.setText)
            self.steam_worker.setAutoDelete(False)

        self.ui.game_actions_stack.setCurrentIndex(0)
        self.ui.game_actions_stack.resize(self.ui.game_actions_stack.minimumSize())

        self.ui.uninstall_button.clicked.connect(self.uninstall)
        self.ui.verify_button.clicked.connect(self.verify)

        self.verify_pool = QThreadPool()
        self.verify_pool.setMaxThreadCount(2)
        if self.args.offline:
            self.ui.repair_button.setDisabled(True)
        else:
            self.ui.repair_button.clicked.connect(self.repair)

        self.ui.install_button.clicked.connect(self.install)

        self.move_game_pop_up = MoveGamePopUp()
        self.move_action = QWidgetAction(self)
        self.move_action.setDefaultWidget(self.move_game_pop_up)
        self.ui.move_button.setMenu(QMenu())
        self.ui.move_button.menu().addAction(self.move_action)

        self.progress_of_moving = QProgressBar()
        self.existing_game_dir = False
        self.is_moving = False
        self.game_moving = None
        self.dest_path_with_suffix = None

        self.widget_container = QWidget()
        box_layout = QHBoxLayout()
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.addWidget(self.ui.move_button)
        self.widget_container.setLayout(box_layout)
        index = self.ui.move_stack.addWidget(self.widget_container)
        self.ui.move_stack.setCurrentIndex(index)
        self.move_game_pop_up.browse_done.connect(self.show_menu_after_browse)
        self.move_game_pop_up.move_clicked.connect(self.ui.move_button.menu().close)
        self.move_game_pop_up.move_clicked.connect(self.move_game)

    @pyqtSlot()
    def install(self):
        if self.rgame.is_origin:
            self.game_utils.launch_game(self.rgame.app_name)
        else:
            self.rgame.install()

    # FIXME: Move to RareGame
    @pyqtSlot()
    def uninstall(self):
        if self.game_utils.uninstall_game(self.rgame.app_name):
            self.game_utils.update_list.emit(self.rgame.app_name)
            self.signals.game.uninstalled.emit(self.rgame.app_name)

    @pyqtSlot()
    def repair(self):
        """ This function is to be called from the button only """
        repair_file = os.path.join(self.core.lgd.get_tmp_path(), f"{self.rgame.app_name}.repair")
        if not os.path.exists(repair_file):
            QMessageBox.warning(
                self,
                self.tr("Error - {}").format(self.rgame.title),
                self.tr(
                    "Repair file does not exist or game does not need a repair. Please verify game first"
                ),
            )
            return
        self.repair_game(self.rgame)

    def repair_game(self, rgame: RareGame):
        rgame.update_game()
        ans = False
        if rgame.has_update:
            ans = QMessageBox.question(
                self,
                self.tr("Repair and update?"),
                self.tr(
                    "There is an update for <b>{}</b> from <b>{}</b> to <b>{}</b>. "
                    "Do you want to update the game while repairing it?"
                ).format(rgame.title, rgame.version, rgame.remote_version),
            ) == QMessageBox.Yes
        rgame.repair(repair_and_update=ans)

    @pyqtSlot()
    def verify(self):
        """ This function is to be called from the button only """
        if not os.path.exists(self.rgame.igame.install_path):
            logger.error(f"Installation path {self.rgame.igame.install_path} for {self.rgame.title} does not exist")
            QMessageBox.warning(
                self,
                self.tr("Error - {}").format(self.rgame.title),
                self.tr("Installation path for <b>{}</b> does not exist. Cannot continue.").format(self.rgame.title),
            )
            return
        self.verify_game(self.rgame)

    def verify_game(self, rgame: RareGame):
        self.ui.verify_widget.setCurrentIndex(1)
        verify_worker = VerifyWorker(rgame, self.core, self.args)
        verify_worker.signals.status.connect(self.verify_status)
        verify_worker.signals.result.connect(self.verify_result)
        verify_worker.signals.error.connect(self.verify_error)
        self.ui.verify_progress.setValue(0)
        self.rgame.active_worker = verify_worker
        self.verify_pool.start(verify_worker)
        self.ui.move_button.setEnabled(False)

    def verify_cleanup(self, rgame: RareGame):
        self.ui.verify_widget.setCurrentIndex(0)
        rgame.active_worker = None
        self.ui.move_button.setEnabled(True)
        self.ui.verify_button.setEnabled(True)

    @pyqtSlot(RareGame, str)
    def verify_error(self, rgame: RareGame, message):
        self.verify_cleanup(rgame)
        QMessageBox.warning(
            self,
            self.tr("Error - {}").format(rgame.title),
            message
        )

    @pyqtSlot(RareGame, int, int, float, float)
    def verify_status(self, rgame: RareGame, num, total, percentage, speed):
        self.ui.verify_progress.setValue(num * 100 // total)

    @pyqtSlot(RareGame, bool, int, int)
    def verify_result(self, rgame: RareGame, success, failed, missing):
        self.verify_cleanup(rgame)
        self.ui.repair_button.setDisabled(success)
        if success:
            QMessageBox.information(
                self,
                self.tr("Summary - {}").format(rgame.title),
                self.tr("<b>{}</b> has been verified successfully. "
                        "No missing or corrupt files found").format(rgame.title),
            )
            self.verification_finished.emit(rgame.igame)
        else:
            ans = QMessageBox.question(
                self,
                self.tr("Summary - {}").format(rgame.title),
                self.tr(
                    "Verification failed, <b>{}</b> file(s) corrupted, <b>{}</b> file(s) are missing. "
                    "Do you want to repair them?"
                ).format(failed, missing),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if ans == QMessageBox.Yes:
                self.repair_game(rgame)

    @pyqtSlot(str)
    def move_game(self, dest_path):
        dest_path = Path(dest_path)
        install_path = Path(self.rgame.igame.install_path)
        self.dest_path_with_suffix = dest_path.joinpath(install_path.stem)

        if self.dest_path_with_suffix.is_dir():
            self.existing_game_dir = is_game_dir(install_path, self.dest_path_with_suffix)

        if not self.existing_game_dir:
            for i in dest_path.iterdir():
                if install_path.stem in i.stem:
                    warn_msg = QMessageBox()
                    warn_msg.setText(self.tr("Destination file/directory exists."))
                    warn_msg.setInformativeText(
                        self.tr("Do you really want to overwrite it? This will delete {}").format(
                            self.dest_path_with_suffix
                        )
                    )
                    warn_msg.addButton(QPushButton(self.tr("Yes")), QMessageBox.YesRole)
                    warn_msg.addButton(QPushButton(self.tr("No")), QMessageBox.NoRole)

                    response = warn_msg.exec()

                    if response != 0:
                        return

                    # Not using pathlib, since we can't delete not-empty folders. With shutil we can.
                    if self.dest_path_with_suffix.is_dir():
                        shutil.rmtree(self.dest_path_with_suffix)
                    else:
                        self.dest_path_with_suffix.unlink()
        self.ui.move_stack.addWidget(self.progress_of_moving)
        self.ui.move_stack.setCurrentWidget(self.progress_of_moving)

        self.game_moving = self.rgame.app_name
        self.is_moving = True

        self.ui.verify_button.setEnabled(False)

        if self.move_game_pop_up.is_different_drive(str(dest_path), str(install_path)):
            # Destination dir on different drive
            self.start_copy_diff_drive()
        else:
            # Destination dir on same drive
            shutil.move(self.rgame.igame.install_path, dest_path)
            self.set_new_game(self.dest_path_with_suffix)

    def update_progressbar(self, progress_int):
        self.progress_of_moving.setValue(progress_int)

    def start_copy_diff_drive(self):
        copy_worker = CopyGameInstallation(
            install_path=self.rgame.igame.install_path,
            dest_path=self.dest_path_with_suffix,
            is_existing_dir=self.existing_game_dir,
            igame=self.rgame.igame,
        )

        copy_worker.signals.progress.connect(self.update_progressbar)
        copy_worker.signals.finished.connect(self.set_new_game)
        copy_worker.signals.no_space_left.connect(self.warn_no_space_left)
        QThreadPool.globalInstance().start(copy_worker)

    def move_helper_clean_up(self):
        self.ui.move_stack.setCurrentWidget(self.ui.move_button)
        self.move_game_pop_up.refresh_indicator()
        self.is_moving = False
        self.game_moving = None
        self.ui.verify_button.setEnabled(True)
        self.ui.move_button.setEnabled(True)

    # This func does the needed UI changes, e.g. changing back to the initial move tool button and other stuff
    def warn_no_space_left(self):
        err_msg = QMessageBox()
        err_msg.setText(self.tr("Out of space or unknown OS error occured."))
        err_msg.exec()
        self.move_helper_clean_up()

    # Sets all needed variables to the new path.
    def set_new_game(self, dest_path_with_suffix):
        self.ui.install_path.setText(str(dest_path_with_suffix))
        self.rgame.igame.install_path = str(dest_path_with_suffix)
        self.core.lgd.set_installed_game(self.rgame.app_name, self.rgame.igame)
        self.move_game_pop_up.install_path = self.rgame.igame.install_path

        self.move_helper_clean_up()

    # We need to re-show the menu, as after clicking on browse, the whole menu gets closed.
    # Otherwise, the user would need to click on the move button again to open it again.
    def show_menu_after_browse(self):
        self.ui.move_button.showMenu()

    def update_game(self, rgame: RareGame):
        if self.rgame is not None:
            if (worker := self.rgame.active_worker) is not None:
                if isinstance(worker, VerifyWorker):
                    try:
                        worker.signals.status.disconnect(self.verify_status)
                    except TypeError as e:
                        logger.warning(f"{self.rgame.app_title} verify worker: {e}")
        self.rgame = rgame
        if (worker := self.rgame.active_worker) is None:
            self.ui.verify_widget.setCurrentIndex(0)
        elif isinstance(worker, VerifyWorker):
            self.ui.verify_widget.setCurrentIndex(1)
            self.ui.verify_progress.setValue(self.rgame.progress)
            worker.signals.status.connect(self.verify_status)
        # FIXME: Use RareGame for the rest of the code
        # self.game = rgame.game
        # self.igame = rgame.igame
        self.title.setTitle(self.rgame.app_title)

        self.image.setPixmap(rgame.pixmap)

        self.ui.app_name.setText(self.rgame.app_name)
        self.ui.version.setText(self.rgame.version)
        self.ui.dev.setText(self.rgame.developer)

        if self.rgame.igame:
            self.ui.install_size.setText(get_size(self.rgame.igame.install_size))
            self.ui.install_path.setText(self.rgame.igame.install_path)
            self.ui.platform.setText(self.rgame.igame.platform)
        elif self.rgame.is_origin and self.rgame.is_installed:
            self.ui.install_path.setText(self.rgame.install_path)
        else:
            self.ui.install_size.setText("N/A")
            self.ui.install_path.setText("N/A")
            self.ui.platform.setText("Windows")

        self.ui.install_size.setEnabled(bool(self.rgame.igame))
        self.ui.lbl_install_size.setEnabled(bool(self.rgame.igame))
        self.ui.install_path.setEnabled(bool(self.rgame.is_installed))
        self.ui.lbl_install_path.setEnabled(bool(self.rgame.is_installed))

        self.ui.uninstall_button.setEnabled(bool(self.rgame.igame))
        self.ui.verify_button.setEnabled(bool(self.rgame.igame))
        self.ui.repair_button.setEnabled(bool(self.rgame.igame))

        if not self.rgame.igame:
            self.ui.game_actions_stack.setCurrentIndex(1)
            if self.rgame.is_origin:
                self.ui.version.setText("N/A")
                self.ui.version.setEnabled(False)
                self.ui.install_button.setText(self.tr("Link to Origin/Launch"))
            else:
                self.ui.install_button.setText(self.tr("Install"))
        else:
            if not self.args.offline:
                self.ui.repair_button.setDisabled(
                    not os.path.exists(os.path.join(self.core.lgd.get_tmp_path(), f"{self.rgame.app_name}.repair"))
                )
            self.ui.game_actions_stack.setCurrentIndex(0)

        grade_visible = not self.rgame.is_unreal and platform.system() != "Windows"
        self.ui.grade.setVisible(grade_visible)
        self.ui.lbl_grade.setVisible(grade_visible)

        if platform.system() != "Windows" and not self.rgame.is_unreal:
            self.ui.grade.setText(self.tr("Loading"))
            self.steam_worker.set_app_name(self.rgame.app_name)
            QThreadPool.globalInstance().start(self.steam_worker)

        # If the game that is currently moving matches with the current app_name, we show the progressbar.
        # Otherwhise, we show the move tool button.
        if self.rgame.igame is not None:
            if self.game_moving == self.rgame.app_name:
                index = self.ui.move_stack.addWidget(self.progress_of_moving)
            else:
                index = self.ui.move_stack.addWidget(self.ui.move_button)
            self.ui.move_stack.setCurrentIndex(index)
        # If a game is verifying or moving, disable both verify and moving buttons.
        if rgame.active_worker is not None:
            self.ui.verify_button.setEnabled(False)
            self.ui.move_button.setEnabled(False)
        if self.is_moving:
            self.ui.move_button.setEnabled(False)
            self.ui.verify_button.setEnabled(False)

        self.move_game_pop_up.update_game(rgame.app_name)


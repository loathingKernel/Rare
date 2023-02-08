import os
from logging import getLogger

from PyQt5.QtCore import QThreadPool, QSettings
from PyQt5.QtWidgets import QWidget, QFileDialog, QLabel, QPushButton, QSizePolicy, QMessageBox, QStackedWidget, \
    QGroupBox
from legendary.models.game import SaveGameStatus

from rare.models.game import RareGame
from rare.shared import LegendaryCoreSingleton
from rare.shared.workers.wine_resolver import WineResolver
from rare.ui.components.tabs.games.game_info.cloud_widget import Ui_CloudWidget
from rare.ui.components.tabs.games.game_info.sync_widget import Ui_SyncWidget
from rare.utils.misc import icon, get_raw_save_path
from rare.widgets.indicator_edit import PathEdit, IndicatorReasonsCommon

logger = getLogger("CloudWidget")


class CloudSaveTab(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_widget = QWidget()
        self.ui = Ui_SyncWidget()
        self.ui.setupUi(self.main_widget)
        self.addWidget(self.main_widget)
        self.change = True

        self.info_label = QLabel(self.tr("This game doesn't support cloud saves"))
        self.addWidget(self.info_label)

        self.core = LegendaryCoreSingleton()
        self.settings = QSettings()

        self.ui.icon_local.setPixmap(icon("mdi.harddisk", "fa.desktop").pixmap(128, 128))
        self.ui.icon_remote.setPixmap(icon("mdi.cloud-outline", "ei.cloud").pixmap(128, 128))

        self.ui.upload_button.clicked.connect(self.upload)
        self.ui.download_button.clicked.connect(self.download)
        self.rgame: RareGame = None

        self.cloud_widget = QGroupBox(self)
        self.cloud_widget_ui = Ui_CloudWidget()
        self.cloud_widget_ui.setupUi(self.cloud_widget)

        self.ui.options_layout.addWidget(self.cloud_widget)

        self.cloud_save_path_edit = PathEdit(
            "",
            file_type=QFileDialog.DirectoryOnly,
            placeholder=self.tr("Cloud save path"),
            edit_func=lambda text: (True, text, None)
            if os.path.exists(text)
            else (False, text, IndicatorReasonsCommon.DIR_NOT_EXISTS),
            save_func=self.save_save_path,
        )
        self.cloud_widget_ui.cloud_layout.addRow(QLabel(self.tr("Save path")), self.cloud_save_path_edit)

        self.compute_save_path_button = QPushButton(icon("fa.magic"), self.tr("Auto compute save path"))
        self.compute_save_path_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.compute_save_path_button.clicked.connect(self.compute_save_path)
        self.cloud_widget_ui.cloud_layout.addRow(None, self.compute_save_path_button)

        self.cloud_widget_ui.cloud_sync.stateChanged.connect(
            lambda: self.settings.setValue(
                f"{self.rgame.app_name}/auto_sync_cloud", self.cloud_widget_ui.cloud_sync.isChecked()
            )
        )

    def upload(self):
        self.ui.upload_button.setDisabled(True)
        self.ui.download_button.setDisabled(True)
        self.rgame.upload_saves()

    def download(self):
        self.ui.upload_button.setDisabled(True)
        self.ui.download_button.setDisabled(True)
        self.rgame.download_saves()

    def compute_save_path(self):
        if self.core.is_installed(self.rgame.app_name) and self.rgame.game.supports_cloud_saves:
            try:
                new_path = self.core.get_save_path(self.rgame.app_name)
            except Exception as e:
                logger.warning(str(e))
                resolver = WineResolver(self.core, get_raw_save_path(self.rgame.game), self.rgame.app_name)
                if not resolver.wine_env.get("WINEPREFIX"):
                    self.cloud_save_path_edit.setText("")
                    QMessageBox.warning(self, "Warning", "No wine prefix selected. Please set it in settings")
                    return
                self.cloud_save_path_edit.setText(self.tr("Loading"))
                self.cloud_save_path_edit.setDisabled(True)
                self.compute_save_path_button.setDisabled(True)

                app_name = self.rgame.app_name[:]
                resolver.signals.result_ready.connect(lambda x: self.wine_resolver_finished(x, app_name))
                QThreadPool.globalInstance().start(resolver)
                return
            else:
                self.cloud_save_path_edit.setText(new_path)

    def wine_resolver_finished(self, path, app_name):
        logger.info(f"Wine resolver finished for {app_name}. Computed save path: {path}")
        if app_name == self.rgame.app_name:
            self.cloud_save_path_edit.setDisabled(False)
            self.compute_save_path_button.setDisabled(False)
            if path and not os.path.exists(path):
                try:
                    os.makedirs(path)
                except PermissionError:
                    self.cloud_save_path_edit.setText("")
                    QMessageBox.warning(
                        None,
                        "Error",
                        self.tr("Error while launching {}. No permission to create {}").format(
                            self.rgame.title, path
                        ),
                    )
                    return
            if not path:
                self.cloud_save_path_edit.setText("")
                return
            self.cloud_save_path_edit.setText(path)
        elif path:
            igame = self.core.get_installed_game(app_name)
            igame.save_path = path
            self.core.lgd.set_installed_game(app_name, igame)

    def save_save_path(self, text):
        if self.rgame.game.supports_cloud_saves and self.change:
            self.rgame.igame.save_path = text
            self.core.lgd.set_installed_game(self.rgame.app_name, self.rgame.igame)

    def __set_buttons_disabled(self, disabled: bool = True):
        self.ui.upload_button.setDisabled(disabled)
        self.ui.download_button.setDisabled(disabled)

    def state_update(self):
        self.__set_buttons_disabled(self.rgame.state in [RareGame.State.SYNCING, RareGame.State.RUNNING])
        if self.rgame.save.res == SaveGameStatus.LOCAL_NEWER:
            self.ui.local_new_label.setVisible(True)
            self.ui.cloud_new_label.setVisible(False)
        elif self.rgame.save.res == SaveGameStatus.REMOTE_NEWER:
            self.ui.local_new_label.setVisible(False)
            self.ui.cloud_new_label.setVisible(True)
        else:
            self.ui.local_new_label.setVisible(False)
            self.ui.cloud_new_label.setVisible(False)

        if hasattr(self.rgame.igame, "save_path") and self.rgame.igame.save_path:
            self.cloud_save_path_edit.setText(self.rgame.igame.save_path)
            dt_local = self.rgame.save.dt_local
            dt_remote = self.rgame.save.dt_remote
            self.ui.date_info_local.setText(dt_local.strftime("%A, %d. %B %Y %X") if dt_local else "None")
            self.ui.date_info_remote.setText(dt_remote.strftime("%A, %d. %B %Y %X") if dt_remote else "None")
        else:
            self.cloud_save_path_edit.setText("")

    def update_game(self, rgame: RareGame):
        if self.rgame:
            self.rgame.signals.widget.update.disconnect(self.state_update)
        self.rgame = rgame
        self.title.setTitle(rgame.title)
        if not rgame.igame or not rgame.game.supports_cloud_saves:
            self.setCurrentIndex(1)
            self.setDisabled(True)
            return

        self.rgame.signals.widget.update.connect(self.state_update)
        self.change = False
        self.setDisabled(False)
        self.setCurrentIndex(0)

        self.state_update()

        sync_cloud = self.settings.value(f"{self.rgame.app_name}/auto_sync_cloud", True, bool)
        self.cloud_widget_ui.cloud_sync.setChecked(sync_cloud)

        self.change = True

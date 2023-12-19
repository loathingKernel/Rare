import os
import platform as pf
import shutil
from typing import Tuple, List, Union, Optional

from PyQt5.QtCore import QThreadPool, QSettings
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QFileDialog, QCheckBox, QWidget, QVBoxLayout, QFormLayout
from legendary.utils.selective_dl import get_sdl_appname

from rare.models.game import RareGame
from rare.models.install import InstallDownloadModel, InstallQueueItemModel, InstallOptionsModel
from rare.shared.workers.install_info import InstallInfoWorker
from rare.ui.components.dialogs.install_dialog import Ui_InstallDialog
from rare.ui.components.dialogs.install_dialog_advanced import Ui_InstallDialogAdvanced
from rare.utils.misc import format_size, icon
from rare.widgets.dialogs import ActionDialog, dialog_title_game
from rare.widgets.collapsible_widget import CollapsibleFrame
from rare.widgets.indicator_edit import PathEdit, IndicatorReasonsCommon


class InstallDialogAdvanced(CollapsibleFrame):
    def __init__(self, parent=None):
        widget = QWidget(parent)
        title = widget.tr("Advanced options")
        self.ui = Ui_InstallDialogAdvanced()
        self.ui.setupUi(widget)
        super(InstallDialogAdvanced, self).__init__(widget=widget, title=title, parent=parent)


class InstallDialog(ActionDialog):
    result_ready = pyqtSignal(InstallQueueItemModel)

    def __init__(self, rgame: RareGame, options: InstallOptionsModel, parent=None):
        super(InstallDialog, self).__init__(parent=parent)

        header = self.tr("Install")
        bicon = icon("ri.install-line")
        if options.repair_mode:
            header = self.tr("Repair")
            bicon = icon("fa.wrench")
            if options.repair_and_update:
                header = self.tr("Repair and update")
        elif options.update:
            header = self.tr("Update")
        elif options.reset_sdl:
            header = self.tr("Modify")
            bicon = icon("fa.gear")
        self.setWindowTitle(dialog_title_game(header, rgame.app_title))

        install_widget = QWidget(self)
        self.ui = Ui_InstallDialog()
        self.ui.setupUi(install_widget)

        self.ui.title_label.setText(f"<h4>{dialog_title_game(header, rgame.app_title)}</h4>")

        self.core = rgame.core
        self.rgame = rgame
        self.__options: InstallOptionsModel = options
        self.__download: Optional[InstallDownloadModel] = None
        self.__queue_item: Optional[InstallQueueItemModel] = None

        self.advanced = InstallDialogAdvanced(parent=self)
        self.ui.advanced_layout.addWidget(self.advanced)

        self.selectable = CollapsibleFrame(widget=None, title=self.tr("Optional downloads"), parent=self)
        self.ui.selectable_layout.addWidget(self.selectable)

        self.options_changed = False

        self.threadpool = QThreadPool(self)
        self.threadpool.setMaxThreadCount(1)

        if options.base_path:
            base_path = options.base_path
        elif rgame.is_installed:
            base_path = rgame.install_path
        else:
            base_path = self.core.get_default_install_dir(rgame.default_platform)

        self.install_dir_edit = PathEdit(
            path=base_path,
            file_mode=QFileDialog.DirectoryOnly,
            edit_func=self.option_changed,
            save_func=self.save_install_edit,
            parent=self,
        )
        self.ui.main_layout.setWidget(
            self.ui.main_layout.getWidgetPosition(self.ui.install_dir_label)[0],
            QFormLayout.FieldRole, self.install_dir_edit
        )

        self.install_dir_edit.setDisabled(rgame.is_installed)
        self.ui.install_dir_label.setDisabled(rgame.is_installed)
        self.ui.shortcut_label.setDisabled(rgame.is_installed)
        self.ui.shortcut_check.setDisabled(rgame.is_installed)
        self.ui.shortcut_check.setChecked(not rgame.is_installed and QSettings().value("create_shortcut", True, bool))

        self.error_box()

        self.ui.platform_combo.addItems(reversed(rgame.platforms))
        combo_text = rgame.igame.platform if rgame.is_installed else rgame.default_platform
        self.ui.platform_combo.setCurrentIndex(self.ui.platform_combo.findText(combo_text))
        self.ui.platform_combo.currentIndexChanged.connect(lambda i: self.option_changed(None))
        self.ui.platform_combo.currentIndexChanged.connect(self.check_incompatible_platform)
        self.ui.platform_combo.currentIndexChanged.connect(self.reset_install_dir)
        self.ui.platform_combo.currentIndexChanged.connect(self.reset_sdl_list)

        self.ui.platform_label.setDisabled(rgame.is_installed)
        self.ui.platform_combo.setDisabled(rgame.is_installed)

        # if we are repairing, disable the SDL selection and open the dialog frame to be visible
        self.selectable.setDisabled(options.repair_mode and not options.repair_and_update)
        if options.repair_mode and not options.repair_and_update:
            self.selectable.click()

        self.advanced.ui.max_workers_spin.setValue(self.core.lgd.config.getint("Legendary", "max_workers", fallback=0))
        self.advanced.ui.max_workers_spin.valueChanged.connect(self.option_changed)

        self.advanced.ui.max_memory_spin.setValue(self.core.lgd.config.getint("Legendary", "max_memory", fallback=0))
        self.advanced.ui.max_memory_spin.valueChanged.connect(self.option_changed)

        self.advanced.ui.dl_optimizations_check.stateChanged.connect(self.option_changed)
        self.advanced.ui.force_download_check.stateChanged.connect(self.option_changed)
        self.advanced.ui.ignore_space_check.stateChanged.connect(self.option_changed)
        self.advanced.ui.download_only_check.stateChanged.connect(
            lambda: self.non_reload_option_changed("download_only")
        )
        self.ui.shortcut_check.stateChanged.connect(
            lambda: self.non_reload_option_changed("shortcut")
        )

        self.selectable_checks: List[TagCheckBox] = []
        self.config_tags: Optional[List[str]] = None

        self.reset_install_dir(self.ui.platform_combo.currentIndex())
        self.reset_sdl_list(self.ui.platform_combo.currentIndex())
        self.check_incompatible_platform(self.ui.platform_combo.currentIndex())

        self.accept_button.setEnabled(False)

        if self.__options.overlay:
            self.ui.platform_label.setEnabled(False)
            self.ui.platform_combo.setEnabled(False)
            self.advanced.ui.ignore_space_label.setEnabled(False)
            self.advanced.ui.ignore_space_check.setEnabled(False)
            self.advanced.ui.download_only_label.setEnabled(False)
            self.advanced.ui.download_only_check.setEnabled(False)
            self.ui.shortcut_label.setEnabled(False)
            self.ui.shortcut_check.setEnabled(False)
            self.selectable.setEnabled(False)

        if pf.system() == "Darwin":
            self.ui.shortcut_label.setDisabled(True)
            self.ui.shortcut_check.setDisabled(True)
            self.ui.shortcut_check.setChecked(False)
            self.ui.shortcut_check.setToolTip(self.tr("Creating a shortcut is not supported on macOS"))

        self.advanced.ui.install_prereqs_label.setEnabled(False)
        self.advanced.ui.install_prereqs_check.setEnabled(False)
        self.advanced.ui.install_prereqs_check.stateChanged.connect(
            lambda: self.non_reload_option_changed("install_prereqs")
        )

        self.non_reload_option_changed("shortcut")

        self.advanced.ui.install_prereqs_check.setChecked(self.__options.install_prereqs)

        # lk: set object names for CSS properties
        self.accept_button.setText(header)
        self.accept_button.setIcon(bicon)
        self.accept_button.setObjectName("InstallButton")

        self.action_button.setText(self.tr("Verify"))
        self.action_button.setIcon(icon("fa.check"))

        self.setCentralWidget(install_widget)

    def showEvent(self, a0: QShowEvent) -> None:
        if a0.spontaneous():
            return super().showEvent(a0)
        self.save_install_edit(self.install_dir_edit.text())
        super().showEvent(a0)

    def execute(self):
        if self.__options.silent:
            self.get_download_info()
        else:
            self.action_handler()
            self.open()

    @pyqtSlot(int)
    def reset_install_dir(self, index: int):
        if not self.rgame.is_installed:
            platform = self.ui.platform_combo.itemText(index)
            default_dir = self.core.get_default_install_dir(platform)
            self.install_dir_edit.setText(default_dir)

    @pyqtSlot(int)
    def reset_sdl_list(self, index: int):
        platform = self.ui.platform_combo.itemText(index)
        for cb in self.selectable_checks:
            cb.disconnect()
            cb.deleteLater()
        self.selectable_checks.clear()

        if config_tags := self.core.lgd.config.get(self.rgame.app_name, 'install_tags', fallback=None):
            self.config_tags = config_tags.split(",")
        config_disable_sdl = self.core.lgd.config.getboolean(self.rgame.app_name, 'disable_sdl', fallback=False)
        sdl_name = get_sdl_appname(self.rgame.app_name)
        if not config_disable_sdl and sdl_name is not None:
            sdl_data = self.core.get_sdl_data(sdl_name, platform=platform)
            if sdl_data:
                widget = QWidget(self.selectable)
                layout = QVBoxLayout(widget)
                layout.setSpacing(0)
                for tag, info in sdl_data.items():
                    cb = TagCheckBox(info["name"].strip(), info["description"].strip(), info["tags"])
                    if tag == "__required":
                        cb.setChecked(True)
                        cb.setDisabled(True)
                    if self.config_tags is not None:
                        if all(elem in self.config_tags for elem in info["tags"]):
                            cb.setChecked(True)
                    layout.addWidget(cb)
                    self.selectable_checks.append(cb)
                for cb in self.selectable_checks:
                    cb.stateChanged.connect(self.option_changed)
                self.selectable.setWidget(widget)
        else:
            self.selectable.setDisabled(True)

    @pyqtSlot(int)
    def check_incompatible_platform(self, index: int):
        platform = self.ui.platform_combo.itemText(index)
        if platform == "Mac" and pf.system() != "Darwin":
            self.error_box(
                self.tr("Warning"),
                self.tr("You will not be able to run the game if you select <b>{}</b> as platform").format(platform)
            )
        else:
            self.error_box()

    def get_options(self):
        self.__options.base_path = "" if self.rgame.is_installed else self.install_dir_edit.text()
        self.__options.max_workers = self.advanced.ui.max_workers_spin.value()
        self.__options.shared_memory = self.advanced.ui.max_memory_spin.value()
        self.__options.order_opt = self.advanced.ui.dl_optimizations_check.isChecked()
        self.__options.force = self.advanced.ui.force_download_check.isChecked()
        self.__options.ignore_space = self.advanced.ui.ignore_space_check.isChecked()
        self.__options.no_install = self.advanced.ui.download_only_check.isChecked()
        self.__options.platform = self.ui.platform_combo.currentText()
        self.__options.install_prereqs = self.advanced.ui.install_prereqs_check.isChecked()
        self.__options.create_shortcut = self.ui.shortcut_check.isChecked()
        if self.selectable_checks:
            self.__options.install_tag = [""]
            for cb in self.selectable_checks:
                if data := cb.isChecked():
                    # noinspection PyTypeChecker
                    self.__options.install_tag.extend(data)

    def get_download_info(self):
        self.__download = None
        info_worker = InstallInfoWorker(self.core, self.__options)
        info_worker.signals.result.connect(self.on_worker_result)
        info_worker.signals.failed.connect(self.on_worker_failed)
        self.threadpool.start(info_worker)

    def action_handler(self):
        self.error_box()
        message = self.tr("Updating...")
        self.ui.download_size_text.setText(message)
        self.ui.download_size_text.setStyleSheet("font-style: italic; font-weight: normal")
        self.ui.install_size_text.setText(message)
        self.ui.install_size_text.setStyleSheet("font-style: italic; font-weight: normal")
        self.setActive(True)
        self.options_changed = False
        self.get_options()
        self.get_download_info()

    def option_changed(self, path) -> Tuple[bool, str, int]:
        self.options_changed = True
        self.accept_button.setEnabled(False)
        self.action_button.setEnabled(not self.active())
        return True, path, IndicatorReasonsCommon.VALID

    def save_install_edit(self, path: str):
        if not os.path.exists(path):
            return
        _, _, free_space = shutil.disk_usage(path)
        self.ui.avail_space.setText(format_size(free_space))

    def non_reload_option_changed(self, option: str):
        if option == "download_only":
            self.__options.no_install = self.advanced.ui.download_only_check.isChecked()
        elif option == "shortcut":
            QSettings().setValue("create_shortcut", self.ui.shortcut_check.isChecked())
            self.__options.create_shortcut = self.ui.shortcut_check.isChecked()
        elif option == "install_prereqs":
            self.__options.install_prereqs = self.advanced.ui.install_prereqs_check.isChecked()

    @staticmethod
    def same_platform(download: InstallDownloadModel) -> bool:
        platform = download.igame.platform
        if pf.system() == "Windows":
            return platform == "Windows" or platform == "Win32"
        elif pf.system() == "Darwin":
            return platform == "Mac"
        else:
            return False

    @pyqtSlot(InstallDownloadModel)
    def on_worker_result(self, download: InstallDownloadModel):
        self.setActive(False)
        self.__download = download
        download_size = download.analysis.dl_size
        install_size = download.analysis.install_size
        # install_size = self.dl_item.download.analysis.disk_space_delta
        if download_size or (not download_size and (download.game.is_dlc or download.repair)):
            self.ui.download_size_text.setText(format_size(download_size))
            self.ui.download_size_text.setStyleSheet("font-style: normal; font-weight: bold")
            self.accept_button.setEnabled(not self.options_changed)
        else:
            self.ui.install_size_text.setText(self.tr("Game already installed"))
            self.ui.install_size_text.setStyleSheet("font-style: italics; font-weight: normal")
        self.ui.install_size_text.setText(format_size(install_size))
        self.ui.install_size_text.setStyleSheet("font-style: normal; font-weight: bold")
        self.action_button.setEnabled(self.options_changed)
        has_prereqs = bool(download.igame.prereq_info) and not download.igame.prereq_info.get("installed", False)
        if has_prereqs:
            prereq_name = download.igame.prereq_info.get("name", "")
            prereq_path = os.path.split(download.igame.prereq_info.get("path", ""))[-1]
            prereq_desc = prereq_name if prereq_name else prereq_path
            self.advanced.ui.install_prereqs_check.setText(self.tr("Also install: {}").format(prereq_desc))
        else:
            self.advanced.ui.install_prereqs_check.setText("")
        # Offer to install prerequisites only on same platforms
        self.advanced.ui.install_prereqs_label.setEnabled(has_prereqs)
        self.advanced.ui.install_prereqs_check.setEnabled(has_prereqs)
        self.advanced.ui.install_prereqs_check.setChecked(has_prereqs and self.same_platform(download))
        if self.__options.silent:
            self.accept()

    def on_worker_failed(self, message: str):
        self.setActive(False)
        error_text = self.tr("Error")
        self.ui.download_size_text.setText(error_text)
        self.ui.install_size_text.setText(error_text)
        self.error_box(error_text, message)
        self.action_button.setEnabled(self.options_changed)
        if self.__options.silent:
            self.open()

    def error_box(self, label: str = "", message: str = ""):
        self.ui.warning_label.setVisible(bool(label))
        self.ui.warning_label.setText(label)
        self.ui.warning_text.setVisible(bool(message))
        self.ui.warning_text.setText(message)

    def done_handler(self):
        self.threadpool.clear()
        self.threadpool.waitForDone()
        self.result_ready.emit(self.__queue_item)

    # lk: __download is already set at this point so just do nothing.
    def accept_handler(self):
        self.__queue_item = InstallQueueItemModel(options=self.__options, download=self.__download)

    def reject_handler(self):
        # FIXME: This is implemented through the selective downloads dialog now. remove soon
        # if self.config_tags is not None:
        #     config_helper.set_option(self.rgame.app_name, 'install_tags', ','.join(self.config_tags))
        # else:
        #     # lk: this is purely for cleaning any install tags we might have added erroneously to the config
        #     config_helper.remove_option(self.rgame.app_name, 'install_tags')
        self.__queue_item = InstallQueueItemModel(options=self.__options, download=None)


class TagCheckBox(QCheckBox):
    def __init__(self, text, desc, tags: List[str], parent=None):
        super(TagCheckBox, self).__init__(parent)
        self.setText(text)
        self.setToolTip(desc)
        self.tags = tags

    def isChecked(self) -> Union[bool, List[str]]:
        return self.tags if super(TagCheckBox, self).isChecked() else False




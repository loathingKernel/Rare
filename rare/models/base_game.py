from abc import abstractmethod
from ctypes import c_uint64
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from logging import getLogger
from typing import Optional, List

from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool, QSettings
from legendary.models.game import SaveGameFile, SaveGameStatus, Game, InstalledGame

from rare.lgndr.core import LegendaryCore
from rare.models.install import UninstallOptionsModel, InstallOptionsModel

logger = getLogger("RareGameBase")


class RareGameBase(QObject):
    @dataclass
    class Save:
        latest_save: SaveGameFile
        saves: list[SaveGameFile]
        res: SaveGameStatus
        dt_remote: datetime
        dt_local: datetime

    class State(IntEnum):
        IDLE = 0
        RUNNING = 1
        DOWNLOADING = 2
        VERIFYING = 3
        MOVING = 4
        UNINSTALLING = 5
        SYNCING = 6

    class Signals:
        class Progress(QObject):
            start = pyqtSignal()
            update = pyqtSignal(int)
            finish = pyqtSignal(bool)

        class Widget(QObject):
            update = pyqtSignal()

        class Download(QObject):
            enqueue = pyqtSignal(str)
            dequeue = pyqtSignal(str)

        class Game(QObject):
            install = pyqtSignal(InstallOptionsModel)
            installed = pyqtSignal(str)
            uninstall = pyqtSignal(UninstallOptionsModel)
            uninstalled = pyqtSignal(str)
            launched = pyqtSignal(str)
            finished = pyqtSignal(str)
            origin_path_ready = pyqtSignal(str, c_uint64)

        def __init__(self):
            super(RareGameBase.Signals, self).__init__()
            self.progress = RareGameBase.Signals.Progress()
            self.widget = RareGameBase.Signals.Widget()
            self.download = RareGameBase.Signals.Download()
            self.game = RareGameBase.Signals.Game()

        def __del__(self):
            self.progress.deleteLater()
            self.widget.deleteLater()
            self.download.deleteLater()
            self.game.deleteLater()

    __slots__ = "igame"

    def __init__(self, legendary_core: LegendaryCore, game: Game):
        super(RareGameBase, self).__init__()
        self.signals = RareGameBase.Signals()
        self.core = legendary_core
        self.game: Game = game
        self._state = RareGameBase.State.IDLE

    def __del__(self):
        del self.signals

    @property
    def state(self) -> 'RareGameBase.State':
        return self._state

    @state.setter
    def state(self, state: 'RareGameBase.State'):
        if state != self._state:
            self._state = state
            self.signals.widget.update.emit()

    @property
    def is_idle(self):
        return self.state == RareGameBase.State.IDLE

    @property
    def app_name(self) -> str:
        return self.igame.app_name if self.igame is not None else self.game.app_name

    @property
    def app_title(self) -> str:
        return self.igame.title if self.igame is not None else self.game.app_title

    @property
    def title(self) -> str:
        return self.app_title

    @property
    @abstractmethod
    def is_installed(self) -> bool:
        pass

    @abstractmethod
    def set_installed(self, installed: bool) -> None:
        pass

    @property
    @abstractmethod
    def is_mac(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_win32(self) -> bool:
        pass


class RareGameSlim(RareGameBase):

    def __init__(self, legendary_core: LegendaryCore, game: Game):
        super(RareGameSlim, self).__init__(legendary_core, game)
        # None if origin or not installed
        self.igame: Optional[InstalledGame] = self.core.get_installed_game(game.app_name)
        self.save = None
        self.saves: List[SaveGameFile] = []

    def is_installed(self) -> bool:
        return True

    def set_installed(self, installed: bool) -> None:
        pass

    @property
    def is_mac(self) -> bool:
        """!
        @brief Property to report if Game has a mac version

        @return bool
        """
        return "Mac" in self.game.asset_infos.keys()

    @property
    def is_win32(self) -> bool:
        """!
        @brief Property to report if Game is 32bit game

        @return bool
        """
        return "Win32" in self.game.asset_infos.keys()

    def set_saves(self, saves: list[SaveGameFile]):
        latest_save = sorted(saves, key=lambda a: a.datetime)[-1]
        res, (dt_local, dt_remote) = self.core.check_savegame_state(
            self.igame.save_path, latest_save
        )
        self.save = RareGameSlim.Save(latest_save, saves, res, dt_remote, dt_local)
        self.signals.widget.update.emit()

    def upload_saves(self, thread=True):
        def _upload():
            print("Uploading...")
            self.state = RareGameBase.State.SYNCING
            self.core.upload_save(self.app_name, self.igame.save_path, self.save.dt_local)
            self.update_savefile()
            self.state = RareGameBase.State.IDLE

        if not self.game.supports_cloud_saves:
            return
        if not self.save or not self.save.dt_local:
            logger.warning("Can't upload non existing save")
            return
        if thread:
            worker = QRunnable.create(lambda: _upload())
            QThreadPool.globalInstance().start(worker)
        else:
            _upload()

    def download_saves(self, thread=True):
        def _download():
            logger.info(f"Start downloading save for {self.title}")
            self.state = RareGameBase.State.SYNCING
            self.core.download_saves(self.app_name, self.save.latest_save.manifest_name, self.igame.save_path)
            self.update_savefile()
            self.state = RareGameBase.State.IDLE

        if not self.game.supports_cloud_saves:
            return
        if not self.save or not self.save.dt_remote:
            logger.error("Can't download non existing save")
            return
        if self.state == RareGameBase.State.SYNCING:
            logger.error(f"{self.title} is already syncing")
            return
        if thread:
            worker = QRunnable.create(lambda: _download())
            QThreadPool.globalInstance().start(worker)
        else:
            _download()

    @property
    def auto_sync_saves(self):
        return self.game.supports_cloud_saves and QSettings().value(f"{self.app_name}/auto_sync_cloud", True, bool)

    def update_savefile(self):
        saves = self.core.get_save_games(self.app_name)
        self.set_saves(saves)

    @property
    def is_save_up_to_date(self):
        return (self.save.res == SaveGameStatus.SAME_AGE) \
            or (self.save.res == SaveGameStatus.NO_SAVE)

import configparser
import os
import platform
import subprocess
import time
from configparser import ConfigParser
from ctypes import c_uint64
from logging import getLogger
from typing import Union

from PyQt5.QtCore import pyqtSignal, QRunnable, QObject

from rare.lgndr.core import LegendaryCore
from rare.models.game import RareGame
from rare.models.pathspec import PathSpec
from rare.utils.misc import get_size
from .worker import Worker

logger = getLogger("WineResolver")


class WineResolver(Worker):
    class Signals(QObject):
        result_ready = pyqtSignal(str)

    def __init__(self, core: LegendaryCore, path: str, app_name: str):
        super(WineResolver, self).__init__()
        self.signals = WineResolver.Signals()
        self.wine_env = os.environ.copy()
        self.wine_env.update(core.get_app_environment(app_name))
        self.wine_env["WINEDLLOVERRIDES"] = "winemenubuilder=d;mscoree=d;mshtml=d;"
        self.wine_env["DISPLAY"] = ""

        self.wine_binary = core.lgd.config.get(
            app_name,
            "wine_executable",
            fallback=core.lgd.config.get("default", "wine_executable", fallback="wine"),
        )
        self.winepath_binary = os.path.join(os.path.dirname(self.wine_binary), "winepath")
        self.path = PathSpec(core, app_name).cook(path)

    def run_real(self):
        if "WINEPREFIX" not in self.wine_env or not os.path.exists(self.wine_env["WINEPREFIX"]):
            # pylint: disable=E1136
            self.signals.result_ready[str].emit("")
            return
        if not os.path.exists(self.wine_binary) or not os.path.exists(self.winepath_binary):
            # pylint: disable=E1136
            self.signals.result_ready[str].emit("")
            return
        path = self.path.strip().replace("/", "\\")
        # lk: if path does not exist form
        cmd = [self.wine_binary, "cmd", "/c", "echo", path]
        # lk: if path exists and needs a case-sensitive interpretation form
        # cmd = [self.wine_binary, 'cmd', '/c', f'cd {path} & cd']
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.wine_env,
            shell=False,
            text=True,
        )
        out, err = proc.communicate()
        # Clean wine output
        out = out.strip().strip('"')
        proc = subprocess.Popen(
            [self.winepath_binary, "-u", out],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.wine_env,
            shell=False,
            text=True,
        )
        out, err = proc.communicate()
        real_path = os.path.realpath(out.strip())
        # pylint: disable=E1136
        self.signals.result_ready[str].emit(real_path)
        return


class OriginWineWorker(QRunnable):
    def __init__(self, core: LegendaryCore, games: Union[list[RareGame], RareGame]):
        super().__init__()
        self.setAutoDelete(True)

        self.__cache: dict[str, ConfigParser] = {}
        if isinstance(games, RareGame):
            games = [games]

        self.games = games
        self.core = core

    # this is a copied function from legendary.utils.wine_helpers, but it reads system.reg in the wine prefix
    @staticmethod
    def read_system_registry(wine_pfx: str) -> ConfigParser:
        reg = configparser.ConfigParser(comment_prefixes=(';', '#', '/', 'WINE'), allow_no_value=True,
                                        strict=False)
        reg.optionxform = str
        reg.read(os.path.join(wine_pfx, 'system.reg'))
        return reg

    @staticmethod
    def get_size(path: str):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size

    def run(self) -> None:
        t = time.time()
        for rgame in self.games:
            if not rgame.is_origin:
                continue

            reg_path: str = rgame.game.metadata \
                .get("customAttributes", {}) \
                .get("RegistryPath", {}).get("value", None)
            if not reg_path:
                continue

            if platform.system() == "Windows":
                import winreg
                from legendary.lfs import windows_helpers
                install_dir = windows_helpers.query_registry_value(winreg.HKEY_LOCAL_MACHINE, reg_path, "Install Dir")
            else:
                wine_prefix = self.core.lgd.config.get(rgame.app_name, "wine_prefix",
                                                       fallback=os.path.expanduser("~/.wine"))
                reg = self.__cache.get(wine_prefix) or self.read_system_registry(wine_prefix)
                self.__cache[wine_prefix] = reg

                # TODO: find a better solution
                reg_path = reg_path.replace("\\", "\\\\") \
                    .replace("SOFTWARE", "Software").replace("WOW6432Node", "Wow6432Node")

                install_dir = reg.get(reg_path, '"Install Dir"', fallback=None)
            if install_dir and os.path.exists(install_dir):
                size = self.get_size(install_dir)
                logger.debug(f"Found size and install path for {rgame.title}: {get_size(size)}, {install_dir}")
                rgame.signals.game.origin_path_ready.emit(install_dir, c_uint64(size))
            if install_dir and not os.path.exists(install_dir):
                logger.warning(f"Found install path {install_dir} for {rgame.title} but it does not exist")
        logger.info(f"Origin registry worker finished in {time.time() - t}s")

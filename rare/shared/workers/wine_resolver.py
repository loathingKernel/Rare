import configparser
import os
import subprocess
import time
from configparser import ConfigParser
from logging import getLogger
from typing import Union

from PyQt5.QtCore import pyqtSignal, QObject

from rare.lgndr.core import LegendaryCore
from rare.models.game import RareGame
from rare.models.pathspec import PathSpec
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
    def __init__(self, games: Union[list[RareGame], RareGame], core: LegendaryCore):
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

            wine_prefix = self.core.lgd.config.get(rgame.app_name, "wine_prefix",
                                                   fallback=os.path.expanduser("~/.wine"))
            reg = self.__cache.get(wine_prefix) or self.read_system_registry(wine_prefix)
            self.__cache[wine_prefix] = reg

            # TODO: find a better solution
            reg_path = reg_path.replace("\\", "\\\\")\
                .replace("SOFTWARE", "Software").replace("WOW6432Node", "Wow6432Node")

            install_dir = reg.get(reg_path, '"Install Dir"', fallback=None)
            if install_dir:
                logger.debug(f"Found install path for {rgame.title}: {install_dir}")
                rgame.signals.game.origin_path_ready.emit(install_dir)
        logger.info(f"Origin registry worker finished in {time.time() - t}s")


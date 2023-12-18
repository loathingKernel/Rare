import platform as pf
from argparse import Namespace
from typing import Any, Type
from .library import LibraryFilter, LibraryOrder


class Value(Namespace):
    key: str
    default: Any
    dtype: Type

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        for v in self.__dict__.values():
            yield v


# They key names are set to the existing option name
class Defaults(Namespace):
    win32_meta = Value(key="win32_meta", default=False, dtype=bool)
    macos_meta = Value(key="macos_meta", default=pf.system() == "Darwin", dtype=bool)
    unreal_meta = Value(key="unreal_meta", default=False, dtype=bool)
    exclude_non_asset = Value(key="exclude_non_asset", default=False, dtype=bool)
    exclude_entitlements = Value(key="exclude_entitlements", default=False, dtype=bool)

    sys_tray = Value(key="sys_tray", default=True, dtype=bool)
    auto_update = Value(key="auto_update", default=False, dtype=bool)
    auto_sync_cloud = Value(key="auto_sync_cloud", default=False, dtype=bool)
    confirm_start = Value(key="confirm_start", default=False, dtype=bool)
    save_size = Value(key="save_size", default=False, dtype=bool)
    window_size = Value(key="window_size", default=(1280, 720), dtype=tuple)
    notification = Value(key="notification", default=True, dtype=bool)
    log_games = Value(key="show_console", default=False, dtype=bool)

    library_filter = Value(
        key="library_filter",
        default=int(LibraryFilter.MAC if pf.system() == "Darwin" else LibraryFilter.ALL), dtype=int
    )
    library_order = Value(
        key="library_order", default=int(LibraryOrder.TITLE), dtype=int
    )

    rpc_enable = Value(key="rpc_enable", default=0, dtype=int)
    rpc_name = Value(key="rpc_game", default=True, dtype=bool)
    rpc_time = Value(key="rpc_time", default=True, dtype=bool)
    rpc_os = Value(key="rpc_os", default=True, dtype=bool)


options = Defaults()

__all__ = ['options']
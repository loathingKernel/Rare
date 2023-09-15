import os
from typing import Callable, Optional, Set, Any

from legendary.core import LegendaryCore
from legendary.models.config import LGDConf

_config: Optional[LGDConf] = None
_save_config: Optional[Callable[[], None]] = None


def init_config_handler(core: LegendaryCore):
    global _config, _save_config
    _config = core.lgd.config
    _save_config = core.lgd.save_config


def save_config():
    if _save_config is None:
        raise RuntimeError("Uninitialized use of config_helper")
    _save_config()


def add_option(app_name: str, option: str, value: str) -> None:
    value = value.replace("%%", "%").replace("%", "%%")
    if not _config.has_section(app_name):
        _config[app_name] = {}
    _config.set(app_name, option, value)
    save_config()


def add_envvar(app_name: str, envvar: str, value: str) -> None:
    add_option(f"{app_name}.env", envvar, value)


def remove_option(app_name: str, option: str) -> None:
    if _config.has_option(app_name, option):
        _config.remove_option(app_name, option)
    # if _config.has_section(app_name) and not _config[app_name]:
    #     _config.remove_section(app_name)
    save_config()


def remove_envvar(app_name: str, option: str) -> None:
    remove_option(f"{app_name}.env", option)


def remove_section(app_name: str) -> None:
    return
    # Disabled due to env variables implementation
    if _config.has_section(app_name):
        _config.remove_section(app_name)
        save_config()


def get_game_option(option: str, app_name: Optional[str] = None, fallback: Any = None) -> str:
    _option = _config.get("default", option, fallback=fallback)
    if app_name is not None:
        _option = _config.get(app_name, option, fallback=_option)
    return _option


def get_game_envvar(option: str, app_name: Optional[str] = None, fallback: Any = None) -> str:
    _option = _config.get("default.env", option, fallback=fallback)
    if app_name is not None:
        _option = _config.get(f'{app_name}.env', option, fallback=_option)
    return _option


def get_proton_compat_data(app_name: Optional[str] = None, fallback: Any = None) -> str:
    _compat = _config.get("default.env", "STEAM_COMPAT_DATA_PATH", fallback=fallback)
    if app_name is not None:
        _compat = _config.get(f'{app_name}.env', "STEAM_COMPAT_DATA_PATH", fallback=_compat)
    # return os.path.join(_compat, "pfx") if _compat else fallback
    return _compat


def get_wine_prefix(app_name: Optional[str] = None, fallback: Any = None) -> str:
    _prefix = _config.get("default.env", "WINEPREFIX", fallback=fallback)
    _prefix = _config.get("default", "wine_prefix", fallback=_prefix)
    if app_name is not None:
        _prefix = _config.get(f'{app_name}.env', 'WINEPREFIX', fallback=_prefix)
        _prefix = _config.get(app_name, 'wine_prefix', fallback=_prefix)
    return _prefix


def get_wine_prefixes() -> Set[str]:
    _prefixes = []
    for name, section in _config.items():
        pfx = section.get("WINEPREFIX") or section.get("wine_prefix")
        if not pfx:
            pfx = os.path.join(compatdata, "pfx") if (compatdata := section.get("STEAM_COMPAT_DATA_PATH")) else ""
        if pfx:
            _prefixes.append(pfx)
    _prefixes = [os.path.expanduser(prefix) for prefix in _prefixes]
    return {p for p in _prefixes if os.path.isdir(p)}


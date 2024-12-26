from cx_Freeze import setup, Executable

from rare import __version__

_name = "Rare"
_author = "RareDevs"
_description = "Open source alternative for Epic Games Launcher, using Legendary"

_icon = "rare/resources/images/Rare"
_license = "LICENSE"

build_exe_options = {
    "bin_excludes": ["libqpdf.so", "libqpdf.dylib"],
    "excludes": [
        "tkinter",
        "unittest",
        "pydoc",
    ],
    "include_msvcr": False,
    "optimize": 2,
}

shortcut_table = [
    (
        "DesktopShortcut",  # Shortcut
        "DesktopFolder",  # Directory_
        "Rare",  # Name
        "TARGETDIR",  # Component_
        "[TARGETDIR]Rare.exe",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        None,  # ShowCmd
        "TARGETDIR",  # WkDir
    ),
]

msi_data = {
    "Shortcut": shortcut_table,
    "ProgId": [
        ("Prog.Id", None, None, _description, "IconId", None),
    ],
    "Icon": [("IcodId", f"{_icon}.ico")],
}

bdist_msi_options = {
    "data": msi_data,
    "license_file": _license,
    # generated with str(uuid.uuid3(uuid.NAMESPACE_DNS, 'io.github.dummerle.rare')).upper()
    "upgrade_code": "{85D9FCC2-733E-3D74-8DD4-8FE33A07ADF8}",
}

bdist_appimage_options = {
    "target_name": _name,
    "target_version": __version__,
}

bdist_mac_options = {
    "iconfile": _icon,
    "bundle_name": f"{_name}",
}

executables = [
    Executable(
        script="rare/main.py",
        copyright=f"Copyright (C) 2024 {_author}",
        base="gui",
        icon=_icon,
        target_name=_name,
    ),
]

setup(
    name=_name,
    version=__version__,
    author=_author,
    description=_description,
    executables=executables,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
        "bdist_appimage": bdist_appimage_options,
        "bdist_mac": bdist_mac_options,
    },
)

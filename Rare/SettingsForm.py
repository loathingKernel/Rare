import os
from logging import getLogger

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *

from Rare.utils import legendaryConfig

logger = getLogger("SettingsForm")


class SettingsForm(QGroupBox):

    def __init__(self, app_name, settings: [tuple], table: bool):
        super(SettingsForm, self).__init__()
        self.config = legendaryConfig.get_config()
        self.app_name = app_name
        self.form = QFormLayout()
        self.rows = []
        self.has_table = table
        for i in settings:
            self.add_Row(*i)
        if table:
            if not f"{self.app_name}.env" in self.config:
                env_vars = {}
            else:
                env_vars = self.config[f"{self.app_name}.env"]

            if env_vars:
                self.table = QTableWidget(len(env_vars), 2)
                for i, label in enumerate(env_vars):
                    self.table.setItem(i, 0, QTableWidgetItem(label))
                    self.table.setItem(i, 1, QTableWidgetItem(env_vars[label]))

            else:
                self.table = QTableWidget(0, 2)

            self.table.setHorizontalHeaderLabels(["Variable", "Value"])

            self.form.addRow(QLabel("Environment Variables"), self.table)

            self.add_button = QPushButton("Add Variable")
            self.add_button.clicked.connect(self.add_variable)

            self.delete_button = QPushButton("Delete Variable")
            self.delete_button.clicked.connect(lambda: self.table.removeRow(self.table.currentRow()))

            self.form.addRow(self.add_button)
            self.form.addRow(self.delete_button)

        self.update_button = QPushButton("Update Settings")
        self.update_button.clicked.connect(self.update_config)
        self.form.addRow(self.update_button)

        self.setLayout(self.form)

    def add_Row(self, info_text: str, type_of_input: str, lgd_name: str, flags: [] = None):
        if flags is None:
            flags = []
        if os.name == "nt" and "wine" in flags:
            return
        field = None
        if not self.app_name in self.config.sections():
            self.config[self.app_name] = {}

        if not lgd_name in self.config[self.app_name]:
            self.config[self.app_name][lgd_name] = ""

        if type_of_input == "QLineEdit":
            field = QLineEdit(self.config[self.app_name][lgd_name])
            field.setPlaceholderText("Default")
            if "only_int" in flags:
                field.setValidator(QIntValidator())

        elif type_of_input == "QComboBox":
            combo_list = []
            if "binary" in flags:
                combo_list = ["unset", "true", "false"]
            else:
                combo_list = flags
            field = QComboBox()
            field.addItems(combo_list)

            if self.config[self.app_name][lgd_name] == "":
                field.setCurrentIndex(0)
            elif self.config[self.app_name][lgd_name] == "true":
                field.setCurrentIndex(1)
            elif not self.config[self.app_name][lgd_name] == "false":
                field.setCurrentIndex(2)

        if not field:
            return

        self.form.addRow(QLabel(info_text), field)
        self.rows.append((field, type_of_input, lgd_name))
        # pprint(self.rows)

    def add_variable(self):
        self.table.insertRow(self.table.rowCount())
        self.table.setItem(self.table.rowCount(), 0, QTableWidgetItem(""))
        self.table.setItem(self.table.rowCount(), 1, QTableWidgetItem(""))

    def update_config(self):
        config = {self.app_name: {}}
        for setting in self.rows:
            field, type_of_input, lgd_name = setting
            if type_of_input == "QLineEdit":
                if field.text() != "":
                    config[self.app_name][lgd_name] = field.text()
            elif type_of_input == "QComboBox":
                # print(type(field.currentText()), field.currentText())
                if field.currentText() == "true":
                    config[self.app_name][lgd_name] = True
                elif field.currentText() == "false":
                    config[self.app_name][lgd_name] = False
                elif field.currentText == "unset":
                    pass
                else:
                    pass
                    # config[self.app_name][lgd_name] = field.currentText()

        if self.has_table:
            if self.table.rowCount() > 0:
                config[f"{self.app_name}.env"] = {}
                for row in range(self.table.rowCount()):
                    config[f"{self.app_name}.env"][self.table.item(row, 0).text()] = self.table.item(row, 1).text()
            else:
                config[f"{self.app_name}.env"] = {}
        lgd_config = legendaryConfig.get_config()
        if config[self.app_name] == {}:
            config.pop(self.app_name)
            lgd_config.remove_section(self.app_name)
        else:
            lgd_config[self.app_name] = config[self.app_name]

        if self.has_table:
            if config[self.app_name + ".env"] == {}:
                config.pop(self.app_name + ".env")
                lgd_config.remove_section(self.app_name + ".env")
            else:
                lgd_config[self.app_name + ".env"] = config[f"{self.app_name}.env"]
        # legendaryConfig.set_config()
        legendaryConfig.set_config(lgd_config)

    def use_proton_template(self):
        for i in self.rows:
            field, type_of_input, lgd_name = i

            if lgd_name == "wrapper":
                for file in os.listdir(os.path.expanduser("~/.steam/steam/steamapps/common")):
                    if file.startswith("Proton"):
                        protonpath = os.path.expanduser("~/.steam/steam/steamapps/common/" + file)
                        break
                else:
                    logger.error("No Proton found")
                    QMessageBox.Warning("Error", "No Proton was found")
                    return
                field.setText(os.path.join(protonpath, "proton") + " run")
            elif lgd_name == "no_wine":
                field.setCurrentIndex(1)

        self.table.insertRow(self.table.rowCount())

        self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem("STEAM_COMPAT_DATA_PATH"))
        self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(os.path.expanduser("~/.proton")))

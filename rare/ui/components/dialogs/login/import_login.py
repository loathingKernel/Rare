# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rare/ui/components/dialogs/login/import_login.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ImportLogin(object):
    def setupUi(self, ImportLogin):
        ImportLogin.setObjectName("ImportLogin")
        ImportLogin.resize(233, 156)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ImportLogin.sizePolicy().hasHeightForWidth())
        ImportLogin.setSizePolicy(sizePolicy)
        ImportLogin.setWindowTitle("ImportLogin")
        self.main_layout = QtWidgets.QVBoxLayout(ImportLogin)
        self.main_layout.setObjectName("main_layout")
        self.title_label = QtWidgets.QLabel(ImportLogin)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.main_layout.addWidget(self.title_label)
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.form_layout.setObjectName("form_layout")
        self.prefix_layout = QtWidgets.QHBoxLayout()
        self.prefix_layout.setObjectName("prefix_layout")
        self.prefix_combo = QtWidgets.QComboBox(ImportLogin)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prefix_combo.sizePolicy().hasHeightForWidth())
        self.prefix_combo.setSizePolicy(sizePolicy)
        self.prefix_combo.setEditable(True)
        self.prefix_combo.setObjectName("prefix_combo")
        self.prefix_layout.addWidget(self.prefix_combo)
        self.prefix_tool = QtWidgets.QToolButton(ImportLogin)
        self.prefix_tool.setObjectName("prefix_tool")
        self.prefix_layout.addWidget(self.prefix_tool)
        self.prefix_layout.setStretch(0, 1)
        self.form_layout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.prefix_layout)
        self.prefix_label = QtWidgets.QLabel(ImportLogin)
        self.prefix_label.setObjectName("prefix_label")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.prefix_label)
        self.status_label = QtWidgets.QLabel(ImportLogin)
        font = QtGui.QFont()
        font.setItalic(True)
        self.status_label.setFont(font)
        self.status_label.setText("")
        self.status_label.setObjectName("status_label")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.status_label)
        self.main_layout.addLayout(self.form_layout)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_layout.addItem(spacerItem)
        self.info_label = QtWidgets.QLabel(ImportLogin)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_label.sizePolicy().hasHeightForWidth())
        self.info_label.setSizePolicy(sizePolicy)
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName("info_label")
        self.main_layout.addWidget(self.info_label)

        self.retranslateUi(ImportLogin)

    def retranslateUi(self, ImportLogin):
        _translate = QtCore.QCoreApplication.translate
        self.title_label.setText(_translate("ImportLogin", "Import existing session from EGL"))
        self.prefix_tool.setText(_translate("ImportLogin", "Browse"))
        self.prefix_label.setText(_translate("ImportLogin", "Select prefix"))
        self.info_label.setText(_translate("ImportLogin", "<i>Please select the Wine prefix where Epic Games Launcher is installed. You will get logged out from EGL in the process.</i>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ImportLogin = QtWidgets.QWidget()
    ui = Ui_ImportLogin()
    ui.setupUi(ImportLogin)
    ImportLogin.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'details.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QFormLayout, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_GameDetails(object):
    def setupUi(self, GameDetails):
        if not GameDetails.objectName():
            GameDetails.setObjectName(u"GameDetails")
        GameDetails.resize(814, 598)
        GameDetails.setWindowTitle(u"GameDetails")
        self.main_layout = QHBoxLayout(GameDetails)
        self.main_layout.setObjectName(u"main_layout")
        self.left_layout = QVBoxLayout()
        self.left_layout.setObjectName(u"left_layout")
        self.tags_group = QGroupBox(GameDetails)
        self.tags_group.setObjectName(u"tags_group")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tags_group.sizePolicy().hasHeightForWidth())
        self.tags_group.setSizePolicy(sizePolicy)
        self.tags_group_layout = QVBoxLayout(self.tags_group)
        self.tags_group_layout.setObjectName(u"tags_group_layout")
        self.add_tag_button = QPushButton(self.tags_group)
        self.add_tag_button.setObjectName(u"add_tag_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_tag_button.sizePolicy().hasHeightForWidth())
        self.add_tag_button.setSizePolicy(sizePolicy1)

        self.tags_group_layout.addWidget(self.add_tag_button, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop)

        self.tags_vlayout = QVBoxLayout()
        self.tags_vlayout.setObjectName(u"tags_vlayout")

        self.tags_group_layout.addLayout(self.tags_vlayout)


        self.left_layout.addWidget(self.tags_group)


        self.main_layout.addLayout(self.left_layout)

        self.right_layout = QVBoxLayout()
        self.right_layout.setObjectName(u"right_layout")
        self.details_layout = QFormLayout()
        self.details_layout.setObjectName(u"details_layout")
        self.details_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.details_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.details_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.details_layout.setHorizontalSpacing(12)
        self.details_layout.setVerticalSpacing(12)
        self.details_layout.setContentsMargins(6, 6, 6, 6)
        self.lbl_dev = QLabel(GameDetails)
        self.lbl_dev.setObjectName(u"lbl_dev")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lbl_dev.sizePolicy().hasHeightForWidth())
        self.lbl_dev.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setBold(True)
        self.lbl_dev.setFont(font)
        self.lbl_dev.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.details_layout.setWidget(0, QFormLayout.LabelRole, self.lbl_dev)

        self.dev = QLabel(GameDetails)
        self.dev.setObjectName(u"dev")
        self.dev.setText(u"error")
        self.dev.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.details_layout.setWidget(0, QFormLayout.FieldRole, self.dev)

        self.lbl_app_name = QLabel(GameDetails)
        self.lbl_app_name.setObjectName(u"lbl_app_name")
        sizePolicy2.setHeightForWidth(self.lbl_app_name.sizePolicy().hasHeightForWidth())
        self.lbl_app_name.setSizePolicy(sizePolicy2)
        self.lbl_app_name.setFont(font)
        self.lbl_app_name.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.details_layout.setWidget(1, QFormLayout.LabelRole, self.lbl_app_name)

        self.app_name = QLabel(GameDetails)
        self.app_name.setObjectName(u"app_name")
        self.app_name.setText(u"error")
        self.app_name.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.details_layout.setWidget(1, QFormLayout.FieldRole, self.app_name)

        self.lbl_version = QLabel(GameDetails)
        self.lbl_version.setObjectName(u"lbl_version")
        sizePolicy2.setHeightForWidth(self.lbl_version.sizePolicy().hasHeightForWidth())
        self.lbl_version.setSizePolicy(sizePolicy2)
        self.lbl_version.setFont(font)
        self.lbl_version.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.details_layout.setWidget(2, QFormLayout.LabelRole, self.lbl_version)

        self.version = QLabel(GameDetails)
        self.version.setObjectName(u"version")
        self.version.setText(u"error")
        self.version.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.details_layout.setWidget(2, QFormLayout.FieldRole, self.version)

        self.lbl_grade = QLabel(GameDetails)
        self.lbl_grade.setObjectName(u"lbl_grade")
        sizePolicy2.setHeightForWidth(self.lbl_grade.sizePolicy().hasHeightForWidth())
        self.lbl_grade.setSizePolicy(sizePolicy2)
        self.lbl_grade.setFont(font)
        self.lbl_grade.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.details_layout.setWidget(3, QFormLayout.LabelRole, self.lbl_grade)

        self.grade = QLabel(GameDetails)
        self.grade.setObjectName(u"grade")
        self.grade.setText(u"error")
        self.grade.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.details_layout.setWidget(3, QFormLayout.FieldRole, self.grade)

        self.lbl_install_size = QLabel(GameDetails)
        self.lbl_install_size.setObjectName(u"lbl_install_size")
        sizePolicy2.setHeightForWidth(self.lbl_install_size.sizePolicy().hasHeightForWidth())
        self.lbl_install_size.setSizePolicy(sizePolicy2)
        self.lbl_install_size.setFont(font)
        self.lbl_install_size.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.details_layout.setWidget(4, QFormLayout.LabelRole, self.lbl_install_size)

        self.install_size = QLabel(GameDetails)
        self.install_size.setObjectName(u"install_size")
        self.install_size.setText(u"error")
        self.install_size.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.details_layout.setWidget(4, QFormLayout.FieldRole, self.install_size)

        self.lbl_install_path = QLabel(GameDetails)
        self.lbl_install_path.setObjectName(u"lbl_install_path")
        sizePolicy2.setHeightForWidth(self.lbl_install_path.sizePolicy().hasHeightForWidth())
        self.lbl_install_path.setSizePolicy(sizePolicy2)
        self.lbl_install_path.setFont(font)
        self.lbl_install_path.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.details_layout.setWidget(5, QFormLayout.LabelRole, self.lbl_install_path)

        self.install_path = QLabel(GameDetails)
        self.install_path.setObjectName(u"install_path")
        self.install_path.setText(u"error")
        self.install_path.setWordWrap(True)
        self.install_path.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.details_layout.setWidget(5, QFormLayout.FieldRole, self.install_path)

        self.lbl_platform = QLabel(GameDetails)
        self.lbl_platform.setObjectName(u"lbl_platform")
        sizePolicy2.setHeightForWidth(self.lbl_platform.sizePolicy().hasHeightForWidth())
        self.lbl_platform.setSizePolicy(sizePolicy2)
        self.lbl_platform.setFont(font)
        self.lbl_platform.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.details_layout.setWidget(6, QFormLayout.LabelRole, self.lbl_platform)

        self.platform = QLabel(GameDetails)
        self.platform.setObjectName(u"platform")
        self.platform.setText(u"error")

        self.details_layout.setWidget(6, QFormLayout.FieldRole, self.platform)

        self.lbl_game_actions = QLabel(GameDetails)
        self.lbl_game_actions.setObjectName(u"lbl_game_actions")
        sizePolicy2.setHeightForWidth(self.lbl_game_actions.sizePolicy().hasHeightForWidth())
        self.lbl_game_actions.setSizePolicy(sizePolicy2)
        self.lbl_game_actions.setFont(font)
        self.lbl_game_actions.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.details_layout.setWidget(7, QFormLayout.LabelRole, self.lbl_game_actions)

        self.game_actions_stack = QStackedWidget(GameDetails)
        self.game_actions_stack.setObjectName(u"game_actions_stack")
        sizePolicy.setHeightForWidth(self.game_actions_stack.sizePolicy().hasHeightForWidth())
        self.game_actions_stack.setSizePolicy(sizePolicy)
        self.game_actions_stack.setMinimumSize(QSize(250, 0))
        self.game_actions_stack.setMaximumSize(QSize(250, 16777215))
        self.installed_page = QWidget()
        self.installed_page.setObjectName(u"installed_page")
        self.installed_layout = QVBoxLayout(self.installed_page)
        self.installed_layout.setObjectName(u"installed_layout")
        self.installed_layout.setContentsMargins(0, 0, 0, 0)
        self.modify_button = QPushButton(self.installed_page)
        self.modify_button.setObjectName(u"modify_button")

        self.installed_layout.addWidget(self.modify_button)

        self.verify_stack = QStackedWidget(self.installed_page)
        self.verify_stack.setObjectName(u"verify_stack")
        self.verify_button_page = QWidget()
        self.verify_button_page.setObjectName(u"verify_button_page")
        self.verify_page_layout = QHBoxLayout(self.verify_button_page)
        self.verify_page_layout.setSpacing(0)
        self.verify_page_layout.setObjectName(u"verify_page_layout")
        self.verify_page_layout.setContentsMargins(0, 0, 0, 0)
        self.verify_button = QPushButton(self.verify_button_page)
        self.verify_button.setObjectName(u"verify_button")

        self.verify_page_layout.addWidget(self.verify_button)

        self.verify_stack.addWidget(self.verify_button_page)
        self.verify_progress_page = QWidget()
        self.verify_progress_page.setObjectName(u"verify_progress_page")
        self.verify_progress_layout = QHBoxLayout(self.verify_progress_page)
        self.verify_progress_layout.setSpacing(0)
        self.verify_progress_layout.setObjectName(u"verify_progress_layout")
        self.verify_progress_layout.setContentsMargins(0, 0, 0, 0)
        self.verify_progress = QProgressBar(self.verify_progress_page)
        self.verify_progress.setObjectName(u"verify_progress")
        self.verify_progress.setValue(24)

        self.verify_progress_layout.addWidget(self.verify_progress)

        self.verify_stack.addWidget(self.verify_progress_page)

        self.installed_layout.addWidget(self.verify_stack)

        self.repair_button = QPushButton(self.installed_page)
        self.repair_button.setObjectName(u"repair_button")

        self.installed_layout.addWidget(self.repair_button)

        self.move_stack = QStackedWidget(self.installed_page)
        self.move_stack.setObjectName(u"move_stack")
        self.move_button_page = QWidget()
        self.move_button_page.setObjectName(u"move_button_page")
        self.move_button_layout = QHBoxLayout(self.move_button_page)
        self.move_button_layout.setSpacing(0)
        self.move_button_layout.setObjectName(u"move_button_layout")
        self.move_button_layout.setContentsMargins(0, 0, 0, 0)
        self.move_button = QPushButton(self.move_button_page)
        self.move_button.setObjectName(u"move_button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.move_button.sizePolicy().hasHeightForWidth())
        self.move_button.setSizePolicy(sizePolicy3)

        self.move_button_layout.addWidget(self.move_button)

        self.move_stack.addWidget(self.move_button_page)
        self.move_progress_page = QWidget()
        self.move_progress_page.setObjectName(u"move_progress_page")
        self.move_progress_layout = QHBoxLayout(self.move_progress_page)
        self.move_progress_layout.setSpacing(0)
        self.move_progress_layout.setObjectName(u"move_progress_layout")
        self.move_progress_layout.setContentsMargins(0, 0, 0, 0)
        self.move_progress = QProgressBar(self.move_progress_page)
        self.move_progress.setObjectName(u"move_progress")
        self.move_progress.setValue(24)

        self.move_progress_layout.addWidget(self.move_progress)

        self.move_stack.addWidget(self.move_progress_page)

        self.installed_layout.addWidget(self.move_stack)

        self.uninstall_button = QPushButton(self.installed_page)
        self.uninstall_button.setObjectName(u"uninstall_button")

        self.installed_layout.addWidget(self.uninstall_button)

        self.game_actions_stack.addWidget(self.installed_page)
        self.uninstalled_page = QWidget()
        self.uninstalled_page.setObjectName(u"uninstalled_page")
        self.uninstalled_layout = QVBoxLayout(self.uninstalled_page)
        self.uninstalled_layout.setObjectName(u"uninstalled_layout")
        self.uninstalled_layout.setContentsMargins(0, 0, 0, 0)
        self.install_button = QPushButton(self.uninstalled_page)
        self.install_button.setObjectName(u"install_button")

        self.uninstalled_layout.addWidget(self.install_button)

        self.import_button = QPushButton(self.uninstalled_page)
        self.import_button.setObjectName(u"import_button")

        self.uninstalled_layout.addWidget(self.import_button)

        self.uninstalled_page_bot_vspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.uninstalled_layout.addItem(self.uninstalled_page_bot_vspacer)

        self.game_actions_stack.addWidget(self.uninstalled_page)

        self.details_layout.setWidget(7, QFormLayout.FieldRole, self.game_actions_stack)


        self.right_layout.addLayout(self.details_layout)

        self.requirements_group = QFrame(GameDetails)
        self.requirements_group.setObjectName(u"requirements_group")
        sizePolicy1.setHeightForWidth(self.requirements_group.sizePolicy().hasHeightForWidth())
        self.requirements_group.setSizePolicy(sizePolicy1)
        self.requirements_group.setFrameShape(QFrame.Shape.StyledPanel)
        self.requirements_group.setFrameShadow(QFrame.Shadow.Sunken)
        self.requirements_layout = QHBoxLayout(self.requirements_group)
        self.requirements_layout.setObjectName(u"requirements_layout")
        self.requirements_layout.setContentsMargins(0, 0, 0, 0)

        self.right_layout.addWidget(self.requirements_group)


        self.main_layout.addLayout(self.right_layout)

        self.main_layout.setStretch(1, 1)

        self.retranslateUi(GameDetails)

        self.game_actions_stack.setCurrentIndex(0)
        self.verify_stack.setCurrentIndex(0)
        self.move_stack.setCurrentIndex(0)

    # setupUi

    def retranslateUi(self, GameDetails):
        self.tags_group.setTitle(QCoreApplication.translate("GameDetails", u"Tags", None))
#if QT_CONFIG(tooltip)
        self.add_tag_button.setToolTip(QCoreApplication.translate("GameDetails", u"Add custom tag", None))
#endif // QT_CONFIG(tooltip)
        self.add_tag_button.setText(QCoreApplication.translate("GameDetails", u"Add tag", None))
        self.lbl_dev.setText(QCoreApplication.translate("GameDetails", u"Developer", None))
        self.lbl_app_name.setText(QCoreApplication.translate("GameDetails", u"Application name", None))
        self.lbl_version.setText(QCoreApplication.translate("GameDetails", u"Version", None))
        self.lbl_grade.setText(QCoreApplication.translate("GameDetails", u"ProtonDB grade", None))
        self.lbl_install_size.setText(QCoreApplication.translate("GameDetails", u"Installation size", None))
        self.lbl_install_path.setText(QCoreApplication.translate("GameDetails", u"Installation path", None))
        self.lbl_platform.setText(QCoreApplication.translate("GameDetails", u"Platform", None))
        self.lbl_game_actions.setText(QCoreApplication.translate("GameDetails", u"Actions", None))
        self.modify_button.setText(QCoreApplication.translate("GameDetails", u"Modify", None))
        self.verify_button.setText(QCoreApplication.translate("GameDetails", u"Verify", None))
        self.repair_button.setText(QCoreApplication.translate("GameDetails", u"Repair", None))
        self.move_button.setText(QCoreApplication.translate("GameDetails", u"Move", None))
        self.uninstall_button.setText(QCoreApplication.translate("GameDetails", u"Uninstall", None))
        self.install_button.setText(QCoreApplication.translate("GameDetails", u"Install", None))
        self.import_button.setText(QCoreApplication.translate("GameDetails", u"Import", None))
        pass
    # retranslateUi


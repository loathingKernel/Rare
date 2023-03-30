# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rare/ui/components/tabs/store/store.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ShopWidget(object):
    def setupUi(self, ShopWidget):
        ShopWidget.setObjectName("ShopWidget")
        ShopWidget.resize(784, 525)
        ShopWidget.setWindowTitle("Store")
        self.shop_layout = QtWidgets.QHBoxLayout(ShopWidget)
        self.shop_layout.setObjectName("shop_layout")
        self.left_layout = QtWidgets.QVBoxLayout()
        self.left_layout.setObjectName("left_layout")
        self.games_scrollarea = QtWidgets.QScrollArea(ShopWidget)
        self.games_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.games_scrollarea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.games_scrollarea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.games_scrollarea.setWidgetResizable(True)
        self.games_scrollarea.setObjectName("games_scrollarea")
        self.games_container = QtWidgets.QWidget()
        self.games_container.setGeometry(QtCore.QRect(0, 0, 611, 511))
        self.games_container.setObjectName("games_container")
        self.games_container_layout = QtWidgets.QVBoxLayout(self.games_container)
        self.games_container_layout.setContentsMargins(0, 0, 3, 0)
        self.games_container_layout.setObjectName("games_container_layout")
        self.free_games_scrollarea = QtWidgets.QScrollArea(self.games_container)
        self.free_games_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.free_games_scrollarea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.free_games_scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.free_games_scrollarea.setWidgetResizable(True)
        self.free_games_scrollarea.setObjectName("free_games_scrollarea")
        self.free_games_container = QtWidgets.QWidget()
        self.free_games_container.setGeometry(QtCore.QRect(0, 0, 608, 166))
        self.free_games_container.setObjectName("free_games_container")
        self.free_games_scrollarea.setWidget(self.free_games_container)
        self.games_container_layout.addWidget(self.free_games_scrollarea)
        self.discounts_group = QtWidgets.QGroupBox(self.games_container)
        self.discounts_group.setObjectName("discounts_group")
        self.discounts_layout = QtWidgets.QVBoxLayout(self.discounts_group)
        self.discounts_layout.setObjectName("discounts_layout")
        self.discount_stack = QtWidgets.QStackedWidget(self.discounts_group)
        self.discount_stack.setObjectName("discount_stack")
        self.discount_widget = QtWidgets.QWidget()
        self.discount_widget.setObjectName("discount_widget")
        self.discount_stack.addWidget(self.discount_widget)
        self.discounts_layout.addWidget(self.discount_stack)
        self.games_container_layout.addWidget(self.discounts_group)
        self.games_group = QtWidgets.QGroupBox(self.games_container)
        self.games_group.setObjectName("games_group")
        self.games_layout = QtWidgets.QVBoxLayout(self.games_group)
        self.games_layout.setObjectName("games_layout")
        self.game_stack = QtWidgets.QStackedWidget(self.games_group)
        self.game_stack.setObjectName("game_stack")
        self.game_widget = QtWidgets.QWidget()
        self.game_widget.setObjectName("game_widget")
        self.game_stack.addWidget(self.game_widget)
        self.games_layout.addWidget(self.game_stack)
        self.games_container_layout.addWidget(self.games_group)
        self.games_scrollarea.setWidget(self.games_container)
        self.left_layout.addWidget(self.games_scrollarea)
        self.shop_layout.addLayout(self.left_layout)
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.setObjectName("right_layout")
        self.reset_button = QtWidgets.QPushButton(ShopWidget)
        self.reset_button.setObjectName("reset_button")
        self.right_layout.addWidget(self.reset_button)
        self.filter_scrollarea = QtWidgets.QScrollArea(ShopWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter_scrollarea.sizePolicy().hasHeightForWidth())
        self.filter_scrollarea.setSizePolicy(sizePolicy)
        self.filter_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.filter_scrollarea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.filter_scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.filter_scrollarea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.filter_scrollarea.setWidgetResizable(True)
        self.filter_scrollarea.setObjectName("filter_scrollarea")
        self.filter_container = QtWidgets.QWidget()
        self.filter_container.setGeometry(QtCore.QRect(0, 0, 151, 479))
        self.filter_container.setObjectName("filter_container")
        self.filter_container_layout = QtWidgets.QVBoxLayout(self.filter_container)
        self.filter_container_layout.setContentsMargins(0, 0, 0, 0)
        self.filter_container_layout.setObjectName("filter_container_layout")
        self.price_group = QtWidgets.QGroupBox(self.filter_container)
        self.price_group.setObjectName("price_group")
        self.price_layout = QtWidgets.QVBoxLayout(self.price_group)
        self.price_layout.setObjectName("price_layout")
        self.none_price = QtWidgets.QRadioButton(self.price_group)
        self.none_price.setChecked(True)
        self.none_price.setObjectName("none_price")
        self.price_layout.addWidget(self.none_price)
        self.free_button = QtWidgets.QRadioButton(self.price_group)
        self.free_button.setObjectName("free_button")
        self.price_layout.addWidget(self.free_button)
        self.under10 = QtWidgets.QRadioButton(self.price_group)
        self.under10.setObjectName("under10")
        self.price_layout.addWidget(self.under10)
        self.under20 = QtWidgets.QRadioButton(self.price_group)
        self.under20.setObjectName("under20")
        self.price_layout.addWidget(self.under20)
        self.under30 = QtWidgets.QRadioButton(self.price_group)
        self.under30.setObjectName("under30")
        self.price_layout.addWidget(self.under30)
        self.above = QtWidgets.QRadioButton(self.price_group)
        self.above.setObjectName("above")
        self.price_layout.addWidget(self.above)
        self.on_discount = QtWidgets.QCheckBox(self.price_group)
        self.on_discount.setObjectName("on_discount")
        self.price_layout.addWidget(self.on_discount)
        self.filter_container_layout.addWidget(self.price_group)
        self.platform_group = QtWidgets.QGroupBox(self.filter_container)
        self.platform_group.setObjectName("platform_group")
        self.platfrom_layout = QtWidgets.QVBoxLayout(self.platform_group)
        self.platfrom_layout.setObjectName("platfrom_layout")
        self.filter_container_layout.addWidget(self.platform_group)
        self.genre_group = QtWidgets.QGroupBox(self.filter_container)
        self.genre_group.setObjectName("genre_group")
        self.genre_layout = QtWidgets.QVBoxLayout(self.genre_group)
        self.genre_layout.setObjectName("genre_layout")
        self.filter_container_layout.addWidget(self.genre_group)
        self.type_group = QtWidgets.QGroupBox(self.filter_container)
        self.type_group.setObjectName("type_group")
        self.type_layout = QtWidgets.QVBoxLayout(self.type_group)
        self.type_layout.setObjectName("type_layout")
        self.filter_container_layout.addWidget(self.type_group)
        self.others_group = QtWidgets.QGroupBox(self.filter_container)
        self.others_group.setObjectName("others_group")
        self.others_layout = QtWidgets.QVBoxLayout(self.others_group)
        self.others_layout.setObjectName("others_layout")
        self.filter_container_layout.addWidget(self.others_group)
        self.filter_scrollarea.setWidget(self.filter_container)
        self.right_layout.addWidget(self.filter_scrollarea)
        self.shop_layout.addLayout(self.right_layout)

        self.retranslateUi(ShopWidget)

    def retranslateUi(self, ShopWidget):
        _translate = QtCore.QCoreApplication.translate
        self.discounts_group.setTitle(_translate("ShopWidget", "Discounts from your wishlist"))
        self.games_group.setTitle(_translate("ShopWidget", "Games"))
        self.reset_button.setText(_translate("ShopWidget", "Reset filters"))
        self.price_group.setTitle(_translate("ShopWidget", "Price"))
        self.none_price.setText(_translate("ShopWidget", "None"))
        self.free_button.setText(_translate("ShopWidget", "Free"))
        self.under10.setText(_translate("ShopWidget", "Under 10"))
        self.under20.setText(_translate("ShopWidget", "Under 20"))
        self.under30.setText(_translate("ShopWidget", "Under 30"))
        self.above.setText(_translate("ShopWidget", "14.99 and above"))
        self.on_discount.setText(_translate("ShopWidget", "Discount"))
        self.platform_group.setTitle(_translate("ShopWidget", "Platform"))
        self.genre_group.setTitle(_translate("ShopWidget", "Genre"))
        self.type_group.setTitle(_translate("ShopWidget", "Type"))
        self.others_group.setTitle(_translate("ShopWidget", "Other tags"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ShopWidget = QtWidgets.QWidget()
    ui = Ui_ShopWidget()
    ui.setupUi(ShopWidget)
    ShopWidget.show()
    sys.exit(app.exec_())

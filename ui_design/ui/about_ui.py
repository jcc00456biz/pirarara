# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(460, 160)
        Dialog.setMaximumSize(QSize(600, 400))
        self.formLayout = QFormLayout(Dialog)
        self.formLayout.setObjectName(u"formLayout")
        self.app_icon = QLabel(Dialog)
        self.app_icon.setObjectName(u"app_icon")
        self.app_icon.setMinimumSize(QSize(64, 64))
        self.app_icon.setMaximumSize(QSize(64, 64))
        self.app_icon.setPixmap(QPixmap(u"../../icon/pirarara.png"))
        self.app_icon.setScaledContents(True)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.app_icon)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.buttonBox)

        self.about_text = QLabel(Dialog)
        self.about_text.setObjectName(u"about_text")
        self.about_text.setTextFormat(Qt.TextFormat.PlainText)
        self.about_text.setWordWrap(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.about_text)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.app_icon.setText("")
        self.about_text.setText(QCoreApplication.translate("Dialog", u"pirarara is an application for managing multimedia files.\n"
"pirarara works on Windows and Linux.\n"
"pirarara is developed using the Python 3 programming language.\n"
"pirarara GUI uses PySide6.\n"
"pirarara is licensed under the GPL.\n"
"The source code of pirarara is available on GitHub.", None))
    # retranslateUi


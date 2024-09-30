from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap


class QLabelFactory:
    @staticmethod
    def create_image_label(parent, geometry, object_name, pixmap=None, bg_color="white"):
        """Factory method to create a QLabel for images."""
        label = QLabel(parent)
        label.setGeometry(QRect(*geometry))
        label.setPixmap(QPixmap(pixmap))
        label.setScaledContents(True)
        label.setObjectName(object_name)
        label.setStyleSheet(f"background-color:{bg_color}")

        return label

    @staticmethod
    def create_label(parent, geometry, text):
        """Factory method to create a QLabel for text or image."""
        label = QLabel(parent)
        label.setGeometry(QRect(*geometry))
        label.setText(text)

        return label
    
    @staticmethod
    def create_status_label(parent, geometry, text_alignment):
        """Factory method to create a QLabel for text or image."""
        label = QLabel(parent)
        label.setGeometry(QRect(*geometry))
        label.setAlignment(text_alignment)

        return label


class QPushButtonFactory:
    @staticmethod
    def create_button(parent, geometry, text, on_click_handler):
        """Factory method to create a QPushButton."""
        button = QPushButton(text, parent)
        button.setGeometry(QRect(*geometry))
        button.clicked.connect(on_click_handler)
        return button
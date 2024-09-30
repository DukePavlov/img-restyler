from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QRect


class QPushButtonFactory:
    @staticmethod
    def create_button(parent, geometry, text, on_click_handler):
        """Factory method to create a QPushButton."""
        button = QPushButton(text, parent)
        button.setGeometry(QRect(*geometry))
        button.clicked.connect(on_click_handler)
        return button

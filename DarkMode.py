from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class DarkPallete(QPalette):
    def __init__(self):
        super().__init__()
        self.darkPalette_color = QPalette()

        self.darkPalette_color.setColor(QPalette.Window, QColor(53, 53, 53))
        self.darkPalette_color.setColor(QPalette.WindowText, Qt.white)
        self.darkPalette_color.setColor(
            QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127)
        )
        self.darkPalette_color.setColor(QPalette.Base, QColor(42, 42, 42))
        self.darkPalette_color.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        self.darkPalette_color.setColor(QPalette.ToolTipBase, Qt.white)
        self.darkPalette_color.setColor(QPalette.ToolTipText, Qt.white)
        self.darkPalette_color.setColor(QPalette.Text, Qt.white)
        self.darkPalette_color.setColor(
            QPalette.Disabled, QPalette.Text, QColor(127, 127, 127)
        )
        self.darkPalette_color.setColor(QPalette.Dark, QColor(35, 35, 35))
        self.darkPalette_color.setColor(QPalette.Shadow, QColor(20, 20, 20))
        self.darkPalette_color.setColor(QPalette.Button, QColor(53, 53, 53))
        self.darkPalette_color.setColor(QPalette.PlaceholderText, QColor(124, 53, 53))
        self.darkPalette_color.setColor(QPalette.ButtonText, Qt.white)
        self.darkPalette_color.setColor(
            QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127)
        )
        self.darkPalette_color.setColor(QPalette.BrightText, Qt.red)
        self.darkPalette_color.setColor(QPalette.Link, QColor(42, 130, 218))
        self.darkPalette_color.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.darkPalette_color.setColor(
            QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80)
        )
        self.darkPalette_color.setColor(QPalette.HighlightedText, Qt.white)
        self.darkPalette_color.setColor(
            QPalette.Disabled,
            QPalette.HighlightedText,
            QColor(127, 127, 127),
        )
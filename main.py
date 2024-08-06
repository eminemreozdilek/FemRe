import PySide6
import sys
import os
import logging
import time

os.environ["QT_API"] = "pyside6"

from PySide6.QtWidgets import QApplication
from ui import OpenWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OpenWindow()
    sys.exit(app.exec_())

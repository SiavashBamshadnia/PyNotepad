import sys

from PySide2 import QtWidgets

from PyNotepad import PyNotepad

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    notepad = PyNotepad()
    notepad.show()

    sys.exit(app.exec_())

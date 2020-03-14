import sys

from PySide2 import QtWidgets

from PyNotepad import PyNotepad

if __name__ == '__main__':
    app = QtWidgets.QApplication()

    args = sys.argv
    del args[0]

    if args:
        for arg in args:
            notepad = PyNotepad(arg)
            notepad.show()
    else:
        notepad = PyNotepad()
        notepad.show()

    sys.exit(app.exec_())

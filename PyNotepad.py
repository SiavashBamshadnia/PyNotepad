import ctypes
import hashlib
import os
import time
import urllib
import webbrowser

from PySide2 import QtWidgets, QtGui, QtPrintSupport

import syntax


class PyNotepad(QtWidgets.QMainWindow):
    windows = []

    def __init__(self, file_path=None):
        super().__init__()

        PyNotepad.windows.append(self)

        self.file_path = file_path

        self.resize(800, 600)
        icon = QtGui.QIcon('icon.png')
        self.setWindowIcon(icon)

        app_id = 'PyNotepad.1.0.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        self.text_edit_widget = QtWidgets.QPlainTextEdit()
        self.setCentralWidget(self.text_edit_widget)

        self.menubar = self.menuBar()
        self.file_menu = QtWidgets.QMenu('File', self)

        self.new_action = QtWidgets.QAction('New', self)
        self.new_action.setShortcut('Ctrl+N')
        self.new_action.triggered.connect(self.new)
        self.file_menu.addAction(self.new_action)

        self.new_window_action = QtWidgets.QAction('New Window', self)
        self.new_window_action.setShortcut('Ctrl+Shift+N')
        self.new_window_action.triggered.connect(PyNotepad.new_window)
        self.file_menu.addAction(self.new_window_action)

        self.open_action = QtWidgets.QAction('Open', self)
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.triggered.connect(self.open)
        self.file_menu.addAction(self.open_action)

        self.file_menu.addSeparator()

        self.print_action = QtWidgets.QAction('Print', self)
        self.print_action.setShortcut('Ctrl+P')
        self.print_action.triggered.connect(self.print)
        self.file_menu.addAction(self.print_action)

        self.save_action = QtWidgets.QAction('Save', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.save)
        self.file_menu.addAction(self.save_action)

        self.save_as_action = QtWidgets.QAction('Save As...', self)
        self.save_as_action.setShortcut('Ctrl+Shift+S')
        self.save_as_action.triggered.connect(self.save_as)
        self.file_menu.addAction(self.save_as_action)

        self.file_menu.addSeparator()

        self.close_action = QtWidgets.QAction('Close', self)
        self.close_action.triggered.connect(self.close)
        self.file_menu.addAction(self.close_action)

        self.close_all_action = QtWidgets.QAction('Close All', self)
        self.close_all_action.triggered.connect(PyNotepad.close_all)
        self.file_menu.addAction(self.close_all_action)

        self.menubar.addMenu(self.file_menu)

        self.edit_menu = QtWidgets.QMenu('Edit', self)

        self.undo_action = QtWidgets.QAction('Undo', self)
        self.undo_action.setShortcut('Ctrl+Z')
        self.undo_action.triggered.connect(self.text_edit_widget.undo)
        self.edit_menu.addAction(self.undo_action)

        self.redo_action = QtWidgets.QAction('Redo', self)
        self.redo_action.setShortcut('Ctrl+Y')
        self.redo_action.triggered.connect(self.text_edit_widget.redo)
        self.edit_menu.addAction(self.redo_action)

        self.edit_menu.addSeparator()

        self.cut_action = QtWidgets.QAction('Cut', self)
        self.cut_action.setShortcut('Ctrl+X')
        self.cut_action.triggered.connect(self.text_edit_widget.cut)
        self.edit_menu.addAction(self.cut_action)

        self.copy_action = QtWidgets.QAction('Copy', self)
        self.copy_action.setShortcut('Ctrl+C')
        self.copy_action.triggered.connect(self.text_edit_widget.copy)
        self.edit_menu.addAction(self.copy_action)

        self.paste_action = QtWidgets.QAction('Paste', self)
        self.paste_action.setShortcut('Ctrl+V')
        self.paste_action.triggered.connect(self.text_edit_widget.paste)
        self.edit_menu.addAction(self.paste_action)

        self.delete_action = QtWidgets.QAction('Delete', self)
        self.delete_action.setShortcut('Del')
        self.delete_action.triggered.connect(self.delete)
        self.edit_menu.addAction(self.delete_action)

        self.edit_menu.addSeparator()

        self.search_with_google_action = QtWidgets.QAction('Search with Google', self)
        self.search_with_google_action.setShortcut('Ctrl+E')
        self.search_with_google_action.triggered.connect(self.search_with_google)
        self.edit_menu.addAction(self.search_with_google_action)

        self.edit_menu.addSeparator()

        self.select_all_action = QtWidgets.QAction('Select All', self)
        self.select_all_action.setShortcut('Ctrl+A')
        self.select_all_action.triggered.connect(self.text_edit_widget.selectAll)
        self.edit_menu.addAction(self.select_all_action)

        self.time_date_action = QtWidgets.QAction('Time/Date', self)
        self.time_date_action.setShortcut('F5')
        self.time_date_action.triggered.connect(self.time_date)
        self.edit_menu.addAction(self.time_date_action)

        self.clear_action = QtWidgets.QAction('Clear', self)
        self.clear_action.triggered.connect(self.text_edit_widget.clear)
        self.edit_menu.addAction(self.clear_action)

        self.menubar.addMenu(self.edit_menu)

        self.format_menu = QtWidgets.QMenu('Format', self)

        self.font_action = QtWidgets.QAction('Font', self)
        self.font_action.triggered.connect(self._font)
        self.format_menu.addAction(self.font_action)

        self.highlight_syntax_action = QtWidgets.QAction('Python Syntax Highlighter', self, checkable=True)
        self.highlight_syntax_action.triggered.connect(self.highlight_syntax)
        self.format_menu.addAction(self.highlight_syntax_action)

        self.menubar.addMenu(self.format_menu)

        help_menu = QtWidgets.QMenu('Help', self)

        about_action = QtWidgets.QAction('About', self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        self.menubar.addMenu(help_menu)

        self.text_edit_widget.textChanged.connect(self.text_changed)
        self.text_changed()

        self.text_edit_widget.selectionChanged.connect(self.selection_changed)
        self.selection_changed()

        self.text_edit_widget.cursorPositionChanged.connect(self.cursor_position_changed)
        self.cursor_position_changed()

        self.text_edit_widget.undoAvailable.connect(self.undo_action.setEnabled)
        self.undo_action.setEnabled(False)

        self.text_edit_widget.redoAvailable.connect(self.redo_action.setEnabled)
        self.redo_action.setEnabled(False)

        if file_path:
            file = open(file_path, encoding='utf-8')
            file_content = file.read()
            self.text_edit_widget.setPlainText(file_content)

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value
        if value:
            file_name = os.path.basename(value)
            self.setWindowTitle(file_name + ' - PyNotepad')
        else:
            self.setWindowTitle('PyNotepad')

    def closeEvent(self, event):
        if self.changes_saved():
            return
        answer = QtWidgets.QMessageBox.question(None, 'PyNotepad', 'Do you want to save changes?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                                                QtWidgets.QMessageBox.Cancel)
        if answer == QtWidgets.QMessageBox.Yes:
            self.save()
        elif answer == QtWidgets.QMessageBox.Cancel:
            event.ignore()

    def text_changed(self):
        text = self.text_edit_widget.toPlainText()
        length = len(text)
        if length == 0:
            self.print_action.setEnabled(False)
            self.search_with_google_action.setEnabled(False)
            self.select_all_action.setEnabled(False)
            self.clear_action.setEnabled(False)
        else:
            self.print_action.setEnabled(True)
            self.search_with_google_action.setEnabled(True)
            self.select_all_action.setEnabled(True)
            self.clear_action.setEnabled(True)

    def selection_changed(self):
        selected_text = self.text_edit_widget.textCursor().selectedText()
        length = len(selected_text)
        if length == 0:
            self.cut_action.setEnabled(False)
            self.copy_action.setEnabled(False)
            self.delete_action.setEnabled(False)
        else:
            self.cut_action.setEnabled(True)
            self.copy_action.setEnabled(True)
            self.delete_action.setEnabled(True)

    def cursor_position_changed(self):
        block_number = self.text_edit_widget.textCursor().blockNumber()
        column_number = self.text_edit_widget.textCursor().columnNumber()
        self.statusBar().showMessage('{}:{}'.format(block_number, column_number))

    def new(self):
        PyNotepad.new_window()
        self.close()

    @staticmethod
    def new_window():
        notepad = PyNotepad()
        notepad.show()

    def open(self):
        name = QtWidgets.QFileDialog.getOpenFileNames(None, filter='Text Files (*.txt);;All Files (*)')
        paths = name[0]
        if not paths:
            return
        for path in paths:
            notepad = PyNotepad(path)
            notepad.show()
        self.close()

    def print(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.text_edit_widget.print_)
        dialog.exec_()

    def save(self):
        if not self.file_path:
            self.save_as()
        else:
            writable_file = open(self.file_path, 'w', encoding='utf-8')
            text = self.text_edit_widget.toPlainText()
            writable_file.write(text)
            writable_file.close()

    def save_as(self):
        name = QtWidgets.QFileDialog.getSaveFileName(None, filter='Text Files (*.txt);;All Files (*)')
        self.file_path = name[0]
        if not self.file_path:
            return False
        file = open(self.file_path, 'w', encoding='utf-8')
        text = self.text_edit_widget.toPlainText()
        file.write(text)
        file.close()
        return True

    @staticmethod
    def close_all():
        for window in PyNotepad.windows:
            window.close()

    def delete(self):
        self.text_edit_widget.textCursor().removeSelectedText()

    def search_with_google(self):
        search_query = {'q': self.text_edit_widget.toPlainText()}
        url = 'https://google.com/search?' + urllib.parse.urlencode(search_query)
        webbrowser.open(url)

    def time_date(self):
        t = time.localtime()
        current_time = time.strftime('%r %x', t)
        self.text_edit_widget.textCursor().insertText(current_time)

    def _font(self):
        ok, font = QtWidgets.QFontDialog.getFont(self.text_edit_widget.font())
        if ok:
            self.text_edit_widget.setFont(font)

    def highlight_syntax(self, checked):
        if checked:
            self.highlighter = syntax.PythonHighlighter(self.text_edit_widget.document())
        else:
            self.highlighter.setDocument(None)

    def about(self):
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle('About PyNotepad')
        message_box.setTextFormat(QtGui.Qt.RichText)
        text = 'This software is an implementation of the Notepad written in Python language <br>' \
               'Github repository: <a href="https://github.com/SiavashBamshadnia/PyNotepad">https://github.com/SiavashBamshadnia/PyNotepad</a> <br>' \
               'Written with ♥ by Siavash Bamshadnia'
        message_box.setText(text)
        message_box.setIconPixmap(QtGui.QPixmap('icon.png'))
        message_box.exec()

    def changes_saved(self):
        new_text = self.text_edit_widget.toPlainText()
        if not self.file_path:
            return not new_text
        old_file = open(self.file_path, encoding='utf-8')
        old_text = old_file.read()
        old_md5 = get_md5(old_text)
        new_md5 = get_md5(new_text)
        return old_md5 == new_md5


def get_md5(my_string):
    md5 = hashlib.md5()
    md5.update(my_string.encode('utf-8'))
    return md5.hexdigest()

from PyQt5.QtCore import Qt, QSize, QItemSelectionModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QStyledItemDelegate
from .view import *
from .reader import Reader
from typing import List, Tuple


def make_enumeration(list_: List[str]) -> List[Tuple[int, str]]:
    return list(enumerate(list_))


class WrappingDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(size.height() * 2)  # Adjust as needed
        return size

class VerseItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        # Reduce the height of each row for compact display
        size = super().sizeHint(option, index)
        return QSize(size.width(), max(18, size.height() - 6))  # minimum of 18 pixels


class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.reader = Reader()
        self.reader.set_root("NLT")

        self.textAreaModel = QStandardItemModel()
        self.textArea.setModel(self.textAreaModel)
        self.textArea.setSelectionMode(QAbstractItemView.SingleSelection)
        self.textArea.setSelectionBehavior(QAbstractItemView.SelectRows)


        # Ensure wrapping and proper item sizing in QListView
        self.textArea.setViewMode(QListView.ListMode)
        self.textArea.setWrapping(True)
        self.textArea.setWordWrap(True)
        self.textArea.setUniformItemSizes(False)
        self.textArea.setItemDelegate(WrappingDelegate(self.textArea))

        self.setUpActions()

        self.populate_translations()
        self.listTranslations.setCurrentRow(0)
        self.listTranslations.setFocus()

        self.show()

    def setUpActions(self):
        self.toggleButton.clicked.connect(self.collapse_sidebar)

        self.listTranslations.currentItemChanged.connect(self.on_translation_selected)
        self.listBooks.currentItemChanged.connect(self.on_book_selected)
        self.listChapters.currentItemChanged.connect(self.on_chapter_selected)
        self.listVerses.currentItemChanged.connect(self.display_verse_text)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def keyPressEvent(self, event):
        current_index = self.stackedWidget.currentIndex()
        total_pages = self.stackedWidget.count()
        focused_widget = QApplication.focusWidget()

        if event.key() == Qt.Key_Right and current_index < total_pages - 1:
            self.stackedWidget.setCurrentIndex(current_index + 1)
        elif event.key() == Qt.Key_Left and current_index > 0:
            self.stackedWidget.setCurrentIndex(current_index - 1)
        elif event.key() in (Qt.Key_Up, Qt.Key_Down):
            if isinstance(focused_widget, QListWidget):
                current_row = focused_widget.currentRow()
                max_row = focused_widget.count() - 1

                if event.key() == Qt.Key_Up and current_row > 0:
                    focused_widget.setCurrentRow(current_row - 1)
                elif event.key() == Qt.Key_Down and current_row < max_row:
                    focused_widget.setCurrentRow(current_row + 1)

            elif isinstance(focused_widget, QListView):
                selection_model = focused_widget.selectionModel()
                current_index = selection_model.currentIndex()
                row = current_index.row()

                if event.key() == Qt.Key_Up and row > 0:
                    next_index = self.textAreaModel.index(row - 1, 0)
                    selection_model.setCurrentIndex(next_index, QItemSelectionModel.SelectCurrent)
                elif event.key() == Qt.Key_Down and row < self.textAreaModel.rowCount() - 1:
                    next_index = self.textAreaModel.index(row + 1, 0)
                    selection_model.setCurrentIndex(next_index, QItemSelectionModel.SelectCurrent)

        else:
            super().keyPressEvent(event)


    def collapse_sidebar(self):
        current_width = self.sidebarContainer.width()
        self.sidebarContainer.setMaximumWidth(5 if current_width > 5 else 200)

    def populate_translations(self):
        self.translations = make_enumeration(self.reader.get_translations())
        self.listTranslations.clear()
        for _, item in self.translations:
            self.listTranslations.addItem(item)

    def on_translation_selected(self, current, previous):
        if current:
            self.reader.set_root(current.text())
            self.listBooks.clear()
            self.listChapters.clear()
            self.listVerses.clear()
            self.textAreaModel.clear()
            self.populate_books()
            self.listBooks.setCurrentRow(0)

    def populate_books(self):
        self.books = make_enumeration(self.reader.get_books())
        self.listBooks.clear()
        for _, book in self.books:
            self.listBooks.addItem(book)

    def on_book_selected(self, current, previous):
        if current:
            self.book_name = current.text()
            self.listChapters.clear()
            self.listVerses.clear()
            self.textAreaModel.clear()
            self.populate_chapters(self.book_name)
            self.listChapters.setCurrentRow(0)

    def populate_chapters(self, book_name: str):
        self.chapters = make_enumeration(self.reader.get_chapters(book_name))
        self.chapter_number = self.chapters[0][1] if self.chapters else "1"

        for _, chapter in self.chapters:
            self.listChapters.addItem(chapter)

    def on_chapter_selected(self, current, previous):
        if current:
            self.chapter_number = current.text()
            self.listVerses.clear()
            self.textAreaModel.clear()
            self.populate_verses(self.book_name, self.chapter_number)
            self.listVerses.setCurrentRow(0)

    def populate_verses(self, book: str, chapter: str):
        self.verses = make_enumeration(self.reader.get_verses(book, chapter))
        for _, verse in self.verses:
            self.listVerses.addItem(verse)

    def display_verse_text(self, item):
        try:
            verse_number = int(item.text()) if item else 1
            book = self.listBooks.currentItem().text() if self.listBooks.currentItem() else self.books[0][1]
            chapter = self.listChapters.currentItem().text() if self.listChapters.currentItem() else self.chapters[0][1]

            verses = self.reader.get_chapter_text(book, chapter, verse_number)

            self.textAreaModel.clear()

            for verse_text, is_red, is_title in verses:
                item = QStandardItem(verse_text)

                if is_red:
                    item.setForeground(Qt.red)
                elif is_title:
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
                self.textAreaModel.appendRow(item)

        except Exception as e:
            self.textAreaModel.clear()
            error_item = QStandardItem(f"Error displaying verse: {e}")
            self.textAreaModel.appendRow(error_item)

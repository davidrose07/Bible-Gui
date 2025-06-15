

from PyQt5.QtCore import Qt
from .view import *
from .reader import Reader
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from typing import List, Tuple
import os

def make_enumeration(list_: List[str]) -> List[Tuple[int, str]]:
    """
    Enumerate a list and return a list of (index, item) tuples.

    :param list_: A list of strings.
    :return: List of tuples pairing index with item.
    """
    return list(enumerate(list_))

class Controller(QMainWindow, Ui_MainWindow):    
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setUpActions()
        self.initialize_reader()

        self.show()

    def setUpActions(self):
        self.toggleButton.clicked.connect(self.collapse_sidebar)
        #TODO: Add events to change sidebar options and verse text when another selection has been made
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()


    def keyPressEvent(self, event):
        current_index = self.stackedWidget.currentIndex()
        total_pages = self.stackedWidget.count()

        if event.key() == Qt.Key_Right:
            if current_index < total_pages - 1:
                self.stackedWidget.setCurrentIndex(current_index + 1)

        elif event.key() == Qt.Key_Left:
            if current_index > 0:
                self.stackedWidget.setCurrentIndex(current_index - 1)

        else:
            super().keyPressEvent(event)

    def initialize_reader(self) -> None:
        """Initialize the reader object for reading text data."""
        self.reader = Reader()
        self.reader.set_root("NLT")  # Set the root text version, e.g., NIV Bible
        self.populate_sidebar()

    def collapse_sidebar(self):
        current_width = self.sidebarContainer.width()
        if current_width > 5:
            self.sidebarContainer.setMaximumWidth(5)
        else:
            self.sidebarContainer.setMaximumWidth(200)

    def display_verse_text(self, item):
        #TODO: populate all verses from currently selected verse(default to first verse) till the end of the currently selected chapter(default chapter 1)
        pass

    def get_current_selections(self):
        self.current_translation = self.listTranslations.currentItem().text()
        self.current_book = self.listBooks.currentItem().text()
        self.current_chapter = self.listChapters.currentItem().text()
        self.current_verse = self.listVerses.currentItem().text()
                          
    def populate_sidebar(self):
        self.translations = make_enumeration(self.reader.get_translations())
        self.books = make_enumeration(self.reader.get_books())

        self.chapters = []
        self.verses = []

        book_name = self.books[0][1] if self.books else None
        if book_name:
            self.chapters = make_enumeration(self.reader.get_chapters(book_name))

        chapter_number = self.chapters[0][1] if self.chapters else None
        if chapter_number:
            self.verses = make_enumeration(self.reader.get_verses(book_name, chapter_number))
            

    def add_sidebar_items(self):
        # Clear the widgets before adding new items
        self.listTranslations.clear()
        self.listBooks.clear()
        self.listChapters.clear()
        self.listVerses.clear()

        for _, item in self.translations:
            self.listTranslations.addItem(item)

        for _, book in self.books:
            self.listBooks.addItem(book)

        for _, chapter in self.chapters:
            self.listChapters.addItem(chapter)

        for _, verse in self.verses:
            self.listVerses.addItem(verse)

    
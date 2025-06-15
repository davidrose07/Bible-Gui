

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
        self.listTranslations.currentItemChanged.connect(self.current_translation)
        self.listBooks.currentItemChanged.connect(self.current_book)
        self.listChapters.currentItemChanged.connect(self.current_chapter)
        self.listVerses.currentItemChanged.connect(self.display_verse_text)
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
        verse_number = item.text()

        if hasattr(self, "book_name") and hasattr(self, "chapter") and self.book_name and self.chapter:
            # Get all verses in the chapter
            all_verses = self.reader.get_verses(self.book_name, self.chapter)

            # Find the starting index (0-based)
            try:
                start_index = all_verses.index(verse_number)
            except ValueError:
                self.textArea.setText("Verse not found in chapter.")
                return

            # Get all verses from selected verse to end
            verses_to_display = all_verses[start_index:]

            # Get the text for each verse
            text_parts = []
            for verse in verses_to_display:
                verse_text = self.reader.get_verse_text(self.book_name, self.chapter, verse)
                text_parts.append(f"{verse} {verse_text}")

            # Display in textArea
            self.textArea.setText("\n".join(text_parts))
        else:
            self.textArea.setText("Book or chapter not selected.")


    def current_translation(self):
        self.translation = self.listTranslations.currentItem().text()
    
    def current_book(self):
        self.book_name = self.listBooks.currentItem().text()
    
    def current_chapter(self):
        self.chapter = self.listChapters.currentItem().text()
              
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

    
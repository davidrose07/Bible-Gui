

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
        
        # Initialize the Reader Object
        self.initialize_reader()

        # Setup event actions
        self.setUpActions()
        
        #Populaate the sidebar menu
        self.populate_translations_books()
        self.populate_chapters_verse()
        
        self.show()

    def setUpActions(self):
        self.toggleButton.clicked.connect(self.collapse_sidebar)
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
        #self.get_current_selections()

    def initialize_reader(self) -> None:
        """Initialize the reader object for reading text data."""
        self.reader = Reader()
        self.reader.set_root("NLT")  # Set the root text version, e.g., NIV Bible
        
    def update(self):
        self.textArea.clear()
        self.listTranslations.clear()
        self.listBooks.clear()
        self.listChapters.clear()
        self.listVerses.clear()

        self.populate_translation_book()
        self.populate_chapter_verse()

	def collapse_sidebar(self):
        current_width = self.sidebarContainer.width()
        if current_width > 5:
            self.sidebarContainer.setMaximumWidth(5)
        else:
            self.sidebarContainer.setMaximumWidth(200)

    """ def get_current_selections(self):
        self.current_translation = self.listTranslations.currentItem().text()
        self.current_book = self.listBooks.currentItem().text()
        self.current_chapter = self.listChapters.currentItem().text()
        self.current_verse = self.listVerses.currentItem().text() """
                          
    def populate_translations_books(self):
        self.translations = make_enumeration(self.reader.get_translations())
        self.books = make_enumeration(self.reader.get_books())

        for _, item in self.translations:
            self.listTranslations.addItem(item)

        for _, book in self.books:
            self.listBooks.addItem(book)


    def populate_chapters_verse(self):
        self.chapters = []
        self.verses = []

        book_name = self.books[0][1] if self.books else None
        if not book_name:
            self.textArea.setText("No book found.")
            return

        self.chapters = make_enumeration(self.reader.get_chapters(book_name))
        chapter_number = self.chapters[0][1] if self.chapters else "1"
        self.verses = make_enumeration(self.reader.get_verses(book_name, chapter_number))

        self.listChapters.clear()
        self.listVerses.clear()

        for _, chapter in self.chapters:
            self.listChapters.addItem(chapter)

        for _, verse in self.verses:
            self.listVerses.addItem(verse)

        # Default to chapter 1 and verse 1
        self.listChapters.setCurrentRow(0)
        self.listVerses.setCurrentRow(0)

        # Trigger display of full chapter from verse 1
        if self.listVerses.count() > 0:
            self.display_verse_text(self.listVerses.item(0))

    def display_verse_text(self, item):
        #TODO: populate all verses from currently selected verse(default to first verse) till the end of the currently selected chapter(default chapter 1)
        try:
            item = int(item.text())
            verses = self.reader.get_chapter_text(self.books[0][1], self.chapters[0][1], item)
            
            
            for verse, _ ,_ in verses:
                self.textArea.addItem(verse)
        except Exception as e:
            print(e)



        

        

    

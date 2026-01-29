"""
Book model for managing e-book data
"""
import json
import os
from datetime import datetime
from typing import List, Optional


class Page:
    """Represents a single page in a book"""
    
    def __init__(self, image_path: str, page_number: int):
        self.image_path = image_path
        self.page_number = page_number
    
    def to_dict(self) -> dict:
        return {
            'image_path': self.image_path,
            'page_number': self.page_number
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Page':
        return Page(data['image_path'], data['page_number'])


class Book:
    """Represents a complete e-book"""
    
    def __init__(self, title: str = "Untitled"):
        self.title = title
        self.pages: List[Page] = []
        self.cover_page_index: int = 0
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
    
    def add_page(self, image_path: str) -> None:
        """Add a page to the book"""
        page_number = len(self.pages)
        self.pages.append(Page(image_path, page_number))
        self._update_modified_time()
    
    def remove_page(self, page_index: int) -> None:
        """Remove a page from the book"""
        if 0 <= page_index < len(self.pages):
            self.pages.pop(page_index)
            # Update page numbers
            for i, page in enumerate(self.pages):
                page.page_number = i
            # Adjust cover page index if necessary
            if self.cover_page_index >= len(self.pages):
                self.cover_page_index = max(0, len(self.pages) - 1)
            self._update_modified_time()
    
    def move_page(self, from_index: int, to_index: int) -> None:
        """Move a page from one position to another"""
        if 0 <= from_index < len(self.pages) and 0 <= to_index < len(self.pages):
            page = self.pages.pop(from_index)
            self.pages.insert(to_index, page)
            # Update page numbers
            for i, p in enumerate(self.pages):
                p.page_number = i
            self._update_modified_time()
    
    def set_cover_page(self, page_index: int) -> None:
        """Set the cover page"""
        if 0 <= page_index < len(self.pages):
            self.cover_page_index = page_index
            self._update_modified_time()
    
    def get_page_image_path(self, page_index: int) -> Optional[str]:
        """Get the image path for a specific page"""
        if 0 <= page_index < len(self.pages):
            return self.pages[page_index].image_path
        return None
    
    def _update_modified_time(self) -> None:
        """Update the modified timestamp"""
        self.modified_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert book to dictionary for serialization"""
        return {
            'title': self.title,
            'pages': [page.to_dict() for page in self.pages],
            'cover_page_index': self.cover_page_index,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Book':
        """Create a book from a dictionary"""
        book = Book(data['title'])
        book.pages = [Page.from_dict(page_data) for page_data in data['pages']]
        book.cover_page_index = data['cover_page_index']
        book.created_at = datetime.fromisoformat(data['created_at'])
        book.modified_at = datetime.fromisoformat(data['modified_at'])
        return book

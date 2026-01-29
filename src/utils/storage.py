"""
File storage utility for saving and loading books
"""
import json
import os
from typing import Optional
from ..models.book import Book


class BookStorage:
    """Handles persistent storage of books"""
    
    def __init__(self, storage_dir: str = "books"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def save_book(self, book: Book, filename: str) -> bool:
        """Save a book to disk"""
        try:
            filepath = os.path.join(self.storage_dir, f"{filename}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(book.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving book: {e}")
            return False
    
    def load_book(self, filename: str) -> Optional[Book]:
        """Load a book from disk"""
        try:
            filepath = os.path.join(self.storage_dir, f"{filename}.json")
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Book.from_dict(data)
        except Exception as e:
            print(f"Error loading book: {e}")
            return None
    
    def list_books(self) -> list:
        """List all saved books"""
        try:
            books = []
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json'):
                    book_name = filename[:-5]  # Remove .json extension
                    books.append(book_name)
            return sorted(books)
        except Exception as e:
            print(f"Error listing books: {e}")
            return []
    
    def delete_book(self, filename: str) -> bool:
        """Delete a saved book"""
        try:
            filepath = os.path.join(self.storage_dir, f"{filename}.json")
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False

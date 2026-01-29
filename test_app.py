"""
Test script to verify application functionality
"""
import sys
sys.path.insert(0, '.')

from src.models.book import Book
from src.utils.storage import BookStorage

# Test 1: Create a book
print("Test 1: Creating a book...")
book = Book("Test Book")
print(f"✓ Created book: {book.title}")

# Test 2: Add pages
print("\nTest 2: Adding test pages...")
# Create test PNG files (1x1 pixel white PNG)
import os
from PIL import Image

os.makedirs("test_images", exist_ok=True)
for i in range(3):
    img = Image.new('RGB', (100, 150), color='white')
    img.save(f"test_images/page{i}.png")
    book.add_page(f"test_images/page{i}.png")

print(f"✓ Added {len(book.pages)} pages")

# Test 3: Test page operations
print("\nTest 3: Testing page operations...")
print(f"  Pages before move: {[p.page_number for p in book.pages]}")
book.move_page(0, 2)
print(f"  Pages after move: {[p.page_number for p in book.pages]}")

# Test 4: Set cover page
print("\nTest 4: Setting cover page...")
book.set_cover_page(1)
print(f"✓ Cover page set to index: {book.cover_page_index}")

# Test 5: Test storage
print("\nTest 5: Testing storage...")
storage = BookStorage(storage_dir="test_books")
storage.save_book(book, "test_book")
print("✓ Book saved")

loaded_book = storage.load_book("test_book")
print(f"✓ Book loaded: {loaded_book.title} with {len(loaded_book.pages)} pages")

# Cleanup
import shutil
if os.path.exists("test_images"):
    shutil.rmtree("test_images")
if os.path.exists("test_books"):
    shutil.rmtree("test_books")

print("\n✓ All tests passed!")

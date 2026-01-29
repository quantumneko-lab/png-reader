"""
Main application window
"""
import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from ..models.book import Book
from ..utils.storage import BookStorage
from .page_manager import PageManagerWidget
from .viewer import ImageViewerWidget
from .book_manager import BookManagerWidget


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("電子書籍ツール - E-Book Viewer")
        self.setGeometry(100, 100, 1400, 900)
        
        self.current_book = None
        self.storage = BookStorage(storage_dir="books")
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Main central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # Create toolbar
        toolbar_layout = self.create_toolbar()
        main_layout.addLayout(toolbar_layout)
        
        # Create main content area with splitter
        content_layout = QHBoxLayout()
        
        # Left side: Page manager
        self.page_manager = PageManagerWidget()
        self.page_manager.page_selected.connect(self.on_page_selected)
        self.page_manager.page_moved.connect(self.on_pages_reordered)
        self.page_manager.page_deleted.connect(self.on_page_deleted)
        self.page_manager.cover_set.connect(self.on_cover_set)
        
        # Right side: Image viewer
        self.image_viewer = ImageViewerWidget()
        
        # Add widgets to splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.page_manager)
        splitter.addWidget(self.image_viewer)
        splitter.setSizes([400, 800])
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        content_layout.addWidget(splitter)
        main_layout.addLayout(content_layout)
        
        central_widget.setLayout(main_layout)
    
    def create_toolbar(self) -> QHBoxLayout:
        """Create the toolbar"""
        toolbar_layout = QHBoxLayout()
        
        # New book button
        new_book_btn = QPushButton("新規作成")
        new_book_btn.clicked.connect(self.new_book)
        toolbar_layout.addWidget(new_book_btn)
        
        # Open book button
        open_book_btn = QPushButton("開く")
        open_book_btn.clicked.connect(self.open_book_dialog)
        toolbar_layout.addWidget(open_book_btn)
        
        # Add images button
        add_images_btn = QPushButton("画像を追加")
        add_images_btn.clicked.connect(self.add_images)
        toolbar_layout.addWidget(add_images_btn)
        
        # Save book button
        save_book_btn = QPushButton("保存")
        save_book_btn.clicked.connect(self.save_book)
        toolbar_layout.addWidget(save_book_btn)
        
        toolbar_layout.addStretch()
        
        # Book title label
        self.title_label = QLabel("新規書籍")
        toolbar_layout.addWidget(self.title_label)
        
        return toolbar_layout
    
    def new_book(self):
        """Create a new book"""
        self.current_book = Book("新規書籍")
        self.page_manager.set_book(self.current_book)
        self.image_viewer.clear()
        self.title_label.setText("新規書籍")
    
    def add_images(self):
        """Add images to the current book"""
        if self.current_book is None:
            QMessageBox.warning(self, "警告", "最初に書籍を新規作成してください。")
            return
        
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("PNG Images (*.png)")
        
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                self.current_book.add_page(file_path)
            
            self.page_manager.set_book(self.current_book)
            QMessageBox.information(self, "成功", f"{len(file_paths)}個の画像を追加しました。")
    
    def on_page_selected(self, page_index: int):
        """Handle page selection"""
        if self.current_book and 0 <= page_index < len(self.current_book.pages):
            image_path = self.current_book.pages[page_index].image_path
            self.image_viewer.load_image(image_path)
    
    def on_pages_reordered(self):
        """Handle pages reordering"""
        if self.current_book:
            self.page_manager.set_book(self.current_book)
    
    def on_page_deleted(self):
        """Handle page deletion"""
        if self.current_book:
            self.page_manager.set_book(self.current_book)
            self.image_viewer.clear()
    
    def on_cover_set(self, page_index: int):
        """Handle cover page setting"""
        if self.current_book:
            self.current_book.set_cover_page(page_index)
            self.page_manager.set_book(self.current_book)
    
    def save_book(self):
        """Save the current book"""
        if self.current_book is None:
            QMessageBox.warning(self, "警告", "保存する書籍がありません。")
            return
        
        filename, ok = self.get_save_filename()
        if ok and filename:
            if self.storage.save_book(self.current_book, filename):
                QMessageBox.information(self, "成功", "書籍を保存しました。")
                self.title_label.setText(filename)
            else:
                QMessageBox.critical(self, "エラー", "書籍の保存に失敗しました。")
    
    def open_book_dialog(self):
        """Open a saved book"""
        books = self.storage.list_books()
        if not books:
            QMessageBox.information(self, "情報", "保存された書籍がありません。")
            return
        
        # Simple book selection dialog
        from .book_manager import BookManagerWidget
        dialog = BookManagerWidget(self.storage)
        dialog.exec_()
        
        selected_book = dialog.selected_book
        if selected_book:
            self.current_book = selected_book
            self.page_manager.set_book(self.current_book)
            self.image_viewer.clear()
            self.title_label.setText(self.current_book.title)
    
    def get_save_filename(self) -> tuple:
        """Get filename for saving book"""
        dialog = QFileDialog()
        dialog.setDefaultSuffix("json")
        dialog.setNameFilter("JSON Files (*.json)")
        dialog.setFileMode(QFileDialog.AnyFile)
        
        if dialog.exec_():
            files = dialog.selectedFiles()
            if files:
                filename = os.path.splitext(os.path.basename(files[0]))[0]
                return filename, True
        
        return "", False

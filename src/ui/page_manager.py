"""
Page manager widget for managing book pages
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QMessageBox, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QMenu
from ..models.book import Book


class PageManagerWidget(QWidget):
    """Widget for managing pages in a book"""
    
    page_selected = pyqtSignal(int)  # Emitted when a page is selected
    page_moved = pyqtSignal()  # Emitted when pages are reordered
    page_deleted = pyqtSignal()  # Emitted when a page is deleted
    cover_set = pyqtSignal(int)  # Emitted when cover is set
    
    def __init__(self):
        super().__init__()
        self.current_book = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("ページ管理")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Page list
        self.page_list = QListWidget()
        self.page_list.itemSelectionChanged.connect(self.on_page_selection_changed)
        self.page_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.page_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.page_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        delete_btn = QPushButton("削除")
        delete_btn.clicked.connect(self.delete_page)
        button_layout.addWidget(delete_btn)
        
        move_up_btn = QPushButton("↑")
        move_up_btn.clicked.connect(self.move_page_up)
        button_layout.addWidget(move_up_btn)
        
        move_down_btn = QPushButton("↓")
        move_down_btn.clicked.connect(self.move_page_down)
        button_layout.addWidget(move_down_btn)
        
        set_cover_btn = QPushButton("表紙に設定")
        set_cover_btn.clicked.connect(self.set_as_cover)
        button_layout.addWidget(set_cover_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def set_book(self, book: Book):
        """Set the book to manage"""
        self.current_book = book
        self.update_page_list()
    
    def update_page_list(self):
        """Update the page list display"""
        self.page_list.clear()
        
        if not self.current_book:
            return
        
        for i, page in enumerate(self.current_book.pages):
            item_text = f"ページ {i + 1}"
            if i == self.current_book.cover_page_index:
                item_text += " (表紙)"
            
            item = QListWidgetItem(item_text)
            # Add thumbnail if possible
            try:
                pixmap = QPixmap(page.image_path)
                if not pixmap.isNull():
                    thumbnail = pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation)
                    item.setIcon(QIcon(thumbnail))
            except:
                pass
            
            self.page_list.addItem(item)
    
    def on_page_selection_changed(self):
        """Handle page selection change"""
        if self.page_list.currentRow() >= 0:
            self.page_selected.emit(self.page_list.currentRow())
    
    def delete_page(self):
        """Delete the selected page"""
        if not self.current_book:
            return
        
        current_index = self.page_list.currentRow()
        if current_index < 0:
            QMessageBox.warning(self, "警告", "ページを選択してください。")
            return
        
        reply = QMessageBox.question(
            self, "確認", 
            f"ページ {current_index + 1} を削除してもよろしいですか？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.current_book.remove_page(current_index)
            self.update_page_list()
            self.page_deleted.emit()
    
    def move_page_up(self):
        """Move the selected page up"""
        if not self.current_book:
            return
        
        current_index = self.page_list.currentRow()
        if current_index <= 0:
            QMessageBox.warning(self, "警告", "上に移動できません。")
            return
        
        self.current_book.move_page(current_index, current_index - 1)
        self.update_page_list()
        self.page_list.setCurrentRow(current_index - 1)
        self.page_moved.emit()
    
    def move_page_down(self):
        """Move the selected page down"""
        if not self.current_book:
            return
        
        current_index = self.page_list.currentRow()
        if current_index < 0 or current_index >= len(self.current_book.pages) - 1:
            QMessageBox.warning(self, "警告", "下に移動できません。")
            return
        
        self.current_book.move_page(current_index, current_index + 1)
        self.update_page_list()
        self.page_list.setCurrentRow(current_index + 1)
        self.page_moved.emit()
    
    def set_as_cover(self):
        """Set the selected page as cover"""
        if not self.current_book:
            return
        
        current_index = self.page_list.currentRow()
        if current_index < 0:
            QMessageBox.warning(self, "警告", "ページを選択してください。")
            return
        
        self.current_book.set_cover_page(current_index)
        self.update_page_list()
        self.cover_set.emit(current_index)
    
    def show_context_menu(self, position):
        """Show context menu for page operations"""
        menu = QMenu()
        menu.addAction("削除", self.delete_page)
        menu.addAction("↑ 上に移動", self.move_page_up)
        menu.addAction("↓ 下に移動", self.move_page_down)
        menu.addSeparator()
        menu.addAction("表紙に設定", self.set_as_cover)
        
        menu.exec_(self.page_list.mapToGlobal(position))

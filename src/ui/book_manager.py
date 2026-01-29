"""
Book manager dialog for loading and managing saved books
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from ..utils.storage import BookStorage


class BookManagerWidget(QDialog):
    """Dialog for managing saved books"""
    
    def __init__(self, storage: BookStorage, parent=None):
        super().__init__(parent)
        self.storage = storage
        self.selected_book = None
        self.setWindowTitle("書籍を開く")
        self.setGeometry(200, 200, 400, 500)
        
        self.init_ui()
        self.load_book_list()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("保存された書籍")
        title.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(title)
        
        # Book list
        self.book_list = QListWidget()
        layout.addWidget(self.book_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        open_btn = QPushButton("開く")
        open_btn.clicked.connect(self.open_selected_book)
        button_layout.addWidget(open_btn)
        
        delete_btn = QPushButton("削除")
        delete_btn.clicked.connect(self.delete_selected_book)
        button_layout.addWidget(delete_btn)
        
        cancel_btn = QPushButton("キャンセル")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_book_list(self):
        """Load the list of saved books"""
        self.book_list.clear()
        books = self.storage.list_books()
        
        for book_name in books:
            item = QListWidgetItem(book_name)
            self.book_list.addItem(item)
    
    def open_selected_book(self):
        """Open the selected book"""
        if self.book_list.currentRow() < 0:
            QMessageBox.warning(self, "警告", "書籍を選択してください。")
            return
        
        book_name = self.book_list.currentItem().text()
        self.selected_book = self.storage.load_book(book_name)
        
        if self.selected_book:
            self.accept()
        else:
            QMessageBox.critical(self, "エラー", "書籍の読み込みに失敗しました。")
    
    def delete_selected_book(self):
        """Delete the selected book"""
        if self.book_list.currentRow() < 0:
            QMessageBox.warning(self, "警告", "書籍を選択してください。")
            return
        
        book_name = self.book_list.currentItem().text()
        reply = QMessageBox.question(
            self, "確認",
            f"『{book_name}』を削除してもよろしいですか？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.storage.delete_book(book_name):
                QMessageBox.information(self, "成功", "書籍を削除しました。")
                self.load_book_list()
            else:
                QMessageBox.critical(self, "エラー", "書籍の削除に失敗しました。")

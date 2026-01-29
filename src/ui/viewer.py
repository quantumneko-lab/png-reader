"""
Image viewer widget for displaying book pages
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ImageViewerWidget(QWidget):
    """Widget for displaying images"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc;")
        self.image_label.setMinimumSize(400, 600)
        
        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.image_label)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { background-color: #f0f0f0; }")
        
        layout.addWidget(scroll_area)
        self.setLayout(layout)
    
    def load_image(self, image_path: str):
        """Load and display an image"""
        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                self.image_label.setText("画像を読み込めませんでした")
            else:
                # Scale image to fit the widget while maintaining aspect ratio
                scaled_pixmap = pixmap.scaledToWidth(
                    min(pixmap.width(), 1000),
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
        except Exception as e:
            self.image_label.setText(f"エラー: {str(e)}")
    
    def clear(self):
        """Clear the displayed image"""
        self.image_label.clear()
        self.image_label.setText("ページを選択してください")

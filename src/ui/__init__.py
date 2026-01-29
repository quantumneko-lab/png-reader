"""
UI package initialization
"""
from .main_window import MainWindow
from .viewer import ImageViewerWidget
from .page_manager import PageManagerWidget
from .book_manager import BookManagerWidget

__all__ = [
    'MainWindow',
    'ImageViewerWidget',
    'PageManagerWidget',
    'BookManagerWidget'
]

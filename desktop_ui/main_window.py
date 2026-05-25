import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from overlay_window import OverlayWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.overlay = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('实时视频翻译 控制中心')
        self.resize(350, 200)

        layout = QVBoxLayout()

        # Target Language
        layout.addWidget(QLabel("目标语言:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["zh", "en", "ja"])
        layout.addWidget(self.lang_combo)

        # Toggle Subtitle Window
        self.toggle_btn = QPushButton("开启桌面字幕", self)
        self.toggle_btn.clicked.connect(self.toggle_overlay)
        self.toggle_btn.setStyleSheet("padding: 10px; font-weight: bold; background-color: #0078D4; color: white;")
        layout.addWidget(self.toggle_btn)

        self.setLayout(layout)

    def toggle_overlay(self):
        if self.overlay is None:
            self.overlay = OverlayWindow()
            self.overlay.show()
            self.toggle_btn.setText("关闭桌面字幕")
            self.toggle_btn.setStyleSheet("padding: 10px; font-weight: bold; background-color: #D13438; color: white;")
        else:
            self.overlay.close()
            self.overlay = None
            self.toggle_btn.setText("开启桌面字幕")
            self.toggle_btn.setStyleSheet("padding: 10px; font-weight: bold; background-color: #0078D4; color: white;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

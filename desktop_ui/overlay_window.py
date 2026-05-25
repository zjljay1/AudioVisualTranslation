import sys
import json
import asyncio
import websockets
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

class WebSocketThread(QThread):
    subtitle_signal = pyqtSignal(str, str)

    def __init__(self, uri="ws://localhost:8765"):
        super().__init__()
        self.uri = uri
        self.loop = None

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect_ws())

    async def connect_ws(self):
        while True:
            try:
                async with websockets.connect(self.uri) as ws:
                    print("Desktop UI connected to WebSocket server")
                    async for message in ws:
                        if isinstance(message, str):
                            data = json.loads(message)
                            if data.get("type") == "subtitle":
                                self.subtitle_signal.emit(
                                    data.get("original", ""),
                                    data.get("translated", "")
                                )
            except Exception as e:
                print(f"WS Connection error: {e}, retrying in 3 seconds...")
                await asyncio.sleep(3)

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Start WebSocket Client Thread
        self.ws_thread = WebSocketThread()
        self.ws_thread.subtitle_signal.connect(self.update_subtitle)
        self.ws_thread.start()

    def initUI(self):
        # 无边框，置顶，工具窗口(不在任务栏显示)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.Tool)
        
        # 窗口透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 鼠标穿透 (如果需要拖拽，可暂时关闭此属性，或者在边缘响应拖拽)
        # self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.layout = QVBoxLayout()
        
        self.translated_label = QLabel("桌面端字幕就绪", self)
        self.translated_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold; background-color: rgba(0,0,0,150); padding: 10px; border-radius: 8px;")
        self.translated_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.original_label = QLabel("Waiting for subtitles...", self)
        self.original_label.setStyleSheet("color: #DDDDDD; font-size: 20px; background-color: rgba(0,0,0,150); padding: 5px; border-radius: 8px;")
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.translated_label)
        self.layout.addWidget(self.original_label)
        self.setLayout(self.layout)

        # 初始位置：屏幕下方
        screen = QApplication.primaryScreen().geometry()
        width = 800
        height = 150
        self.setGeometry((screen.width() - width) // 2, screen.height() - height - 100, width, height)

    def update_subtitle(self, original, translated):
        self.original_label.setText(original)
        self.translated_label.setText(translated)
        
        if not original:
            self.original_label.hide()
        else:
            self.original_label.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPosition = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.dragPosition)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OverlayWindow()
    window.show()
    sys.exit(app.exec())

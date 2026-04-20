
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame
import subprocess



class GestureApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gesture Reel Simulator")
        self.setGeometry(400, 150, 500, 400)

        self.setStyleSheet("""
    QWidget {
        background-color: #0b0b0b;
        color: #e5e5e5;
        font-family: Segoe UI;
    }

    QLabel#title {
        font-size: 24px;
        font-weight: 600;
        color: #ffffff;
    }

    QLabel#subtitle {
        font-size: 13px;
        color: #9ca3af;
    }

    QPushButton {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 10px;
        font-size: 13px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    QPushButton:hover {
        background-color: rgba(255, 255, 255, 0.15);
    }

    QPushButton:pressed {
        background-color: rgba(255, 255, 255, 0.25);
    }
""")

        layout = QVBoxLayout()

        
        self.title = QLabel("Gesture Reel Simulator")
        self.title.setObjectName("Title")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        layout.addWidget(self.title)

        
        self.welcome = QLabel("Control your reels with natural gestures")
        self.welcome.setObjectName("subtitle")
        self.welcome.setAlignment(Qt.AlignCenter)
        self.welcome.setAlignment(Qt.AlignCenter)
        self.welcome.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.welcome)

        
        self.start_btn = QPushButton("Start Gesture Control")
        self.start_btn.setFont(QFont("Segoe UI", 11))
        self.start_btn.setStyleSheet(self.button_style())
        self.start_btn.clicked.connect(self.start_gesture)
        layout.addWidget(self.start_btn)

        
        self.exit_btn = QPushButton("Exit")
        self.exit_btn.setFont(QFont("Segoe UI", 11))
        self.exit_btn.setStyleSheet(self.button_style())
        self.exit_btn.clicked.connect(self.close_app)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)
        
        

    
    def button_style(self):
        return """
        QPushButton {
            background-color: rgba(255,255,255,0.15);
            border-radius: 15px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: rgba(255,255,255,0.3);
        }
        """

    
    def start_gesture(self):
        self.welcome.setText("System Running...\nShow your gestures now!")

        
        threading.Thread(target=self.run_gesture_code).start()

    def run_gesture_code(self):
       import sys 
       import subprocess

       subprocess.Popen([sys.executable, "gesture_control.py"])
        
        
    def close_app(self):
        try:
            if hasattr(self, "process"):
                self.process.terminate()   
        except:
            pass
        self.close()




app = QApplication(sys.argv)
window = GestureApp()
window.show()
sys.exit(app.exec_())

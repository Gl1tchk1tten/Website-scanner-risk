from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QFont
from PySide6.QtCore import Qt

class ScoreBadge(QWidget):
    def __init__(self):
        super().__init__()
        self.scoreValue = 0
        self.scoreLabel = "N/A"
        self.setMinimumSize(120, 120)

    def setScore(self, value, label):
        self.scoreValue = value
        self.scoreLabel = label
        self.update()

    def paintEvent(self, event):  
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.scoreValue <= 20:
            color = QColor("#4caf50") 
        elif self.scoreValue <= 40:
            color = QColor("#ffc107") 
        elif self.scoreValue <= 60:
            color = QColor("#ff9800") 
        elif self.scoreValue <= 80:
            color = QColor("#f44336")  
        else:
            color = QColor("#b71c1c")  

        # Cercle de fond
        circleRect = self.rect().adjusted(10, 10, -10, -10)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(circleRect)

        painter.setPen(Qt.white)
        fontScore = QFont("Segoe UI", 16, QFont.Bold)
        painter.setFont(fontScore)
        painter.drawText(circleRect, Qt.AlignCenter, str(self.scoreValue))

        fontLevel = QFont("Segoe UI", 10)
        painter.setFont(fontLevel)
        labelRect = circleRect.adjusted(0, circleRect.height() // 2, 0, 0)
        painter.drawText(labelRect, Qt.AlignCenter, self.scoreLabel)

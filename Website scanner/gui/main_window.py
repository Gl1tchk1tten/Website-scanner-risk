from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from scanner import scan_website
from gui.widgets.score_badge import ScoreBadge


class ScanWorker(QThread):
    finished = Signal(dict)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        report = scan_website(self.url)
        self.finished.emit(report)

class SafeStreamApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GlitchScanner")
        self.setFixedSize(650, 500)
        self.setStyleSheet(open("gui/style.qss").read())

        self.urlField = QLineEdit()
        self.urlField.setPlaceholderText("Entrez l'URL du site à scanner")

        self.scanButton = QPushButton("Scanner")
        self.scanButton.clicked.connect(self.startScan)


        self.exportButton = QPushButton("Exporter le rapport")
        self.exportButton.clicked.connect(self.exportReport)
        self.exportButton.setEnabled(False)

        self.resultArea = QTextEdit()
        self.resultArea.setReadOnly(True)

        self.scoreDisplay = ScoreBadge()  

        top = QHBoxLayout()
        top.addWidget(self.urlField)
        top.addWidget(self.scanButton)

        middle = QHBoxLayout()
        middle.addWidget(self.scoreDisplay, alignment=Qt.AlignTop)
        middle.addWidget(self.resultArea)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>GlitchScanner</h2>"))
        layout.addLayout(top)
        layout.addLayout(middle)
        layout.addWidget(self.exportButton)

        self.setLayout(layout)
        self.reportData = None

    def startScan(self):
        url = self.urlField.text().strip()
        if not url:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une URL.")
            return

        self.resultArea.setText("🔍 Scan en cours...\nPatientez quelques secondes...")
        self.exportButton.setEnabled(False)
        self.scoreDisplay.setScore(0, "En cours")  

        self.thread = ScanWorker(url)
        self.thread.finished.connect(self.displayReport)
        self.thread.start()

    def displayReport(self, report):
        self.reportData = report
        score = report["risk_score"]

        if score <= 20:
            level = "Sûr"
        elif score <= 40:
            level = "Méfiance"
        elif score <= 60:
            level = "Suspect"
        elif score <= 80:
            level = "Dangereux"
        else:
            level = "Toxique"

        self.scoreDisplay.setScore(score, level)  

        text = f"🛡️ Score : {score}/100 — {level}\n\n📌 Raisons :\n"
        for reason in report["reasons"]:
            text += f" • {reason}\n"

        text += "\n📊 Détails techniques :\n"
        text += f" - Liens externes : {len(report['external_links'])}\n"
        text += f" - Scripts JS externes : {len(report['js_scripts'])}\n"
        text += f" - Redirections détectées : {len(report['redirects'])}\n"

        if report["js_scripts"]:
            text += f"\n🔍 Exemple de script : {report['js_scripts'][0]}\n"

        if report.get("popup_detected"):
            text += "\n⚠️ Popup JS détectée.\n"

        self.resultArea.setText(text)
        self.exportButton.setEnabled(True)

    def exportReport(self):
        if not self.reportData:
            return
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Exporter le rapport", "rapport.txt", "Fichiers texte (*.txt)"
        )
        if filePath:
            with open(filePath, "w", encoding="utf-8") as f:
                f.write(self.resultArea.toPlainText())
            QMessageBox.information(self, "Exporté", "Rapport exporté avec succès.")

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog

class App(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        btn = QPushButton("Save File")
        btn.clicked.connect(self.save_file)
        layout.addWidget(btn)
        self.setLayout(layout)

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save",
            "example.txt",
            "Text (*.txt)"
        )

        if path:
            with open(path, "w") as f:
                f.write("Saved!")

app = QApplication(sys.argv)
w = App()
w.show()
sys.exit(app.exec())
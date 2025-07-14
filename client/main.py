import sys
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Caver - Dass Automação")

        container = QWidget()
        layout = QVBoxLayout(container)

        # Titulo
        title = QLabel("Automação Produção Laser")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        desc = QLabel("Configure o intervalo de operação")
        desc.setStyleSheet("font-size: 13px;")
        layout.addWidget(desc)
        
        # Coleta de dados do User
        input = QLineEdit()
        input.setPlaceholderText("Intervalo (segundos)")
        layout.addWidget(input)

        # Iniciar
        start_button = QPushButton("Iniciar")
        layout.addWidget(start_button)
        start_button.clicked.connect(lambda: print(f"Intervalo: {input.text()}"))

        # Cancelar
        cancel_button = QPushButton("Cancelar")
        layout.addWidget(cancel_button)
        cancel_button.clicked.connect(self.close)

        container.setLayout(layout)
        self.setCentralWidget(container)
        self.resize(400, 200)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

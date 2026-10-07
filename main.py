import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class OrganizerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.folder = None

        self.setWindowTitle("Type File Organizer")
        self.resize(900, 550)

        self.folder_label = QLabel("Selecciona una carpeta para comenzar.")
        self.folder_label.setWordWrap(True)

        select_button = QPushButton("Seleccionar carpeta")
        select_button.clicked.connect(self.select_folder)

        self.analyze_button = QPushButton("Analizar carpeta")
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self.analyze_folder)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Archivo", "Extensión"])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.status_label = QLabel("Sin análisis.")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Organizador de archivos por categorías"))
        layout.addWidget(self.folder_label)
        layout.addWidget(select_button)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.table)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Seleccionar carpeta"
        )

        if folder:
            self.folder = Path(folder)
            self.folder_label.setText(str(self.folder))
            self.analyze_button.setEnabled(True)
            self.table.setRowCount(0)
            self.status_label.setText("Carpeta lista para analizar.")

    def analyze_folder(self):
        if self.folder is None:
            return

        self.table.setRowCount(0)

        try:
            files = sorted(
                (item for item in self.folder.iterdir() if item.is_file()),
                key=lambda item: item.name.casefold(),
            )
        except OSError as error:
            QMessageBox.warning(
                self, "No se pudo leer la carpeta", str(error)
            )
            self.status_label.setText("El análisis no pudo completarse.")
            return

        self.table.setRowCount(len(files))

        for row, file in enumerate(files):
            self.table.setItem(row, 0, QTableWidgetItem(file.name))
            self.table.setItem(
                row,
                1,
                QTableWidgetItem(file.suffix.lower() or "Sin extensión"),
            )

        self.status_label.setText(
            f"Archivos encontrados: {len(files)}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrganizerWindow()
    window.show()
    sys.exit(app.exec())
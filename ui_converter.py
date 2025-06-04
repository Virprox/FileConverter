import sys
import json
import yaml
import xmltodict
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, 
                             QMessageBox, QVBoxLayout, QPushButton, 
                             QLabel, QWidget, QComboBox)
from PyQt5.QtCore import QThread, pyqtSignal

class FileWorker(QThread):
    """Klasa wątku do obsługi operacji na plikach."""
    finished = pyqtSignal(bool, str)  # (sukces, komunikat)

    def __init__(self, operation, *args):
        super().__init__()
        self.operation = operation  # 'load' lub 'convert'
        self.args = args  # Argumenty operacji

    def run(self):
        try:
            if self.operation == 'load':
                data = self._read_file(*self.args)
                self.finished.emit(bool(data), "Plik wczytany pomyślnie")
            elif self.operation == 'convert':
                success = self._save_file(*self.args)
                msg = "Konwersja zakończona" if success else "Błąd konwersji"
                self.finished.emit(success, msg)
        except Exception as e:
            error_msg = "Wystąpił błąd: {str(e)}"
            self.finished.emit(False, error_msg)

    def _read_file(self, file_path):
        """Wczytuje dane z pliku (JSON/YAML/XML)."""
        try:
            extension = Path(file_path).suffix.lower()
            with open(file_path, 'r', encoding='utf-8') as file:
                if extension == '.json':
                    return json.load(file)
                elif extension in ('.yml', '.yaml'):
                    return yaml.safe_load(file)
                elif extension == '.xml':
                    return xmltodict.parse(file.read())
                else:
                    raise ValueError("Nieobsługiwany format pliku")
        except Exception as e:
            raise Exception("Błąd wczytywania: {str(e)}")

    def _save_file(self, data, file_path, target_format):
        """Zapisuje dane w wybranym formacie."""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                if target_format == 'json':
                    json.dump(data, file, indent=4)
                elif target_format == 'yaml':
                    yaml.dump(data, file, default_flow_style=False)
                elif target_format == 'xml':
                    file.write(xmltodict.unparse(data, pretty=True))
            return True
        except Exception as e:
            raise Exception("Błąd zapisu: {str(e)}")

class FileConverterUI(QMainWindow):
    """Główne okno aplikacji."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter plików v1.4")
        self.setGeometry(100, 100, 600, 300)
        self.input_file = None
        self.file_data = None
        self.worker = None

        # Widgety
        self.label = QLabel("Wybierz plik źródłowy i format docelowy", self)
        self.btn_load = QPushButton("Wybierz plik", self)
        self.combo_format = QComboBox(self)
        self.combo_format.addItems(["JSON", "YAML", "XML"])
        self.btn_convert = QPushButton("Konwertuj", self)
        self.status_label = QLabel("Status: Gotowy", self)

        # Układ
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_load)
        layout.addWidget(self.combo_format)
        layout.addWidget(self.btn_convert)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Połączenia sygnałów
        self.btn_load.clicked.connect(self.load_file)
        self.btn_convert.clicked.connect(self.convert_file)

    def load_file(self):
        """Obsługa wyboru pliku."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz plik", "",
            "Wszystkie pliki (*.*);;JSON (*.json);;YAML (*.yml *.yaml);;XML (*.xml)"
        )
        if file_path:
            self._set_ui_enabled(False)
            self.status_label.setText("Wczytywanie...")
            self.worker = FileWorker('load', file_path)
            self.worker.finished.connect(self._on_load_finished)
            self.worker.start()

    def convert_file(self):
        """Obsługa konwersji pliku z pełną kontrolą nazwy."""
        if not self.input_file or not self.file_data:
            QMessageBox.warning(self, "Błąd", "Najpierw wybierz plik!")
            return

        target_format = self.combo_format.currentText().lower()
        default_name = "{Path(self.input_file).stem}_converted.{target_format}"
        
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz jako",
            str(Path(self.input_file).parent / default_name),
            "{target_format.upper()} (*.{target_format})",
            options=QFileDialog.Options()
        )
        
        if output_path:
            # Normalizacja ścieżki i wymuszenie rozszerzenia
            output_path = str(Path(output_path).with_suffix(f'.{target_format}'))
            
            # Potwierdzenie nadpisania
            if Path(output_path).exists():
                reply = QMessageBox.question(
                    self,
                    "Potwierdzenie",
                    "Plik '{Path(output_path).name}' już istnieje. Nadpisać?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return

            self._set_ui_enabled(False)
            self.status_label.setText("Konwersja...")
            self.worker = FileWorker('convert', self.file_data, output_path, target_format)
            self.worker.finished.connect(self._on_convert_finished)
            self.worker.start()

    def _on_load_finished(self, success, message):
        """Obsługa zakończenia wczytywania."""
        if success:
            self.file_data = self.worker._read_file(self.worker.args[0])
            self.input_file = self.worker.args[0]
        self._handle_operation_result(success, message)

    def _on_convert_finished(self, success, message):
        """Obsługa zakończenia konwersji."""
        self._handle_operation_result(success, message)

    def _handle_operation_result(self, success, message):
        """Wspólna obsługa wyników operacji."""
        self._set_ui_enabled(True)
        safe_message = message.replace("{", "{{").replace("}", "}}")
        self.status_label.setText(safe_message)
        if not success:
            QMessageBox.warning(self, "Błąd", safe_message)
        self.worker = None

    def _set_ui_enabled(self, enabled):
        """Włącza/wyłącza elementy UI."""
        self.btn_load.setEnabled(enabled)
        self.btn_convert.setEnabled(enabled)
        self.combo_format.setEnabled(enabled)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileConverterUI()
    window.show()
    sys.exit(app.exec_())
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class CustomInputDialog(QDialog):
    """Власне модальне діалогове вікно з кількома полями введення (QDialog)."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Власний діалог налаштувань")
        self.setMinimumSize(320, 200)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Поля введення
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Введіть ім'я...")
        form_layout.addRow("Ім'я:", self.name_field)

        self.city_field = QLineEdit()
        self.city_field.setPlaceholderText("Введіть місто...")
        form_layout.addRow("Місто:", self.city_field)

        layout.addLayout(form_layout)

        # Кнопки підтвердження / скасування
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Скасувати")

        # Присвоюємо objectName для стилізації через QSS окремого віджета
        self.ok_btn.setObjectName("accentButton")

        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        # З'єднання
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def get_data(self) -> tuple[str, str]:
        """Повертає введені користувачем дані до основного вікна."""
        return self.name_field.text().strip(), self.city_field.text().strip()


class MainWindowTask5(QMainWindow):
    """Головне вікно додатка."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Вікно додатка")
        self.setMinimumSize(550, 400)

        # Центральний віджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Заголовок
        self.title_label = QLabel("Панель роботи з діалогами та стилями")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)

        # Інформаційне поле (демонстрація отриманих даних від діалогів)
        self.info_label = QLabel("Тут з'являтимуться результати виконання діалогів...")
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName("infoLabel")  # Для окремої QSS-стилізації
        main_layout.addWidget(self.info_label)

        # Кнопки для виклику трьох різних діалогів
        btn_layout = QVBoxLayout()

        self.std_dialog_btn = QPushButton("1. Стандартний діалог (QMessageBox)")
        self.std_dialog_btn.clicked.connect(self.open_standard_dialog)
        btn_layout.addWidget(self.std_dialog_btn)

        self.input_dialog_btn = QPushButton("2. Діалог введення значення (QInputDialog)")
        self.input_dialog_btn.clicked.connect(self.open_input_dialog)
        btn_layout.addWidget(self.input_dialog_btn)

        self.custom_dialog_btn = QPushButton("3. Власний модальний діалог (QDialog)")
        self.custom_dialog_btn.clicked.connect(self.open_custom_dialog)
        btn_layout.addWidget(self.custom_dialog_btn)

        main_layout.addLayout(btn_layout)

        # Застосування глобальної та локальної QSS-стилізації
        self.apply_qss_styles()

    def apply_qss_styles(self) -> None:
        """Застосування глобального stylesheet з псевдостанами та селекторами."""
        qss_stylesheet = """
            /* Глобальні стилі для головного вікна */
            QMainWindow {
                background-color: #f4f6f9;
            }

            /* Шрифт і відступи для міток (QLabel) */
            QLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #2c3e50;
            }

            /* Стилізація кнопок (QPushButton) з псевдостанами */
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }

            /* Псевдостан :hover (при наведенні миші) */
            QPushButton:hover {
                background-color: #2980b9;
            }

            /* Псевдостан :pressed (при натисканні) */
            QPushButton:pressed {
                background-color: #1abc9c;
            }

            /* Псевдостан :disabled (неактивна кнопка) */
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }

            /* Стилізація полів введення (QLineEdit) з псевдостаном фокусу */
            QLineEdit {
                background-color: #ffffff;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
                font-size: 13px;
            }

            /* Псевдостан :focus (коли поле в фокусі введення) */
            QLineEdit:focus {
                border: 2px solid #3498db;
            }

            /* Стилізація окремого віджета за його objectName (InfoLabel) */
            QLabel#infoLabel {
                background-color: #ffffff;
                border: 1px solid #dcdde1;
                border-radius: 6px;
                padding: 12px;
                color: #e67e22;
                font-weight: bold;
            }

            /* Стилізація спеціальної кнопки за objectName (accentButton) */
            QPushButton#accentButton {
                background-color: #2ecc71;
            }
            QPushButton#accentButton:hover {
                background-color: #27ae60;
            }
        """
        self.setStyleSheet(qss_stylesheet)

    def open_standard_dialog(self) -> None:
        """1. Виклик стандартного діалогу QMessageBox."""
        reply = QMessageBox.question(
            self,
            "Підтвердження дії",
            "Бажаєте продовжити виконання операції?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.info_label.setText("Результат: Користувач натиснув 'Yes' у стандартному QMessageBox.")
        else:
            self.info_label.setText("Результат: Користувач скасував дію в QMessageBox.")

    def open_input_dialog(self) -> None:
        """2. Виклик стандартного діалогу введення даних QInputDialog."""
        text, ok = QInputDialog.getText(
            self, "Введення даних", "Введіть нове значення назви проєкта:"
        )
        if ok and text:
            self.info_label.setText(f"Результат QInputDialog: Отримано текст -> '{text}'")

    def open_custom_dialog(self) -> None:
        """3. Виклик власного модального діалогу (QDialog) та отримання даних."""
        dialog = CustomInputDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, city = dialog.get_data()
            if name or city:
                self.info_label.setText(
                    f"Результат власного діалогу:\nКористувач: {name or 'Не вказано'}\nМісто: {city or 'Не вказано'}"
                )
            else:
                self.info_label.setText("Власний діалог закрито порожнім.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowTask5()
    window.show()
    sys.exit(app.exec())

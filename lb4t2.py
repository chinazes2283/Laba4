import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class InteractiveFormWindow(QMainWindow):
    """Головне вікно для Завдання 2: Сигнали, слоти, валідація та скидання."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Вікно додатка")
        self.setMinimumSize(480, 400)

        # Центральний віджет та головний layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Заголовок
        title_label = QLabel("Реєстрація та налаштування параметрів")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-bottom: 5px;")
        main_layout.addWidget(title_label)

        # Форма введення даних (3 різних типи введення: QLineEdit, QSpinBox, QComboBox)
        form_layout = QFormLayout()

        # 1. Текстове введення (QLineEdit)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введіть ім'я (мін. 3 символи)")
        form_layout.addRow("Ім'я користувача:", self.name_input)

        # 2. Числове введення (QSpinBox)
        self.age_spinbox = QSpinBox()
        self.age_spinbox.setRange(0, 120)
        self.age_spinbox.setValue(18)
        form_layout.addRow("Вік:", self.age_spinbox)

        # 3. Вибір зі списку (QComboBox)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Студент", "Викладач", "Гість"])
        form_layout.addRow("Категорія:", self.category_combo)

        main_layout.addLayout(form_layout)

        # Прапорець для керування станом кнопки підтвердження
        self.terms_checkbox = QCheckBox("Погоджуюсь з умовами обробки даних")
        main_layout.addWidget(self.terms_checkbox)

        # Рядок із кнопками керування (Підтвердити та Скинути)
        buttons_layout = QHBoxLayout()

        self.submit_button = QPushButton("Підтвердити")
        self.submit_button.setEnabled(False)  # Спочатку вимкнена, поки не увімкнено прапорець
        buttons_layout.addWidget(self.submit_button)

        self.reset_button = QPushButton("Скинути")
        buttons_layout.addWidget(self.reset_button)

        main_layout.addLayout(buttons_layout)

        # Мітка для виведення результатів валідації
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-weight: bold; color: #333;")
        main_layout.addWidget(self.result_label)

        # ==================== СТВОРЕННЯ СИГНАЛІВ ТА СЛОТІВ ====================

        # 1. З'єднання з вбудованим сигналом (valueChanges) для динамічного виведення віку через лямбду
        self.age_spinbox.valueChanged.connect(
            lambda val: self.result_label.setText( поточний_вік_текст(val) )
        )

        # 2. З'єднання, що змінює властивість іншого віджета (активація кнопки підтвердження від стану прапорця)
        self.terms_checkbox.toggled.connect(self.submit_button.setEnabled)

        # 3. З'єднання вбудованого сигналу clicked кнопки підтвердження з методом валідації
        self.submit_button.clicked.connect(self.validate_and_submit_form)

        # 4. З'єднання кнопки скидання з функцією/методом повернення форми до початкового стану
        self.reset_button.clicked.connect(self.reset_form)

        # Додатковий вбудований сигнал textChanged для перевірки введення тексту
        self.name_input.textChanged.connect(self.on_text_changed)

    def on_text_changed(self, text: str) -> None:
        """Слот для реагування на зміну тексту в реальному часі."""
        if len(text.strip()) < 3:
            self.name_input.setStyleSheet("border: 1px solid red;")
        else:
            self.name_input.setStyleSheet("border: 1px solid green;")

    def validate_input_data(self) -> tuple[bool, str]:
        """Окрема функція валідації даних (логіка винесена без дублювання)."""
        name = self.name_input.text().strip()
        age = self.age_spinbox.value()

        if not name:
            return False, "Помилка: Поле імені не може бути порожнім!"
        if len(name) < 3:
            return False, "Помилка: Ім'я має містити щонайменше 3 символи!"
        if age < 16 or age > 95:
            return False, "Помилка: Вік має бути у допустимому діапазоні від 16 до 95 років!"

        return True, f"Успіх! Вітаю, {name} ({age} років, категорія: {self.category_combo.currentText()})."

    def validate_and_submit_form(self) -> None:
        """Обробник натискання кнопки підтвердження."""
        is_valid, message = self.validate_input_data()
        self.result_label.setText(message)
        if is_valid:
            self.result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.result_label.setStyleSheet("color: red; font-weight: bold;")

    def reset_form(self) -> None:
        """Повертає всі поля форми до початкового стану."""
        self.name_input.clear()
        self.name_input.setStyleSheet("")
        self.age_spinbox.setValue(18)
        self.category_combo.setCurrentIndex(0)
        self.terms_checkbox.setChecked(False)
        self.result_label.clear()


def поточний_вік_текст(age: int) -> str:
    """Звичайна функція (не метод класу), яка використовується як слот через лямбду."""
    return f"Вибрано вік: {age} років"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InteractiveFormWindow()
    window.show()
    sys.exit(app.exec())

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
    QProgressBar,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """Головне вікно додатка для демонстрації віджетів та менеджерів компонування."""

    def __init__(self) -> None:
        super().__init__()

        # Встановлюємо заголовок та мінімальний розмір вікна
        self.setWindowTitle("Вікно програмиі")
        self.setMinimumSize(450, 350)

        # Центральний віджет та головний вертикальний layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 1. Заголовок (QLabel)
        title_label = QLabel("Панель управління та налаштувань")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # 2. Використання QFormLayout для полів введення (форма налаштувань)
        form_layout = QFormLayout()

        # Поле введення тексту (QLineEdit) із placeholder-текстом та tooltip
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введіть ваше ім'я...")
        self.username_input.setToolTip("Поле для введення унікального ідентифікатора користувача")
        form_layout.addRow("Користувач:", self.username_input)

        # Випадаючий список (QComboBox) з початковим вибором та tooltip
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Адміністратор", "Оператор", "Гість"])
        self.role_combo.setCurrentIndex(1)  # Початкове значення (Оператор)
        self.role_combo.setToolTip("Оберіть рівень доступу в системі")
        form_layout.addRow("Роль:", self.role_combo)

        # Додаємо форматоване компонування у головний layout
        main_layout.addLayout(form_layout)

        # 3. Прапорець (QCheckBox) та Кнопка (QPushButton) у горизонтальному рядку (QHBoxLayout)
        h_layout = QHBoxLayout()

        self.active_checkbox = QCheckBox("Активний режим")
        self.active_checkbox.setChecked(True)  # Початковий стан — увімкнено
        self.active_checkbox.setToolTip("Увімкнути або вимкнути фонові процеси")
        h_layout.addWidget(self.active_checkbox)

        self.action_button = QPushButton("Виконати")
        self.action_button.setToolTip("Натисніть для запуску операції")
        h_layout.addWidget(self.action_button)

        main_layout.addLayout(h_layout)

        # 4. Повзунок (QSlider) із заданим діапазоном та прогрес-бар (QProgressBar)
        # Використовуємо сітку або вертикальне розташування для повзунка та шкали
        slider_layout = QVBoxLayout()
        
        slider_label = QLabel("Рівень навантаження:")
        slider_layout.addWidget(slider_label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)  # Діапазон значень від 0 до 100
        self.slider.setValue(45)     # Початкове значення
        self.slider.setToolTip("Перетягніть для зміни інтенсивності")
        slider_layout.addWidget(self.slider)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(45)   # Синхронізовано з повзунком для наочності
        slider_layout.addWidget(self.progress_bar)

        main_layout.addLayout(slider_layout)

        # Зв'язуємо повзунок із прогрес-баром для демонстрації інтерактивності
        self.slider.valueChanged.connect(self.progress_bar.setValue)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

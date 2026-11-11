import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

class InputPanel(QWidget):
    """Кастомний компонент для введення даних користувача."""
    
    # Визначення не менше двох кастомних сигналів з різними типами параметрів
    data_submitted = pyqtSignal(str, int)  # pyqtSignal(str, int)
    status_changed = pyqtSignal(list)       # pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Панель введення даних</b>"))

        # Поле для введення імені
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введіть ім'я...")
        self.name_input.textChanged.connect(self.emit_status)
        layout.addWidget(self.name_input)

        # Поле для введення рівня (число)
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 100)
        self.level_spin.setValue(10)
        self.level_spin.valueChanged.connect(self.emit_status)
        layout.addWidget(self.level_spin)

        # Кнопка відправки
        self.send_btn = QPushButton("Надіслати дані")
        self.send_btn.clicked.connect(self.trigger_submit)
        layout.addWidget(self.send_btn)

    def trigger_submit(self) -> None:
        """Випромінювання сигналу з даними імені та рівня."""
        name = self.name_input.text().strip() or "Анонім"
        level = self.level_spin.value()
        # Випромінюємо сигнал pyqtSignal(str, int)
        self.data_submitted.emit(name, level)

    def emit_status(self) -> None:
        """Випромінювання сигналу pyqtSignal(list) зі статусом форми."""
        name_len = len(self.name_input.text())
        level = self.level_spin.value()
        # Випромінюємо сигнал pyqtSignal(list)
        self.status_changed.emit([name_len, level])

class DisplayPanel(QWidget):
    """Кастомний компонент для виведення та візуалізації результатів."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<b>Панель відображення</b>"))

        self.info_label = QLabel("Очікування даних...")
        layout.addWidget(self.info_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(1, 100)
        self.progress_bar.setValue(10)
        layout.addWidget(self.progress_bar)

    def display_submitted_data(self, name: str, level: int) -> None:
        """Слот для прийому сигналу data_submitted (str, int)."""
        self.info_label.setText(f"Отримано: Користувач <b>{name}</b>, Рівень: <b>{level}</b>")
        self.progress_bar.setValue(level)

    def update_metrics(self, data_list: list) -> None:
        """Слот для прийому сигналу status_changed (list)."""
        chars_len, level = data_list
        pass


# ==================== ГОЛОВНЕ ВІКНО (Зовнішнє зв'язування) ====================
class MainWindowTask4(QMainWindow):
    """Головне вікно, що координує компоненти через зовнішні з'єднання."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Вікно додатка")
        self.setMinimumSize(550, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Створення незалежних компонентів
        self.input_panel = InputPanel()
        self.display_panel = DisplayPanel()

        main_layout.addWidget(self.input_panel)
        main_layout.addWidget(self.display_panel)

        # Додаємо кнопку для демонстрації блокування сигналів (blockSignals)
        control_layout = QVBoxLayout()
        self.block_btn = QPushButton("Блокувати сигнали введення")
        self.block_btn.setCheckable(True)
        self.block_btn.toggled.connect(self.toggle_signal_blocking)
        control_layout.addStretch()
        control_layout.addWidget(self.block_btn)
        main_layout.addLayout(control_layout)

        self.input_panel.data_submitted.connect(self.display_panel.display_submitted_data)
        self.input_panel.status_changed.connect(self.display_panel.update_metrics)

    def toggle_signal_blocking(self, checked: bool) -> None:
        """Демонстрація blockSignals у змістовному сценарії."""
        self.input_panel.blockSignals(checked)
        if checked:
            self.block_btn.setText("Розблокувати сигнали")
            self.statusBar().showMessage("Сигнали від InputPanel заблоковані. Оновлення заморожено.", 3000)
        else:
            self.block_btn.setText("Блокувати сигнали введення")
            self.statusBar().showMessage("Сигнали розблоковані.", 3000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowTask4()
    window.show()
    sys.exit(app.exec())

import sys
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class MainWindowApp(QMainWindow):
    """Головне вікно додатка для Завдання 3: QMainWindow, меню, toolbar, statusBar."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Вікно додатка")
        self.setMinimumSize(600, 450)

        # 1. Центральний віджет (текстова область як функціональний віджет)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Введіть текст або відкрийте файл через меню...")
        self.setCentralWidget(self.text_edit)

        # 2. Рядок стану (statusBar)
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Готово до роботи")

        # 3. Створення меню та панелі інструментів
        self.create_actions()
        self.create_menus()
        self.create_toolbar()

        # Підключення сигналу зміни тексту для оновлення рядка стану
        self.text_edit.textChanged.connect(self.update_char_count)

    def create_actions(self) -> None:
        """Створення об'єктів QAction із гарячими клавішами та іконками/описом."""
        
        # Дія: Відкрити файл
        self.open_action = QAction("&Відкрити...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)  # Ctrl+O
        self.open_action.setStatusTip("Відкрити існуючий текстовий файл")
        self.open_action.triggered.connect(self.open_file_dialog)

        # Дія: Зберегти файл
        self.save_action = QAction("&Зберегти", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)  # Ctrl+S
        self.save_action.setStatusTip("Зберегти поточний текст у файл")
        self.save_action.triggered.connect(self.save_file_dialog)

        # Дія: Вихід
        self.exit_action = QAction("&Вихід", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)  # Ctrl+Q
        self.exit_action.setStatusTip("Вийти з додатка")
        self.exit_action.triggered.connect(self.close)

        # Дія: Про програму (стандартний діалог QMessageBox.about)
        self.about_action = QAction("Про &програму", self)
        self.about_action.setStatusTip("Відомості про розробника та версію")
        self.about_action.triggered.connect(self.show_about_dialog)

    def create_menus(self) -> None:
        """Створення головного меню (≥2 розділи, кожен з ≥2 пунктами)."""
        menu_bar = self.menuBar()

        # Розділ 1: «Файл»
        file_menu = menu_bar.addMenu("&Файл")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Розділ 2: «Довідка»
        help_menu = menu_bar.addMenu("&Довідка")
        help_menu.addAction(self.about_action)

    def create_toolbar(self) -> None:
        """Створення панелі інструментів (QToolBar) з кнопками швидкого доступу."""
        self.toolbar = self.createPopupMenu() # Реєстрація тулбара
        toolbar = self.addToolBar("Головна панель")
        toolbar.setMovable(False)

        # Додаємо дії до панелі інструментів (дублюють пункти меню)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.about_action)

    def update_char_count(self) -> None:
        """Динамічне оновлення інформації в рядочку стану про кількість символів."""
        text = self.text_edit.toPlainText()
        char_count = len(text)
        word_count = len(text.split()) if text.strip() else 0
        self.status_bar.showMessage(f"Символів: {char_count} | Слів: {word_count}")

    def open_file_dialog(self) -> None:
        """Відкриття стандартного діалогу вибору файлу (QFileDialog)."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Відкрити текстовий файл", "", "Текстові файли (*.txt);;Усі файли (*.*)"
        )
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_edit.setPlainText(content)
                self.status_bar.showMessage(f"Файл успішно відкрито: {file_name}", 4000)
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Не вдалося відкрити файл:\n{e}")

    def save_file_dialog(self) -> None:
        """Збереження файлу через стандартний діалог."""
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Зберегти файл", "", "Текстові файли (*.txt);;Усі файли (*.*)"
        )
        if file_name:
            try:
                with open(file_name, "w", encoding="utf-8") as file:
                    content = self.text_edit.toPlainText()
                    file.write(content)
                self.status_bar.showMessage(f"Файл успішно збережено: {file_name}", 4000)
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти файл:\n{e}")

    def show_about_dialog(self) -> None:
        """Виклик стандартного інформаційного діалогу QMessageBox.about."""
        QMessageBox.about(
            self,
            "Про програму",
            "Лабораторна робота №4\nЗавдання 3: QMainWindow додаток\n\nРозроблено на базі PyQt6.",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowApp()
    window.show()
    sys.exit(app.exec())

"""
Графический интерфейс пользователя для алгоритма шифрования Эль-Гамаля.
Реализация на PyQt6 с темной темой.
"""
import json
import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QTabWidget, QTextEdit, QPushButton, QFileDialog, 
    QMessageBox, QFrame, QSplitter, QGroupBox, QMenuBar, QMenu
)
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QAction
from PyQt6.QtCore import Qt, QSize
from elgamal import ElGamal

class ElGamalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Инициализация алгоритма Эль-Гамаля
        # Используем небольшой размер ключа для демонстрации (для продакшена нужно больше)
        self.cipher = ElGamal(key_size=512)
        
        self.setWindowTitle("Шифрование Эль-Гамаля")
        self.setGeometry(100, 100, 900, 700)
        
        # Применяем темную тему
        self.apply_dark_theme()
        
        # Создание интерфейса
        self.create_menu()
        self.create_widgets()
        
        # Отображение информации о ключах
        self.update_key_info()
    
    def apply_dark_theme(self):
        """Применение темной темы оформления"""
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2D2D30;
                color: #E0E0E0;
            }
            QTabWidget::pane {
                border: 1px solid #3F3F46;
                background-color: #252526;
            }
            QTabBar::tab {
                background-color: #2D2D30;
                color: #E0E0E0;
                border: 1px solid #3F3F46;
                padding: 8px 15px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #252526;
                border-bottom-color: #252526;
            }
            QTextEdit {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #3F3F46;
                border-radius: 4px;
                font-family: Consolas, monospace;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #0E639C;
                color: white;
                border-radius: 4px;
                padding: 6px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177BB;
            }
            QPushButton:pressed {
                background-color: #0D5989;
            }
            QGroupBox {
                border: 1px solid #3F3F46;
                border-radius: 4px;
                margin-top: 0.5em;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
            QMenu {
                background-color: #2D2D30;
                color: #E0E0E0;
                border: 1px solid #3F3F46;
            }
            QMenu::item:selected {
                background-color: #3E3E42;
            }
            QMenuBar {
                background-color: #2D2D30;
                color: #E0E0E0;
            }
            QMenuBar::item:selected {
                background-color: #3E3E42;
            }
        """)
    
    def create_menu(self):
        """Создание верхнего меню приложения"""
        menubar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menubar.addMenu("Файл")
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню "Ключи"
        keys_menu = menubar.addMenu("Ключи")
        
        gen_keys_action = QAction("Сгенерировать новые ключи", self)
        gen_keys_action.triggered.connect(self.generate_new_keys)
        keys_menu.addAction(gen_keys_action)
    
    def create_widgets(self):
        """Создание основных элементов интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Фрейм для информации о ключах
        key_frame = QGroupBox("Информация о ключах")
        key_layout = QVBoxLayout(key_frame)
        
        self.key_info = QTextEdit()
        self.key_info.setReadOnly(True)
        self.key_info.setMaximumHeight(100)
        key_layout.addWidget(self.key_info)
        
        main_layout.addWidget(key_frame)
        
        # Создание вкладок
        tab_widget = QTabWidget()
        
        # Вкладка шифрования
        encrypt_tab = QWidget()
        self.setup_encrypt_tab(encrypt_tab)
        tab_widget.addTab(encrypt_tab, "Шифрование")
        
        # Вкладка расшифрования
        decrypt_tab = QWidget()
        self.setup_decrypt_tab(decrypt_tab)
        tab_widget.addTab(decrypt_tab, "Расшифрование")
        
        main_layout.addWidget(tab_widget)
    
    def setup_encrypt_tab(self, tab):
        """Настройка вкладки шифрования"""
        layout = QVBoxLayout(tab)
        
        # Разделитель, который позволяет регулировать размер панелей
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Верхняя панель - исходный текст
        input_group = QGroupBox("Исходный текст")
        input_layout = QVBoxLayout(input_group)
        
        self.encrypt_input = QTextEdit()
        input_layout.addWidget(self.encrypt_input)
        
        # Кнопки для верхней панели
        input_buttons = QHBoxLayout()
        load_btn = QPushButton("Загрузить из файла")
        load_btn.clicked.connect(self.load_text_for_encrypt)
        encrypt_btn = QPushButton("Шифровать")
        encrypt_btn.clicked.connect(self.encrypt_text)
        
        input_buttons.addWidget(load_btn)
        input_buttons.addWidget(encrypt_btn)
        input_buttons.addStretch()
        
        input_layout.addLayout(input_buttons)
        
        # Нижняя панель - зашифрованный текст
        output_group = QGroupBox("Зашифрованный текст")
        output_layout = QVBoxLayout(output_group)
        
        self.encrypt_output = QTextEdit()
        self.encrypt_output.setReadOnly(True)
        output_layout.addWidget(self.encrypt_output)
        
        # Кнопки для нижней панели
        output_buttons = QHBoxLayout()
        output_buttons.addStretch()
        save_btn = QPushButton("Сохранить в файл")
        save_btn.clicked.connect(self.save_encrypted_text)
        output_buttons.addWidget(save_btn)
        
        output_layout.addLayout(output_buttons)
        
        # Добавляем панели в разделитель
        splitter.addWidget(input_group)
        splitter.addWidget(output_group)
        
        # Добавляем разделитель в основной макет
        layout.addWidget(splitter)
    
    def setup_decrypt_tab(self, tab):
        """Настройка вкладки расшифрования"""
        layout = QVBoxLayout(tab)
        
        # Разделитель, который позволяет регулировать размер панелей
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Верхняя панель - зашифрованный текст
        input_group = QGroupBox("Зашифрованный текст")
        input_layout = QVBoxLayout(input_group)
        
        self.decrypt_input = QTextEdit()
        input_layout.addWidget(self.decrypt_input)
        
        # Кнопки для верхней панели
        input_buttons = QHBoxLayout()
        load_btn = QPushButton("Загрузить из файла")
        load_btn.clicked.connect(self.load_text_for_decrypt)
        decrypt_btn = QPushButton("Расшифровать")
        decrypt_btn.clicked.connect(self.decrypt_text)
        
        input_buttons.addWidget(load_btn)
        input_buttons.addWidget(decrypt_btn)
        input_buttons.addStretch()
        
        input_layout.addLayout(input_buttons)
        
        # Нижняя панель - расшифрованный текст
        output_group = QGroupBox("Расшифрованный текст")
        output_layout = QVBoxLayout(output_group)
        
        self.decrypt_output = QTextEdit()
        self.decrypt_output.setReadOnly(True)
        output_layout.addWidget(self.decrypt_output)
        
        # Кнопки для нижней панели
        output_buttons = QHBoxLayout()
        output_buttons.addStretch()
        save_btn = QPushButton("Сохранить в файл")
        save_btn.clicked.connect(self.save_decrypted_text)
        output_buttons.addWidget(save_btn)
        
        output_layout.addLayout(output_buttons)
        
        # Добавляем панели в разделитель
        splitter.addWidget(input_group)
        splitter.addWidget(output_group)
        
        # Добавляем разделитель в основной макет
        layout.addWidget(splitter)
    
    def update_key_info(self):
        """Обновление информации о ключах в интерфейсе"""
        p, g, y = self.cipher.public_key
        x = self.cipher.private_key
        
        key_text = f"Открытый ключ: (p: {p}, g: {g}, y: {y})\n"
        key_text += f"Закрытый ключ: x: {x}"
        
        self.key_info.setText(key_text)
    
    def generate_new_keys(self):
        """Генерация новой пары ключей"""
        try:
            self.cipher = ElGamal(key_size=512)
            self.update_key_info()
            QMessageBox.information(self, "Успех", "Новые ключи успешно сгенерированы")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сгенерировать ключи: {str(e)}")
    
    def encrypt_text(self):
        """Шифрование текста из текстового поля"""
        try:
            plaintext = self.encrypt_input.toPlainText().strip()
            if not plaintext:
                QMessageBox.warning(self, "Предупреждение", "Введите текст для шифрования")
                return
            
            encrypted = self.cipher.encrypt_string(plaintext)
            
            # Преобразуем в JSON для отображения
            encrypted_json = json.dumps([(int(a), int(b)) for a, b in encrypted], indent=2)
            
            self.encrypt_output.setText(encrypted_json)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при шифровании: {str(e)}")
    
    def decrypt_text(self):
        """Расшифрование текста из текстового поля"""
        try:
            encrypted_json = self.decrypt_input.toPlainText().strip()
            if not encrypted_json:
                QMessageBox.warning(self, "Предупреждение", "Введите зашифрованный текст для расшифрования")
                return
            
            # Парсим JSON
            encrypted_data = json.loads(encrypted_json)
            encrypted_data = [(int(a), int(b)) for a, b in encrypted_data]
            
            decrypted = self.cipher.decrypt_string(encrypted_data)
            
            self.decrypt_output.setText(decrypted)
            
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Ошибка", "Неверный формат зашифрованных данных. Ожидается JSON-массив.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при расшифровании: {str(e)}")
    
    def load_text_for_encrypt(self):
        """Загрузка текста из файла для шифрования"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл для шифрования",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.encrypt_input.setText(content)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")
    
    def load_text_for_decrypt(self):
        """Загрузка зашифрованного текста из файла для расшифрования"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл для расшифрования",
            "",
            "JSON файлы (*.json);;Все файлы (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.decrypt_input.setText(content)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")
    
    def save_encrypted_text(self):
        """Сохранение зашифрованного текста в файл"""
        encrypted_text = self.encrypt_output.toPlainText().strip()
        if not encrypted_text:
            QMessageBox.warning(self, "Предупреждение", "Нет данных для сохранения")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить зашифрованный текст",
            "",
            "JSON файлы (*.json);;Все файлы (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(encrypted_text)
                QMessageBox.information(self, "Успех", f"Файл успешно сохранен: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении файла: {str(e)}")
    
    def save_decrypted_text(self):
        """Сохранение расшифрованного текста в файл"""
        decrypted_text = self.decrypt_output.toPlainText().strip()
        if not decrypted_text:
            QMessageBox.warning(self, "Предупреждение", "Нет данных для сохранения")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить расшифрованный текст",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(decrypted_text)
                QMessageBox.information(self, "Успех", f"Файл успешно сохранен: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении файла: {str(e)}")

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ElGamalApp()
    window.show()
    sys.exit(app.exec())

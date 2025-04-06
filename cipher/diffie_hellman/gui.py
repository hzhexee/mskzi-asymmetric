"""
Графический интерфейс пользователя для алгоритма обмена ключами Диффи-Хеллмана.
Реализация на PyQt6 с темной темой.
"""
import os
import sys
import base64
import hashlib
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QTabWidget, QTextEdit, QPushButton, QFileDialog, 
    QMessageBox, QComboBox, QSplitter, QGroupBox, QMenuBar, QMenu
)
from PyQt6.QtGui import QFont, QPalette, QAction
from PyQt6.QtCore import Qt
from diffie_hellman import DiffieHellman
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class DiffieHellmanApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Инициализация алгоритма Диффи-Хеллмана
        self.alice = None
        self.bob = None
        self.shared_secret = None
        
        self.setWindowTitle("Диффи-Хеллман шифрование")
        self.setGeometry(100, 100, 900, 700)
        
        # Применяем темную тему
        self.apply_dark_theme()
        
        # Создание интерфейса
        self.create_menu()
        self.create_widgets()
    
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
            QComboBox {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #3F3F46;
                border-radius: 4px;
                padding: 4px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #1E1E1E;
                color: #E0E0E0;
                border: 1px solid #3F3F46;
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
        gen_keys_action.triggered.connect(self.generate_keys)
        keys_menu.addAction(gen_keys_action)
    
    def create_widgets(self):
        """Создание основных элементов интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Создание вкладок
        tab_widget = QTabWidget()
        
        # Вкладка генерации ключей
        key_tab = QWidget()
        self.setup_key_tab(key_tab)
        tab_widget.addTab(key_tab, "Генерация ключей")
        
        # Вкладка шифрования
        encrypt_tab = QWidget()
        self.setup_encrypt_tab(encrypt_tab)
        tab_widget.addTab(encrypt_tab, "Шифрование")
        
        # Вкладка расшифрования
        decrypt_tab = QWidget()
        self.setup_decrypt_tab(decrypt_tab)
        tab_widget.addTab(decrypt_tab, "Расшифрование")
        
        main_layout.addWidget(tab_widget)
    
    def setup_key_tab(self, tab):
        """Настройка вкладки генерации ключей"""
        layout = QVBoxLayout(tab)
        
        # Фрейм для параметров ключей
        params_group = QGroupBox("Параметры ключа")
        params_layout = QVBoxLayout(params_group)
        
        key_size_layout = QHBoxLayout()
        key_size_layout.addWidget(QLabel("Размер ключа (в битах):"))
        self.key_size_combo = QComboBox()
        self.key_size_combo.addItems(["512", "1024", "2048", "4096"])
        self.key_size_combo.setCurrentIndex(1)  # По умолчанию 1024 бит
        key_size_layout.addWidget(self.key_size_combo)
        key_size_layout.addStretch()
        
        params_layout.addLayout(key_size_layout)
        
        generate_btn = QPushButton("Сгенерировать ключи")
        generate_btn.clicked.connect(self.generate_keys)
        params_layout.addWidget(generate_btn)
        
        layout.addWidget(params_group)
        
        # Фрейм для информации о ключах
        info_group = QGroupBox("Информация о ключах")
        info_layout = QVBoxLayout(info_group)
        
        self.key_info_text = QTextEdit()
        self.key_info_text.setReadOnly(True)
        info_layout.addWidget(self.key_info_text)
        
        layout.addWidget(info_group)
    
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
        load_btn.clicked.connect(lambda: self.load_file(self.encrypt_input))
        encrypt_btn = QPushButton("Шифровать")
        encrypt_btn.clicked.connect(self.encrypt_data)
        
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
        save_btn.clicked.connect(lambda: self.save_file(self.encrypt_output.toPlainText()))
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
        load_btn.clicked.connect(lambda: self.load_file(self.decrypt_input))
        decrypt_btn = QPushButton("Расшифровать")
        decrypt_btn.clicked.connect(self.decrypt_data)
        
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
        save_btn.clicked.connect(lambda: self.save_file(self.decrypt_output.toPlainText()))
        output_buttons.addWidget(save_btn)
        
        output_layout.addLayout(output_buttons)
        
        # Добавляем панели в разделитель
        splitter.addWidget(input_group)
        splitter.addWidget(output_group)
        
        # Добавляем разделитель в основной макет
        layout.addWidget(splitter)
    
    def generate_keys(self):
        """Генерация ключей Диффи-Хеллмана"""
        try:
            key_size = int(self.key_size_combo.currentText())
            
            # Сначала генерируем параметры для Alice
            self.alice = DiffieHellman(key_size)
            
            # Используем те же параметры p и g для Bob
            self.bob = DiffieHellman(key_size=key_size, p=self.alice.p, g=self.alice.g)
            
            # Вычисляем общие секретные ключи
            alice_shared_secret = self.alice.generate_shared_secret(self.bob.public_key)
            bob_shared_secret = self.bob.generate_shared_secret(self.alice.public_key)
            
            # Для отладки выводим значения
            print(f"Alice's shared secret: {alice_shared_secret}")
            print(f"Bob's shared secret: {bob_shared_secret}")
            
            # Проверяем, что общие ключи совпадают
            if alice_shared_secret == bob_shared_secret:
                self.shared_secret = alice_shared_secret
                
                # Обновляем информацию о ключах
                info = f"Простое число p: {self.alice.p}\n\n"
                info += f"Основание g: {self.alice.g}\n\n"
                info += f"Публичный ключ Alice: {self.alice.public_key}\n\n"
                info += f"Публичный ключ Bob: {self.bob.public_key}\n\n"
                info += f"Общий секретный ключ (первые 50 знаков): {str(self.shared_secret)[:50]}...\n\n"
                info += "Ключи успешно сгенерированы!"
                
                self.key_info_text.clear()
                self.key_info_text.insertPlainText(info)
                
                QMessageBox.information(self, "Успех", "Ключи успешно сгенерированы!")
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка генерации ключей: общие секреты не совпадают!\n"
                                     f"Alice: {alice_shared_secret}\n"
                                     f"Bob: {bob_shared_secret}")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при генерации ключей: {str(e)}")
    
    def load_file(self, text_widget):
        """Загрузка текста из файла"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    text_widget.clear()
                    text_widget.insertPlainText(content)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")
                
    def save_file(self, content):
        """Сохранение текста в файл"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                QMessageBox.information(self, "Успех", "Файл успешно сохранен!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")
    
    def encrypt_data(self):
        """Шифрование данных"""
        if not self.shared_secret:
            QMessageBox.critical(self, "Ошибка", "Сначала сгенерируйте ключи!")
            return
        
        plaintext = self.encrypt_input.toPlainText().strip()
        if not plaintext:
            QMessageBox.warning(self, "Предупреждение", "Введите текст для шифрования!")
            return
        
        try:
            # Подготовка ключа для AES (нужно ровно 32 байта)
            key = hashlib.sha256(str(self.shared_secret).encode()).digest()
            
            # Шифрование с помощью AES
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(plaintext.encode()) + padder.finalize()
            
            # Используем случайный IV (вектор инициализации)
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            
            # Комбинируем IV и шифротекст и кодируем в base64 для удобства отображения
            result = base64.b64encode(iv + ciphertext).decode('utf-8')
            
            self.encrypt_output.clear()
            self.encrypt_output.insertPlainText(result)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка шифрования: {str(e)}")
    
    def decrypt_data(self):
        """Расшифрование данных"""
        if not self.shared_secret:
            QMessageBox.critical(self, "Ошибка", "Сначала сгенерируйте ключи!")
            return
        
        ciphertext_b64 = self.decrypt_input.toPlainText().strip()
        if not ciphertext_b64:
            QMessageBox.warning(self, "Предупреждение", "Введите текст для расшифрования!")
            return
        
        try:
            # Подготовка ключа для AES
            key = hashlib.sha256(str(self.shared_secret).encode()).digest()
            
            # Декодируем из base64
            ciphertext_full = base64.b64decode(ciphertext_b64)
            
            # Разделяем IV и сам шифротекст
            iv = ciphertext_full[:16]
            ciphertext = ciphertext_full[16:]
            
            # Расшифровываем с помощью AES
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Убираем паддинг
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            
            self.decrypt_output.clear()
            self.decrypt_output.insertPlainText(plaintext.decode('utf-8'))
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка расшифрования: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = DiffieHellmanApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

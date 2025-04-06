import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
                           QGroupBox, QFileDialog, QMessageBox, QSplitter, QStyle)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from rsa import RSA  # Импортируем класс RSA из модуля rsa

class RSAApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSA Шифрование/Дешифрование")
        self.setGeometry(100, 100, 600, 600)
        self.rsa = RSA(1024)  # Инициализация RSA с ключом 1024 бит
        
        # Установка темной темы
        self.set_dark_theme()
        
        # Создание центрального виджета
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Основной вертикальный лейаут
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.create_widgets()
        
    def set_dark_theme(self):
        # Создание тёмной темы
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        
        # Применение темы
        self.setPalette(dark_palette)
        
        # Установка стиля Fusion для совместимости
        QApplication.setStyle("Fusion")
        
        # Дополнительные стили CSS для улучшения внешнего вида
        self.setStyleSheet("""
            QPushButton {
                background-color: #1e88e5;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #42a5f5;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QGroupBox {
                border: 1px solid #616161;
                border-radius: 5px;
                margin-top: 1ex;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
            QTextEdit, QLineEdit {
                border: 1px solid #424242;
                border-radius: 3px;
                background-color: #303030;
                color: white;
            }
            QTabWidget::pane { 
                border: 1px solid #616161;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #424242;
                color: #f5f5f5;
                padding: 5px 10px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #1e88e5;
            }
        """)
    
    def create_widgets(self):
        # Создание вкладок
        self.tabs = QTabWidget()
        
        self.text_tab = QWidget()
        self.file_tab = QWidget()
        
        self.tabs.addTab(self.text_tab, "Работа с текстом")
        self.tabs.addTab(self.file_tab, "Работа с файлами")
        
        # Настройка вкладки с текстом
        self.setup_text_tab()
        
        # Настройка вкладки с файлами
        self.setup_file_tab()
        
        # Отображение информации о ключах
        self.show_key_info()
        
        # Добавление вкладок в основной лейаут
        self.main_layout.addWidget(self.tabs)
    
    def setup_text_tab(self):
        # Создаем лейаут для текстовой вкладки
        text_layout = QVBoxLayout(self.text_tab)
        
        # Создаем splitter для возможности изменения размеров полей
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Группа для ввода текста
        input_group = QGroupBox("Исходный текст")
        input_layout = QVBoxLayout(input_group)
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Введите текст для шифрования или зашифрованные блоки для расшифровки...")
        input_layout.addWidget(self.input_text)
        
        # Группа кнопок
        button_layout = QHBoxLayout()
        
        self.encrypt_btn = QPushButton("Зашифровать")
        self.encrypt_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        self.encrypt_btn.clicked.connect(self.encrypt_text)
        
        self.decrypt_btn = QPushButton("Расшифровать")
        self.decrypt_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton))
        self.decrypt_btn.clicked.connect(self.decrypt_text)
        
        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton))
        self.clear_btn.clicked.connect(self.clear_text)
        
        button_layout.addWidget(self.encrypt_btn)
        button_layout.addWidget(self.decrypt_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_btn)
        
        # Группа для вывода результата
        output_group = QGroupBox("Результат")
        output_layout = QVBoxLayout(output_group)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Здесь появится результат операции...")
        output_layout.addWidget(self.output_text)
        
        # Добавляем группы на splitter
        splitter.addWidget(input_group)
        splitter.addWidget(output_group)
        
        # Добавляем все на лейаут вкладки
        text_layout.addWidget(splitter)
        text_layout.addLayout(button_layout)
    
    def setup_file_tab(self):
        # Создаем лейаут для файловой вкладки
        file_layout = QVBoxLayout(self.file_tab)
        
        # Группа для выбора входного файла
        input_file_group = QGroupBox("Исходный файл")
        input_file_layout = QHBoxLayout(input_file_group)
        
        self.input_file_path = QLineEdit()
        self.input_file_path.setPlaceholderText("Путь к исходному файлу...")
        self.browse_input_btn = QPushButton("Обзор...")
        self.browse_input_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        self.browse_input_btn.clicked.connect(self.browse_input_file)
        
        input_file_layout.addWidget(self.input_file_path)
        input_file_layout.addWidget(self.browse_input_btn)
        
        # Группа кнопок
        button_layout = QHBoxLayout()
        
        self.encrypt_file_btn = QPushButton("Зашифровать файл")
        self.encrypt_file_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        self.encrypt_file_btn.clicked.connect(self.encrypt_file)
        
        self.decrypt_file_btn = QPushButton("Расшифровать файл")
        self.decrypt_file_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton))
        self.decrypt_file_btn.clicked.connect(self.decrypt_file)
        
        button_layout.addWidget(self.encrypt_file_btn)
        button_layout.addWidget(self.decrypt_file_btn)
        button_layout.addStretch()
        
        # Группа для выбора выходного файла
        output_file_group = QGroupBox("Сохранить результат")
        output_file_layout = QHBoxLayout(output_file_group)
        
        self.output_file_path = QLineEdit()
        self.output_file_path.setPlaceholderText("Путь для сохранения результата...")
        self.browse_output_btn = QPushButton("Выбрать...")
        self.browse_output_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.browse_output_btn.clicked.connect(self.browse_output_file)
        
        output_file_layout.addWidget(self.output_file_path)
        output_file_layout.addWidget(self.browse_output_btn)
        
        # Группа для отображения статуса
        status_group = QGroupBox("Статус операции")
        status_layout = QVBoxLayout(status_group)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setPlaceholderText("Статус операции будет отображаться здесь...")
        
        status_layout.addWidget(self.status_text)
        
        # Добавляем все на лейаут вкладки
        file_layout.addWidget(input_file_group)
        file_layout.addWidget(output_file_group)
        file_layout.addLayout(button_layout)
        file_layout.addWidget(status_group)
    
    def show_key_info(self):
        # Создаем фрейм для информации о ключах
        key_group = QGroupBox("Информация о ключах")
        key_layout = QVBoxLayout(key_group)
        
        n, e = self.rsa.public_key
        key_info = QLabel(f"Модуль (n): {n}\nОткрытая экспонента (e): {e}\nРазмер ключа: {n.bit_length()} бит")
        key_info.setWordWrap(True)
        
        key_layout.addWidget(key_info)
        
        self.main_layout.addWidget(key_group)
    
    def encrypt_text(self):
        try:
            input_text = self.input_text.toPlainText().strip()
            if not input_text:
                QMessageBox.warning(self, "Предупреждение", "Введите текст для шифрования!")
                return
            
            encrypted_blocks = self.rsa.encrypt_string(input_text)
            result = "\n".join([str(block) for block in encrypted_blocks])
            
            self.output_text.clear()
            self.output_text.setPlainText(result)
            
            QMessageBox.information(self, "Успех", "Текст успешно зашифрован!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось зашифровать текст: {e}")
    
    def decrypt_text(self):
        try:
            input_text = self.input_text.toPlainText().strip()
            if not input_text:
                QMessageBox.warning(self, "Предупреждение", "Введите зашифрованные блоки для расшифровки!")
                return
            
            # Преобразуем строки в числа (блоки)
            encrypted_blocks = []
            for line in input_text.split("\n"):
                if line.strip():
                    encrypted_blocks.append(int(line.strip()))
            
            if not encrypted_blocks:
                QMessageBox.warning(self, "Предупреждение", "Не удалось распознать зашифрованные блоки!")
                return
                
            decrypted_text = self.rsa.decrypt_string(encrypted_blocks)
            
            self.output_text.clear()
            self.output_text.setPlainText(decrypted_text)
            
            QMessageBox.information(self, "Успех", "Текст успешно расшифрован!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось расшифровать текст: {e}")
    
    def clear_text(self):
        self.input_text.clear()
        self.output_text.clear()
    
    def browse_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл")
        if file_path:
            self.input_file_path.setText(file_path)
    
    def browse_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как")
        if file_path:
            self.output_file_path.setText(file_path)
    
    def encrypt_file(self):
        input_file = self.input_file_path.text()
        output_file = self.output_file_path.text()
        
        if not input_file:
            QMessageBox.warning(self, "Предупреждение", "Выберите файл для шифрования!")
            return
        
        if not output_file:
            QMessageBox.warning(self, "Предупреждение", "Выберите файл для сохранения результата!")
            return
        
        try:
            # Чтение файла
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Шифрование содержимого
            encrypted_blocks = self.rsa.encrypt_string(content)
            encrypted_content = "\n".join([str(block) for block in encrypted_blocks])
            
            # Запись зашифрованных данных
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(encrypted_content)
            
            self.status_text.clear()
            self.status_text.setPlainText(f"Файл успешно зашифрован и сохранен в {output_file}")
            
        except Exception as e:
            self.status_text.clear()
            self.status_text.setPlainText(f"Ошибка при шифровании файла: {e}")
    
    def decrypt_file(self):
        input_file = self.input_file_path.text()
        output_file = self.output_file_path.text()
        
        if not input_file:
            QMessageBox.warning(self, "Предупреждение", "Выберите файл для расшифровки!")
            return
        
        if not output_file:
            QMessageBox.warning(self, "Предупреждение", "Выберите файл для сохранения результата!")
            return
        
        try:
            # Чтение зашифрованного файла
            with open(input_file, 'r', encoding='utf-8') as f:
                encrypted_content = f.read()
            
            # Преобразование строк в числа (блоки)
            encrypted_blocks = []
            for line in encrypted_content.split("\n"):
                if line.strip():
                    encrypted_blocks.append(int(line.strip()))
            
            # Расшифровка
            decrypted_content = self.rsa.decrypt_string(encrypted_blocks)
            
            # Запись расшифрованных данных
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(decrypted_content)
            
            self.status_text.clear()
            self.status_text.setPlainText(f"Файл успешно расшифрован и сохранен в {output_file}")
            
        except Exception as e:
            self.status_text.clear()
            self.status_text.setPlainText(f"Ошибка при расшифровке файла: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAApplication()
    window.show()
    sys.exit(app.exec())

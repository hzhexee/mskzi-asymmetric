import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import sys
from pathlib import Path
from rsa import RSA  # Импортируем класс RSA из модуля rsa

# # Добавляем путь к модулю RSA
# sys.path.append(str(Path(__file__).parent))
# from cipher.rsa.rsa import RSA

class RSAApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RSA Шифрование/Дешифрование")
        self.geometry("800x600")
        self.rsa = RSA(1024)  # Инициализация RSA с ключом 1024 бит
        
        self.create_widgets()
        
    def create_widgets(self):
        # Создание вкладок
        tab_control = ttk.Notebook(self)
        
        text_tab = ttk.Frame(tab_control)
        file_tab = ttk.Frame(tab_control)
        
        tab_control.add(text_tab, text="Работа с текстом")
        tab_control.add(file_tab, text="Работа с файлами")
        tab_control.pack(expand=1, fill="both")
        
        # Настройка вкладки с текстом
        self.setup_text_tab(text_tab)
        
        # Настройка вкладки с файлами
        self.setup_file_tab(file_tab)
        
        # Отображение информации о ключах
        self.show_key_info()
    
    def setup_text_tab(self, parent):
        # Фрейм для ввода
        input_frame = ttk.LabelFrame(parent, text="Исходный текст")
        input_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=8)
        self.input_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Фрейм с кнопками
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        encrypt_btn = ttk.Button(button_frame, text="Зашифровать", command=self.encrypt_text)
        encrypt_btn.pack(side=tk.LEFT, padx=5)
        
        decrypt_btn = ttk.Button(button_frame, text="Расшифровать", command=self.decrypt_text)
        decrypt_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Очистить", command=self.clear_text)
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # Фрейм для вывода
        output_frame = ttk.LabelFrame(parent, text="Результат")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=8)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def setup_file_tab(self, parent):
        # Фрейм для выбора файла
        input_frame = ttk.LabelFrame(parent, text="Исходный файл")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.input_file_path = tk.StringVar()
        input_file_entry = ttk.Entry(input_frame, textvariable=self.input_file_path, width=60)
        input_file_entry.pack(side=tk.LEFT, padx=5, pady=10, fill="x", expand=True)
        
        browse_btn = ttk.Button(input_frame, text="Обзор...", command=self.browse_input_file)
        browse_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # Фрейм с кнопками
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        encrypt_file_btn = ttk.Button(button_frame, text="Зашифровать файл", command=self.encrypt_file)
        encrypt_file_btn.pack(side=tk.LEFT, padx=5)
        
        decrypt_file_btn = ttk.Button(button_frame, text="Расшифровать файл", command=self.decrypt_file)
        decrypt_file_btn.pack(side=tk.LEFT, padx=5)
        
        # Фрейм для выбора выходного файла
        output_frame = ttk.LabelFrame(parent, text="Сохранить результат")
        output_frame.pack(fill="x", padx=10, pady=5)
        
        self.output_file_path = tk.StringVar()
        output_file_entry = ttk.Entry(output_frame, textvariable=self.output_file_path, width=60)
        output_file_entry.pack(side=tk.LEFT, padx=5, pady=10, fill="x", expand=True)
        
        save_btn = ttk.Button(output_frame, text="Выбрать...", command=self.browse_output_file)
        save_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # Фрейм для отображения статуса операции
        status_frame = ttk.LabelFrame(parent, text="Статус операции")
        status_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, wrap=tk.WORD, height=8)
        self.status_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def show_key_info(self):
        # Создаем фрейм для информации о ключах
        key_frame = ttk.LabelFrame(self, text="Информация о ключах")
        key_frame.pack(fill="x", padx=10, pady=5)
        
        n, e = self.rsa.public_key
        key_info = f"Модуль (n): {n}\nОткрытая экспонента (e): {e}\nРазмер ключа: {n.bit_length()} бит"
        
        key_label = ttk.Label(key_frame, text=key_info, justify=tk.LEFT)
        key_label.pack(padx=5, pady=5)
    
    def encrypt_text(self):
        try:
            input_text = self.input_text.get("1.0", tk.END).strip()
            if not input_text:
                messagebox.showwarning("Предупреждение", "Введите текст для шифрования!")
                return
            
            encrypted_blocks = self.rsa.encrypt_string(input_text)
            result = "\n".join([str(block) for block in encrypted_blocks])
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            
            messagebox.showinfo("Успех", "Текст успешно зашифрован!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось зашифровать текст: {e}")
    
    def decrypt_text(self):
        try:
            input_text = self.input_text.get("1.0", tk.END).strip()
            if not input_text:
                messagebox.showwarning("Предупреждение", "Введите зашифрованные блоки для расшифровки!")
                return
            
            # Преобразуем строки в числа (блоки)
            encrypted_blocks = []
            for line in input_text.split("\n"):
                if line.strip():
                    encrypted_blocks.append(int(line.strip()))
            
            if not encrypted_blocks:
                messagebox.showwarning("Предупреждение", "Не удалось распознать зашифрованные блоки!")
                return
                
            decrypted_text = self.rsa.decrypt_string(encrypted_blocks)
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", decrypted_text)
            
            messagebox.showinfo("Успех", "Текст успешно расшифрован!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось расшифровать текст: {e}")
    
    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
    
    def browse_input_file(self):
        file_path = filedialog.askopenfilename(title="Выбрать файл")
        if file_path:
            self.input_file_path.set(file_path)
    
    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(title="Сохранить как")
        if file_path:
            self.output_file_path.set(file_path)
    
    def encrypt_file(self):
        input_file = self.input_file_path.get()
        output_file = self.output_file_path.get()
        
        if not input_file:
            messagebox.showwarning("Предупреждение", "Выберите файл для шифрования!")
            return
        
        if not output_file:
            messagebox.showwarning("Предупреждение", "Выберите файл для сохранения результата!")
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
            
            self.status_text.delete("1.0", tk.END)
            self.status_text.insert("1.0", f"Файл успешно зашифрован и сохранен в {output_file}")
            
        except Exception as e:
            self.status_text.delete("1.0", tk.END)
            self.status_text.insert("1.0", f"Ошибка при шифровании файла: {e}")
    
    def decrypt_file(self):
        input_file = self.input_file_path.get()
        output_file = self.output_file_path.get()
        
        if not input_file:
            messagebox.showwarning("Предупреждение", "Выберите файл для расшифровки!")
            return
        
        if not output_file:
            messagebox.showwarning("Предупреждение", "Выберите файл для сохранения результата!")
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
            
            self.status_text.delete("1.0", tk.END)
            self.status_text.insert("1.0", f"Файл успешно расшифрован и сохранен в {output_file}")
            
        except Exception as e:
            self.status_text.delete("1.0", tk.END)
            self.status_text.insert("1.0", f"Ошибка при расшифровке файла: {e}")
            

if __name__ == "__main__":
    app = RSAApplication()
    app.mainloop()

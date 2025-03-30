"""
Графический интерфейс пользователя для алгоритма шифрования Эль-Гамаля.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
import os
from elgamal import ElGamal

class ElGamalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифрование Эль-Гамаля")
        self.root.geometry("800x600")
        
        # Инициализация алгоритма Эль-Гамаля
        # Используем небольшой размер ключа для демонстрации (для продакшена нужно больше)
        self.cipher = ElGamal(key_size=512)
        
        # Создание верхнего меню
        self.create_menu()
        
        # Создание основного интерфейса
        self.create_widgets()
        
        # Отображение информации о ключах
        self.update_key_info()

    def create_menu(self):
        """Создание верхнего меню приложения"""
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        keys_menu = tk.Menu(menubar, tearoff=0)
        keys_menu.add_command(label="Сгенерировать новые ключи", command=self.generate_new_keys)
        
        menubar.add_cascade(label="Файл", menu=file_menu)
        menubar.add_cascade(label="Ключи", menu=keys_menu)
        
        self.root.config(menu=menubar)
    
    def create_widgets(self):
        """Создание основных элементов интерфейса"""
        # Создание вкладок
        tab_control = ttk.Notebook(self.root)
        
        encrypt_tab = ttk.Frame(tab_control)
        decrypt_tab = ttk.Frame(tab_control)
        
        tab_control.add(encrypt_tab, text="Шифрование")
        tab_control.add(decrypt_tab, text="Расшифрование")
        
        tab_control.pack(expand=1, fill="both")
        
        # Настройка вкладки шифрования
        self.setup_encrypt_tab(encrypt_tab)
        
        # Настройка вкладки расшифрования
        self.setup_decrypt_tab(decrypt_tab)
        
        # Фрейм для информации о ключах
        key_frame = ttk.LabelFrame(self.root, text="Информация о ключах")
        key_frame.pack(padx=10, pady=10, fill="x")
        
        self.key_info = scrolledtext.ScrolledText(key_frame, height=4)
        self.key_info.pack(padx=5, pady=5, fill="x")
        self.key_info.config(state="disabled")
    
    def setup_encrypt_tab(self, parent):
        """Настройка вкладки шифрования"""
        # Текстовое поле для ввода исходного текста
        input_frame = ttk.LabelFrame(parent, text="Исходный текст")
        input_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.encrypt_input = scrolledtext.ScrolledText(input_frame)
        self.encrypt_input.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Кнопки для работы с файлами и шифрования
        button_frame = ttk.Frame(parent)
        button_frame.pack(padx=10, pady=5, fill="x")
        
        load_btn = ttk.Button(button_frame, text="Загрузить из файла", command=self.load_text_for_encrypt)
        load_btn.pack(side="left", padx=5)
        
        encrypt_btn = ttk.Button(button_frame, text="Шифровать", command=self.encrypt_text)
        encrypt_btn.pack(side="left", padx=5)
        
        # Текстовое поле для вывода зашифрованного текста
        output_frame = ttk.LabelFrame(parent, text="Зашифрованный текст")
        output_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.encrypt_output = scrolledtext.ScrolledText(output_frame)
        self.encrypt_output.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Кнопка для сохранения результата
        save_btn = ttk.Button(output_frame, text="Сохранить в файл", command=self.save_encrypted_text)
        save_btn.pack(side="right", padx=5, pady=5)
    
    def setup_decrypt_tab(self, parent):
        """Настройка вкладки расшифрования"""
        # Текстовое поле для ввода зашифрованного текста
        input_frame = ttk.LabelFrame(parent, text="Зашифрованный текст")
        input_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.decrypt_input = scrolledtext.ScrolledText(input_frame)
        self.decrypt_input.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Кнопки для работы с файлами и расшифрования
        button_frame = ttk.Frame(parent)
        button_frame.pack(padx=10, pady=5, fill="x")
        
        load_btn = ttk.Button(button_frame, text="Загрузить из файла", command=self.load_text_for_decrypt)
        load_btn.pack(side="left", padx=5)
        
        decrypt_btn = ttk.Button(button_frame, text="Расшифровать", command=self.decrypt_text)
        decrypt_btn.pack(side="left", padx=5)
        
        # Текстовое поле для вывода расшифрованного текста
        output_frame = ttk.LabelFrame(parent, text="Расшифрованный текст")
        output_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.decrypt_output = scrolledtext.ScrolledText(output_frame)
        self.decrypt_output.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Кнопка для сохранения результата
        save_btn = ttk.Button(output_frame, text="Сохранить в файл", command=self.save_decrypted_text)
        save_btn.pack(side="right", padx=5, pady=5)
    
    def update_key_info(self):
        """Обновление информации о ключах в интерфейсе"""
        p, g, y = self.cipher.public_key
        x = self.cipher.private_key
        
        key_text = f"Открытый ключ: (p: {p}, g: {g}, y: {y})\n"
        key_text += f"Закрытый ключ: x: {x}"
        
        self.key_info.config(state="normal")
        self.key_info.delete(1.0, tk.END)
        self.key_info.insert(tk.END, key_text)
        self.key_info.config(state="disabled")
    
    def generate_new_keys(self):
        """Генерация новой пары ключей"""
        try:
            self.cipher = ElGamal(key_size=512)
            self.update_key_info()
            messagebox.showinfo("Успех", "Новые ключи успешно сгенерированы")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать ключи: {str(e)}")
    
    def encrypt_text(self):
        """Шифрование текста из текстового поля"""
        try:
            plaintext = self.encrypt_input.get(1.0, tk.END).strip()
            if not plaintext:
                messagebox.showwarning("Предупреждение", "Введите текст для шифрования")
                return
            
            encrypted = self.cipher.encrypt_string(plaintext)
            
            # Преобразуем в JSON для отображения
            encrypted_json = json.dumps([(int(a), int(b)) for a, b in encrypted], indent=2)
            
            self.encrypt_output.delete(1.0, tk.END)
            self.encrypt_output.insert(tk.END, encrypted_json)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при шифровании: {str(e)}")
    
    def decrypt_text(self):
        """Расшифрование текста из текстового поля"""
        try:
            encrypted_json = self.decrypt_input.get(1.0, tk.END).strip()
            if not encrypted_json:
                messagebox.showwarning("Предупреждение", "Введите зашифрованный текст для расшифрования")
                return
            
            # Парсим JSON
            encrypted_data = json.loads(encrypted_json)
            encrypted_data = [(int(a), int(b)) for a, b in encrypted_data]
            
            decrypted = self.cipher.decrypt_string(encrypted_data)
            
            self.decrypt_output.delete(1.0, tk.END)
            self.decrypt_output.insert(tk.END, decrypted)
            
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Неверный формат зашифрованных данных. Ожидается JSON-массив.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при расшифровании: {str(e)}")
    
    def load_text_for_encrypt(self):
        """Загрузка текста из файла для шифрования"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл для шифрования",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.encrypt_input.delete(1.0, tk.END)
                self.encrypt_input.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {str(e)}")
    
    def load_text_for_decrypt(self):
        """Загрузка зашифрованного текста из файла для расшифрования"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл для расшифрования",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.decrypt_input.delete(1.0, tk.END)
                self.decrypt_input.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {str(e)}")
    
    def save_encrypted_text(self):
        """Сохранение зашифрованного текста в файл"""
        encrypted_text = self.encrypt_output.get(1.0, tk.END).strip()
        if not encrypted_text:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Сохранить зашифрованный текст",
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(encrypted_text)
                messagebox.showinfo("Успех", f"Файл успешно сохранен: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {str(e)}")
    
    def save_decrypted_text(self):
        """Сохранение расшифрованного текста в файл"""
        decrypted_text = self.decrypt_output.get(1.0, tk.END).strip()
        if not decrypted_text:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Сохранить расшифрованный текст",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(decrypted_text)
                messagebox.showinfo("Успех", f"Файл успешно сохранен: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {str(e)}")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ElGamalApp(root)
    root.mainloop()

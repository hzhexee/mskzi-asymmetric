import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from diffie_hellman import DiffieHellman
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import hashlib

class DiffieHellmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Диффи-Хеллман шифрование")
        self.root.geometry("800x600")
        
        # Инициализация алгоритма Диффи-Хеллмана
        self.alice = None
        self.bob = None
        self.shared_secret = None
        
        # Создаем интерфейс
        self.create_widgets()
        
    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка генерации ключей
        key_frame = ttk.Frame(notebook)
        notebook.add(key_frame, text="Генерация ключей")
        
        # Вкладка шифрования
        encrypt_frame = ttk.Frame(notebook)
        notebook.add(encrypt_frame, text="Шифрование")
        
        # Вкладка расшифрования
        decrypt_frame = ttk.Frame(notebook)
        notebook.add(decrypt_frame, text="Расшифрование")
        
        # Настройка вкладки генерации ключей
        self.setup_key_frame(key_frame)
        
        # Настройка вкладки шифрования
        self.setup_encrypt_frame(encrypt_frame)
        
        # Настройка вкладки расшифрования
        self.setup_decrypt_frame(decrypt_frame)
        
    def setup_key_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Параметры ключа")
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Размер ключа (в битах):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.key_size = ttk.Combobox(frame, values=["512", "1024", "2048", "4096"])
        self.key_size.current(1)  # По умолчанию 1024 бит
        self.key_size.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Button(frame, text="Сгенерировать ключи", command=self.generate_keys).grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        
        info_frame = ttk.LabelFrame(parent, text="Информация о ключах")
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.key_info_text = tk.Text(info_frame, wrap=tk.WORD, height=15)
        self.key_info_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.key_info_text.config(state=tk.DISABLED)
        
    def setup_encrypt_frame(self, parent):
        input_frame = ttk.LabelFrame(parent, text="Исходный текст")
        input_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.encrypt_input = tk.Text(input_frame, wrap=tk.WORD, height=8)
        self.encrypt_input.pack(fill='both', expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Загрузить из файла", command=lambda: self.load_file(self.encrypt_input)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Зашифровать", command=self.encrypt_data).pack(side=tk.RIGHT, padx=5)
        
        output_frame = ttk.LabelFrame(parent, text="Зашифрованный текст")
        output_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.encrypt_output = tk.Text(output_frame, wrap=tk.WORD, height=8)
        self.encrypt_output.pack(fill='both', expand=True, padx=5, pady=5)
        
        save_button_frame = ttk.Frame(output_frame)
        save_button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(save_button_frame, text="Сохранить в файл", command=lambda: self.save_file(self.encrypt_output.get('1.0', tk.END))).pack(side=tk.RIGHT, padx=5)
        
    def setup_decrypt_frame(self, parent):
        input_frame = ttk.LabelFrame(parent, text="Зашифрованный текст")
        input_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.decrypt_input = tk.Text(input_frame, wrap=tk.WORD, height=8)
        self.decrypt_input.pack(fill='both', expand=True, padx=5, pady=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Загрузить из файла", command=lambda: self.load_file(self.decrypt_input)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Расшифровать", command=self.decrypt_data).pack(side=tk.RIGHT, padx=5)
        
        output_frame = ttk.LabelFrame(parent, text="Расшифрованный текст")
        output_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.decrypt_output = tk.Text(output_frame, wrap=tk.WORD, height=8)
        self.decrypt_output.pack(fill='both', expand=True, padx=5, pady=5)
        
        save_button_frame = ttk.Frame(output_frame)
        save_button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(save_button_frame, text="Сохранить в файл", command=lambda: self.save_file(self.decrypt_output.get('1.0', tk.END))).pack(side=tk.RIGHT, padx=5)
        
    def generate_keys(self):
        try:
            key_size = int(self.key_size.get())
            
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
                
                self.key_info_text.config(state=tk.NORMAL)
                self.key_info_text.delete('1.0', tk.END)
                self.key_info_text.insert('1.0', info)
                self.key_info_text.config(state=tk.DISABLED)
                
                messagebox.showinfo("Успех", "Ключи успешно сгенерированы!")
            else:
                messagebox.showerror("Ошибка", f"Ошибка генерации ключей: общие секреты не совпадают!\n"
                                             f"Alice: {alice_shared_secret}\n"
                                             f"Bob: {bob_shared_secret}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при генерации ключей: {str(e)}")
    
    def load_file(self, text_widget):
        file_path = filedialog.askopenfilename(title="Выберите файл")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    text_widget.delete('1.0', tk.END)
                    text_widget.insert('1.0', content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {str(e)}")
                
    def save_file(self, content):
        file_path = filedialog.asksaveasfilename(title="Сохранить как")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Успех", "Файл успешно сохранен!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
    
    def encrypt_data(self):
        if not self.shared_secret:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте ключи!")
            return
        
        plaintext = self.encrypt_input.get('1.0', tk.END).strip()
        if not plaintext:
            messagebox.showwarning("Предупреждение", "Введите текст для шифрования!")
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
            
            self.encrypt_output.delete('1.0', tk.END)
            self.encrypt_output.insert('1.0', result)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка шифрования: {str(e)}")
    
    def decrypt_data(self):
        if not self.shared_secret:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте ключи!")
            return
        
        ciphertext_b64 = self.decrypt_input.get('1.0', tk.END).strip()
        if not ciphertext_b64:
            messagebox.showwarning("Предупреждение", "Введите текст для расшифрования!")
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
            
            self.decrypt_output.delete('1.0', tk.END)
            self.decrypt_output.insert('1.0', plaintext.decode('utf-8'))
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка расшифрования: {str(e)}")

def main():
    root = tk.Tk()
    app = DiffieHellmanApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

"""
Реализация алгоритма RSA для шифрования и дешифрования.
"""
import random
import sympy
import math


class RSA:
    def __init__(self, key_size=1024):
        """
        Инициализация RSA алгоритма.
        
        :param key_size: Размер ключа в битах
        """
        # Генерация ключевой пары
        self.public_key, self.private_key = self._generate_keypair(key_size)
        
    def _generate_keypair(self, key_size):
        """
        Генерация ключевой пары RSA.
        
        :param key_size: Размер ключа
        :return: Кортеж (открытый ключ, закрытый ключ)
        """
        # Размер каждого простого числа должен быть примерно половиной от общего размера ключа
        prime_size = key_size // 2
        
        # Генерация двух больших простых чисел p и q
        p = sympy.randprime(2**(prime_size-1), 2**prime_size)
        q = sympy.randprime(2**(prime_size-1), 2**prime_size)
        
        # Вычисление модуля n
        n = p * q
        
        # Вычисление функции Эйлера φ(n) = (p-1)*(q-1)
        phi = (p - 1) * (q - 1)
        
        # Выбор открытой экспоненты e
        # Обычно используется 65537 (0x10001), так как это простое число и имеет форму 2^k+1
        e = 65537
        
        # Убедимся, что e взаимно просто с phi
        if math.gcd(e, phi) != 1:
            raise ValueError("Выбранная открытая экспонента не подходит")
        
        # Вычисление закрытой экспоненты d (мультипликативно обратное e по модулю phi)
        d = pow(e, -1, phi)
        
        # Открытый ключ: пара (n, e)
        public_key = (n, e)
        # Закрытый ключ: пара (n, d)
        private_key = (n, d)
        
        return public_key, private_key
    
    def encrypt(self, plaintext, public_key=None):
        """
        Шифрование сообщения.
        
        :param plaintext: Сообщение для шифрования (целое число)
        :param public_key: Открытый ключ для шифрования. Если None, используется собственный открытый ключ.
        :return: Зашифрованное сообщение
        """
        if public_key is None:
            public_key = self.public_key
        
        n, e = public_key
        
        # Проверка, что сообщение меньше модуля n
        if plaintext >= n:
            raise ValueError(f"Сообщение слишком длинное. Должно быть меньше {n}")
        
        # C = M^e mod n
        ciphertext = pow(plaintext, e, n)
        return ciphertext
    
    def decrypt(self, ciphertext, private_key=None):
        """
        Дешифрование сообщения.
        
        :param ciphertext: Зашифрованное сообщение
        :param private_key: Закрытый ключ для дешифрования. Если None, используется собственный закрытый ключ.
        :return: Расшифрованное сообщение
        """
        if private_key is None:
            private_key = self.private_key
        
        n, d = private_key
        
        # M = C^d mod n
        plaintext = pow(ciphertext, d, n)
        return plaintext
    
    def encrypt_string(self, text, public_key=None):
        """
        Шифрование текстовой строки по блокам.
        
        :param text: Текст для шифрования
        :param public_key: Открытый ключ
        :return: Список зашифрованных блоков
        """
        if public_key is None:
            public_key = self.public_key
        
        n, _ = public_key
        
        # Определим размер блока в байтах (с запасом для безопасности)
        block_size = (n.bit_length() - 1) // 8
        
        # Кодируем текст в байты
        text_bytes = text.encode('utf-8')
        
        # Разбиваем на блоки и шифруем каждый блок
        encrypted_blocks = []
        for i in range(0, len(text_bytes), block_size):
            block = text_bytes[i:i + block_size]
            block_int = int.from_bytes(block, byteorder='big')
            encrypted_block = self.encrypt(block_int, public_key)
            encrypted_blocks.append(encrypted_block)
        
        return encrypted_blocks
    
    def decrypt_string(self, encrypted_blocks, private_key=None):
        """
        Дешифрование списка зашифрованных блоков в строку.
        
        :param encrypted_blocks: Список зашифрованных блоков
        :param private_key: Закрытый ключ
        :return: Расшифрованный текст
        """
        if private_key is None:
            private_key = self.private_key
        
        n, _ = private_key
        
        # Определим размер блока в байтах
        block_size = (n.bit_length() + 7) // 8
        
        # Расшифровываем блоки и собираем байты
        decrypted_bytes = bytearray()
        for block in encrypted_blocks:
            decrypted_block = self.decrypt(block, private_key)
            
            # Преобразуем число обратно в байты
            # Длина каждого блока может быть разной, поэтому не указываем фиксированную длину
            block_bytes = decrypted_block.to_bytes((decrypted_block.bit_length() + 7) // 8, byteorder='big')
            
            decrypted_bytes.extend(block_bytes)
        
        # Преобразуем байты в строку
        try:
            return decrypted_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Если не удалось декодировать, вернем байты
            return decrypted_bytes

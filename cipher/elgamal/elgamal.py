"""
Реализация алгоритма шифрования Эль-Гамаля.
"""
import random
import sympy


class ElGamal:
    def __init__(self, key_size=1024):
        """
        Инициализация алгоритма Эль-Гамаля.
        
        :param key_size: Размер ключа в битах
        """
        # Генерация ключей
        self.public_key, self.private_key = self._generate_keypair(key_size)
        
    def _generate_keypair(self, key_size):
        """
        Генерация пары ключей Эль-Гамаля.
        
        :param key_size: Размер ключа в битах
        :return: Кортеж (открытый ключ, закрытый ключ)
        """
        # Генерация большого простого числа p
        p = sympy.randprime(2**(key_size-1), 2**key_size)
        
        # Находим примитивный корень g по модулю p
        # На практике часто используются небольшие числа, например 2 или 3
        g = 2
        
        # Убедимся, что g действительно является примитивным корнем
        # Это сложная операция, на практике обычно используются проверенные значения
        
        # Генерация закрытого ключа x (случайное число от 1 до p-2)
        x = random.randint(1, p - 2)
        
        # Вычисление открытого ключа y = g^x mod p
        y = pow(g, x, p)
        
        # Открытый ключ: тройка (p, g, y)
        public_key = (p, g, y)
        # Закрытый ключ: x
        private_key = x
        
        return public_key, private_key
        
    def encrypt(self, plaintext, public_key=None):
        """
        Шифрование сообщения по алгоритму Эль-Гамаля.
        
        :param plaintext: Сообщение для шифрования (целое число)
        :param public_key: Открытый ключ получателя. Если None, используется собственный открытый ключ.
        :return: Пара (a, b) - зашифрованное сообщение
        """
        if public_key is None:
            public_key = self.public_key
        
        p, g, y = public_key
        
        # Проверка, что сообщение меньше модуля p
        if plaintext >= p:
            raise ValueError(f"Сообщение слишком длинное. Должно быть меньше {p}")
        
        # Выбор случайного k, взаимно простого с p-1
        while True:
            k = random.randint(1, p - 2)
            if sympy.gcd(k, p - 1) == 1:
                break
        
        # Вычисление a = g^k mod p
        a = pow(g, k, p)
        
        # Вычисление b = (y^k * M) mod p
        b = (pow(y, k, p) * plaintext) % p
        
        return a, b
        
    def decrypt(self, ciphertext, private_key=None):
        """
        Дешифрование сообщения по алгоритму Эль-Гамаля.
        
        :param ciphertext: Пара (a, b) - зашифрованное сообщение
        :param private_key: Закрытый ключ. Если None, используется собственный закрытый ключ.
        :return: Расшифрованное сообщение
        """
        if private_key is None:
            private_key = self.private_key
        
        a, b = ciphertext
        p = self.public_key[0]
        x = private_key
        
        # Вычисление M = b * (a^x)^(-1) mod p
        # Это эквивалентно M = b * a^(-x) mod p
        
        # Вычисляем a^x mod p
        a_x = pow(a, x, p)
        
        # Находим мультипликативно обратное к a^x по модулю p
        a_x_inv = pow(a_x, p - 2, p)
        
        # Восстанавливаем исходное сообщение M
        plaintext = (b * a_x_inv) % p
        
        return plaintext
    
    def encrypt_string(self, text, public_key=None):
        """
        Шифрование текстовой строки по алгоритму Эль-Гамаля.
        
        :param text: Текст для шифрования
        :param public_key: Открытый ключ
        :return: Список пар (a, b) для каждого символа текста
        """
        if public_key is None:
            public_key = self.public_key
            
        # Кодируем текст в байты
        text_bytes = text.encode('utf-8')
        
        # Шифруем каждый байт отдельно
        result = []
        for byte in text_bytes:
            encrypted = self.encrypt(byte, public_key)
            result.append(encrypted)
            
        return result
    
    def decrypt_string(self, encrypted_data, private_key=None):
        """
        Дешифрование зашифрованной строки.
        
        :param encrypted_data: Список пар (a, b) для каждого байта
        :param private_key: Закрытый ключ
        :return: Расшифрованный текст
        """
        if private_key is None:
            private_key = self.private_key
        
        # Расшифровываем каждый байт
        decrypted_bytes = bytearray()
        for pair in encrypted_data:
            byte = self.decrypt(pair, private_key)
            decrypted_bytes.append(byte)
        
        # Преобразуем байты в строку
        return decrypted_bytes.decode('utf-8')

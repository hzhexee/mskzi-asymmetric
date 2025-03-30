"""
Реализация алгоритма Диффи-Хеллмана для обмена ключами.
"""
import random
import sympy


class DiffieHellman:
    def __init__(self, key_size=1024):
        """
        Инициализация алгоритма Диффи-Хеллмана.
        
        :param key_size: Размер ключа в битах
        """
        # Генерация большого простого числа p
        self.p = sympy.randprime(2**(key_size-1), 2**key_size)
        # Выбор основания g (часто используется 2 или 5)
        self.g = 2
        # Сгенерируем случайное целое число в качестве секретного ключа
        self._private_key = random.randint(2, self.p - 2)
        # Вычисление открытого ключа
        self._public_key = pow(self.g, self._private_key, self.p)
    
    @property
    def public_key(self):
        """Получить открытый ключ"""
        return self._public_key
    
    def generate_shared_secret(self, other_public_key):
        """
        Генерация общего секретного ключа на основе открытого ключа другой стороны.
        
        :param other_public_key: Открытый ключ другой стороны
        :return: Общий секретный ключ
        """
        return pow(other_public_key, self._private_key, self.p)
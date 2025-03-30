"""
Реализация алгоритма Диффи-Хеллмана для обмена ключами.
"""
import random
import sympy


class DiffieHellman:
    def __init__(self, key_size=1024, p=None, g=None):
        """
        Инициализация алгоритма Диффи-Хеллмана.
        
        :param key_size: Размер ключа в битах
        :param p: Простое число p (если None, будет сгенерировано)
        :param g: Основание g (если None, будет использовано значение 2)
        """
        # Используем переданное значение p или генерируем новое
        self.p = p if p is not None else sympy.randprime(2**(key_size-1), 2**key_size)
        
        # Используем переданное значение g или значение 2
        self.g = g if g is not None else 2
        
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
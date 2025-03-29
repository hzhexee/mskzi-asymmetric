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
    
    @classmethod
    def demonstrate(cls, key_size=64):
        """
        Демонстрация работы алгоритма Диффи-Хеллмана.
        
        :param key_size: Размер ключа для демонстрации (меньше для удобства отображения)
        """
        print(f"Демонстрация алгоритма Диффи-Хеллмана (размер ключа: {key_size} бит)")
        print("-" * 50)
        
        # Создаем участников обмена
        alice = cls(key_size)
        bob = cls(key_size)
        
        # Используем один и тот же параметр p для обоих участников в демонстрации
        bob.p = alice.p
        bob.g = alice.g
        
        # Пересчитываем открытый ключ Боба с теми же параметрами
        bob._public_key = pow(bob.g, bob._private_key, bob.p)
        
        print(f"Общие параметры:")
        print(f"p = {alice.p}")
        print(f"g = {alice.g}")
        print()
        
        print("Alice:")
        print(f"Закрытый ключ a = {alice._private_key}")
        print(f"Открытый ключ A = g^a mod p = {alice.public_key}")
        print()
        
        print("Bob:")
        print(f"Закрытый ключ b = {bob._private_key}")
        print(f"Открытый ключ B = g^b mod p = {bob.public_key}")
        print()
        
        # Создание общего секретного ключа
        alice_secret = alice.generate_shared_secret(bob.public_key)
        bob_secret = bob.generate_shared_secret(alice.public_key)
        
        print("Вычисление общего секретного ключа:")
        print(f"Алиса вычисляет: K = B^a mod p = {bob.public_key}^{alice._private_key} mod {alice.p} = {alice_secret}")
        print(f"Боб вычисляет:    K = A^b mod p = {alice.public_key}^{bob._private_key} mod {bob.p} = {bob_secret}")
        print()
        
        if alice_secret == bob_secret:
            print(f"✓ Успех! Оба участника получили одинаковый секретный ключ: {alice_secret}")
        else:
            print("✗ Ошибка! Секретные ключи не совпадают.")


if __name__ == "__main__":
    # Демонстрация работы алгоритма с небольшим ключом для наглядности
    DiffieHellman.demonstrate(key_size=32)
    
    # Более реалистичная демонстрация с ключом большего размера
    DiffieHellman.demonstrate(key_size=256)
#!/usr/bin/env python3
"""
Демонстрация работы алгоритмов асимметричной криптографии:
- Алгоритм Диффи-Хеллмана для обмена ключами
- RSA для шифрования и дешифрования
- Алгоритм Эль-Гамаля для шифрования и дешифрования
"""

import sys
import time
from cipher.diffie_hellman import DiffieHellman
from cipher.rsa import RSA
from cipher.elgamal import ElGamal


def print_header(title):
    """
    Вывод заголовка секции.
    
    :param title: Заголовок
    """
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")


def demonstrate_diffie_hellman():
    """
    Демонстрация работы алгоритма Диффи-Хеллмана.
    """
    print_header("Алгоритм Диффи-Хеллмана для обмена ключами")
    
    # Демонстрация с маленьким ключом для наглядного отображения
    DiffieHellman.demonstrate(key_size=32)
    
    # Замеряем время работы с более реалистичным ключом
    print("\nРабота с реалистичным размером ключа (1024 бит):")
    
    start_time = time.time()
    alice = DiffieHellman(key_size=1024)
    bob = DiffieHellman(key_size=1024)
    
    # Используем один и тот же параметр p для обоих участников
    bob.p = alice.p
    bob.g = alice.g
    bob._public_key = pow(bob.g, bob._private_key, bob.p)
    
    # Обмен открытыми ключами и создание общего секретного ключа
    alice_secret = alice.generate_shared_secret(bob.public_key)
    bob_secret = bob.generate_shared_secret(alice.public_key)
    
    elapsed_time = time.time() - start_time
    
    print(f"Время выполнения: {elapsed_time:.4f} секунд")
    print(f"Ключи совпадают: {'Да' if alice_secret == bob_secret else 'Нет'}")
    print(f"Длина общего секретного ключа (в битах): {alice_secret.bit_length()}")


def demonstrate_rsa():
    """
    Демонстрация работы алгоритма RSA.
    """
    print_header("Алгоритм RSA для шифрования и дешифрования")
    
    # Демонстрация с подробным выводом
    RSA.demonstrate()
    
    # Замеряем время работы с более реалистичным ключом
    print("\nРабота с реалистичным размером ключа (2048 бит):")
    
    start_time = time.time()
    
    # Создание RSA с ключом 2048 бит
    rsa = RSA(key_size=2048)
    
    key_generation_time = time.time() - start_time
    print(f"Время генерации ключей (2048 бит): {key_generation_time:.4f} секунд")
    
    # Шифрование и дешифрование сообщения с большим ключом
    message = "Это тестовое сообщение для проверки шифрования RSA с ключом 2048 бит."
    
    start_time = time.time()
    encrypted = rsa.encrypt_string(message)
    encryption_time = time.time() - start_time
    
    start_time = time.time()
    decrypted = rsa.decrypt_string(encrypted)
    decryption_time = time.time() - start_time
    
    print(f"Время шифрования: {encryption_time:.4f} секунд")
    print(f"Время дешифрования: {decryption_time:.4f} секунд")
    print(f"Проверка корректности: {'успешно' if decrypted == message else 'ошибка'}")


def demonstrate_elgamal():
    """
    Демонстрация работы алгоритма Эль-Гамаля.
    """
    print_header("Алгоритм Эль-Гамаля для шифрования и дешифрования")
    
    # Демонстрация с подробным выводом
    ElGamal.demonstrate()
    
    # Замеряем время работы с более реалистичным ключом
    print("\nРабота с реалистичным размером ключа (512 бит):")
    
    start_time = time.time()
    
    # Создание инстанса Эль-Гамаля с ключом 512 бит
    elgamal = ElGamal(key_size=512)
    
    key_generation_time = time.time() - start_time
    print(f"Время генерации ключей (512 бит): {key_generation_time:.4f} секунд")
    
    # Шифрование и дешифрование сообщения с большим ключом
    message = "Это тестовое сообщение для проверки шифрования Эль-Гамаля."
    
    start_time = time.time()
    encrypted = elgamal.encrypt_string(message)
    encryption_time = time.time() - start_time
    
    start_time = time.time()
    decrypted = elgamal.decrypt_string(encrypted)
    decryption_time = time.time() - start_time
    
    print(f"Время шифрования: {encryption_time:.4f} секунд")
    print(f"Время дешифрования: {decryption_time:.4f} секунд")
    print(f"Проверка корректности: {'успешно' if decrypted == message else 'ошибка'}")


def main():
    """
    Главная функция программы.
    """
    print("Демонстрация алгоритмов асимметричной криптографии\n")
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == "diffie" or arg == "dh":
            demonstrate_diffie_hellman()
        elif arg == "rsa":
            demonstrate_rsa()
        elif arg == "elgamal" or arg == "el":
            demonstrate_elgamal()
        else:
            print(f"Неизвестный аргумент: {arg}")
            print("Доступные опции: diffie (dh), rsa, elgamal (el)")
    else:
        # Запускаем демонстрацию всех трёх алгоритмов
        demonstrate_diffie_hellman()
        demonstrate_rsa()
        demonstrate_elgamal()


if __name__ == "__main__":
    main()
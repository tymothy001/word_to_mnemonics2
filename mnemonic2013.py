import hashlib
import random
from datetime import datetime
from bip_utils import Bip39MnemonicGenerator

def generate_fixed_timestamp_2013():
    """
    Generuje stały timestamp dla początku roku 2013 (1 stycznia 2013, 00:00:00 UTC).
    """
    #timestamp_2013 = int(datetime(2013, 1, 1, 1, 1, 1).timestamp())
    #timestamp_2013 = int(datetime(2012, 7, 1, 18, 9, 0).timestamp())
     timestamp_2013 = int(datetime(2016, 12, 8, 0, 0, 0).timestamp())
 #


    print(f"Stały timestamp: {timestamp_2013}")
    return timestamp_2013

def generate_weak_entropy_with_timestamp():
    """
    Generuje słabą entropię na podstawie stałego timestampu i prostego losowego ciągu.
    """
    timestamp_2013 = generate_fixed_timestamp_2013()
    weak_random = random.randint(0, 1000)  # Bardzo ograniczony zakres
    print(f"Użyty losowy element: {weak_random}")
    return f"{timestamp_2013}-{weak_random}"

def generate_mnemonic_from_entropy():
    """
    Generuje mnemonic seed na podstawie słabej entropii.
    """
    weak_entropy = generate_weak_entropy_with_timestamp()
    hash_entropy = hashlib.sha256(weak_entropy.encode()).digest()[:16]  # Tylko 128 bitów
    mnemonic = Bip39MnemonicGenerator().FromEntropy(hash_entropy)
    return mnemonic, weak_entropy

def save_to_file(filename, data):
    """
    Zapisuje dane do pliku tekstowego.
    """
    with open(filename, "a") as file:
        file.write(data + "\n")
    print(f"Dane zapisane do pliku: {filename}")

def main():
    filename = "mnemonic_seeds_2013.txt"
    print("Generowanie mnemonic seed...")
    for _ in range(2000):  # Generowanie 5 przykładów
        mnemonic, used_entropy = generate_mnemonic_from_entropy()
        print(f"Mnemonic: {mnemonic}")

        # Zapisanie do pliku
        save_to_file(filename, f"{mnemonic}")

if __name__ == "__main__":
    main()

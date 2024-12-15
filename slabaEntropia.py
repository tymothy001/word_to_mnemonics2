import hashlib
import time
import random
from bip_utils import Bip39MnemonicGenerator

def generate_weak_entropy():
    """
    Generuje słabą entropię na podstawie czasu i prostego losowego ciągu.
    """
    timestamp = int(time.time())  # Sekundy od 1970 roku
    weak_random = random.randint(0, 1000)  # Bardzo ograniczony zakres
    print(f"Użyty czas (timestamp): {timestamp}")
    return f"{timestamp}-{weak_random}"

def generate_mnemonic_from_weak_entropy():
    """
    Generuje mnemonic seed na podstawie słabej entropii.
    """
    weak_entropy = generate_weak_entropy()
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
    filename = "mnemonic_seeds.txt"
    print("Generowanie mnemonic seed...")
    for _ in range(1000):  # Generowanie 5 przykładów
        mnemonic, used_entropy = generate_mnemonic_from_weak_entropy()
        print(f"Mnemonic: {mnemonic}")

        # Zapisanie do pliku
        save_to_file(filename, f"{mnemonic}")
#save_to_file(filename, f"Entropy: {used_entropy} -> Mnemonic: {mnemonic}")
if __name__ == "__main__":
    main()

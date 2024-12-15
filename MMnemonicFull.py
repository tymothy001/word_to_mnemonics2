import hashlib
import os
import random
import time
from datetime import datetime
from bip_utils import Bip39MnemonicGenerator, Bip39WordsNum

def generate_historical_entropy():
    """
    Generuje słabą entropię opartą na stałych wartościach środowiskowych z 2011 roku.
    """
    # Przykładowa data z 2011 roku
    historical_date = datetime(2011, 6, 29, 9, 11)
    unix_time = int(time.mktime(historical_date.timetuple()))

    # Pobranie stałych wartości środowiskowych
    pid = os.getpid()  # PID procesu
    user_id = os.getuid() if hasattr(os, 'getuid') else 1000  # ID użytkownika (domyślnie 1000)

    # Kombinacja słabej entropii
    weak_entropy = f"{unix_time}-{pid}-{user_id}-{random.randint(0, 1000)}"
    return weak_entropy

def generate_mnemonic_from_entropy(entropy):
    """
    Generuje mnemonic seed na podstawie słabej entropii.
    """
    hash_entropy = hashlib.sha256(entropy.encode()).digest()
    mnemonic = Bip39MnemonicGenerator().FromEntropy(hash_entropy[:16])
    return mnemonic

def save_mnemonics_to_file(mnemonics, filename="generated_mnemonics.txt"):
    """
    Zapisuje listę mnemonic do pliku tekstowego.
    """
    with open(filename, "w") as file:
        for mnemonic in mnemonics:
            file.write(f"{mnemonic}\n")
    print(f"Zapisano {len(mnemonics)} mnemoniców do pliku: {filename}")

def main():
    mnemonics = []  # Lista do przechowywania wygenerowanych mnemoniców

    print("Generowanie 189 mnemoniców...")
    for _ in range(6000):
        # Generowanie słabej entropii historycznej
        entropy = generate_historical_entropy()

        # Generowanie mnemonic
        mnemonic = generate_mnemonic_from_entropy(entropy)
        mnemonics.append(str(mnemonic))  # Konwersja do string i dodanie do listy

    # Zapisanie mnemoniców do pliku
    save_mnemonics_to_file(mnemonics)

    # Wyświetlenie pierwszych 10 mnemoniców jako przykład
    print("Przykładowe wygenerowane mnemoniki:")
    for mnemonic in mnemonics[:10]:
        print(mnemonic)

if __name__ == "__main__":
    main()

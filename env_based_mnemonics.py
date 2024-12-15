import os
import hashlib
import time
import socket
from bip_utils import Bip39MnemonicGenerator

def generate_entropy_from_env():
    """
    Generuje entropię na podstawie zmiennych środowiskowych:
    - Znacznik czasu (timestamp)
    - Nazwa hosta
    - ID użytkownika (UID)
    """
    # Pobierz aktualny timestamp (sekundy od 1970-01-01)
    timestamp = int(time.time())
    print(f"Timestamp: {timestamp}")

    # Pobierz nazwę hosta
    hostname = socket.gethostname()
    print(f"Nazwa hosta: {hostname}")

    # Pobierz ID użytkownika (UID)
    uid = os.getuid() if hasattr(os, 'getuid') else 1000  # Ustaw UID domyślny, jeśli niedostępny
    print(f"UID: {uid}")

    # Połącz dane w ciąg
    combined_data = f"{timestamp}-{hostname}-{uid}"
    print(f"Dane łączone jako entropia: {combined_data}")

    # Hashuj dane, aby uzyskać entropię (256-bitów, skrócone do 128-bitów)
    entropy = hashlib.sha256(combined_data.encode()).digest()[:16]
    return entropy

def generate_mnemonic_from_env_entropy():
    """
    Generuje mnemonic seed na podstawie entropii wygenerowanej z danych środowiskowych.
    """
    entropy = generate_entropy_from_env()
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    return mnemonic

def save_mnemonics_to_file(mnemonics, filename="env_based_mnemonics.txt"):
    """
    Zapisuje mnemoniki do pliku tekstowego.
    """
    with open(filename, "w") as file:
        for mnemonic in mnemonics:
            file.write(mnemonic.ToStr() + "\n")  # Konwersja Bip39Mnemonic na string
    print(f"Zapisano {len(mnemonics)} mnemoniców do pliku: {filename}")

def main():
    mnemonics = []
    print("Generowanie 10 mnemoniców na podstawie zmiennych środowiskowych...")
    for _ in range(10):  # Generowanie 10 przykładów
        mnemonic = generate_mnemonic_from_env_entropy()
        print(f"Mnemonic: {mnemonic.ToStr()}")
        mnemonics.append(mnemonic)

    # Zapisanie do pliku
    save_mnemonics_to_file(mnemonics)

if __name__ == "__main__":
    main()

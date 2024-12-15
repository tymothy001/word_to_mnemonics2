 
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
    print(f"Słaba entropia (2011): {weak_entropy}")
    return weak_entropy

def generate_mnemonic_from_entropy(entropy):
    """
    Generuje mnemonic seed na podstawie słabej entropii.
    """
    hash_entropy = hashlib.sha256(entropy.encode()).digest()
    mnemonic = Bip39MnemonicGenerator().FromEntropy(hash_entropy[:16])
    return mnemonic

def main():
    # Generowanie słabej entropii historycznej
    entropy = generate_historical_entropy()

    # Generowanie mnemonic
    mnemonic = generate_mnemonic_from_entropy(entropy)
    print(f"Wygenerowany mnemonic z entropii 2011: {mnemonic}")

if __name__ == "__main__":
    main()

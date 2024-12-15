import hashlib
from bip_utils import Bip39MnemonicGenerator

def generate_entropy_from_number(number, hash_count=9000):
    """
    Generuje 12 różnych entropii na podstawie liczby, każda pochodząca z kolejnego hashowania.
    """
    entropies = []
    current_data = str(number).encode()
    for i in range(hash_count):
        # Hashuj aktualne dane i skracaj do 128 bitów (16 bajtów)
        hashed_data = hashlib.sha256(current_data).digest()[:16]
        entropies.append(hashed_data)
        current_data = hashed_data  # Użyj hashu jako danych wejściowych do kolejnego hashowania
    return entropies

def generate_mnemonics_from_number(number):
    """
    Generuje 12 mnemoniców na podstawie 12-krotnego hashowania liczby.
    """
    entropies = generate_entropy_from_number(number)
    mnemonics = [Bip39MnemonicGenerator().FromEntropy(entropy) for entropy in entropies]
    return mnemonics

def save_mnemonics_to_file(mnemonics, filename="number_based_mnemonics.txt"):
    """
    Zapisuje mnemoniki do pliku tekstowego.
    """
    with open(filename, "w") as file:
        for number, mnemonic_list in mnemonics:
            file.write(f"")
            for i, mnemonic in enumerate(mnemonic_list, start=1):
                file.write(f"{mnemonic.ToStr()}\n")
    print(f"Zapisano mnemoniki do pliku: {filename}")

def main():
    mnemonics = []
    print("Generowanie mnemoniców dla cyfr od 0 do 1000...")
    for number in range(1):  # Iteracja od 0 do 1000
        mnemonic_list = generate_mnemonics_from_number(number)
        print(f"Number: {number}, Mnemonics: {[mnemonic.ToStr() for mnemonic in mnemonic_list]}")
        mnemonics.append((number, mnemonic_list))

    # Zapisanie do pliku
    save_mnemonics_to_file(mnemonics)

if __name__ == "__main__":
    main()

import hashlib
import random
from bip_utils import Bip39MnemonicGenerator

def generate_electrum_entropy():
    """
    Generuje losową entropię zgodnie z wczesnym schematem Electrum.
    """
    entropy = random.getrandbits(8)  # Generacja 128-bitowego ciągu
    print(f"Entropia: {entropy:0128b}")  # Wyświetlenie entropii w binarnej formie
    return entropy.to_bytes(16, 'big')  # Konwersja do bajtów

def generate_electrum_mnemonic(entropy):
    """
    Generuje mnemonik w stylu wczesnych wersji Electrum.
    """
    # Użycie hash SHA-256 do dodatkowego przetwarzania entropii
    hashed_entropy = hashlib.sha256(entropy).digest()

    # Wykorzystanie standardu BIP-39 do generacji mnemonic
    mnemonic = Bip39MnemonicGenerator().FromEntropy(hashed_entropy[:16])  # 128-bitowe dane wejściowe
    return mnemonic

def save_mnemonics_to_file(mnemonics, filename="electrum_mnemonics.txt"):
    """
    Zapisuje mnemoniki do pliku tekstowego.
    """
    with open(filename, "w") as file:
        for mnemonic in mnemonics:
            file.write(mnemonic.ToStr() + "\n")  # Konwersja Bip39Mnemonic na string
    print(f"Zapisano {len(mnemonics)} mnemoniców do pliku: {filename}")

def main():
    mnemonics = []
    print("Generowanie 102 mnemoniców w stylu pierwszych wersji Electrum...")
    for _ in range(10002):  # Generacja 102 mnemoniców
        entropy = generate_electrum_entropy()
        mnemonic = generate_electrum_mnemonic(entropy)
        print(f"Mnemonic: {mnemonic.ToStr()}")  # Wyświetlenie mnemonika jako string
        mnemonics.append(mnemonic)

    # Zapisanie do pliku
    save_mnemonics_to_file(mnemonics)

if __name__ == "__main__":
    main()

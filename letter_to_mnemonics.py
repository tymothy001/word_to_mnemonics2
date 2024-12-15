import hashlib
from string import ascii_letters
from bip_utils import Bip39MnemonicGenerator

def generate_entropy_from_letter(letter):
    """
    Generuje entropię na podstawie pojedynczej litery.
    """
    print(f"Generowanie entropii dla litery: {letter}")

    # Hashuj literę, aby uzyskać entropię (128-bitów)
    entropy = hashlib.sha256(letter.encode()).digest()[:16]  # Skrócone do 128 bitów (16 bajtów)
    return entropy

def generate_mnemonic_from_letter(letter):
    """
    Generuje mnemonic seed na podstawie entropii wygenerowanej z pojedynczej litery.
    """
    entropy = generate_entropy_from_letter(letter)
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    return mnemonic

def save_mnemonics_to_file(mnemonics, filename="letter_based_mnemonics.txt"):
    """
    Zapisuje mnemoniki do pliku tekstowego.
    """
    with open(filename, "w") as file:
        for letter, mnemonic in mnemonics:
            file.write(f"{mnemonic.ToStr()}\n")  # Litera + mnemonik
    print(f"Zapisano {len(mnemonics)} mnemoniców do pliku: {filename}")

def main():
    mnemonics = []
    print("Generowanie mnemoniców dla wszystkich liter alfabetu (duże i małe)...")
    for letter in ascii_letters:  # Iteracja przez litery alfabetu
        mnemonic = generate_mnemonic_from_letter(letter)
        print(f"Letter: {letter}, Mnemonic: {mnemonic.ToStr()}")
        mnemonics.append((letter, mnemonic))

    # Zapisanie do pliku
    save_mnemonics_to_file(mnemonics)

if __name__ == "__main__":
    main()

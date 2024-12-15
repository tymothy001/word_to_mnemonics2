import hashlib
from bip_utils import Bip39MnemonicGenerator

def read_words_from_file(filename="words.txt"):
    """
    Wczytuje słowa z pliku tekstowego. Każde słowo powinno znajdować się w nowej linii.
    """
    try:
        with open(filename, "r") as file:
            words = [line.strip() for line in file if line.strip()]  # Usuwa puste linie i białe znaki
        print(f"Wczytano {len(words)} słów z pliku: {filename}")
        return words
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {filename}")
        return []

def generate_entropy_from_word(word, hash_count=777):
    """
    Generuje 12 różnych entropii na podstawie słowa, każda pochodząca z kolejnego hashowania.
    """
    entropies = []
    current_data = word.encode()
    for i in range(hash_count):
        # Hashuj aktualne dane i skracaj do 128 bitów (16 bajtów)
        hashed_data = hashlib.sha256(current_data).digest()[:16]
        entropies.append(hashed_data)
        current_data = hashed_data  # Użyj hashu jako danych wejściowych do kolejnego hashowania
    return entropies

def generate_mnemonics_from_word(word):
    """
    Generuje 12 mnemoniców na podstawie 12-krotnego hashowania słowa.
    """
    entropies = generate_entropy_from_word(word)
    mnemonics = [Bip39MnemonicGenerator().FromEntropy(entropy) for entropy in entropies]
    return mnemonics

def save_mnemonics_to_file(mnemonics, filename="word_based_mnemonics.txt"):
    """
    Zapisuje mnemoniki do pliku tekstowego.
    """
    with open(filename, "w") as file:
        for word, mnemonic_list in mnemonics:
            file.write(f"Word: {word}\n")
            for i, mnemonic in enumerate(mnemonic_list, start=1):
                file.write(f"{mnemonic.ToStr()}\n")
    print(f"Zapisano mnemoniki do pliku: {filename}")

def main():
    words = read_words_from_file("words.txt")  # Plik z listą słów
    if not words:
        return

    mnemonics = []
    print("Generowanie mnemoniców dla słów z pliku...")
    for word in words:
        mnemonic_list = generate_mnemonics_from_word(word)
        print(f"Word: {word}, Mnemonics: {[mnemonic.ToStr() for mnemonic in mnemonic_list]}")
        mnemonics.append((word, mnemonic_list))

    # Zapisanie do pliku
    save_mnemonics_to_file(mnemonics)

if __name__ == "__main__":
    main()

import os
import hashlib
from bip_utils import Bip39MnemonicGenerator

def read_words_from_file(filename="most_used_passwords.txt"):
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

def generate_entropy_from_word(word):
    """
    Generuje entropię na podstawie słowa.
    """
    print(f"Generowanie entropii dla słowa: {word}")

    # Hashuj słowo, aby uzyskać entropię (128-bitów)
    entropy = hashlib.sha256(word.encode()).digest()[:16]  # Skrócone do 128 bitów (16 bajtów)
    return entropy

def generate_mnemonic_from_word(word):
    """
    Generuje mnemonic seed na podstawie entropii wygenerowanej ze słowa.
    """
    entropy = generate_entropy_from_word(word)
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    return mnemonic

def save_mnemonics_to_file(mnemonics, filename):
    """
    Zapisuje mnemoniki do pliku tekstowego.
    """
    with open(filename, "w") as file:
        for word, mnemonic in mnemonics:
            file.write(f"{mnemonic.ToStr()}\n")  # Mnemonik
    print(f"Zapisano {len(mnemonics)} mnemoniców do pliku: {filename}")

def main():
    words = read_words_from_file("most_used_passwords.txt")  # Plik z listą słów BIP-39
    if not words:
        return

    total_words = len(words)
    chunk_size = total_words // 10
    if total_words % 10 != 0:
        chunk_size += 1  # Dodaj dodatkowy chunk, jeśli nie dzieli się równo na 10 części

    output_dir = "mnemonic_output"
    os.makedirs(output_dir, exist_ok=True)  # Upewnij się, że katalog istnieje

    print("Generowanie mnemoniców na podstawie słów z pliku...")

    for i in range(10):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_words)

        if start_idx >= total_words:
            break  # Jeśli przekroczono liczbę słów, przerwij

        chunk_words = words[start_idx:end_idx]
        mnemonics = []

        for word in chunk_words:
            mnemonic = generate_mnemonic_from_word(word)
            mnemonics.append((word, mnemonic))

        output_file = os.path.join(output_dir, f"{(i + 1) * 10}pmnemonic.txt")
        save_mnemonics_to_file(mnemonics, output_file)

if __name__ == "__main__":
    main()

import os
import hashlib

# Wczytanie listy słów Electrum (wersja 1.7.3)
def load_wordlist(filename="wordlist.txt"):
    try:
        with open(filename, "r") as f:
            words = [word.strip() for word in f.readlines()]
        if len(words) != 1626:  # Lista Electrum miała dokładnie 1626 słów
            raise ValueError(f"Nieprawidłowa liczba słów w pliku ({len(words)}), oczekiwano 1626.")
        return words
    except FileNotFoundError:
        raise FileNotFoundError(f"Plik {filename} nie został znaleziony. Upewnij się, że znajduje się w tym samym katalogu co skrypt.")

# Generowanie losowego seeda
def generate_random_seed(seed_length=16):
    return os.urandom(seed_length)

# Przekształcenie seeda w mnemonik
def seed_to_mnemonic(seed, wordlist):
    # Seed jest haszowany, ale obcinany do 54 bitów
    hashed_seed = hashlib.sha256(seed).digest()
    seed_bits = bin(int.from_bytes(hashed_seed, "big"))[2:].zfill(256)[:128]  # Przycięcie do 54 bitów

    # Debug: Sprawdź długość seed_bits
    print(f"Długość seed_bits: {len(seed_bits)} (powinno być 54)")

    mnemonic = []
    for i in range(0, len(seed_bits), 11):
        index = int(seed_bits[i:i+11], 2)  # Konwersja 11-bitowego segmentu na liczbę
        index %= len(wordlist)  # Ograniczenie indeksu do zakresu listy słów
        mnemonic.append(wordlist[index])

    # Debug: Pokaż generowany mnemonik
    print(f"Generowany mnemonik: {' '.join(mnemonic)}")
    return " ".join(mnemonic)

# Główna funkcja symulacji
def generate_electrum_mnemonic():
    try:
        wordlist = load_wordlist()  # Wczytaj listę słów
        print(f"Liczba słów w wordlist: {len(wordlist)} (powinno być 1626)")

        seed = generate_random_seed()  # Wygeneruj losowy seed
        print(f"Seed (w bajtach): {seed.hex()}")

        mnemonic = seed_to_mnemonic(seed, wordlist)  # Przekształć seed na mnemonik
        return mnemonic
    except Exception as e:
        print(f"Błąd: {e}")
        return None

if __name__ == "__main__":
    print("Symulacja generowania mnemonika Electrum (old):")
    mnemonic = generate_electrum_mnemonic()
    if mnemonic:
        print(f"Mnemonik: {mnemonic}")

import hashlib
from bip_utils import Bip39MnemonicGenerator

def generate_entropy_from_seed(seed):
    """
    Generuje entropię na podstawie wartości seed.
    """
    # Konwertuj seed na ciąg znaków
    seed_string = str(seed)
    print(f"Generowanie entropii dla seed: {seed_string}")

    # Hashuj seed, aby uzyskać entropię (128-bitów)
    entropy = hashlib.sha256(seed_string.encode()).digest()[:16]  # Skrócone do 128 bitów (16 bajtów)
    return entropy

def generate_mnemonic_from_seed(seed):
    """
    Generuje mnemonic seed na podstawie entropii wygenerowanej z wartości seed.
    """
    entropy = generate_entropy_from_seed(seed)
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    return mnemonic

def save_mnemonics_to_file(mnemonics, filename="seed_to_mnemonics.txt"):
    """
    Zapisuje mnemoniki do pliku tekstowego.
    """
    with open(filename, "w") as file:
        for seed, mnemonic in mnemonics:
            file.write(f"{mnemonic.ToStr()}\n")  # Seed + mnemonik
    print(f"Zapisano {len(mnemonics)} mnemoniców do pliku: {filename}")

def main():
    mnemonics = []
    print("Generowanie mnemoniców dla seed od 0 do 3400...")
    for seed in range(3401):  # Iteracja od 0 do 3400
        mnemonic = generate_mnemonic_from_seed(seed)
        print(f"Seed: {seed}, Mnemonic: {mnemonic.ToStr()}")
        mnemonics.append((seed, mnemonic))

    # Zapisanie do pliku
    save_mnemonics_to_file(mnemonics)

if __name__ == "__main__":
    main()

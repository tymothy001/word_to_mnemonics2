import hashlib
from bip_utils import Bip39MnemonicGenerator

def generate_entropy_from_mnemonic_seed():
    """
    Generuje entropię na podstawie stałego mnemonic seed.
    """

    # Stały mnemonic seed
    mnemonic_seed = "hill stamp cube reopen patrol supreme grace crawl sample flavor couch toe"
    print(f"Używany mnemonic seed jako entropia: {mnemonic_seed}")

    # Hashuj seed, aby uzyskać entropię (128-bitów)
    entropy = hashlib.sha256(mnemonic_seed.encode()).digest()[:16]  # Skrócone do 128 bitów (16 bajtów)
    return entropy

def generate_mnemonic_from_seed_entropy():
    """
    Generuje mnemonic seed na podstawie entropii wygenerowanej ze stałego mnemonic seed.
    """
    entropy = generate_entropy_from_mnemonic_seed()
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    return mnemonic

def save_mnemonics_to_file(mnemonics, filename="seed_based_mnemonics.txt"):
    """
    Zapisuje mnemoniki do pliku tekstowego.
    """
    with open(filename, "w") as file:
        for mnemonic in mnemonics:
            file.write(mnemonic.ToStr() + "\n")  # Konwersja Bip39Mnemonic na string
    print(f"Zapisano {len(mnemonics)} mnemoniców do pliku: {filename}")

def main():
    mnemonics = []
    print("Generowanie 10 mnemoniców na podstawie stałego mnemonic seed...")
    for _ in range(1):  # Generowanie 10 przykładów
        mnemonic = generate_mnemonic_from_seed_entropy()
        print(f"Mnemonic: {mnemonic.ToStr()}")
        mnemonics.append(mnemonic)

    # Zapisanie do pliku
    save_mnemonics_to_file(mnemonics)

if __name__ == "__main__":
    main()

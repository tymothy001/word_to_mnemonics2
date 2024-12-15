import hashlib
import random
from bip_utils import Bip39MnemonicGenerator, Bip39MnemonicValidator, Bip39Languages

def generate_entropy_with_checksum():
    """
    Generuje entropię z dodaniem checksum (na podstawie SHA-256).
    """
    raw_entropy = random.getrandbits(128)  # 128-bitowa losowość
    entropy_bytes = raw_entropy.to_bytes(16, 'big')  # 16 bajtów

    # Obliczamy hash SHA-256 i dodajemy pierwsze 4 bity jako checksum
    checksum = hashlib.sha256(entropy_bytes).digest()[0] >> 4  # Pierwsze 4 bity
    entropy_with_checksum = (raw_entropy << 4) | checksum  # Dodanie checksum na końcu

    print(f"Entropia (bez checksum): {raw_entropy:0128b}")
    print(f"Checksum: {checksum:04b}")
    print(f"Entropia z checksum: {entropy_with_checksum:0132b}")
    return entropy_with_checksum.to_bytes(17, 'big')  # Z checksum jest 132 bity -> 17 bajtów

def generate_mnemonic_from_entropy():
    """
    Generuje mnemonic seed na podstawie entropii z checksum.
    """
    entropy_with_checksum = generate_entropy_with_checksum()
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy_with_checksum[:16])  # Tylko 128 bitów
    return mnemonic, entropy_with_checksum.hex()

def validate_mnemonic(mnemonic):
    """
    Waliduje mnemonic zgodnie z BIP-39.
    """
    # Usunięto `lang` jako jawny parametr
    validator = Bip39MnemonicValidator(mnemonic)
    is_valid = validator.IsValid()
    print(f"Walidacja mnemonic: {'Poprawny' if is_valid else 'Niepoprawny'}")
    return is_valid

def save_to_file(filename, data):
    """
    Zapisuje dane do pliku tekstowego.
    """
    with open(filename, "a") as file:
        file.write(data + "\n")
    print(f"Dane zapisane do pliku: {filename}")

def main():
    filename = "mnemonic_with_checksum.txt"
    print("Generowanie mnemonic seed...")
    for _ in range(5):  # Generowanie 5 przykładów
        mnemonic, entropy_hex = generate_mnemonic_from_entropy()
        print(f"Mnemonic: {mnemonic}")

        # Walidacja mnemonic
        validate_mnemonic(mnemonic)

        # Zapisanie do pliku
        save_to_file(filename, f"Entropy: {entropy_hex} -> Mnemonic: {mnemonic}")

if __name__ == "__main__":
    main()

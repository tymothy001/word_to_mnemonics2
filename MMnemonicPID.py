import hashlib
from bip_utils import Bip39MnemonicGenerator

def generate_mnemonic_from_pid(pid):
    """
    Generuje mnemonic seed na podstawie podanego PID.
    """
    entropy = f"{pid}"  # PID jako źródło entropii
    hash_entropy = hashlib.sha256(entropy.encode()).digest()
    mnemonic = Bip39MnemonicGenerator().FromEntropy(hash_entropy[:16])
    return mnemonic

def save_mnemonics_to_file(filename, start_pid, end_pid):
    """
    Generuje i zapisuje mnemoniki dla wszystkich PID w podanym zakresie.
    """
    with open(filename, "w") as file:
        for pid in range(start_pid, end_pid + 1):
            mnemonic = generate_mnemonic_from_pid(pid)
            file.write(f"{mnemonic}\n")
            if pid % 1000 == 0:  # Informacja o postępie co 1000 PID
                print(f"Wygenerowano mnemoniki do PID: {pid}")
    print(f"Zapisano mnemoniki dla PID od {start_pid} do {end_pid} do pliku: {filename}")

def main():
    start_pid = 99999  # Początkowy PID
    end_pid = 100200  # Końcowy PID (dla Windows)

    filename = "pid_mnemonics_0_to_100200.txt"
    save_mnemonics_to_file(filename, start_pid, end_pid)

if __name__ == "__main__":
    main()

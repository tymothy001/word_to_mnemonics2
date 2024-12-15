from datetime import datetime, timedelta
import hashlib
from bip_utils import Bip39MnemonicGenerator

def generate_entropy_from_date(date):
    """
    Generuje entropię na podstawie podanej daty w formacie YYYYMMDD.
    """
    date_string = date.strftime("%Y%m%d")  # Format daty jako string
    print(f"Używana data jako entropia: {date_string}")

    # Hashuj datę, aby uzyskać entropię (128-bitów)
    entropy = hashlib.sha256(date_string.encode()).digest()[:16]  # Skrócone do 128 bitów (16 bajtów)
    return entropy

def generate_mnemonic_from_date(date):
    """
    Generuje mnemonic seed na podstawie entropii wygenerowanej z daty.
    """
    entropy = generate_entropy_from_date(date)
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    return mnemonic

def save_mnemonics_to_file(mnemonics, filename="date_based_mnemonics_range.txt"):
    """
    Zapisuje mnemoniki do pliku tekstowego.
    """
    with open(filename, "w") as file:
        for date, mnemonic in mnemonics:
            file.write(f"{mnemonic.ToStr()}\n")  # Data + mnemonik
    print(f"Zapisano {len(mnemonics)} mnemoniców do pliku: {filename}")

def main():
    start_date = datetime(2017, 1, 1)  # Początkowa data
    end_date = datetime(2022, 12, 8)    # Końcowa data

    current_date = start_date
    mnemonics = []

    print(f"Generowanie mnemoniców od {start_date.strftime('%Y-%m-%d')} do {end_date.strftime('%Y-%m-%d')}...")
    while current_date <= end_date:
        mnemonic = generate_mnemonic_from_date(current_date)
        print(f"Data: {current_date.strftime('%Y-%m-%d')}, Mnemonic: {mnemonic.ToStr()}")
        mnemonics.append((current_date, mnemonic))
        current_date += timedelta(days=1)  # Przejście do kolejnej daty

    # Zapisanie do pliku
    save_mnemonics_to_file(mnemonics)

if __name__ == "__main__":
    main()

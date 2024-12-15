import hashlib
import os
import requests
from bip_utils import Bip44, Bip44Coins, Bip44Changes, Bip39SeedGenerator

ELECTRUM_RPC_URL = "http://127.0.0.1:7777"
ELECTRUM_RPC_USER = "user"
ELECTRUM_RPC_PASSWORD = "toor777"

def call_electrum_rpc(method, params=None):
    """
    Wywołuje metodę Electrum RPC.
    :param method: Nazwa metody RPC.
    :param params: Lista parametrów dla metody.
    :return: Wynik metody RPC.
    """
    payload = {
        "id": 1,
        "method": method,
        "params": params or []
    }
    response = requests.post(ELECTRUM_RPC_URL, json=payload, auth=(ELECTRUM_RPC_USER, ELECTRUM_RPC_PASSWORD))
    if response.status_code == 200:
        return response.json().get("result")
    else:
        raise Exception(f"Błąd RPC: {response.status_code}, {response.text}")

def generate_seed_from_input(data):
    """
    Generuje seed na podstawie dowolnego wejścia (mnemonik, jedno słowo, znak, litera lub cyfra).
    :param data: Dane wejściowe.
    :return: Seed jako bajty.
    """
    if len(data.split()) == 1:  # Jeśli dane składają się z jednego elementu
        print(f"Używanie danych wejściowych: {data}")
        hashed_data = hashlib.sha256(data.encode()).digest()  # Hash SHA-256 z wejścia
        return hashed_data
    else:  # Jeśli dane to pełny mnemonik
        return Bip39SeedGenerator(data).Generate()

def generate_addresses(seed, num_addresses=7):
    """
    Generuje adresy Bitcoin z seeda dla różnych ścieżek BIP.
    :param seed: Seed jako bajty.
    :param num_addresses: Liczba adresów do wygenerowania.
    :return: Lista adresów Bitcoin.
    """
    paths = [
        (Bip44Coins.BITCOIN, 0, "BIP44"),  # Standard BIP44 legacy (Account 0)
        (Bip44Coins.BITCOIN, 0, "BIP49"),  # Standard BIP49 compatibility segwit (Account 0)
        (Bip44Coins.BITCOIN, 1, "BIP49"),  # Standard BIP49 compatibility segwit (Account 1)
        (Bip44Coins.BITCOIN, 0, "BIP84"),  # Standard BIP84 native segwit (Account 0)
        (Bip44Coins.BITCOIN, 0, "Non-Standard Legacy"),  # Non-standard legacy (Account 0)
        (Bip44Coins.BITCOIN, 0, "Non-Standard Compatibility Segwit"),  # Non-standard compatibility segwit (Account 0)
        (Bip44Coins.BITCOIN, 0, "Non-Standard Native Segwit"),  # Non-standard native segwit (Account 0)
    ]

    addresses = []
    for coin, account, path_type in paths:
        bip44_ctx = Bip44.FromSeed(seed, coin).Purpose().Coin().Account(account)
        for change in [Bip44Changes.CHAIN_EXT, Bip44Changes.CHAIN_INT]:  # Adresy zewnętrzne i wewnętrzne
            for address_index in range(num_addresses):  # Pierwsze `num_addresses` adresów
                address = bip44_ctx.Change(change).AddressIndex(address_index).PublicKey().ToAddress()
                addresses.append({"address": address, "path_type": path_type})
    return addresses

def save_to_file(file_name, data):
    """
    Zapisuje dane do pliku.
    :param file_name: Nazwa pliku.
    :param data: Dane do zapisania.
    """
    with open(file_name, "a") as file:
        file.write(data + "\n")

def check_all_addresses(addresses, mnemonic):
    """
    Sprawdza saldo i historię transakcji dla wszystkich adresów.
    :param addresses: Lista adresów Bitcoin.
    :param mnemonic: Mnemonic, który wygenerował adresy.
    :return: Lista adresów z ich stanem (saldo, liczba transakcji).
    """
    results = []
    for address_info in addresses:
        address = address_info["address"]
        path_type = address_info["path_type"]
        try:
            balance = call_electrum_rpc("getaddressbalance", [address])
            history = call_electrum_rpc("getaddresshistory", [address])  # Pobiera historię transakcji

            confirmed_balance = int(balance.get("confirmed", "0"))
            unconfirmed_balance = int(balance.get("unconfirmed", "0"))
            total_balance = confirmed_balance + unconfirmed_balance
            num_transactions = len(history)

            if num_transactions > 0:
                # Zapisujemy do pliku, jeśli wykryto transakcje
                save_to_file("addresses_with_transactions.txt", f"Mnemonic: {mnemonic}, Address: {address}, Path: {path_type}")

            results.append({
                "address": address,
                "path_type": path_type,
                "confirmed_balance": confirmed_balance,
                "unconfirmed_balance": unconfirmed_balance,
                "total_balance": total_balance,
                "num_transactions": num_transactions,
            })

            # Debugowanie
            print(f"Adres: {address}, Ścieżka: {path_type}, Saldo: {total_balance} satoshi, Transakcje: {num_transactions}")
        except Exception as e:
            print(f"Błąd przy sprawdzaniu adresu {address}: {e}")
    return results

def check_custom_addresses(custom_addresses):
    """
    Sprawdza dostarczone adresy niestandardowe (np. Copay, Coolwallet S).
    :param custom_addresses: Lista adresów do sprawdzenia.
    """
    for address in custom_addresses:
        try:
            balance = call_electrum_rpc("getaddressbalance", [address])
            history = call_electrum_rpc("getaddresshistory", [address])  # Pobiera historię transakcji

            confirmed_balance = int(balance.get("confirmed", "0"))
            unconfirmed_balance = int(balance.get("unconfirmed", "0"))
            total_balance = confirmed_balance + unconfirmed_balance
            num_transactions = len(history)

            print(f"Adres: {address}, Saldo: {total_balance} satoshi, Transakcje: {num_transactions}")

        except Exception as e:
            print(f"Błąd przy sprawdzaniu adresu {address}: {e}")

if __name__ == "__main__":
    try:
        # Ścieżka do katalogu z plikami mnemoników
        mnemonic_dir = "mnemonic_output"

        # Przetwarzanie plików w katalogu mnemonic_output
        for file_name in sorted(os.listdir(mnemonic_dir)):
            if file_name.endswith(".txt"):
                full_path = os.path.join(mnemonic_dir, file_name)
                print(f"Wczytywanie pliku: {full_path}")
                try:
                    with open(full_path, "r") as file:
                        lines = file.readlines()

                    # Przetwarzanie każdej linii jako osobnego mnemonika/danych wejściowych
                    for mnemonic in lines:
                        mnemonic = mnemonic.strip()
                        if not mnemonic:
                            continue  # Pomijamy puste linie

                        print(f"Przetwarzanie danych: {mnemonic}")
                        num_addresses = 1  # Można ustawić domyślną wartość lub wczytać z pliku

                        print("Generowanie adresów...")
                        seed = generate_seed_from_input(mnemonic)
                        addresses = generate_addresses(seed, num_addresses)
                        print(f"Wygenerowano {len(addresses)} adresów.")

                        print("Rozpoczynam sprawdzanie wszystkich adresów...")
                        results = check_all_addresses(addresses, mnemonic)
                        for result in results:
                            print(result)

                except FileNotFoundError:
                    print(f"Plik {file_name} nie został znaleziony, pomijam.")

        # Sprawdzanie adresów niestandardowych
        print("Sprawdzanie niestandardowych adresów...")
        custom_addresses = [
            "bc1qmll3fcxy28gq97svl3chh93addgwwz3jnvkj7p",  # Coolwallet S
            "35QXNdkZ5cdFTzPGJDQeUsZAXxfqabrFnj"  # Copay
        ]
        check_custom_addresses(custom_addresses)

    except Exception as e:
        print(f"Błąd: {e}")

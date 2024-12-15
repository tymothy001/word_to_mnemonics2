import os
import subprocess
from datetime import datetime, timedelta

def scan_existing_accounts(path):
    existing_accounts = []

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                content = file.read()
                if "milk sad wage cup reward umbrella raven visa give list decorate broccoli" in content:
                    existing_accounts.append(filepath)

    return existing_accounts

def generate_and_save_mnemonics(start_time, end_time, interval_seconds, output_dir):
    current_time = start_time
    total_time = end_time - start_time
    total_mnemonics = (total_time // interval_seconds) + 1
    chunk_size = max(1, total_mnemonics // 10)

    chunk_index = 0
    mnemonics = []

    while current_time <= end_time:
        env = {
            "LD_PRELOAD": "/usr/lib/x86_64-linux-gnu/faketime/libfaketime.so.1",
            "FAKETIME_FMT": "%s",
            "FAKETIME": str(current_time)
        }

        process = subprocess.Popen(["./bx", "seed", "-b", "128"], stdout=subprocess.PIPE, env=env)
        output, _ = process.communicate()
        mnemonic_seed = subprocess.check_output(["./bx", "mnemonic-new"], input=output, env=env).decode().strip()
        mnemonics.append(mnemonic_seed)

        print(f"Generated mnemonic seed for FAKETIME={current_time}")

        if len(mnemonics) == chunk_size or current_time == end_time:
            chunk_index += 1
            filename = os.path.join(output_dir, f"{chunk_index*10}pmnemonic.txt")
            with open(filename, "w") as file:
                file.write("\n".join(mnemonics))
            print(f"Saved {chunk_index*10}% mnemonics to {filename}")
            mnemonics = []

        current_time += interval_seconds

def main():
    time_intervals = {
        1: ("1 sekunda", 1),
        2: ("1 minuta", 60),
        3: ("1 godzina", 3600),
        4: ("1 dzień", 86400),
        5: ("15 dni", 86400 * 15),
        6: ("30 dni", 86400 * 30),
        7: ("1 rok", 86400 * 365)
    }

    print("Wybierz odstęp czasowy generowania mnemoników:")
    for key, (label, _) in time_intervals.items():
        print(f"{key}: {label}")

    interval_choice = int(input("Twój wybór: "))
    if interval_choice not in time_intervals:
        print("Nieprawidłowy wybór.")
        return

    interval_label, interval_seconds = time_intervals[interval_choice]

    start_date_str = input("Podaj datę początkową (YYYY-MM-DD): ")
    end_date_str = input("Podaj datę końcową (YYYY-MM-DD): ")

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    start_time = int(start_date.timestamp())
    end_time = int(end_date.timestamp())

    if start_time >= end_time:
        print("Data początkowa musi być wcześniejsza niż data końcowa.")
        return

    output_dir = "mnemonic_output"
    os.makedirs(output_dir, exist_ok=True)

    generate_and_save_mnemonics(start_time, end_time, interval_seconds, output_dir)

    print("Proces generowania zakończony.")

if __name__ == "__main__":
    main()

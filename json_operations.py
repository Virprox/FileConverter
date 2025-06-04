import json

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("Plik JSON został poprawnie wczytany!")
            return data
    except json.JSONDecodeError:
        print("BŁĄD: To nie jest poprawny plik JSON!")
        return None
    except FileNotFoundError:
        print("BŁĄD: Nie ma takiego pliku!")
        return None

def save_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # indent=4 dla czytelności
            print(f"Dane zapisano poprawnie do pliku {file_path}!")
        return True
    except Exception as e:
        print(f"BŁĄD przy zapisie: {e}")
        return False

if __name__ == "__main__":
    # Test wczytywania
    sciezka_wejsciowa = input("Podaj ścieżkę do pliku JSON (do wczytania): ")
    dane = load_json(sciezka_wejsciowa)
    
    if dane:
        print("Zawartość pliku:", dane)
        # Test zapisywania
        sciezka_wyjsciowa = input("Podaj ścieżkę do nowego pliku JSON (do zapisu): ")
        save_json(dane, sciezka_wyjsciowa)  # Tu wywołujemy save_json
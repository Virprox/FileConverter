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

if __name__ == "__main__":
    sciezka = input("Podaj ścieżkę do pliku JSON: ")
    dane = load_json(sciezka)
    if dane:
        print("Zawartość pliku:", dane)
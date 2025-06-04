import yaml

def load_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)  # bezpieczne wczytywanie
            print("Plik YAML został poprawnie wczytany!")
            return data
    except yaml.YAMLError as e:
        print("BŁĄD YAML: {e}")
        return None
    except FileNotFoundError:
        print("BŁĄD: Nie ma takiego pliku!")
        return None

if __name__ == "__main__":
    sciezka = input("Podaj ścieżkę do pliku YAML: ")
    dane = load_yaml(sciezka)
    if dane:
        print("Zawartość pliku:", dane)
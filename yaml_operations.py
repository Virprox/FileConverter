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

def save_yaml(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
            print(f"Dane zapisano poprawnie do pliku {file_path}!")
        return True
    except Exception as e:
        print(f"BŁĄD przy zapisie YAML: {e}")
        return False

if __name__ == "__main__":
    # Test wczytywania
    sciezka_wejsciowa = input("Podaj ścieżkę do pliku YAML (do wczytania): ")
    dane = load_yaml(sciezka_wejsciowa)
    
    if dane:
        print("Zawartość pliku:", dane)
        # Test zapisywania
        sciezka_wyjsciowa = input("Podaj ścieżkę do nowego pliku YAML (do zapisu): ")
        save_yaml(dane, sciezka_wyjsciowa)
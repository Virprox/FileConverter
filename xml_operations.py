import xmltodict

def load_xml(file_path):
    """Wczytuje plik XML i zwraca słownik Pythona."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = xmltodict.parse(file.read())
            print("Plik XML został poprawnie wczytany!")
            return data
    except Exception as e:
        print(f"BŁĄD WCZYTYWANIA XML: {e}")
        return None

def save_xml(data, file_path):
    """Zapisuje słownik Pythona do pliku XML."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(xmltodict.unparse(data, pretty=True))
            print(f"Dane zapisano poprawnie do pliku {file_path}!")
        return True
    except Exception as e:
        print(f"BŁĄD ZAPISU XML: {e}")
        return False

if __name__ == "__main__":
    # Test wczytywania
    input_path = input("Podaj ścieżkę do pliku XML (do wczytania): ")
    loaded_data = load_xml(input_path)
    
    if loaded_data:
        print("Zawartość pliku:", loaded_data)
        # Test zapisywania
        output_path = input("Podaj ścieżkę do nowego pliku XML (do zapisu): ")
        save_xml(loaded_data, output_path)
import xmltodict

def load_xml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = xmltodict.parse(file.read())  # parsowanie XML na słownik
            print("Plik XML został poprawnie wczytany!")
            return data
    except Exception as e:
        print("BŁĄD XML: {e}")
        return None

def save_xml(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(xmltodict.unparse(data, pretty=True))  # pretty=True dla czytelności
            print("Dane zapisano poprawnie do pliku {file_path}!")
        return True
    except Exception as e:
        print("BŁĄD przy zapisie XML: {e}")
        return False

if __name__ == "__main__":
    # Test wczytywania
    sciezka_wejsciowa = input("Podaj ścieżkę do pliku XML (do wczytania): ")
    dane = load_xml(sciezka_wejsciowa)
    
    if dane:
        print("Zawartość pliku:", dane)
        # Test zapisywania
        sciezka_wyjsciowa = input("Podaj ścieżkę do nowego pliku XML (do zapisu): ")
        save_xml(dane, sciezka_wyjsciowa)
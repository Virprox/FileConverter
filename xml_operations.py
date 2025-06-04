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

if __name__ == "__main__":
    sciezka = input("Podaj ścieżkę do pliku XML: ")
    dane = load_xml(sciezka)
    if dane:
        print("Zawartość pliku:", dane)
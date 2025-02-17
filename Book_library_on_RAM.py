class Ksiazka:
    def __init__(self, tytul, autor, rok, strony, gatunek, isbn13):
        self.tytul = tytul
        self.autor = autor
        self.rok = rok
        self.strony = strony
        self.gatunek = gatunek
        self.isbn13 = isbn13
        self.wypozyczona = False
        self.czytelnik = None

    def wypozycz(self, czytelnik):
        if self.wypozyczona:
            return f"Książka '{self.tytul}' jest już wypożyczona przez {self.czytelnik.imie} {self.czytelnik.nazwisko} (PESEL: {self.czytelnik.pesel})."
        self.wypozyczona = True
        self.czytelnik = czytelnik
        return f"Książka '{self.tytul}' została wypożyczona przez {czytelnik.imie} {czytelnik.nazwisko} (PESEL: {czytelnik.pesel})."


    def oddaj(self):
        if not self.wypozyczona:
            return f"Książka '{self.tytul}' nie jest wypożyczona."
        self.wypozyczona = False
        self.czytelnik = None
        return f"Książka '{self.tytul}' została oddana."

    def __str__(self):
        status = "Wypożyczona" if self.wypozyczona else "Dostępna"
        return f"'{self.tytul}' autorstwa [{self.autor}] z roku {self.rok} - {self.strony} stron, {self.gatunek} - ISBN-13: {self.isbn13} ({status})"


class Czytelnik:
    def __init__(self, imie, nazwisko, pesel):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.wypozyczone_ksiazki = 0

    def __str__(self):
        return f"{self.imie} {self.nazwisko} (PESEL: {self.pesel}, Wypożyczone książki: {self.wypozyczone_ksiazki})"



class Biblioteka:
    def __init__(self):
        self.ksiazki = []
        self.czytelnicy = []

    def dodaj_ksiazke(self, ksiazka):
        self.ksiazki.append(ksiazka)
        return f"Książka '{ksiazka.tytul}' została dodana do biblioteki."

    def usun_ksiazke(self, tytul):
        for ksiazka in self.ksiazki:
            if ksiazka.tytul == tytul:
                if ksiazka.wypozyczona:
                    return f"Książka '{tytul}' nie może zostać usunięta, ponieważ jest wypożyczona."
                self.ksiazki.remove(ksiazka)
                return f"Książka '{tytul}' została usunięta z biblioteki."
        return f"Książki '{tytul}' nie znaleziono w bibliotece."

    def dodaj_czytelnika(self, czytelnik):
        self.czytelnicy.append(czytelnik)
        return f"Czytelnik {czytelnik.imie} {czytelnik.nazwisko} został dodany do biblioteki."

    def usun_czytelnika(self, imie, nazwisko):
        for czytelnik in self.czytelnicy:
            if czytelnik.imie == imie and czytelnik.nazwisko == nazwisko:
                for ksiazka in self.ksiazki:
                    if ksiazka.czytelnik == czytelnik:
                        return f"Czytelnik {imie} {nazwisko} ma wypożyczone książki i nie może zostać usunięty."
                self.czytelnicy.remove(czytelnik)
                return f"Czytelnik {imie} {nazwisko} został usunięty z biblioteki."
        return f"Czytelnika {imie} {nazwisko} nie znaleziono."

    def wypozycz_ksiazke(self, tytul, czytelnik):
        if czytelnik.wypozyczone_ksiazki >= 5:
            return f"Czytelnik {czytelnik.imie} {czytelnik.nazwisko} (PESEL: {czytelnik.pesel}) osiągnął limit 5 wypożyczonych książek. Zwolnij miejsce, zwracając wypożyczoną książkę."
        for ksiazka in self.ksiazki:
            if ksiazka.tytul == tytul:
                if ksiazka.wypozyczona:
                    return ksiazka.wypozycz(czytelnik)
                czytelnik.wypozyczone_ksiazki += 1
                return ksiazka.wypozycz(czytelnik)
        return f"Książka '{tytul}' nie została znaleziona w bibliotece."

    def oddaj_ksiazke(self, tytul, czytelnik):
        for ksiazka in self.ksiazki:
            if ksiazka.tytul == tytul:
                if ksiazka.czytelnik == czytelnik:
                    czytelnik.wypozyczone_ksiazki -= 1
                    return ksiazka.oddaj()
                return f"Książka '{tytul}' nie została wypożyczona przez {czytelnik.imie} {czytelnik.nazwisko}."
        return f"Książka '{tytul}' nie została znaleziona w bibliotece."

    def lista_ksiazek(self):
        if not self.ksiazki:
            return "Biblioteka jest pusta."
        return "\n".join(str(ksiazka) for ksiazka in self.ksiazki)

    def lista_czytelnikow(self):
        if not self.czytelnicy:
            return "Brak czytelników w bazie."
        return "\n".join(str(czytelnik) for czytelnik in self.czytelnicy)
    
    def szukaj_ksiazki(self, kryterium, wartosc):
        znalezione = []
        for ksiazka in self.ksiazki:
            if kryterium == "tytul" and wartosc.lower() in ksiazka.tytul.lower():
                znalezione.append(ksiazka)
            elif kryterium == "autor" and wartosc.lower() in ksiazka.autor.lower():
                znalezione.append(ksiazka)
            elif kryterium == "isbn" and wartosc == ksiazka.isbn13:
                znalezione.append(ksiazka)
        return "\n".join(str(ksiazka) for ksiazka in znalezione) if znalezione else "Nie znaleziono książek."

def wyswietl_i_sortuj_ksiazki():
    while True:
        print("\nWybierz sposób sortowania książek:")
        print("1. Autor A-Z")
        print("2. Autor Z-A")
        print("3. Tytuł A-Z")
        print("4. Tytuł Z-A")
        print("5. Rok wydania rosnąco")
        print("6. Rok wydania malejąco")
        print("7. Liczba stron rosnąco")
        print("8. Liczba stron malejąco")
        print("9. Gatunek A-Z")
        print("0. Powrót do głównego menu")

        wybor = input("Podaj numer opcji: ").strip()

        if wybor == "1":
            ksiazki = sortujAZautor(biblioteka.ksiazki)
        elif wybor == "2":
            ksiazki = sortujZAautor(biblioteka.ksiazki)
        elif wybor == "3":
            ksiazki = sortujAZtytul(biblioteka.ksiazki)
        elif wybor == "4":
            ksiazki = sortujZAtytul(biblioteka.ksiazki)
        elif wybor == "5":
            ksiazki = sortuj09rok(biblioteka.ksiazki)
        elif wybor == "6":
            ksiazki = sortuj90rok(biblioteka.ksiazki)
        elif wybor == "7":
            ksiazki = sortujILEstron09(biblioteka.ksiazki)
        elif wybor == "8":
            ksiazki = sortujILEstron90(biblioteka.ksiazki)
        elif wybor == "9":
            ksiazki = sortujGatunek(biblioteka.ksiazki)
        elif wybor == "0":
            return
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")
            continue

        print("\nLista książek:")
        for ksiazka in ksiazki:
            print(ksiazka)

def wyswietl_i_sortuj_czytelnikow():
    while True:
        print("\nWybierz sposób sortowania czytelników:")
        print("1. Nazwisko A-Z")
        print("2. Nazwisko Z-A")
        print("3. Numer PESEL")
        print("0. Powrót do głównego menu")

        wybor = input("Podaj numer opcji: ").strip()

        if wybor == "1":
            czytelnicy = sortujAZnazwisko(biblioteka.czytelnicy)
        elif wybor == "2":
            czytelnicy = sortujZAnazwisko(biblioteka.czytelnicy)
        elif wybor == "3":
            czytelnicy = sortujPoPESEL(biblioteka.czytelnicy)
        elif wybor == "0":
            return
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")
            continue

        print("\nLista czytelników:")
        for czytelnik in czytelnicy:
            print(czytelnik)


def dodaj_ksiazke_interaktywnie():
    print("\nDodawanie nowej książki (wpisz 'q', aby wrócić do menu):")
    
    # Walidacja tytułu
    tytul = input("Podaj tytuł książki: ").strip()
    if tytul.lower() == 'q':
        return
    if not tytul:
        print("Tytuł książki nie może być pusty. Spróbuj ponownie.")
        return

    # Walidacja autora
    autor = input("Podaj autora książki: ").strip()
    if autor.lower() == 'q':
        return
    if not autor:
        print("Autor książki nie może być pusty. Spróbuj ponownie.")
        return

    # Walidacja roku wydania (od 1 A.D.)
    rok = input("Podaj rok wydania: ").strip()
    if rok.lower() == 'q':
        return
    if not rok.isdigit() or int(rok) <= 0:
        print("Rok wydania musi być dodatnią liczbą. Spróbuj ponownie.")
        return

    # Walidacja liczby stron (dodatnie)
    strony = input("Podaj liczbę stron: ").strip()
    if strony.lower() == 'q':
        return
    if not strony.isdigit() or int(strony) <= 0:
        print("Liczba stron musi być większa od zera. Spróbuj ponownie.")
        return

    # Walidacja gatunku
    gatunek = input("Podaj gatunek książki: ").strip()
    if gatunek.lower() == 'q':
        return
    if not gatunek:
        print("Gatunek książki nie może być pusty. Spróbuj ponownie.")
        return

    # Walidacja numeru ISBN-13
    isbn13 = input("Podaj numer ISBN-13: ").strip()
    if isbn13.lower() == 'q':
        return
    if not isbn13.isdigit() or len(isbn13) != 13:
        print("Numer ISBN-13 musi składać się z 13 cyfr. Spróbuj ponownie.")
        return

    ksiazka = Ksiazka(tytul, autor, rok, strony, gatunek, isbn13)
    print(biblioteka.dodaj_ksiazke(ksiazka))


def sortujAZautor(ksiazki):
    return sorted(ksiazki, key=lambda ksiazka: ksiazka.autor)
def sortujZAautor(ksiazki):
    return sorted(ksiazki, key=lambda ksiazka: ksiazka.autor, reverse=True)
def sortujAZtytul(ksiazki):
    return sorted(ksiazki, key=lambda ksiazka: ksiazka.tytul)
def sortujZAtytul(ksiazki):
    return sorted(ksiazki, key=lambda ksiazka: ksiazka.tytul, reverse=True)
def sortuj09rok(ksiazki):
    return sorted(ksiazki, key=lambda ksiazka: int(ksiazka.rok))
def sortuj90rok(ksiazki):
    return sorted(ksiazki, key=lambda ksiazka: int(ksiazka.rok), reverse=True)
def sortujILEstron09(ksiazki):
    return sorted(ksiazki, key=lambda ksiazka: int(ksiazka.strony))
def sortujILEstron90(ksiazki):
    return sorted(ksiazki, key=lambda ksiazka: int(ksiazka.strony), reverse=True)
def sortujGatunek(ksiazki):
    return sorted(ksiazki, key=lambda ksiazka: ksiazka.gatunek)

def edytuj_ksiazke():
    tytul = input("Podaj tytuł książki, którą chcesz edytować: ").strip()
    for ksiazka in biblioteka.ksiazki:
        if ksiazka.tytul == tytul:
            print(f"Edytujesz książkę: {ksiazka}")
            ksiazka.tytul = input("Nowy tytuł (pozostaw puste, aby nie zmieniać): ") or ksiazka.tytul
            ksiazka.autor = input("Nowy autor (pozostaw puste, aby nie zmieniać): ") or ksiazka.autor
            ksiazka.rok = input("Nowy rok wydania (pozostaw puste, aby nie zmieniać): ") or ksiazka.rok
            ksiazka.strony = input("Nowa liczba stron (pozostaw puste, aby nie zmieniać): ") or ksiazka.strony
            ksiazka.gatunek = input("Nowy gatunek (pozostaw puste, aby nie zmieniać): ") or ksiazka.gatunek
            print("Dane książki zostały zaktualizowane.")
            return
    print("Nie znaleziono książki o podanym tytule.")




def dodaj_czytelnika_interaktywnie():
    print("\nDodawanie nowego czytelnika (wpisz 'q', aby wrócić do menu):")
    
    # Walidacja imienia
    imie = input("Podaj imię czytelnika: ").strip()
    if imie.lower() == 'q':
        return
    if not imie:
        print("Imię nie może być puste. Spróbuj ponownie.")
        return

    # Walidacja nazwiska
    nazwisko = input("Podaj nazwisko czytelnika: ").strip()
    if nazwisko.lower() == 'q':
        return
    if not nazwisko:
        print("Nazwisko nie może być puste. Spróbuj ponownie.")
        return

    # Walidacja PESEL
    pesel = input("Podaj numer PESEL: ").strip()
    if pesel.lower() == 'q':
        return
    if not pesel.isdigit() or len(pesel) != 11:
        print("Numer PESEL musi składać się z 11 cyfr. Spróbuj ponownie.")
        return

    # Sprawdzanie unikalności PESEL
    if any(czytelnik.pesel == pesel for czytelnik in biblioteka.czytelnicy):
        print("Czytelnik z tym numerem PESEL już istnieje!")
        return

    czytelnik = Czytelnik(imie, nazwisko, pesel)
    print(biblioteka.dodaj_czytelnika(czytelnik))



def usun_czytelnika_interaktywnie():
    print("\nUsuwanie czytelnika (wpisz 'q', aby wrócić do menu):")
    imie = input("Podaj imię czytelnika: ").strip()
    if imie.lower() == 'q':
        return
    nazwisko = input("Podaj nazwisko czytelnika: ").strip()
    if nazwisko.lower() == 'q':
        return
    print(biblioteka.usun_czytelnika(imie, nazwisko))

def sortujAZnazwisko(czytelnicy):
    return sorted(czytelnicy, key=lambda czytelnik: czytelnik.nazwisko)
def sortujZAnazwisko(czytelnicy):
    return sorted(czytelnicy, key=lambda czytelnik: czytelnik.nazwisko, reverse=True)
def sortujPoPESEL(czytelnicy):
    return sorted(czytelnicy, key=lambda czytelnik: czytelnik.pesel)

def szukaj_czytelnika_po_pesel():
    print("\nWyszukiwanie czytelnika (wpisz 'q', aby wrócić do menu):")
    pesel = input("Podaj numer PESEL: ").strip()
    if pesel.lower() == 'q':
        return

    for czytelnik in biblioteka.czytelnicy:
        if czytelnik.pesel == pesel:
            print("\nZnaleziony czytelnik:")
            print(czytelnik)
            return

    print("Czytelnik z podanym numerem PESEL nie został znaleziony.")


def wypozycz_ksiazke_interaktywnie():
    print("\nWypożyczanie książki (wpisz 'q', aby wrócić do menu):")
    tytul = input("Podaj tytuł książki: ").strip()
    if tytul.lower() == 'q':
        return
    print("\nLista czytelników:")
    for i, czytelnik in enumerate(biblioteka.czytelnicy, 1):
        print(f"{i}. {czytelnik}")
    wybor_czytelnika = input("Wybierz numer czytelnika (lub wpisz 'q', aby wrócić): ").strip()
    if wybor_czytelnika.lower() == 'q':
        return

    if not wybor_czytelnika.isdigit() or int(wybor_czytelnika) < 1 or int(wybor_czytelnika) > len(biblioteka.czytelnicy):
        print("Nieprawidłowy wybór czytelnika.")
        return

    czytelnik = biblioteka.czytelnicy[int(wybor_czytelnika) - 1]
    print(biblioteka.wypozycz_ksiazke(tytul, czytelnik))


def oddaj_ksiazke_interaktywnie():
    print("\nZwrot książki (wpisz 'q', aby wrócić do menu):")
    tytul = input("Podaj tytuł książki: ").strip()
    if tytul.lower() == 'q':
        return
    print("\nLista czytelników:")
    for i, czytelnik in enumerate(biblioteka.czytelnicy, 1):
        print(f"{i}. {czytelnik}")
    wybor_czytelnika = input("Wybierz numer czytelnika (lub wpisz 'q', aby wrócić): ").strip()
    if wybor_czytelnika.lower() == 'q':
        return

    if not wybor_czytelnika.isdigit() or int(wybor_czytelnika) < 1 or int(wybor_czytelnika) > len(biblioteka.czytelnicy):
        print("Nieprawidłowy wybór czytelnika.")
        return

    czytelnik = biblioteka.czytelnicy[int(wybor_czytelnika) - 1]
    print(biblioteka.oddaj_ksiazke(tytul, czytelnik))


def szukaj_ksiazki_interaktywnie():
    print("\nWyszukiwanie książki (wpisz 'q', aby wrócić do menu):")
    print("1. Po tytule")
    print("2. Po autorze")
    print("3. Po ISBN")
    wybor = input("Wybierz kryterium wyszukiwania: ").strip()
    if wybor.lower() == 'q':
        return

    if wybor == "1":
        wartosc = input("Podaj tytuł: ").strip()
        if wartosc.lower() == 'q':
            return
        print(biblioteka.szukaj_ksiazki("tytul", wartosc))
    elif wybor == "2":
        wartosc = input("Podaj autora: ").strip()
        if wartosc.lower() == 'q':
            return
        print(biblioteka.szukaj_ksiazki("autor", wartosc))
    elif wybor == "3":
        wartosc = input("Podaj ISBN: ").strip()
        if wartosc.lower() == 'q':
            return
        print(biblioteka.szukaj_ksiazki("isbn", wartosc))
    else:
        print("Nieprawidłowy wybór kryterium.")

def szukaj_zaawansowane():
    kryterium = input("Podaj kryterium (np. autor=Tolkien, rok>2000): ").strip().lower()
    for ksiazka in biblioteka.ksiazki:
        if "autor=" in kryterium and kryterium.split("=")[1] not in ksiazka.autor.lower():
            continue
        if "rok>" in kryterium and int(ksiazka.rok) <= int(kryterium.split(">")[1]):
            continue
        if "gatunek=" in kryterium and kryterium.split("=")[1] not in ksiazka.gatunek.lower():
            continue
        print(ksiazka)

def usun_ksiazke_interaktywnie():
    print("\nUsuwanie książki (wpisz 'q', aby wrócić do menu):")
    tytul = input("Podaj tytuł książki do usunięcia: ").strip()
    if tytul.lower() == 'q':
        return
    print(biblioteka.usun_ksiazke(tytul))

def wypozycz_ksiazke_po_pesel():
    print("\nWypożyczanie książki (wpisz 'q', aby wrócić do menu):")
    tytul = input("Podaj tytuł książki: ").strip()
    if tytul.lower() == 'q':
        return

    pesel = input("Podaj numer PESEL czytelnika: ").strip()
    if pesel.lower() == 'q':
        return

    # Walidacja numeru PESEL
    if not pesel.isdigit() or len(pesel) != 11:
        print("Nieprawidłowy numer PESEL. Spróbuj ponownie.")
        return

    # Znajdź czytelnika na podstawie PESEL
    czytelnik = next((c for c in biblioteka.czytelnicy if c.pesel == pesel), None)
    if not czytelnik:
        print("Czytelnik z podanym numerem PESEL nie został znaleziony.")
        return

    # Wypożycz książkę
    print(biblioteka.wypozycz_ksiazke(tytul, czytelnik))





def inicjalizuj_biblioteke(biblioteka):
    # Tworzenie książek
    ksiazki = [
        Ksiazka("Harry Potter i kamien filozoficzny", "Rowling J. K.", "1997", "320", "Fantastyka", "9780590353403"),
        Ksiazka("Straz! Straz!", "Pratchett Terry", "1989", "416", "Fantastyka", "9780552134620"),
        Ksiazka("Hotel Winterhouse", "Guterson Ben", "2018", "384", "Fantastyka", "9781250123886"),
        Ksiazka("Winnetou", "May Karol", "1998", "762", "Przygodowa", "9780826410924"),
        Ksiazka("Lew, Czarownica i Stara Szafa", "St. Lewis Clive", "1994", "208", "Fantastyka", "9780064404990"),
        Ksiazka("Silmarillion", "Tolkien J. R. R.", "2023", "484", "Fantastyka", "9788383350967"),
        Ksiazka("Ziemiomorze", "LeGuin Ursula K.", "2024", "1144", "Fantastyka", "9788383523880"),
        Ksiazka("Wiedzmin: Ostatnie Zyczenie", "Sapkowski Andrzej", "2022", "332", "Fantastyka", "9788375780635"),
        Ksiazka("Atlas Paradox", "Blake Olivie", "2023", "480", "Fantastyka", "9788328728028"),
    ]
    for ksiazka in ksiazki:
        # Dodawanie tylko unikalnych książek (po ISBN)
        if all(k.isbn13 != ksiazka.isbn13 for k in biblioteka.ksiazki):
            biblioteka.dodaj_ksiazke(ksiazka)

    # Tworzenie czytelników
    czytelnicy = [
        Czytelnik("Adrian", "Abacki", "88101012345"),
        Czytelnik("Beata", "Babacka", "77112254321"),
    ]
    for czytelnik in czytelnicy:
        # Dodawanie tylko unikalnych czytelników (po imieniu i nazwisku)
        if all(c.imie != czytelnik.imie or c.nazwisko != czytelnik.nazwisko for c in biblioteka.czytelnicy):
            biblioteka.dodaj_czytelnika(czytelnik)

# Inicjalizacja biblioteki
biblioteka = Biblioteka()

# Pasywne dodanie książek i czytelników
inicjalizuj_biblioteke(biblioteka)

def menu():
    while True:
        print("\n" + "=" * 40)
        print("       SYSTEM ZARZĄDZANIA BIBLIOTEKĄ")
        print("=" * 40)
        print("FUNKCJE DOTYCZĄCE KSIĄŻEK:")
        print("1. Dodaj książkę")
        print("2. Wyświetl listę książek")
        print("3. Wyszukaj książkę")
        print("4. Edytuj dane książki")
        print("5. Usuń książkę")
        print("6. Wypożycz książkę")
        print("7. Wypożycz książkę po PESEL")
        print("8. Oddaj książkę")
        print("\nFUNKCJE DOTYCZĄCE CZYTELNIKÓW:")
        print("9. Dodaj czytelnika")
        print("10. Wyświetl listę czytelników")
        print("11. Wyszukaj czytelnika po PESEL")
        print("12. Usuń czytelnika")
        print("\nINNE:")
        print("0. Wyjdź")
        print("=" * 40)

        wybor = input("Wybierz opcję: ").strip()
        print("=" * 40)

        if wybor == "1":
            dodaj_ksiazke_interaktywnie()
        elif wybor == "2":
            wyswietl_i_sortuj_ksiazki()
        elif wybor == "3":
            szukaj_zaawansowane()
        elif wybor == "4":
            edytuj_ksiazke()
        elif wybor == "5":
            usun_ksiazke_interaktywnie()
        elif wybor == "6":
            wypozycz_ksiazke_interaktywnie()
        elif wybor == "7":
            wypozycz_ksiazke_po_pesel()
        elif wybor == "8":
            oddaj_ksiazke_interaktywnie()
        elif wybor == "9":
            dodaj_czytelnika_interaktywnie()
        elif wybor == "10":
            wyswietl_i_sortuj_czytelnikow()
        elif wybor == "11":
            szukaj_czytelnika_po_pesel()
        elif wybor == "12":
            usun_czytelnika_interaktywnie()
        elif wybor == "0":
            print("Do widzenia!")
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

# Uruchomienie programu
menu()

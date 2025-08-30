import random
import time
import os

# --- Klasy Podstawowe ---

class Zawodnik:
    """
    Reprezentuje pojedynczego zawodnika w grze.
    """
    def __init__(self, imie, szybkosc, wytrzymalosc, refleks, taktyka, agresja):
        self.imie = imie
        # Atrybuty bazowe (0-100)
        self.szybkosc = szybkosc
        self.wytrzymalosc = wytrzymalosc
        self.refleks = refleks
        self.taktyka = taktyka
        self.agresja = agresja
        # Atrybuty dynamiczne
        self.forma = 80  # Forma od 0 do 100
        self.zmeczenie = 0 # Zmęczenie od 0 do 100

    @property
    def overall(self):
        """Oblicza ocenę ogólną jako średnią ważoną atrybutów."""
        return int((self.szybkosc * 1.5 + self.wytrzymalosc + self.refleks + self.taktyka) / 4.5)

    def __str__(self):
        return (f"{self.imie} | Overall: {self.overall} | "
                f"Szyb: {self.szybkosc}, Wytrz: {self.wytrzymalosc}, Refl: {self.refleks}, Takt: {self.taktyka} | "
                f"Forma: {self.forma}%, Zmęczenie: {self.zmeczenie}%")

    def odpocznij(self):
        """Regeneruje zawodnika."""
        self.zmeczenie = max(0, self.zmeczenie - 30)

    def trenuj(self):
        """Prosta symulacja treningu - losowo podnosi statystyki."""
        stat_to_improve = random.choice(['szybkosc', 'wytrzymalosc', 'refleks', 'taktyka'])
        if getattr(self, stat_to_improve) < 100:
            setattr(self, stat_to_improve, getattr(self, stat_to_improve) + 1)
            print(f"Atrybut '{stat_to_improve}' zawodnika {self.imie} wzrósł!")
        self.zmeczenie = min(100, self.zmeczenie + 10)

class Druzyna:
    """
    Reprezentuje drużynę składającą się z zawodników.
    """
    def __init__(self, nazwa, zawodnicy=None, czy_gracz=False):
        self.nazwa = nazwa
        self.zawodnicy = zawodnicy if zawodnicy else []
        self.punkty = 0
        self.reputacja = 50
        self.czy_gracz = czy_gracz

    def dodaj_zawodnika(self, zawodnik):
        self.zawodnicy.append(zawodnik)

    def usun_zawodnika(self, zawodnik):
        self.zawodnicy.remove(zawodnik)

    def __str__(self):
        return f"Drużyna: {self.nazwa} (Punkty: {self.punkty}, Reputacja: {self.reputacja})"

# --- Silnik Gry ---

class LigaTorow:
    """
    Główna klasa zarządzająca całą grą.
    """
    def __init__(self):
        self.druzyny = []
        self.wolni_zawodnicy = []
        self.druzyna_gracza = None
        self.dzien = 1

    def _czysc_ekran(self):
        """Czyści ekran konsoli dla lepszej czytelności."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _generuj_imie(self):
        """Generuje losowe imię i nazwisko."""
        imiona = ["Jan", "Piotr", "Adam", "Kamil", "Marek", "Łukasz"]
        nazwiska = ["Kowalski", "Nowak", "Wiśniewski", "Wójcik", "Lis"]
        return f"{random.choice(imiona)} {random.choice(nazwiska)}"

    def _generuj_zawodnika(self, min_overall=40, max_overall=80):
        """Tworzy nowego, losowego zawodnika."""
        szybkosc = random.randint(min_overall, max_overall)
        wytrzymalosc = random.randint(min_overall, max_overall)
        refleks = random.randint(min_overall, max_overall)
        taktyka = random.randint(min_overall, max_overall)
        agresja = random.randint(30, 90)
        return Zawodnik(self._generuj_imie(), szybkosc, wytrzymalosc, refleks, taktyka, agresja)

    def przygotuj_gre(self):
        """Tworzy drużyny i wolnych zawodników na start gry."""
        # Drużyna gracza
        nazwa_druzyny_gracza = input("Podaj nazwę swojej drużyny: ")
        zawodnicy_gracza = [self._generuj_zawodnika(50, 65) for _ in range(4)]
        self.druzyna_gracza = Druzyna(nazwa_druzyny_gracza, zawodnicy_gracza, czy_gracz=True)
        self.druzyny.append(self.druzyna_gracza)

        # Drużyny AI
        nazwy_druzyn_ai = ["Stalowe Tłoki", "Nocne Jastrzębie", "Tytani Prędkości"]
        for nazwa in nazwy_druzyn_ai:
            zawodnicy = [self._generuj_zawodnika(50, 70) for _ in range(4)]
            self.druzyny.append(Druzyna(nazwa, zawodnicy))

        # Wolni zawodnicy
        self.wolni_zawodnicy = [self._generuj_zawodnika(40, 75) for _ in range(10)]
        print(f"\nWitaj w Lidze Torów, menedżerze drużyny {self.druzyna_gracza.nazwa}!")

    def symuluj_wyscig(self, uczestnicy):
        """
        Przeprowadza symulację wyścigu.
        Kluczowa logika - wydajność zawodnika to suma jego statystyk, formy i odrobiny losowości.
        """
        print("\n--- ROZPOCZYNA SIĘ WYŚCIG! ---")
        wyniki = []

        for zawodnik in uczestnicy:
            # Obliczanie "mocy" zawodnika w tym wyścigu
            moc_bazowa = (zawodnik.szybkosc * 1.2 + zawodnik.wytrzymalosc + zawodnik.refleks + zawodnik.taktyka)
            moc_z_forma = moc_bazowa * (zawodnik.forma / 100)
            
            # Element losowy i agresja
            bonus_agresji = (zawodnik.agresja / 10) * random.uniform(0.5, 1.5) # Agresja to ryzyko
            losowosc = random.randint(-15, 15)
            
            finalny_wynik = int(moc_z_forma + bonus_agresji + losowosc)
            wyniki.append({'zawodnik': zawodnik, 'wynik': finalny_wynik})

            # Aktualizacja zmęczenia
            zawodnik.zmeczenie = min(100, zawodnik.zmeczenie + random.randint(20, 35))

        # Sortowanie wyników od najlepszego
        wyniki.sort(key=lambda x: x['wynik'], reverse=True)

        # Wyświetlanie i przyznawanie punktów
        print("\n--- WYNIKI WYŚCIGU ---")
        punkty_do_zdobycia = [10, 8, 6, 4, 2, 1]
        for i, res in enumerate(wyniki):
            zawodnik = res['zawodnik']
            druzyna_zawodnika = next(d for d in self.druzyny if zawodnik in d.zawodnicy)
            
            print(f"{i+1}. {zawodnik.imie} ({druzyna_zawodnika.nazwa}) - Wynik: {res['wynik']}")
            
            if i < len(punkty_do_zdobycia):
                punkty = punkty_do_zdobycia[i]
                druzyna_zawodnika.punkty += punkty
                # Aktualizacja formy
                zawodnik.forma = min(100, zawodnik.forma + 10 - i) # Lepsze miejsce = większy wzrost formy
            else:
                # Spadek formy za słaby wynik
                zawodnik.forma = max(0, zawodnik.forma - 5)

    def wyswietl_menu_glowne(self):
        print(f"\n--- Dzień {self.dzien} | Menu Główne ---")
        print("1. Mój klub (zarządzanie składem i trening)")
        print("2. Wolni zawodnicy (rynek transferowy)")
        print("3. Tabela ligi")
        print("4. Rozegraj następny wyścig")
        print("5. Zakończ grę")
        return input("Wybierz opcję: ")

    def menu_klubu(self):
        while True:
            self._czysc_ekran()
            print(f"--- Zarządzanie Klubem: {self.druzyna_gracza.nazwa} ---")
            for i, z in enumerate(self.druzyna_gracza.zawodnicy):
                print(f"{i+1}. {z}")
            
            print("\nCo chcesz zrobić?")
            print("t [numer] - Trenuj zawodnika")
            print("o [numer] - Daj odpocząć zawodnikowi")
            print("z [numer] - Zwolnij zawodnika (jeśli masz więcej niż 4)")
            print("w - Wróć do menu głównego")
            
            wybor = input("> ").lower().split()
            cmd = wybor[0]

            if cmd == 'w':
                break
            
            if len(wybor) < 2 or not wybor[1].isdigit():
                print("Nieprawidłowa komenda.")
                time.sleep(1)
                continue

            idx = int(wybor[1]) - 1
            if 0 <= idx < len(self.druzyna_gracza.zawodnicy):
                zawodnik = self.druzyna_gracza.zawodnicy[idx]
                if cmd == 't':
                    zawodnik.trenuj()
                elif cmd == 'o':
                    zawodnik.odpocznij()
                    print(f"{zawodnik.imie} odpoczywa.")
                elif cmd == 'z':
                    if len(self.druzyna_gracza.zawodnicy) > 4:
                        potwierdzenie = input(f"Czy na pewno chcesz zwolnić {zawodnik.imie}? (t/n): ")
                        if potwierdzenie.lower() == 't':
                            self.druzyna_gracza.usun_zawodnika(zawodnik)
                            self.wolni_zawodnicy.append(zawodnik)
                            print(f"{zawodnik.imie} został zwolniony.")
                    else:
                        print("Nie możesz mieć mniej niż 4 zawodników!")
                else:
                    print("Nieznana komenda.")
            else:
                print("Nieprawidłowy numer zawodnika.")
            
            input("\nNaciśnij Enter, aby kontynuować...")


    def menu_wolnych_zawodnikow(self):
        self._czysc_ekran()
        print("--- Rynek Wolnych Zawodników ---")
        if not self.wolni_zawodnicy:
            print("Brak dostępnych zawodników.")
        else:
            for i, z in enumerate(self.wolni_zawodnicy):
                print(f"{i+1}. {z}")
        
        print("\nAby zakontraktować zawodnika, wpisz jego numer. (Wpisz 'w', aby wrócić)")
        wybor = input("> ")

        if wybor.lower() == 'w':
            return

        if wybor.isdigit():
            idx = int(wybor) - 1
            if 0 <= idx < len(self.wolni_zawodnicy):
                if len(self.druzyna_gracza.zawodnicy) < 6:
                    zawodnik = self.wolni_zawodnicy.pop(idx)
                    self.druzyna_gracza.dodaj_zawodnika(zawodnik)
                    print(f"\nGratulacje! {zawodnik.imie} dołączył do Twojej drużyny!")
                else:
                    print("\nMasz już maksymalną liczbę zawodników (6)!")
            else:
                print("\nNieprawidłowy numer.")
        else:
            print("\nNieprawidłowe polecenie.")
        
        input("Naciśnij Enter, aby kontynuować...")

    def wyswietl_tabele(self):
        self._czysc_ekran()
        print("--- Tabela Ligi ---")
        posortowane_druzyny = sorted(self.druzyny, key=lambda d: d.punkty, reverse=True)
        for i, d in enumerate(posortowane_druzyny):
            gracz_tag = " (Twoja drużyna)" if d.czy_gracz else ""
            print(f"{i+1}. {d.nazwa}{gracz_tag} - {d.punkty} pkt.")
        input("\nNaciśnij Enter, aby kontynuować...")
    
    def start_wyscigu(self):
        self._czysc_ekran()
        print("--- Dzień Wyścigu ---")
        
        # Wybór składu przez gracza
        print("Wybierz 3 zawodników na wyścig (podaj numery oddzielone spacją):")
        for i, z in enumerate(self.druzyna_gracza.zawodnicy):
            print(f"{i+1}. {z}")
        
        while True:
            wybor = input("> ").split()
            if len(wybor) == 3 and all(n.isdigit() for n in wybor):
                indeksy = [int(n) - 1 for n in wybor]
                if all(0 <= i < len(self.druzyna_gracza.zawodnicy) for i in indeksy):
                    sklad_gracza = [self.druzyna_gracza.zawodnicy[i] for i in indeksy]
                    break
            print("Nieprawidłowy wybór. Podaj dokładnie 3 różne numery z listy.")

        # AI wybiera swoich najlepszych zawodników
        uczestnicy = list(sklad_gracza)
        for druzyna in self.druzyny:
            if not druzyna.czy_gracz:
                # AI wybiera 3 zawodników z najwyższą formą i najmniejszym zmęczeniem
                sklad_ai = sorted(druzyna.zawodnicy, key=lambda z: z.forma - z.zmeczenie, reverse=True)[:3]
                uczestnicy.extend(sklad_ai)
        
        self.symuluj_wyscig(uczestnicy)
        self.dzien += 1
        input("\nNaciśnij Enter, aby kontynuować...")


    def petla_gry(self):
        self._czysc_ekran()
        self.przygotuj_gre()

        while True:
            self._czysc_ekran()
            wybor = self.wyswietl_menu_glowne()

            if wybor == '1':
                self.menu_klubu()
            elif wybor == '2':
                self.menu_wolnych_zawodnikow()
            elif wybor == '3':
                self.wyswietl_tabele()
            elif wybor == '4':
                self.start_wyscigu()
            elif wybor == '5':
                print("Dziękujemy za grę!")
                break
            else:
                print("Nieprawidłowa opcja, spróbuj ponownie.")
                time.sleep(1)

if __name__ == "__main__":
    gra = LigaTorow()
    gra.petla_gry()

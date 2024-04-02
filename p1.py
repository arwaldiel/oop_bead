from datetime import datetime
from abc import ABC, abstractmethod

class Szoba(ABC):
    def __init__(self, szobaszam):
        self.szobaszam = szobaszam

    @abstractmethod
    def szoba_tipus(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(szobaszam)
        self.ar = 5000

    def szoba_tipus(self):
        return "Egyágyas Szoba"


class KetagyasSzoba(Szoba):

    def __init__(self, szobaszam):
        super().__init__(szobaszam)
        self.ar = 9000

    def szoba_tipus(self):
        return "Kétágyas Szoba"

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_room(self,szoba): #szoba hozzáadása
        self.szobak.append(szoba)

    def show_rooms(self): #kilistázza az összes szobát, árral
        print("Teszt Hotel szobalista:")
        for szoba in self.szobak:
            print("Szobaszám:",szoba.szobaszam,"Ár:",szoba.ar)
        print("")

    def reservation(self, szobaszam, datum):
        foglalas_datum = datetime.strptime(datum, '%Y-%m-%d')
        if datetime.now() < foglalas_datum: #ha legalább holnapi a dátum
            b = False
            for i in self.foglalasok:
                if i.szoba.szobaszam == szobaszam and foglalas_datum == i.datum: #ha az adott szobára van foglalás az adott dátumon
                    print("Hibás foglalás: Az adott szobára az adott napon már van foglalás!")
                    b = True
                    break
            if b == False:
                j = self.get_room(szobaszam)
                if j == False:
                    print("Hibás foglalás: Nincs ilyen szoba!")
                else:
                    fogl = Foglalas(j, foglalas_datum)
                    print("Az alábbi foglalás történt:")
                    print("Szoba:",j.szobaszam,"Ár:",j.ar,"Dátum:",datum)
                    print()
                    self.foglalasok.append(fogl)
        else:#ha mai vagy korábbi a foglalási dátum
            print("Dátumhiba: Mai vagy korábbi a dátum!")

    def cancel(self, szobaszam, datum):
        foglalas_datum = datetime.strptime(datum, '%Y-%m-%d')
        for i in self.foglalasok:
            if i.szoba.szobaszam == szobaszam and i.datum == foglalas_datum:
                self.foglalasok.remove(i)
                print("Foglalás törölve!")
                break

    def list_reservations(self):
        for i in self.foglalasok:
            i.print_reservations()
        print()

    def get_room(self, szobaszam):
        for i in self.szobak:
            if i.szobaszam == szobaszam:
                return i
        return False
class Foglalas(Szoba):
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

    def szoba_tipus(self):
        return self

    def print_reservations(self):
        print("Szobaszám:",self.szoba.szobaszam,"Foglalás dátuma:",datetime.strftime(self.datum, '%Y-%m-%d'))

szoba1 = EgyagyasSzoba(101)
szoba2 = EgyagyasSzoba(102)
szoba3 = KetagyasSzoba(103)

szobalista = [szoba1, szoba2, szoba3]

hotel = Szalloda("Teszt Hotel")
for szoba in szobalista:
    hotel.add_room(szoba)

#hotel.show_rooms()

hotel.reservation(101, "2024-04-03")
hotel.reservation(101, "2024-04-05")
hotel.reservation(102, "2024-04-04")
hotel.reservation(103, "2024-04-06")
hotel.reservation(103, "2024-04-08")

#hotel.reservation(101, "2024-04-03")

class FelhasznaloiInterface:
    def __init__(self, szalloda):
        self.szalloda = szalloda

    def futtat(self):
        while True:
            print("\nVálasszon műveletet:")
            print("1. Foglalás")
            print("2. Lemondás")
            print("3. Foglalások listázása")
            print("0. Kilépés")

            valasztas = input("Adja meg a kívánt művelet számát: ")

            if valasztas == "1":
                self.foglalas()
            elif valasztas == "2":
                self.lemondas()
            elif valasztas == "3":
                self.szalloda.list_reservations()
            elif valasztas == "0":
                print("Kilépés...")
                break
            else:
                print("Érvénytelen választás.")

    def foglalas(self):
        szobaszam = input("Adja meg a foglalandó szoba számát: ")
        datum = input("Adja meg a foglalás dátumát (pl. 2024-04-01): ")
        self.szalloda.reservation(int(szobaszam), datum)

    def lemondas(self):
        szobaszam = input("Adja meg a lemondandó foglalás szobaszámát: ")
        datum = input("Adja meg a lemondandó foglalás dátumát (pl. 2024-04-01): ")
        self.szalloda.cancel(int(szobaszam), datum)

interface = FelhasznaloiInterface(hotel)
interface.futtat()
from datetime import datetime
from abc import ABC, abstractmethod


class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def szoba_tipus(self):
        pass

class EgyagyasSzoba(Szoba):
    def szoba_tipus(self):
        return self

class KetagyasSzoba(Szoba):
    def szoba_tipus(self):
        return self

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
            if self.isempty():  #ha üres a foglalási lista
                i = self.get_room(szobaszam)
                if i == False:
                    print("Hibás foglalás: Nincs ilyen szoba!")
                else:
                    fogl = Foglalas(i, foglalas_datum)
                    print("Az alábbi foglalás történt:")
                    print("Szoba:", i.szobaszam, "Ár:", i.ar, "Dátum:", datum)
                    print()
                    self.foglalasok.append(fogl)
            else: #ha nem üres a foglalási lista
                for i in self.foglalasok:
                    if i.szoba.szobaszam == szobaszam and foglalas_datum == i.datum: #ha az adott szobára van foglalás az adott dátumon
                        print("Hibás foglalás: Az adott szobára az adott napon már van foglalás!")
                        break
                    else:
                        j = self.get_room(szobaszam)
                        if j == False:
                            print("Hibás foglalás: Nincs ilyen szoba!")
                        else:
                            fogl = Foglalas(j, foglalas_datum)
                            print("Az alábbi foglalás történt:")
                            print("Szoba:",j.szobaszam,"Ár:",j.ar,"Dátum:",datum)
                            print()
                            self.foglalasok.append(fogl)
                            break
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

    def isempty(self):
        return (len(self.foglalasok) == 0)

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

    """def check_room_reserved(self,szobaszam,datum):
        for i in self.foglalasok:
            if i.szoba.szobaszam == szobaszam and datum == i.szoba.datum:
                return True"""

szoba1 = EgyagyasSzoba(101,5000)
szoba2 = EgyagyasSzoba(102,5000)
szoba3 = KetagyasSzoba(103,9000)


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

class FelhasznaloiInterfesz:
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
                hotel.list_reservations()
            elif valasztas == "0":
                print("Kilépés...")
                break
            else:
                print("Érvénytelen választás.")

    def foglalas(self):
        szobaszam = input("Adja meg a foglalandó szoba számát: ")
        datum = input("Adja meg a foglalás dátumát (pl. 2024-04-01): ")
        hotel.reservation(int(szobaszam), datum)


    def lemondas(self):
        szobaszam = input("Adja meg a lemondandó foglalás szobaszámát: ")
        datum = input("Adja meg a lemondandó foglalás dátumát (pl. 2024-04-01): ")
        hotel.cancel(int(szobaszam), datum)

interfesz = FelhasznaloiInterfesz(hotel)
interfesz.futtat()
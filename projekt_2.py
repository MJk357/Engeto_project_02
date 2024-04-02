"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Michal Jelínek
email: jelmic@gmail.com
discord: michal2853
"""
#Bulls & Cows
import random
import time

#Proměnné
odrazka = '-' * 50
pocet_cifer = 4
soubor = "vysledky.txt"

def vygeneruj_nahodne_cislo(pocet_cifer) -> str:
    """
    Vygeneruje náhodné číslo, které nezačíná nulou např. 2013
    a nemá duplicitní čísla
    :param pocet_cifer: počet cifer náhosného čísla
    :return: náhodně číslo
    """
    nahodne_cislo = ''
    while len(nahodne_cislo) < pocet_cifer:
        cislo = random.randint(0, 9)
        #první nesmí být 0
        if len(nahodne_cislo) == 0 and cislo == 0:
            continue
        #Nesmí být duplicitní čísla
        if str(cislo) in nahodne_cislo:
            continue
        nahodne_cislo += str(cislo)
    return nahodne_cislo

def over_cislo(vstupni_cislo: str) -> bool:
    """
    Ověří korektnost zadávaného čísla
    jestli má správnou délku, nezačíná nulou, obsahuje jen čísla a
    neobsahuje duplicita
    :param vstupni_cislo: číslo ve formátu str
    :return: bool (True/False)
    """
    #delka
    if len(vstupni_cislo) != pocet_cifer:
        return False
    #nula na začátku
    if vstupni_cislo.startswith('0'):
        return False
    for i in range(len(vstupni_cislo)):
        #jen numeric
        if not vstupni_cislo[i].isdigit():
            return False
        #duplicita
        if vstupni_cislo[i] in vstupni_cislo[i + 1:len(vstupni_cislo) + 1]:
            return False
    return True

def vyhodnot_cislo(vstupni_cislo: str, nahodne_cislo: str) -> list:
    """
    Porovná vstupní číslo s náhodným.
    Kolik čísel je na stejné pozici (bulls)
    Kolik čísel je na jiné pozici (cows)
    :param vstupni_cislo: tip od uživatele
    :param nahodne_cislo: hádané číslo
    :return: list[bulls: int, cows: int]
    """
    vysledek = [0, 0]
    for i in range(len(vstupni_cislo)):
        if vstupni_cislo[i] == nahodne_cislo[i]:
            vysledek[0] += 1
            continue
        if vstupni_cislo[i] in nahodne_cislo:
            vysledek[1] += 1
    return vysledek

def slovni_hodnoceni(pocet_pokusu: int, pocet_cifer: int) -> str:
    """
    Slovně ohodnotí počet potřebných pokusů o uhádnutí
    Hodnocení bere v úvahu počet cifer, tedy obtížnost
    :param pocet_pokusu: počet pokusů pro zjištění hádaného čísla
    :param pocet_cifer: počet cifer hádaného čísla
    :return: slovní hodnocení
    """
    if pocet_pokusu < pocet_cifer:
        return "amazing"
    elif pocet_pokusu < pocet_cifer * 2:
        return "average"
    elif pocet_pokusu < pocet_cifer *3:
        return "not so good"
    else:
        return "pretty bad"

def zapis_do_souboru(hodnoty_do_souboru: list, soubor: str) -> None:
    """
    Zapíše výsledné hodnoty hádání do souboru
    :param hodnoty_do_souboru: list[pocet_cifer, pocet_pokusu, celkovy_cas]
    :param soubor: jméno souboru
    :return: None
    """
    # Pro kontrolu, zda je soubor prázdný
    with open(soubor, "r") as f:
        soubor_obsah = f.read()

    with open(soubor, "a") as f:
        if soubor_obsah.strip():  # Pokud není soubor prázdný, přidáme nový řádek
            f.write("\n")
        for i, number in enumerate(hodnoty_do_souboru):
            if i == len(hodnoty_do_souboru) - 1:
                f.write(str(number))  # Zapíše číslo bez středníku na konci
            else:
                f.write(f"{number};")  # Zapíše číslo s následujícím středníkem

def vrat_poradi(vysledek: list, soubor: str) -> int:
    """
    Vrátí pořadí výsledku mezi minulými pokusy v souboru
    Hodnoceno dle potřebného počtu pokusů a v případě shody, podle potřebného času
    :param vysledek: list[pocet_cifer, pocet_pokusu, celkovy_cas]
    :param soubor: jméno souboru
    :return: pořadí (int)
    """
    #Načte soubor s výsledky
    vysledky = []
    with open(soubor, 'r') as file:
        for line in file:
            hodnoty = line.strip().split(';')
            cisla = (int(hodnoty[0]), int(hodnoty[1]), float(hodnoty[2]))
            vysledky.append(cisla)
    #Seřadí výsledky
    vysledky_pro_pocet_cifer = [x for x in vysledky if x[0] == vysledek[0]]
    serazena_data = sorted(vysledky_pro_pocet_cifer, key=lambda x: (x[1], x[2]))
    # Zjistí, na kolikátém místě je výsledek v pořadí
    poradi = serazena_data.index(tuple(vysledek)) + 1
    return poradi


#Pozdrav
print('Hi there!',odrazka, sep='\n')
print(f"I've generated a random {pocet_cifer} digit number for you."
      f"\nLet's play a bulls and cows game."
      f"\n{odrazka}\nEnter a number:\n{odrazka}",sep='')

#Generování náhodného čísla
nahodne_cislo = (vygeneruj_nahodne_cislo(pocet_cifer))
print(nahodne_cislo) #SMAZAT

#Spuštění časovace
pocatecni_cas = time.time()

#Hádání čísla
pocet_pokusu = 0
while True:
    tipovane_cislo = input()
    if not over_cislo(tipovane_cislo):
        print('Incorrect number, try again:')
        continue
    vysledek = vyhodnot_cislo(tipovane_cislo, nahodne_cislo)
    pocet_pokusu += 1
    if vysledek[0] == pocet_cifer:
        break
    #text bull/bulls, cow/cows podle počtu
    bull = "bull" if vysledek[0] < 2 else "bulls"
    cow = "cow" if vysledek[1] < 2 else "cows"
    print(f"{vysledek[0]} {bull}, {vysledek[1]} {cow}\n{odrazka}")

#Výpočet času hádání
celkovy_cas = round((time.time() - pocatecni_cas), 2)

#Výpis výsledků
print(f"Correct, you've guessed the right number"
      f"\nin {pocet_pokusu} guesses!")
print(odrazka)
print("That's", slovni_hodnoceni(pocet_pokusu, pocet_cifer))
print("Total guessing time: " + str(celkovy_cas), "sec.")

#Zápis výsledků do souboru
hodnoty_do_souboru = [pocet_cifer, pocet_pokusu, celkovy_cas]
zapis_do_souboru(hodnoty_do_souboru, soubor)

#Porovnání se ostatními výsledky
poradi = vrat_poradi(hodnoty_do_souboru, soubor)
print(f"Your result is on {poradi}. place.")

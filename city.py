#!/usr/bin/python3
from random import randint, random
from sys import argv

openended_high = False
openended_low = False
#openended_high = True
#openended_low = True

def D100(n: int = 1, no_open: bool = False) -> int:
    def d100():
        sum = (x := randint(1,100))
        if no_open:
            return sum
        if openended_high:
            while x > 95:
                sum += (x := randint(1,100))
        if openended_low:
            if sum < 6:
                sum -= (x := randint(1,100))
                while x > 95:
                    sum -= (x := randint(1,100))
        return sum
    total = 0
    while n > 0:
        total += d100()
        n -= 1
    return total


def Round(x: float) -> int:
    if x <= 0:
        return 0
    i = int(x)
    return i + (random() <= x - i)


# input from either cmd line param or stdin
if len(argv) > 1:
    population = int(argv[1])
else:
    population = int(input('City population? '))
    print()

accounted_for = 0

# Clear screen ANSI-pako-koodeilla
# Näyttäisi, että jos kummastakaan jättää yhdenkään komennon pois, niin ei
# toimi kunnolla, eli tyhjennä koko bufferia, tms. Vaan parempi kai, kun ei
# räplää näitten kanssa, niin saa sievemmin ohjattua outputit tiedostoon jne.
#print('\x1bc\x1b[3J', end='')            # Tää on vissiin joku ihan Linux-juttu.
#print('\x1b[2J\x1b[3J\x1b[1;1H', end='') # Tää saattaa toimia Windouksessakin, ainakin 11:ssä.

#print('Step 1: Fighters')
print(f"Basic Fighters: {(army     := Round(population / 1000 * (50 + D100()))):6}  [2th to 5th level]")
print(f"NCO's:          {(ncos     := Round(army / 20))                        :6}  [6th to 10th level]") # platoon leaders?
print(f"Junior Officers:{(junioff  := Round(ncos / 5))                         :6}  [8th to 15th level]") # centurions / company commanders?
print(f"Senior Officers:{(senioff  := Round(junioff / 5))                      :6}  [13th to 18th level]")# bataille commanders?
print(f"Generals:       {(generals := Round(senioff / 5))                      :6}  [15th level or more]")
accounted_for += army + ncos + junioff + senioff + generals

print()
#print('Step 2: Monasteries')
stmonks = Round( population / 20000 * D100(2) )
print(f"Monasteries:              {Round(stmonks / 10000 * (50 + D100()))             :5}")
print(f"Student Monks:            {stmonks                                            :5}  [1st to 5th level]")
print(f"    Warrior Monk Students:{(warrmonkst   := Round(0.7 * stmonks))             :5}")
print(f"    Monk Students:        {(monkst       := stmonks - warrmonkst)             :5}")
print(f"Warrior Monks:            {(warrmonks    := Round(warrmonkst / 5))            :5}  [6th to 10th level]")
print(f"Monks:                    {(monks        := Round(monkst / 5))                :5}  [6th to 10th level]")
print(f"Warrior Monk Masters:     {(warrmonkmast := Round(warrmonks / 1000 * D100(2))):5}")  
print(f"Monk Masters:             {(monkmast     := Round(monks / 1000 * D100(2)))    :5}")
accounted_for += stmonks + warrmonks + monks + warrmonkmast + monkmast

print()
#print('Step 3: Churches')
print(f"Clerics:              {(clergy     := Round(population / 15000 * (50 + D100()))):5}")
print(f"Temples:              {(temples    := Round(clergy / 300 * (50 + D100())))      :5}")
shrines = Round(temples / 300 * (50 + D100()))
print(f'   "Regular" Churches:{temples - shrines                                        :5}')
print(f"    Shrines:          {shrines                                                  :5}")
print(f"Temple Squires:       {(squires    := shrines * randint(1,10))                  :5}  [1st to 6th level]")
print(f"Paladins in Residence:{(paladins   := shrines * randint(1,5))                   :5}  [7th level and up]")
print(f"Paladin Errants:      {(paladinerr := shrines * randint(1,5))                   :5}  [7th level and up]")
accounted_for += clergy + squires + paladins + paladinerr

print()
#print('Step 4: Healers')
print(f"Total Healers:         {(healers  := Round(population / 10000 * (50 + D100())))         :5}")
print(f"    Channeling Healers:{(chanheal := Round(0.3 * healers))                              :5}")
print(f"    Lay Healers:       {(layheal  := healers - chanheal)                                :5}")
print(f"Clinics:               {Round(healers / (randint(1,10) + randint(1,10) + randint(1,10))):5}")
accounted_for += healers

print()
#print('Step 5: The Underworld')
print(f"Underworld:     {(underworld := Round(population / 10000 * D100(2)))                      :5}")
print(f"    Nightblades:{(nightbl    := Round(underworld / 100 * (randint(1,10) + randint(1,10)))):5}")
print(f"    Thieves:    {(thieves    := Round((underworld - nightbl) / 100 * D100(no_open=True))) :5}")
print(f"    Rogues:     {underworld - nightbl - thieves                                           :5}")
accounted_for += underworld

print()
#print('Step 6: The Essence Masters')
print(f"Alchemists:  {(alchem := Round(population / 10000 * (50 + D100())))  :5}")
print(f"Magicians:   {(mages  := Round(population / 30000 * D100(2)))        :5}")
print(f"Illusionists:{(illus  := Round(population / 60000 * D100(2)))        :5}")
print(f"Academies:   {Round((alchem + mages + illus) / 10000 * (50 + D100())):5}")
accounted_for += alchem + mages + illus

print()
#print('Step 7: The Theaters')
print(f"Bards:   {(bards    := Round(population / 20000 * D100(2)))           :6}")
print(f"Theaters:{(theaters := Round(bards / (randint(1,10) + randint(1,10)))):6}")
extras = 0
if theaters > 0:
    ext_per_th = [max(0, D100()) for i in range(theaters)]
    extras = sum(ext_per_th)
    if theaters > 12 or theaters == 1:
        print(f"Extras:  {extras:6}")
    else:
        ext_per_th.sort()
        print("Extras: ", end="")
        print(', '.join([str(x) for x in ext_per_th]), end=", respectively\n")
accounted_for += bards + extras

print()
#print('Step 9: The Special Agents')
print(f"Sorcerers:{(sorc := Round(population / 100000 * D100(2))):5}")
print(f"Mystics:  {(myst := Round(population / 100000 * D100(2))):5}")
print(f"Agencies: {Round((myst + sorc) / 800 * (50 + D100()))    :5}")
accounted_for += myst + sorc

print()
#print('Step 10: The Scholars')
print(f"Astrologers:       {(astro := Round(population / 60000 * D100(2))):5}")
print(f"Seers:             {(seers := Round(population / 60000 * D100(2))):5}")
print(f"Halls of Knowledge:{Round((astro + seers) / 2500 * D100(2))       :5}")
accounted_for += astro + seers

print()
#print('Step 11: The Druids')
print(f"Druids:{(druids := Round(population / 100000 * D100(2))):5}")
print(f"Groves:{Round(druids / 1000 * (50 + D100()))            :5}")
accounted_for += druids

print()
#print('Step 8: The Rangers')
print(f"Rangers:   {(rangers := Round(army / 1000 * D100(2))):5}")
accounted_for += rangers

#print()
#print('Step 12: The Animists')
print(f"Animists:  {(anim := Round(population / 60000 * D100(2))):5}")
accounted_for += anim

#print()
#print('Step 13: The Mentalists')
print(f"Mentalists:{(mental := Round(population / 60000 * D100(2))):5}")
accounted_for += mental

#print('\nThe Rest of the Population')
spellcasters = healers + clergy + anim + alchem + mages + illus + sorc + myst + astro + seers + mental + druids
print(f"Archmages: {(arch := Round(spellcasters / 10000 * D100(2))):5}")

print(f"\nNot accounted for above: {population - accounted_for - arch}")
print(f"If there are barbarians, there are {(barb := Round(population / 5000 * D100(2)))} of them.")

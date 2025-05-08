
import random

# Liste möglicher Wörter
woerter=["python", "spiel", "programm", "schule", "computer"]
wort=random.choice(woerter)
erraten=["_"] * len(wort)
versuche=6
benutzte_buchstaben= []
print("Willkommen bei Hangman!")
while versuche > 0 and "_" in erraten:
    print("\nWort:", " ".join(erraten))
    print("Benutzte Buchstaben:", ", ".join(benutzte_buchstaben))
    print("Verbleibende Versuche:", versuche)
    buchstabe = input("Rate einen Buchstaben: ").lower()
    if len(buchstabe) != 1 or not buchstabe.isalpha():
        print("Bitte gib nur einen Buchstaben ein.")
        continue
    if buchstabe in benutzte_buchstaben:
        print("Diesen Buchstaben hast du schon probiert.")
        continue
    benutzte_buchstaben.append(buchstabe)
    if buchstabe in wort:
        for i in range(len(wort)):
            if wort[i] == buchstabe:
                erraten[i] = buchstabe
        print("Richtig!")
    else:
        versuche -= 1
        print("Falsch!")
if "_" not in erraten:
    print("\nGlückwunsch! Du hast das Wort erraten:", wort)
else:
    print("\nLeider verloren. Das Wort war:", wort)
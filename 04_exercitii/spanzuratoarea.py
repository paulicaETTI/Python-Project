cuvant = 'bazaconii'   #o_o___o___ee
cuvant_de_ghicit = list(cuvant)

prima_litera = cuvant[0]
ultima_litera = cuvant[-1]

for i, value in enumerate(cuvant):
    if value != prima_litera and value != ultima_litera:
        cuvant_de_ghicit[i] = '_'

cuvant_de_ghicit = ''.join(cuvant_de_ghicit)    #list to string
print(cuvant_de_ghicit)

vieti =7
litere_incercate = set()

while vieti != 0:

    litera = input("Alege o litera: ")
    cuvant_de_ghicit = list(cuvant_de_ghicit)
    if not litera.isalpha() or len(litera) != 1:
        print("Sunt permise doar litere, cate una!")
        continue
    else:
        if litera in cuvant:
            for index, value in enumerate(cuvant):
                if litera == value:
                    cuvant_de_ghicit[index] = litera
            if '_' not in cuvant_de_ghicit:
                print(f'Ai castigat! Cuvantul era: {cuvant}')
                break

        else:
            if litera not in litere_incercate:
                vieti -= 1
                if vieti == 0:
                    print(f'Ai pierdut! Cuvantul era {cuvant}')
                    break

                print(f'Mai ai {vieti} vieti!')
            litere_incercate.add(litera)

        if len(list(litere_incercate)) != 0:
            print(f"Literele incercate sunt: {', '.join(litere_incercate)}")

        cuvant_de_ghicit = ''.join(cuvant_de_ghicit)
        print(cuvant_de_ghicit, '\n')



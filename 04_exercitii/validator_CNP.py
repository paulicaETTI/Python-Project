cnp = '7031113411839'
valid = True
def e_bisect(an):
    if (an % 400 == 0 or (an % 4 == 0 and an % 100 != 0)):
        return True
    return False

if len(cnp) != 13 or not cnp.isdigit():
    valid = False

s, aa, ll, zz, jj, nnn, c = int(cnp[0]), int(cnp[1:3]), int(cnp[3:5]), int(cnp[5:7]), int(cnp[7:9]), int(cnp[9:12]), int(cnp[12])

if s == 0:
    valid = False

secol = 1900 if s in {1, 2, 7, 8, 9} else 1800 if s in {3, 4} else 2000
an_nastere = secol + aa
#print(f'Data nasterii: {zz}.{ll}.{an_nastere}')

if an_nastere >= 2024:
    valid = False

if ll < 1 or ll > 12:
    valid = False

if zz < 1:
    valid = False

if ll in [1, 3, 5, 7 ,8 ,10 ,12] and zz > 31:
    valid = False

if ll in [4, 6 ,9 , 11] and zz > 30:
    valid = False

if ll == 2 and e_bisect(an_nastere) and zz > 29:
    valid = False
elif ll == 2 and not e_bisect(an_nastere) and zz > 28:
    valid = False

if jj not in range(1, 53):
    valid = False

if nnn == 0:
    valid = False

list_cnp = [int(cifra) for cifra in cnp[:-1]]
control_list = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]

control = 0
for a, b in zip(list_cnp, control_list):
    control += a * b

control = control % 11
if control == 10:
    control = 1

if control != c:
    valid = False

if valid == True:
    print("CNP valid!")
else:
    print("CNP invalid")
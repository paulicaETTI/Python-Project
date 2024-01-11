categorii = {"curs", "cumparaturi", "munca", "cadouri"}
with open("./categorii.txt", "w") as f:
    for categorie in categorii:
        f.write(categorie + "\n")

categorii_citite = []

with open("./categorii.txt", "r") as f:
    for line in f.readlines():
        categorii_citite.append(line.strip())

def delete_line_by_task():
    while True:
        task_to_delete = input("Alege numele taskului de sters: ")
        with open('taskuri.txt', 'r') as file:
            lines = file.readlines()

        # Verificam daca este gasit task ul
        task_gasit = False
        updated_lines = []
        for line in lines:
            if line.strip().split(',')[0] == task_to_delete:
                task_gasit = True
            else:
                updated_lines.append(line)

        # Scriem lista modificata
        with open('taskuri.txt', 'w') as file:
            file.writelines(updated_lines)

        if task_gasit:
            print(f'Task-ul "{task_to_delete}" a fost sters.')
            break
        else:
            print(f'Task-ul "{task_to_delete}" nu a fost gasit.')
            continue

def adauga_taskuri():

    while True:
        gasit = True
        while gasit:
            nume = input('Introdu numele taskului: ')
            with open("./taskuri.txt", "r") as f:
                taskuri_citite = []
                for line in f.readlines():
                    taskuri_citite.append(line.strip())
                for task in taskuri_citite:
                    if nume in task:
                        print("taskul exista deja")
                        break
                    else:
                        gasit = False
        dl = input('Introdu deadlineul: ')
        persoana = input('Introdu omul desemnat: ')

        while True:
            categorie_task = input("Introduceti categoria task-ului: ")
            if categorie_task in categorii_citite:
                break
            else:
                print("Categoria nu exista")

        with open('taskuri.txt', 'a') as file:
            file.write(f'{nume},{dl},{persoana},{categorie_task}\n')

        flag = True
        while True:
            raspuns = input("Doriti sa continuati? Da/Nu: ")
            if raspuns.lower() == "nu":
                flag = False
                break
            elif raspuns.lower() == "da":
                break
            else:
                print("Raspunsul nu este valid")
                continue
        if flag == False:
            break

def filtrare(): # de completat
    criteriu = input('Introdu criteriul de filtrare(task/deadline/om desemnat/categorie):')
    valabil = True
    while valabil:
        if criteriu == "task":
            lista_taskuri = []
            with open("./taskuri.txt", "r") as f:
                f.readlines()
            break
        elif criteriu == "deadline":
            break
        elif criteriu == "om desemnat":
            break
        elif criteriu == "categorie":
            break
        else:
            print("Alege un criteriu valabil!")
            continue

def editare_task(id_ales):
   with open("./taskuri.txt", "r") as f:
       lista_taskuri = []
       for line in f.readlines():
           lista_taskuri.append(line.strip().split(","))


       for i in range(len(lista_taskuri)):
           if i == id_ales:
               print(lista_taskuri[i])
               while True:
                   print("Meniu editare: ")
                   print("1. Editare nume task")
                   print("2. Editare deadline task")
                   print("3. Editare persoana responsabila")
                   print("4. Editare categorie")
                   print("5. Revenire la meniul principal")
                   optiune_editare = input("Introduceti optiunea: ")


                   if optiune_editare == "1":
                       nume_task = input("Introduceti numele task-ului: ")
                       nume_vechi = lista_taskuri[i][0]
                       lista_taskuri[i][0] = nume_task
                       print(f"Task-ul '{nume_vechi}' a fost modificat in '{nume_task}'")
                       break
                   elif optiune_editare == "2":
                       deadline_task = input("Introduceti deadline-ul task-ului: ")
                       deadline_vechi = lista_taskuri[i][1]
                       lista_taskuri[i][1] = deadline_task
                       print(f"Deadline-ul '{deadline_vechi}' a fost modificat in '{deadline_task}'")
                       break
                   elif optiune_editare == "3":
                       persoana_task = input("Introduceti persoana responsabila pentru task: ")
                       persoana_veche = lista_taskuri[i][2]
                       lista_taskuri[i][2] = persoana_task
                       print(f"Persoana responsabila '{persoana_veche}' a fost modificata in '{persoana_task}'")
                       break
                   elif optiune_editare == "4":
                       while True:
                           categorie_task = input("Introduceti categoria task-ului: ")
                           if categorie_task in categorii_citite:
                               categorie_veche = lista_taskuri[i][3]
                               lista_taskuri[i][3] = categorie_task
                               print(f"Categoria '{categorie_veche}' a fost modificata in '{categorie_task}'")
                               break
                           else:
                               print("Categoria nu exista")
                       break
                   elif optiune_editare == "5":
                       break
                   else:
                       print("Optiunea nu este valida")
                       continue


       with open("./taskuri.txt", "w") as file:
           for task in lista_taskuri:
               file.write(f"{task[0]},{task[1]},{task[2]},{task[3]}\n")

def afisare_dupa_categorie():
    with open("./taskuri.txt", "r") as f:
        lista_taskuri = []
        for line in f.readlines():
            lista_taskuri.append(line.strip().split(","))
        lista_taskuri.sort(key=lambda x: x[3])
        for task in lista_taskuri:
            print(task)

def sortare_task(tip_sortare):
   tip_sortare = int(tip_sortare)
   with open("./taskuri.txt", "r") as f:
       lista_taskuri = []
       for line in f.readlines():
           lista_taskuri.append(line.strip().split(","))
       if tip_sortare == 1:
           lista_taskuri.sort(key=lambda x: x[0])
       elif tip_sortare == 0:
           lista_taskuri.sort(key=lambda x: x[0], reverse=True)
       for task in lista_taskuri:
           print(task)


def sortare_deadline(tip_sortare):
   tip_sortare = int(tip_sortare)
   with open("./taskuri.txt", "r") as f:
       lista_taskuri = []
       for line in f.readlines():
           lista_taskuri.append(line.strip().split(","))
       if tip_sortare == 1:
           lista_taskuri.sort(key=lambda x: x[1])
       elif tip_sortare == 0:
           lista_taskuri.sort(key=lambda x: x[1], reverse=True)
       for task in lista_taskuri:
           print(task)


def sortare_persoana(tip_sortare):
   tip_sortare = int(tip_sortare)
   with open("./taskuri.txt", "r") as f:
       lista_taskuri = []
       for line in f.readlines():
           lista_taskuri.append(line.strip().split(","))
       if tip_sortare == 1:
           lista_taskuri.sort(key=lambda x: x[2])
       elif tip_sortare == 0:
           lista_taskuri.sort(key=lambda x: x[2], reverse=True)
       for task in lista_taskuri:
           print(task)


def sortare_taskuri_categoria(tip_sortare):
   tip_sortare = int(tip_sortare)
   with open("./taskuri.txt", "r") as f:
       lista_taskuri = []
       for line in f.readlines():
           lista_taskuri.append(line.strip().split(","))
       if tip_sortare == 1:
           lista_taskuri.sort(key=lambda x: x[3])
       elif tip_sortare == 0:
           lista_taskuri.sort(key=lambda x: x[3], reverse=True)
       for task in lista_taskuri:
           print(task)


adauga_taskuri()
while True:
   print("Meniu: ")
   print("1. Listare date: în afișarea inițială a datelor se realizează o sortare în funcție de categorie.")
   print("2. Sortare: se alege o opțiune din cele 8 de mai jos:")
   print("3. Filtrare date: filtrarea datelor reprezintă de fapt o listare a datelor în funcție de anumite detalii date de la tastatură. criteriile de filtrare sunt:")
   print("4. Adăugare task: se adaugă un nou task.")
   print("5. Editarea detaliilor referitoare la task, dată, persoană sau categorie dintr-un anumit task ales de utilizator de la tastatură (când se cere această opțiune, se va lista lista de taskuri cu un identificator unic pe rand, astfel încât să se știe ce informație urmează să editeze utilizatorul)")
   print("6. Ștergerea unui task din lista inițială.")
   print("7. Ieșire")
   optiune = input("Introduceti optiunea: ")


   if optiune == "1":
       sortare_taskuri_categoria(1)
       continue

   elif optiune == "2":
       print("Meniu sortare: ")
       print("1. sortare ascendentă task")
       print("2. sortare descendentă task")
       print("3. sortare ascendentă deadline")
       print("4. sortare descendentă deadline")
       print("5. sortare ascendentă persoană responsabilă")
       print("6. sortare descendentă persoană responsabilă")
       print("7. sortare ascendentă categorie")
       print("8. sortare descendentă categorie")
       print("9. revenire la meniul principal")
       while True:
           optiune_sortare = input("Introduceti optiunea: ")
           if optiune_sortare == "1":
               sortare_task(1)
               break
           elif optiune_sortare == "2":
               sortare_task(0)
               break
           elif optiune_sortare == "3":
               sortare_deadline(1)
               break
           elif optiune_sortare == "4":
               sortare_deadline(0)
               break
           elif optiune_sortare == "5":
               sortare_persoana(1)
               break
           elif optiune_sortare == "6":
               sortare_persoana(0)
               break
           elif optiune_sortare == "7":
               sortare_taskuri_categoria(1)
               break
           elif optiune_sortare == "8":
               sortare_taskuri_categoria(0)
               break
           elif optiune_sortare == "9":
               break
           else:
               print("Alege optiune valabila!")
               continue


   elif optiune == "3":
       # filtrare
       continue


   elif optiune == "4":
       adauga_taskuri()
       continue



   elif optiune == "5":

       # editare task

       # listare taskuri cu id

       with open("./taskuri.txt", "r") as f:

           lista_taskuri = []

           for line in f.readlines():
               lista_taskuri.append(line.strip().split(","))

           id = 0

           for task in lista_taskuri:
               print(f"{id}. {task}")

               id += 1

       # editare task

       id_ales = input("Introduceti id-ul task-ului pe care doriti sa il editati: ")

       id_ales = int(id_ales)

       editare_task(id_ales)

       continue


   elif optiune == "6":
       delete_line_by_task()
       continue


   elif optiune == "7":
       # iesire
       break
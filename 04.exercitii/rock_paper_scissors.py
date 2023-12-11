import random
def computer_choice():
    choice = random.randint(1, 3)
    if choice == 1:
        return "r", "rock"
    elif choice == 2:
        return "p", "paper"
    else:
        return "s", "scissors"

print("Welcome to rock, paper, scissors!")
print("To quit the game enter 'quit' or enter r/p/s to play VS the computer.\n")

while True:
    score_user = 0
    score_computer = 0
    user_command = input("Enter command: ")
    computer_symbol, computer_name = computer_choice()
    if user_command == "quit":
        break
    elif user_command == 'r':
        print(f"You selected rock!")
        print(f"Computer selected {computer_name}!")
    elif user_command == 'p':
        print(f"You selected paper!")
        print(f"Computer selected {computer_name}!")
    elif user_command == 'r':
        print(f"You selected scissors!")
        print(f"Computer selected {computer_name}!")
    else:
        print("Please select a valid command('quit','r','p','s')")



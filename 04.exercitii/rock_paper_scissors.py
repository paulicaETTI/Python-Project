import random
def outcome(player, computer):
    if player == computer:
        return 0  # Draw
    elif (player == 'r' and computer == 's') or (player == 'p' and computer == 'r') or (player == 's' and computer == 'p'):
        return 1  # Player wins
    else:
        return -1  # Computer wins

def computer_choice():
    choice = random.randint(1, 3)
    if choice == 1:
        return 'r', 'rock'
    elif choice == 2:
        return 'p', 'paper'
    else:
        return 's', 'scissors'

score_player = 0
score_computer = 0

while True:
    player_command = input("Enter command: ")
    computer_command, computer_name = computer_choice()

    if player_command == "quit":
        print(f"Final score is: Player-{score_player}, Computer-{score_computer}")
        break
    elif player_command in ['r', 'p', 's']:
        print(f"You selected {player_command}!")
        print(f"Computer selected {computer_name}!")

        outcome_result = outcome(player_command, computer_command)

        if outcome_result == 0:
            print("It's a draw!")
        elif outcome_result == 1:
            print("You win!")
            score_player += 1
        else:
            print("Computer wins!")
            score_computer += 1

        print(f"Score: Player: {score_player}, Computer: {score_computer}")
    else:
        print("Please select a valid command ('quit', 'r', 'p', 's')")
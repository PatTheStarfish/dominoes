import random


class DominoGame:

    def __init__(self):
        self.dominoes = [[x, y] for x in range(7) for y in range(x, 7)]
        self.stock_pieces = []
        self.computer_pieces = []
        self.player_pieces = []
        self.domino_snake = []
        self.status = None

    def shuffle_dominoes(self):
        while True:
            random.shuffle(self.dominoes)
            self.stock_pieces = [x for x in self.dominoes if self.dominoes.index(x) <= 13]
            self.computer_pieces = [x for x in self.dominoes if 14 <= self.dominoes.index(x) <= 20]
            self.player_pieces = [x for x in self.dominoes if 21 <= self.dominoes.index(x) <= 27]
            for x in range(7):
                if [6 - x, 6 - x] in self.player_pieces:
                    self.player_pieces.remove([6 - x, 6 - x])
                    self.domino_snake.append([6 - x, 6 - x])
                    self.status = "computer"
                    break
                elif [6 - x, 6 - x] in self.computer_pieces:
                    self.computer_pieces.remove([6 - x, 6 - x])
                    self.domino_snake.append([6 - x, 6 - x])
                    self.status = "player"
                    break
            if self.status is not None:
                break

    def print_state(self):
        print(70 * "=")
        print(f"Stock size: {len(self.stock_pieces)}")
        print(f"Computer pieces: {len(self.computer_pieces)}")
        print()
        if len(self.domino_snake) <= 6:
            for x in self.domino_snake:
                print(x, end="")
        else:
            print(f"{self.domino_snake[0]}{self.domino_snake[1]}{self.domino_snake[2]}"
                  f"...{self.domino_snake[-3]}{self.domino_snake[-2]}{self.domino_snake[-1]}")
        print()
        print()
        print("Your pieces:")
        for x in self.player_pieces:
            print(f"{self.player_pieces.index(x) + 1}:{x}")
        print()

    def advance_turn(self):
        if self.status == "player":
            print("Status: It's your turn to make a move. Enter your command.")
            while True:
                player_command = input()
                if len(player_command) == 2 and player_command[1].isdigit() and \
                        player_command[0] == "-" and 0 < int(player_command[1]) <= len(self.player_pieces):
                    if self.check_move(self.player_pieces[int(player_command[1]) - 1], "start"):
                        self.domino_snake.insert(0, self.orient_domino(self.player_pieces[int(player_command[1]) - 1],
                                                                       "start"))
                        self.player_pieces.pop(int(player_command[1]) - 1)
                        self.status = "computer"
                        break
                    else:
                        print("Illegal move. Please try again.")
                elif len(player_command) == 1 and player_command.isdigit() and -len(self.player_pieces)\
                        <= int(player_command) <= len(self.player_pieces):
                    if int(player_command) == 0 and len(self.stock_pieces) > 0:
                        rand = random.randrange(0, len(self.stock_pieces))
                        self.player_pieces.append(self.stock_pieces[rand])
                        self.stock_pieces.pop(rand)
                        self.status = "computer"
                        break
                    elif int(player_command) == 0 and len(self.stock_pieces) == 0:
                        print("Illegal move. Please try again.")
                    elif 0 < int(player_command) <= len(self.player_pieces) and \
                            self.check_move(self.player_pieces[int(player_command) - 1], "end"):
                        self.domino_snake.append(self.orient_domino(self.player_pieces[int(player_command) - 1], "end"))
                        self.player_pieces.pop(int(player_command) - 1)
                        self.status = "computer"
                        break
                else:
                    print("Invalid input. Please try again.")
        elif self.status == "computer":
            self.computer_move()

    def check_win(self):
        temp = [y for x in self.domino_snake for y in x if y == self.domino_snake[0][0]]
        if len(self.player_pieces) == 0:
            self.print_state()
            print("Status: The game is over. You won!")
            exit(0)
        elif len(self.computer_pieces) == 0:
            self.print_state()
            print("Status: The game is over. The computer won!")
            exit(0)
        elif self.domino_snake[0][0] == self.domino_snake[-1][-1] and len(temp) == 8:
            self.print_state()
            print("Status: The game is over. It's a draw!")
            exit(0)

    def play_game(self):
        self.shuffle_dominoes()
        while True:
            self.print_state()
            self.advance_turn()
            self.check_win()

    def check_move(self, domino, position):
        if position == "start" and self.domino_snake[0][0] in domino:
            return True
        elif position == "end" and self.domino_snake[-1][-1] in domino:
            return True
        else:
            if self.status == "player":
                print("Illegal move. Please try again.")
            return False

    def orient_domino(self, domino, position):
        if position == "start" and self.domino_snake[0][0] == domino[1]:
            return domino
        elif position == "end" and self.domino_snake[-1][-1] == domino[0]:
            return domino
        else:
            return domino[::-1]

    def assess_pieces(self):
        temp = self.domino_snake + self.computer_pieces
        temp = [y for x in temp for y in x]
        assessment = [temp.count(x) for x in range(7)]
        rank = [assessment[x[0]] + assessment[x[1]] for x in self.computer_pieces]
        return rank

    def computer_move(self):
        priority_list = self.assess_pieces()
        print("Status: Computer is about to make a move. Press Enter to continue...")
        input()
        while True:
            if any(priority_list):
                choice = priority_list.index(max(priority_list))
                priority_list[choice] = 0
                choice += 1
                choice = random.choice([choice, -choice])
                if choice > 0 and self.check_move(self.computer_pieces[choice - 1], "end"):
                    self.domino_snake.append(self.orient_domino(self.computer_pieces[choice - 1], "end"))
                    self.computer_pieces.pop(choice - 1)
                    self.status = "player"
                    break
                elif choice < 0 and self.check_move(self.computer_pieces[-choice - 1], "start"):
                    self.domino_snake.insert(0, self.orient_domino(self.computer_pieces[-choice - 1], "start"))
                    self.computer_pieces.pop(-choice - 1)
                    self.status = "player"
                    break
                choice = -choice
                if choice > 0 and self.check_move(self.computer_pieces[choice - 1], "end"):
                    self.domino_snake.append(self.orient_domino(self.computer_pieces[choice - 1], "end"))
                    self.computer_pieces.pop(choice - 1)
                    self.status = "player"
                    break
                elif choice < 0 and self.check_move(self.computer_pieces[-choice - 1], "start"):
                    self.domino_snake.insert(0, self.orient_domino(self.computer_pieces[-choice - 1], "start"))
                    self.computer_pieces.pop(-choice - 1)
                    self.status = "player"
                    break
            else:
                if len(self.stock_pieces) > 0:
                    rand = random.randrange(0, len(self.stock_pieces))
                    self.computer_pieces.append(self.stock_pieces[rand])
                    self.stock_pieces.pop(rand)
                    self.status = "player"
                    break


game = DominoGame()
game.play_game()

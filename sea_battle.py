from random import randint


# dot class definition and methods

class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_coordinate_x(self):
        return self.x

    def get_coordinate_y(self):
        return self.y

    def __str__(self):
        return f'(x: {self.x}, y: {self.y})'


# class BoardException(Exception):
#    pass


class Out(Exception):
    def __str__(self):
        return "Out of board range!"


class Used(Exception):
    def __str__(self):
        return "This one was shot before"


class BadShip(Exception):
    pass


class Ship:
    def __init__(self, head, length, orientation):
        self.head = head
        self.length = length
        self.orientation = orientation
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        i = 0
        for i in range(self.length):
            x = self.head.x
            y = self.head.y
            if self.orientation == 0:  # horizontal
                x = x + i
            elif self.orientation == 1:  # vertical
                y = y + i
            ship_dots.append(Dot(x, y))

        return ship_dots

#    def hit(self, shot):
#        return shot in self.dots


class Board:
    def __init__(self, size, hidden=False):
        self.size = size
        self.hidden = hidden
        self.count = 0
        i = 0
        self.matrix = [["_"] * self.size for i in range(self.size)]
#        print(self.matrix)
        self.busy = []
        self.ships = []

    def add_ship(self, ship):

        for dot_ in ship.dots:
            if self.out(dot_) or dot_ in self.busy:
                raise BadShip()
 #       for dot_ in ship.dots:
            self.matrix[dot_.x][dot_.y] = "■"
            self.busy.append(dot_)

        self.ships.append(ship)
        self.canvas(ship)

    def canvas(self, ship, verb=False):
        around_ = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot_ in ship.dots:
            for d_x, d_y in around_:
                can_ = Dot(dot_.x + d_x, dot_.y + d_y)
                if not (self.out(can_)) and can_ not in self.busy:
                    if verb:
                        self.matrix[can_.x][can_.y] = "*"
                    self.busy.append(can_)

    def __str__(self):
        res = " "
        for n in range(self.size):
            res = res + "   " + str(n+1)
        for i, row in enumerate(self.matrix):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hidden:
            res = res.replace("■", "_")
        return res

    def out(self, dot_):
        return not ((0 <= dot_.x < self.size) and (0 <= dot_.y < self.size))

    def shot(self, dot_):
        if self.out(dot_):
            raise Out()

        if dot_ in self.busy:
            raise Used()

        self.busy.append(dot_)

        for ship in self.ships:
            if dot_ in ship.dots:
                ship.lives -= 1
                self.matrix[dot_.x][dot_.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.canvas(ship, verb=True)
                    print("The ship is destroyed")
                    return False
                else:
                    print("The ship was hit!")
                    return True

        self.matrix[dot_.x][dot_.y] = "*"
        print("Missed")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
#                print ("target",  target)
                repeat = self.enemy.shot(target)
                return repeat
            except Exception as e:
                print(e)


class AI(Player):
    def ask(self):
        x, y = randint(0, self.board.size-1), randint(0, self.board.size-1)
        dot_ = Dot(x, y)
        print(f"Computer shoot at: {x + 1} {y + 1}")
        return dot_


class User(Player):
    def ask(self):
        while True:
            str_ = input("Enter two digits, comma separated: ")
            xy = str_.split(',')
            try:
                x, y = int(xy[0]), int(xy[1])
                return Dot(x - 1, y - 1)
            except:
                print("You have to enter two digits, comma in between")

class Game:
    def __init__(self):
        print("-"*50)
        print("  Hello there, welcome to Sea Battle! ")
        print("-"*50)
        size_correct = False
        while size_correct == False:
            try:
                self.size = int(input("Please enter the board side size > 5: "))
                if self.size > 5:
                    size_correct = True
            except:
                pass
        player = self.random_board()
        computer = self.random_board()
        player.hidden = False
        computer.hidden = True
        self.comp = AI(computer, player)
        self.user = User(player, computer)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        ship_set = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for length in ship_set:
            while True:
                attempts += 1
                if attempts > self.size ** 2:
                    return None
                ship = Ship(Dot(randint(0, self.size-1), randint(0, self.size-1)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BadShip:
                    pass
        board.begin()
        return board

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Player board:")
            print(self.user.board)
            print("-" * 20)
            print("Computer board:")
            print(self.comp.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Your move")
                repeat = self.user.move()
            else:
                print("-" * 20)
                print("Computer shot at: ")
                repeat = self.comp.move()
            if repeat:
                num -= 1

            if self.comp.board.count == 7:
                print("-" * 20)
                print("You won!")
                break

            if self.user.board.count == 7:
                print("-" * 20)
                print("You lost!")
                break
            num += 1

    def start(self):
        self.loop()


g = Game()
g.start()

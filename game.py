from player import Player
from hamsters import Hamster

class Game:
    hamsters_count = 3
    happy_message = "WOW! You won!"
    map = """****\n****\n****\n****"""
    gameon = True

    def __init__(self):
        self.player = Player()
        self.hamsters = []
        for i in range(self.hamsters_count):
            self.hamsters.append(Hamster(i+1, self.get_full_map(True)))

    def add_point(self, position, name, s):
        li = s.split("\n")
        row = li[position[1]]
        row = row[:position[0]] + name + row[position[0]+1:]
        li[position[1]] = row
        return "\n".join(li)

    def render_map(self):
        s = self.map
        s = self.add_point(self.player.position, 'x', s)
        for h in self.hamsters:
            if h.health > 0:
                s = self.add_point(h.position, str(h.id), s)
        print(s)

    def move_player(self, destination):
        """ destination = w,a,s,d """
        if destination == 's':          #bottom
            if self.player.position[1] == len(self.map.split('\n'))-1:
                return False
            self.player.position[1] += 1
        if destination == 'w':          #top
            if self.player.position[1] == 0:
                return False
            self.player.position[1] -= 1
        if destination == 'd':          #right
            if self.player.position[0] == len(self.map.split('\n')[0])-1:
                return False
            self.player.position[0] += 1
        if destination == 'a':          #left
            if self.player.position[0] == 0:
                return False
            self.player.position[0] -= 1
        self.on_move(destination)

    def get_hamster_on_position(self, coords):
        s = self.get_full_map()
        return s.split('\n')[coords[1]][coords[0]]

    def get_full_map(self, start_game = False):
        s = self.map
        if start_game:
            s = self.add_point(self.player.position, 'x', s)
        for h in self.hamsters:
            s = self.add_point(h.position, str(h.id), s)
        return s

    directions = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}
    def on_move(self, direction):
        hamster = self.get_hamster_on_position(self.player.position)
        if not hamster == '*':
            self.player.was_hit(int(hamster))
            if self.player.health <= 0:
                self.gameon = False
                print('game over... sorry!')
                return False
            print("player's health: ", self.player.health)
            killed = self.hamsters[int(hamster)-1].on_shot()
            if not killed:
                print('wasnt killed')
                self.move_player(self.directions[direction])
            else:
                print(self.hamsters[int(hamster)-1].id, 'was killed')

    def start(self):
        self.render_map()
        while self.gameon:
            if len([h for h in self.hamsters if h.health > 0]) == 0:
                print(self.happy_message)
                return True
            command = input('Insert command: ')
            if command in ['a', 's', 'w', 'd']:
                self.move_player(command)
                self.render_map()
            if command == 'e':
                self.player.wait()
            if command == 'q':
                self.gameon = False

game = Game()

game.start()
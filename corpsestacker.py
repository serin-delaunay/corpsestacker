
# coding: utf-8
from bearlibterminal import terminal as blt
from vec import vec
from itertools import count, product
from random import randint, choice

class Actor(object):
    def __init__(self):
        self.position = None
        self.is_player = False
        self.character = 'z'

class Game(object):
    def __init__(self):
        blt.open()
        self.width = 10
        self.height = 10
        self.size = vec(10,10)
        blt.set("window:title='Corpse Stacker',size={0}x{1}".format(self.size.x*3, self.size.y))
        blt.set('font: UbuntuMono-R.ttf, size=24')
        self.height_map = self.make_grid(0)
        self.player = Actor()
        self.player.position = self.size//2
        self.player.is_player = True
        self.player.character = '@'
        self.occupants = self.make_grid()
        self.place_actor(self.player)
        self.turn_number = 0
        self.enemies = []
        self.stop = False
        self.restart = False
    def intro(self):
        blt.print_(0,0,
"""Move: WASD/Arrow keys
Attack: WASD/Arrow keys
Rest: Space
Aim: Stack 10 corpses!""")
        blt.refresh()
        blt.read()
    def run(self):
        self.intro()
        while not self.stop:
            self.spawn()
            self.draw()
            self.player_move(self.player)
            if self.calculate_score() >= 10:
                self.win()
            for enemy in self.enemies:
                self.enemy_move(enemy)
            self.turn_number += 1
    def spawn(self):
        spawn_rate = 5-self.calculate_score()
        spawn_count = 0
        while spawn_rate <= 0:
            spawn_rate += 10
            spawn_count += 1
        if randint(1,10) >= spawn_rate:
            spawn_count += 1
        free_spaces = [vec(*xy)
                       for xy in product(range(self.size.x), range(self.size.y))
                       if self.at_edge(vec(*xy))
                       and self.get_grid_item(self.occupants, vec(*xy)) is None]
        for i in range(spawn_count):
            if len(free_spaces) == 0:
                break
            xy = choice(free_spaces)
            free_spaces.remove(xy)
            spawnee = Actor()
            spawnee.position = xy
            self.place_actor(spawnee)
            self.enemies.append(spawnee)
    def at_edge(self, position):
        return position.x in [0,self.size.x-1] or position.y in [0,self.size.y-1]
    def player_move(self, player):
        moved = False
        while not moved:
            kp = blt.read()
            if kp == blt.TK_CLOSE:
                moved = True
                self.stop = True
            elif kp in [blt.TK_UP, blt.TK_W]:
                if self.try_move(self.player, vec(0,-1)):
                    moved = True
            elif kp in [blt.TK_DOWN, blt.TK_S]:
                if self.try_move(self.player, vec(0,1)):
                    moved = True
            elif kp in [blt.TK_LEFT, blt.TK_A]:
                if self.try_move(self.player, vec(-1,0)):
                    moved = True
            elif kp in [blt.TK_RIGHT, blt.TK_D]:
                if self.try_move(self.player, vec(1,0)):
                    moved = True
            elif kp in [blt.TK_SPACE, blt.TK_PERIOD]:
                moved = True
            elif kp == blt.TK_R:
                # disable in normal play
                self.increment_height(self.player.position)
    def enemy_move(self, enemy):
        directions = list(filter(lambda xy: self.check_move(enemy, xy),
                                 [vec(0,-1),vec(0,1),vec(-1,0),vec(1,0)]))
        if directions:
            direction = choice(directions)
            self.try_move(enemy, direction)
    def try_move(self, actor, direction):
        if self.check_move(actor, direction):
            self.move_actor(actor, actor.position + direction)
            return True
        return False
    def check_move(self, actor, direction):
        destination = actor.position + direction
        if destination == actor.position:
            return True
        if not self.in_bounds(destination):
            return False
        height_from = self.get_grid_item(self.height_map, actor.position)
        height_to = self.get_grid_item(self.height_map, destination)
        if height_to > height_from + 1:
            return False
        if height_to < height_from - 3:
            return False
        occupant = self.get_grid_item(self.occupants, destination)
        return occupant is None or occupant.is_player != actor.is_player
    def draw(self):
        blt.clear()
        for height_row, occupant_row, y in zip(self.height_map, self.occupants, count()):
            for height, occupant, x in zip(height_row, occupant_row, count()):
                blt.put(x*3,y,str(height%10))
                blt.put(x*3+1,y,' ' if occupant is None else occupant.character)
        blt.refresh()
    def increment_height(self, position):
        self.set_grid_item(self.height_map, position,
                           self.get_grid_item(self.height_map, position) + 1)
    def calculate_score(self):
        return max(max(row) for row in self.height_map)
    def get_grid_item(self, grid, position):
        return grid[position.y][position.x]
    def set_grid_item(self, grid, position, value):
        grid[position.y][position.x]= value
    def make_grid(self, value=None):
        return [[value for x in range(self.size.x)] for y in range(self.size.y)]
    def displace_actor(self, actor):
        self.set_grid_item(self.occupants, actor.position, None)
    def place_actor(self, actor):
        self.set_grid_item(self.occupants, actor.position, actor)
    def in_bounds(self, position):
        return 0 <= position.x < self.size.x and 0 <= position.y < self.size.y
    def move_actor(self, actor, destination):
        if not self.in_bounds(destination):
            raise RuntimeError("Destination invalid")
        occupant = self.get_grid_item(self.occupants,destination)
        if occupant is not None:
            if occupant.is_player:
                self.lose()
                return
            else:
                self.displace_actor(occupant)
                self.increment_height(occupant.position)
                self.enemies.remove(occupant)
                return
        self.displace_actor(actor)
        actor.position = destination
        self.place_actor(actor)
    def win(self):
        blt.clear()
        blt.set('window:size=60x20')
        blt.set('font: UbuntuMono-R.ttf, size=14')
        blt.print_(0,0,
"""
Suddenly the air fills with applause.
An unseen crowd chants "TEN-STACK, TEN-STACK!"
as a pair of guards leads you out of the arena to freedom.
A bitter freedom, still trapped in a society
with daily trials by combat,
and trapped with the memory of your own trial.

*** Press Escape ***
*** Press R to restart ***
""",
                   blt.state(blt.TK_WIDTH),blt.state(blt.TK_HEIGHT),blt.TK_ALIGN_CENTER)
        blt.refresh()
        while True:
            kp = blt.read()
            if kp == blt.TK_R:
                self.restart = True
            if kp in [blt.TK_CLOSE, blt.TK_ESCAPE, blt.TK_R]:
                break
        blt.close()
        self.stop = True
    def lose(self):
        blt.clear()
        blt.set('window:size=60x20')
        blt.set('font: UbuntuMono-R.ttf, size=14')
        blt.print_(0,0,
"""
A zombie blunders into you
and grasps your arm instinctively.
the smell of blood fills the air after one bite,
and as you black out you can almost
see the rest of the zombies
shambling towards their next meal.

*** Press Escape to exit ***
*** Press R to restart ***
""",
                   blt.state(blt.TK_WIDTH),blt.state(blt.TK_HEIGHT),blt.TK_ALIGN_CENTER)
        blt.refresh()
        while True:
            kp = blt.read()
            if kp == blt.TK_R:
                self.restart = True
            if kp in [blt.TK_CLOSE, blt.TK_ESCAPE, blt.TK_R]:
                break
        blt.close()
        self.stop = True

if __name__ == '__main__':
    while True:
        game = Game()
        game.run()
        if not game.restart:
            break
    blt.close()
    print(game.turn_number)

blt.close()

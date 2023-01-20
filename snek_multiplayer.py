#!/usr/bin/env python3
'''
Coded with <3 and ☕️ and not nearly enough sleep
by Reiddragon
'''
import pyxel
from random import randint


# Global consts so they're easier to change
WIDTH = 64
HEIGHT = 64
SCALE = 5
FRAMERATE = 15
MINIMUM_FOOD = 1  # how many food to have on screen at a minimum


class Snake:
    def __init__(self, x, y, direction, name, colour, controls):
        self.tail = [
            (x, y),
            (x - 1, y),
        ]
        self.direction = direction
        self.name = name
        self.colour = colour
        self.controls = controls
        self.alive = True

    def update(self, food):
        # lotsa ifs to check if any arrow keys are pressed and change the
        # direction the snake is moving while also making sure to not let the
        # snake do a 180 in a single frame, that would be bad
        if self.direction != 'DOWN' and pyxel.btnp(self.controls['UP']):
            self.direction = 'UP'
        elif self.direction != 'UP' and pyxel.btnp(self.controls['DOWN']):
            self.direction = 'DOWN'
        elif self.direction != 'RIGHT' and pyxel.btnp(self.controls['LEFT']):
            self.direction = 'LEFT'
        elif self.direction != 'LEFT' and pyxel.btnp(self.controls['RIGHT']):
            self.direction = 'RIGHT'

        # see which direction the snake is moving and add a new head where it
        # needs to be
        match self.direction:
            case 'UP':
                self.tail.insert(0, (
                    self.tail[0][0],
                    (self.tail[0][1] - 1) % HEIGHT
                ))
            case 'DOWN':
                self.tail.insert(0, (
                    self.tail[0][0],
                    (self.tail[0][1] + 1) % HEIGHT
                ))
            case 'LEFT':
                self.tail.insert(0, (
                    (self.tail[0][0] - 1) % WIDTH,
                    self.tail[0][1]
                ))
            case 'RIGHT':
                self.tail.insert(0, (
                    (self.tail[0][0] + 1) % WIDTH,
                    self.tail[0][1]
                ))
        self.tail.pop()  # then pop the tail

        # finally see if the snek should any the food
        for i in reversed(range(len(food))):
            if self.tail[0] == food[i]:
                # if yes, add a new segment to the snek, and pop the food
                self.tail.insert(1, self.tail[0])
                food.pop(i)

    def draw(self):
        # Draw the snek, this one's fun cuz it uses lambdas cuz I wrote this
        # during a crunch for the functional programming exam
        #
        # tl;dr: draw rectangles that are only 4/5 of the full square, then do
        # a bunch of checks to see where to fill in the gaps so only the
        # segments adjacent in self.tail are visually connected
        pyxel.rect(
            *map(lambda x: x * SCALE, self.tail[0]),
            SCALE - 1, SCALE - 1, self.colour
        )
        for i in range(1, len(self.tail)):
            pyxel.rect(
                *map(lambda x: x * SCALE, self.tail[i]),
                SCALE - 1, SCALE - 1, self.colour
            )

            if self.tail[i][0] < self.tail[i - 1][0]:
                pyxel.line(
                    self.tail[i][0] * SCALE + SCALE - 1,
                    self.tail[i][1] * SCALE,
                    self.tail[i][0] * SCALE + SCALE - 1,
                    self.tail[i][1] * SCALE + SCALE - 2,
                    self.colour
                )
            elif self.tail[i][0] > self.tail[i - 1][0]:
                pyxel.line(
                    self.tail[i][0] * SCALE - 1,
                    self.tail[i][1] * SCALE,
                    self.tail[i][0] * SCALE - 1,
                    self.tail[i][1] * SCALE + SCALE - 2,
                    self.colour
                )
            elif self.tail[i][1] < self.tail[i - 1][1]:
                pyxel.line(
                    self.tail[i][0] * SCALE,
                    self.tail[i][1] * SCALE + SCALE - 1,
                    self.tail[i][0] * SCALE + SCALE - 2,
                    self.tail[i][1] * SCALE + SCALE - 1,
                    self.colour
                )
            elif self.tail[i][1] > self.tail[i - 1][1]:
                pyxel.line(
                    self.tail[i][0] * SCALE,
                    self.tail[i][1] * SCALE - 1,
                    self.tail[i][0] * SCALE + SCALE - 2,
                    self.tail[i][1] * SCALE - 1,
                    self.colour
                )

    def check_colisions(self, other_snakes):
        # colision detection to see if the snek is trying to eat itself
        if self.tail[0] in self.tail[4:]:
            self.die()

        # and to see if the snek pumped into another snek
        for s in other_snakes:
            # complete with a skip for itself
            if self.name == s.name:
                continue

            if self.tail[0] in s.tail:
                self.die()

    def die(self):
        self.alive = False
        print(f'{self.name} died with score {len(self.tail)}')


# And the main Pyxel App() object! Not a lot to say here, some init code, some
# Pyxel boilerplate, and the drawing code for the food cause there's no
# dedicated class to put that code in because there's not enough going on with
# the food to make it worth making a new class for it
class App:
    def __init__(self):
        pyxel.init(
            WIDTH * SCALE, HEIGHT * SCALE,
            fps=FRAMERATE,
            title='Sneky Boi'
        )
        self.s = []
        self.s.append(Snake(
            48, 32,
            'RIGHT', 'Atlas', 12,
            {
                'UP': pyxel.KEY_W,
                'DOWN': pyxel.KEY_S,
                'LEFT': pyxel.KEY_A,
                'RIGHT': pyxel.KEY_D
            }
        ))
        self.s.append(Snake(
            16, 32,
            'RIGHT', 'P-Body', 9,
            {
                'UP': pyxel.KEY_UP,
                'DOWN': pyxel.KEY_DOWN,
                'LEFT': pyxel.KEY_LEFT,
                'RIGHT': pyxel.KEY_RIGHT
            }
        ))
        self.s.append(Snake(
            16, 16,
            'RIGHT', 'GLaDOS', 11,
            {
                'UP': pyxel.KEY_K,
                'DOWN': pyxel.KEY_J,
                'LEFT': pyxel.KEY_H,
                'RIGHT': pyxel.KEY_L
            }
        ))
        self.f = []
        pyxel.run(self.update, self.draw)

    def update(self):
        if len(self.f) < MINIMUM_FOOD:
            self.f.append((
                randint(0, WIDTH - 1),
                randint(0, HEIGHT - 1)
            ))

        for s in self.s:
            s.update(self.f)

        # Split this from the loop above because otherwise you end up with
        # weird situations where 2 snakes bump head to head but only one of
        # them dies
        for s in self.s:
            s.check_colisions(self.s)

        # Clean up any snakes with the .alive parameter set to False after the
        # last loop. Go trough the list in reverse so the indexing doesn't get
        # messed up as I remove from it
        for i in reversed(range(len(self.s))):
            if not self.s[i].alive:
                # First the 20% chance per segment to leave food behind
                for segment in self.s[i].tail:
                    if randint(0, 5) < 2:
                        self.f.append(segment)
                # then delete the snake object from the list
                del self.s[i]

        if not self.s:
            print('All sneks are ded, quitting')
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)

        for s in self.s:
            s.draw()

        for f in self.f:
            pyxel.rect(
                *map(lambda x: x * SCALE, f),
                SCALE - 1, SCALE - 1, 8
            )


if __name__ == '__main__':
    App()

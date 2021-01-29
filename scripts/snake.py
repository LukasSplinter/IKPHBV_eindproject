from pygame.locals import *
from random import randint
import pygame
import time
import os


class Syringe:
    x = 0
    y = 0
    step = 44

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Virus:
    x = 0
    y = 0
    step = 44

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
        self.length = length
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        # initial positions, no collision.
        self.x[1] = 1 * 44
        self.x[2] = 2 * 44

    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # update previous positions
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))


class Game:
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False


class App:
    windowWidth = 1320
    windowHeight = 880
    player = 0
    syringe = 0

    amountOfVirus = 2
    viruses = []

    amountOfSyringe = 3
    syringes = []

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._syringe_surf = None
        self.game = Game()
        self.player = Player(3)
        # self.syringe = Syringe(5, 5)
        # self.virus = Virus(29, 19)

        for virus in range(0, App.amountOfVirus):
            #ranges 0 <-> 29 || 0 ↨ 19
            virus = Virus(randint(0, 29), randint(0, 19))
            App.viruses.append(virus)
        for syringe in range(0, App.amountOfSyringe):
            # ranges 0 <-> 29 || 0 ↨ 19
            syringe = Syringe(randint(0, 29), randint(0, 19))
            App.syringes.append(syringe)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('corona snake')
        self._running = True
        self._syringe_surf = pygame.transform.scale(pygame.image.load(os.getcwd() + "\\images\\syringe.png").convert(), (44,44))
        self._virus_surf = pygame.transform.scale(pygame.image.load(os.getcwd() + "\\images\\corona.png").convert(), (44,44))

        # change parameters to make game more difficult if user isnt wearing mask
        # read from ./ROI file to see if player wears mask
        if len(os.listdir(os.getcwd() + "\\data\\ROI")) < 2:
            # no images saved from maskdetection.py, fall back to default prites
            print("[INFO] No faces in ROI folder found, falling back to default sprites")
            self._image_surf = pygame.image.load(os.getcwd() + "\\images\\snake.png").convert()
        else:
            faceFileName = os.listdir(os.getcwd() + "\\data\\ROI")[1]   #index [1] to avoid using .gitkeep file
            # set face in ROI folder as snake sprite and resize to 44px x 44px

            self._image_surf = pygame.transform.scale(
                pygame.image.load(os.getcwd() + "\\data\\ROI\\" + faceFileName).convert(), (44, 44))

            # see if face in ROI folder is wearing mask
            # if filename contains 'No Mask' > user isnt wearing mask
            if "No Mask" in faceFileName:
                # if wearing no mask > make game harder
                print("No mask")
                self.player.length = 2
                App.viruses = 6
                App.syringes = 1
            else:
                # if wearing mask > make game easier
                print("Mask")
                self.player.length = 4
                App.viruses = 3
                App.syringes = 4

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()

        if self.player.length < 1:
            exit(0)

        # does snake eat syringe?
        for i in range(0, self.player.length):
            for syringe in App.syringes:
                if self.game.isCollision(syringe.x, syringe.y, self.player.x[i], self.player.y[i], 44):
                    syringe.x = randint(1, 29) * 44
                    syringe.y = randint(1, 19) * 44
                    # self.virus.x = randint(1, 29) * 44
                    # self.virus.y = randint(1, 19) * 44
                    self.player.length = self.player.length + 1
        # does snake get corona
        for i in range(0, self.player.length):
            for virus in App.viruses:
                if self.game.isCollision(virus.x, virus.y, self.player.x[i], self.player.y[i], 44):
                    exit(0)

        # does snake collide with itself?
        for i in range(2, self.player.length):
            if self.game.isCollision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], 40):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                exit(0)

        for i in range(2, self.player.length):
            if self.player.x[0] >= self.windowWidth or self.player.x[0] <= -1:
                print("Stinkie Border")
                exit(0)

            if self.player.y[0] >= self.windowHeight or self.player.y[0] <= -1:
                print("Stinkie border")
                exit(0)

        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.player.draw(self._display_surf, self._image_surf)
        # self.syringe.draw(self._display_surf, self._syringe_surf)
        # self.virus.draw(self._display_surf, self._virus_surf)

        for virus in App.viruses:
            virus.draw(self._display_surf, self._virus_surf)
        for syringe in App.syringes:
            syringe.draw(self._display_surf, self._syringe_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.moveRight()

            if (keys[K_LEFT]):
                self.player.moveLeft()

            if (keys[K_UP]):
                self.player.moveUp()

            if (keys[K_DOWN]):
                self.player.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0);
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()

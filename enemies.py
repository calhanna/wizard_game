import pygame, pathfinding
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, matrix):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.matrix = matrix
        self.facing = 'right'

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.end = 0

        self.path = [((self.rect.centerx + 32)/32, (self.rect.centery + 32)/32 )]

    def find_path(self, player):
        self.matrix.cleanup()
        start = (int(self.rect.centerx / 32), int(self.rect.centery / 32))
        start = self.matrix.node(start[0], start[1])

        self.end = (int(player[0] / 32), int(player[1] / 32))
        end = self.matrix.node(self.end[0], self.end[1])

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, self.matrix)

        return path

    def move(self, player):
        try:
            goal = self.path[0]
            goal = (goal[0] * 32, goal[1] * 32)
        except IndexError:
            return pygame.Vector2((0,0))

        move = pygame.Vector2((0,0))

        if self.rect.center == goal:
            self.path = self.find_path(player)
            self.path.remove(self.path[0])
            if len(self.path) > 0:
                goal = self.path[0]
                goal = (goal[0] * 32, goal[1] * 32)
            else:
                return pygame.Vector2((0,0))

        if self.rect.centerx < goal[0]:
            move[0] += 1
            if self.facing == 'right':
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing = 'left'
        elif self.rect.centerx > goal[0]:
            move[0] -= 1
            if self.facing == 'left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing = 'right'
        
        if self.rect.centery < goal[1]:
            move[1] += 1
        elif self.rect.centery > goal[1]:
            move[1] -= 1

        return move

class Wolf(Enemy):
    def __init__(self, x, y, matrix):
        self.image = pygame.image.load('images/wolf/wolf_0.png')
        Enemy.__init__(self, x, y, self.image, matrix)

        self.anim_count = -1
        self.tick = 0

        self.animation = [self.image]
        for i in range(0, 2):
            s = str(i)
            self.animation.append(pygame.image.load('images/wolf/wolf_' + s + '.png'))

    def cycle_anim(self):
        if self.tick >= 15:
            self.anim_count += 1

            if self.anim_count >= 2:
                self.anim_count = -1

            if self.facing == 'left':
                self.image = self.animation[self.anim_count]
            else:
                self.image = pygame.transform.flip(self.animation[self.anim_count], True, False)

            self.tick = 0
        else:
            self.tick += 1
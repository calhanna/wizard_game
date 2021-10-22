import pygame, pathfinding, random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.facing = 'right'

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def find_path(self, goal, matrix):
        start = (int(self.rect.centery/32), int(self.rect.centerx/32))
        end = (int(goal[1]/32), int(goal[0]/32))

        path = pathfinding.astar(matrix, start, end)

        return path

    def move(self):
        move = pygame.Vector2((0,0))

        goal = self.path[1]

        if (int(self.rect.centery / 32), int(self.rect.centerx / 32)) == goal:
            return True
        else:
            if self.rect.centerx < goal[1] * 32: move[0] += 1
            if self.rect.centerx > goal[1] * 32: move[0] -= 1
            if self.rect.centery < goal[0] * 32: move[1] += 1
            if self.rect.centery > goal[0] * 32: move[1] -= 1

            return move

class Wolf(Enemy):
    def __init__(self, x, y):
        #self.image = pygame.image.load('images/wolf/wolf_0.png')
        self.image = pygame.surface.Surface((32,32))
        self.image.fill((255,0,0))
        Enemy.__init__(self, x, y, self.image)

        #self.anim_count = -1
        #self.tick = 0

        #self.animation = [self.image]
        #for i in range(0, 2):
        #    s = str(i)
        #    self.animation.append(pygame.image.load('images/wolf/wolf_' + s + '.png'))

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
import pygame, math

SPEED = 4

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, origin, angle):
        """
            Base Bullet class. Contains movement logic and variable definition
        """

        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.origin = origin                                                    # Tracks whether the bullet came from the player or an enemy
        self.angle = angle

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.image = pygame.transform.rotate(self.image, self.angle)            # Rotate fireball so that it is facing in the correct angle
        if self.angle == 90 or self.angle == 270:                               # Flipping the fireball so it faces the correct direction
            self.image = pygame.transform.flip(self.image, False, True)
        elif self.angle != 0 and self.angle != 180:
            self.image = pygame.transform.flip(self.image, False, True)

    def move(self):
        move = [0,0]                                                            # Movement Vector

        if self.angle % 90 == 0:
            move[1] += int((SPEED * math.sin(math.radians(self.angle))))        #y
            move[0] += int((SPEED * math.cos(math.radians(self.angle))))        #x
        else:
            move[1] += int((SPEED*1.15 * math.sin(math.radians(self.angle))))   # The speed of angled fireballs *felt* wrong, so we increase the speed slightly to create an illusion of equal speed, while the angled fireballs actually move faster.
            move[0] += int((SPEED*1.15 * math.cos(math.radians(self.angle))))

        return move

class Fireball(Bullet):
    def __init__(self, x, y, angle):
        image = pygame.image.load('images/fireball.png')
        Bullet.__init__(self, x, y, image, 'plr', angle)
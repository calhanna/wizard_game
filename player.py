import pygame, math
from pygame import sprite

SPEED = 2

class Player(sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.idle = pygame.image.load('images/wizard/wizard.png')                           # Idle standing sprite
        self.image = self.idle
        self.rect = self.image.get_rect()
        self.rect.center = (320, 320)
        self.facing = 'right'                                                               # Tracks the direction the player is facing so we can make them flip horizontally when it changes

        self.tick = 0                                                                       # Limits the fps of the walk cycle animation
        self.anim_count = 0                                                                 # Current animation frame

        self.animation = []
        for i in range(0, 2):
            s = str(i)
            self.animation.append(pygame.image.load('images/wizard/wizard_' + s + '.png'))  # Animation frames are stored as wizard_[n].png

    def move(self):
        keys = pygame.key.get_pressed()
        move = pygame.Vector2((0,0))
        
        if keys[pygame.K_w]: move[1] -= SPEED
        if keys[pygame.K_a]: move[0] -= SPEED
        if keys[pygame.K_s]: move[1] += SPEED
        if keys[pygame.K_d]: move[0] += SPEED

        if move[0] != 0 and move[1] != 0:                                                   # This section makes it so that the speed that the player 
            move = move.normalize() * SPEED * 1.45                                          # travels *looks* constant regardless of angle.
            move[0] = int(move[0])                                                          # Note that it doesn't at matter if the speed isn't really constant at all
            move[1] = int(move[1])

        if move[0] > 0 and self.facing == 'left':                                           # Make player face right when moving right
            self.facing = 'right'
            self.image = pygame.transform.flip(self.image, True, False)
        elif move[0] < 0 and self.facing == 'right':                                        # Make player face left when moving left
            self.facing = 'left'
            self.image = pygame.transform.flip(self.image, True, False)

        if move[0] != 0 or move[1] != 0:                                                    # Cycle through the 'walking animation'
            self.tick += 1
            if self.tick >= 15:
                self.tick = 0
                self.anim_count = -self.anim_count + 1
                self.image = self.animation[self.anim_count]

                if self.facing != 'right':
                    self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.idle
            if self.facing != 'right':
                self.image = pygame.transform.flip(self.image, True, False)

        return move

    

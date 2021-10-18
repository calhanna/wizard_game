import pygame, pytmx, pathfinding, math
from pathfinding.core.grid import Grid

import projectiles, enemies

from player import Player

pygame.init()

screen = pygame.display.set_mode((640, 640))

tick = 0
clock = pygame.time.Clock()

# Variable Definition
background = pygame.image.load('images/grass_background.png')
all_sprites = pygame.sprite.Group()

player = Player()

fireball_cooldown = 0
max_cooldown = 20

bullets = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()

all_sprites.add(player)

matrix = []
for i in range(20):
    matrix.append([])

def load_level(level):
    level = pytmx.load_pygame('maps/level_' + level + '.tmx')

    y_num = 0
    for x, y, gid in level.get_layer_by_name('Objects'):
        if level.get_tile_image_by_gid(gid) != None:
            matrix[y_num].append(0)
        else:
            matrix[y_num].append(1)
        
        if x == 19: y_num += 1

    return level

level = load_level('1')
grid = Grid(matrix=matrix)

wolf_1 = enemies.Wolf(100, 220, grid)
wolf_2 = enemies.Wolf(100, 420, grid)
all_sprites.add(wolf_1)
all_sprites.add(wolf_2)
all_enemies.add(wolf_1)
all_enemies.add(wolf_2)

def draw():
    screen.blit(background, (0,0))

    #bullets.draw(screen)
    for bullet in bullets:
        if bullet.origin == 'plr':
            if distance(player.rect.center, bullet.rect.center) > 25:
                screen.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

    all_sprites.draw(screen)

    for x, y, gid in level.get_layer_by_name('Objects'):
        image = level.get_tile_image_by_gid(gid)
        if image != None:
            screen.blit(image, (x * level.tilewidth, y * level.tileheight))

    pygame.display.flip()

def handle_event(event):
    if event.type == pygame.QUIT:
        return True

def distance(a, b):
    """
        Returns the distance between points a and b using trigonometry.
    """
    dx = a[0] - b[0]
    dy = a[1] - b[1]

    return math.sqrt(dx*dx + dy*dy)

def fire():
    global fireball_cooldown

    mouse_pos = pygame.mouse.get_pos()
    dx = mouse_pos[0] - player.rect.centerx
    dy = mouse_pos[1] - player.rect.centery
    angle = math.degrees(math.atan2(dy, dx))

    if pygame.mouse.get_pressed()[0]:
        fireball_cooldown += 1

        new_bullet = projectiles.Fireball(player.rect.center[0], player.rect.center[1], angle)
        bullets.add(new_bullet)

done = False
while not done:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        done = handle_event(event)

    if done:
        break
    
    for bullet in bullets.sprites():
        move = bullet.move()
        bullet.rect.x += move[0]
        bullet.rect.y += move[1]

        if not bullet.rect.colliderect(screen.get_rect()):
            bullets.remove(bullet)
    
    for enemy in all_enemies:
        enemy.cycle_anim()

        collide = False
        for enemy_2 in all_enemies:
            if enemy != enemy_2:
                if enemy.rect.move(enemy.move(player.rect.center)).colliderect(enemy_2.rect):
                    collide = True
                    enemy.path = enemy.find_path(player.rect.center)

        if not collide:
            enemy.rect.center += enemy.move(player.rect.center)

        for fireball in bullets:
            if fireball.origin == 'plr':
                if enemy.rect.colliderect(fireball.rect):
                    all_sprites.remove(enemy)
                    all_enemies.remove(enemy)
                    bullets.remove(fireball)
    
    if fireball_cooldown >= max_cooldown:
        fireball_cooldown = 0

    player.rect.center += player.move()

    if fireball_cooldown > 0:
        fireball_cooldown += 1
    else:
        fire()

    draw()

    tick += clock.tick(60)/1000
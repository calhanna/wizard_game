import pygame, pytmx, math, random                  # Premade libraries

import projectiles, enemies, pathfinding            # Additional Files

from player import Player

pygame.init()                                       # Pygame initialisation

screen = pygame.display.set_mode((640, 640))        # Window Creation

tick = 0                                            # Runtime tracker
clock = pygame.time.Clock()

# Variable Definition
background = pygame.image.load('images/grass_background.png')
all_sprites = pygame.sprite.Group()                 # Main sprite group. Handles drawing of everything except bullets.

player = Player()

fireball_cooldown = 0                               # Limits the speed at which the player can cast fireball. Incremented every tick.
max_cooldown = 30                                   # The threshold of fireball_cooldown after which another fireball can be cast

bullets = pygame.sprite.Group()                     # Handles drawing of bullets below other sprites
all_enemies = pygame.sprite.Group()                 # Handles enemy behavior

all_sprites.add(player)

matrix = []                                         # Generates map as 1s and 0s - 1 representing obstacles and 0 representing empty space
for i in range(20):
    matrix.append([])

def load_level(level):
    """ Loading Tiledmap with pytmx """

    global spawn_boxes

    level = pytmx.load_pygame('maps/level_' + level + '.tmx')

    y_num = 0
    for x, y, gid in level.get_layer_by_name('Objects'):
        if level.get_tile_image_by_gid(gid) != None:
            matrix[y_num].append(1)
        else:
            matrix[y_num].append(0)
        
        if x == 19: y_num += 1

    spawn_boxes = []                                                # Areas in which enemies can spawn. Requires tiled type 'spawn_box'
    for obj in level.get_layer_by_name('Triggers'):
        if obj.type == 'spawn_box':
            rect = pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height)
            if obj.name == 'north': 
                rect = rect.move(0, -64)
                rect.height += 64
            if obj.name == 'east': 
                rect = rect.move(64, 0)
                rect.width += 64
            if obj.name == 'south': 
                rect = rect.move(0, 64)
                rect.height += 64
            if obj.name == 'west': 
                rect = rect.move(-64, 0)
                rect.width += 64
            spawn_boxes.append(rect)

    return level

level = load_level('1')

def draw():
    screen.blit(background, (0,0))

    #bullets.draw(screen)
    for bullet in bullets:
        if bullet.origin == 'plr':
            if distance(player.rect.center, bullet.rect.center) > 25:
                screen.blit(bullet.image, (bullet.rect.x, bullet.rect.y))

    all_sprites.draw(screen)

    for x, y, gid in level.get_layer_by_name('Objects'):                        # Handles drawing of tile images.
        image = level.get_tile_image_by_gid(gid)                                # Retrieves the image of a tile using it's 'gid'. IDK what a gid is tho.
        if image != None:
            screen.blit(image, (x * level.tilewidth, y * level.tileheight))

    pygame.display.flip()                                                       # Refresh display

def handle_event(event):
    """ Returns True if the game has been closed. """
    if event.type == pygame.QUIT:
        return True

def distance(a, b):
    """
        Returns the distance between points a and b using trigonometry.
    """
    dx = a[0] - b[0]
    dy = a[1] - b[1]

    return math.sqrt(dx*dx + dy*dy)

def fire_mouse():
    """ Firing function that uses the mouse rather than the arrow keys. """

    global fireball_cooldown

    mouse_pos = pygame.mouse.get_pos()
    dx = mouse_pos[0] - player.rect.centerx
    dy = mouse_pos[1] - player.rect.centery
    angle = math.degrees(math.atan2(dy, dx))

    if pygame.mouse.get_pressed()[0]:
        fireball_cooldown += 1

        new_bullet = projectiles.Fireball(player.rect.center[0], player.rect.center[1], angle)
        bullets.add(new_bullet)

def fire_arrows():
    """ Firing function that uses the arrow keys rather than the mouse. """

    global fireball_cooldown

    angle = None
    if keys[pygame.K_UP]: 
        angle = 270
        if keys[pygame.K_LEFT]: angle = 225
        elif keys[pygame.K_RIGHT]: angle = 315
    elif keys[pygame.K_DOWN]: 
        angle = 90
        if keys[pygame.K_LEFT]: angle = 135
        elif keys[pygame.K_RIGHT]: angle = 45
    elif keys[pygame.K_LEFT]: angle = 180
    elif keys[pygame.K_RIGHT]: angle = 0


    if angle != None:
        fireball_cooldown += 1

        new_bullet = projectiles.Fireball(player.rect.center[0], player.rect.center[1], angle)
        bullets.add(new_bullet)

def spawn_enemies():
    """ Spawns a random amount of enemies from a random spawning box. Currently non-functional due to rewrite"""

    enemy_num = random.randint(1,5)
    spawn_box = spawn_boxes[random.randint(0, 3)]

    if spawn_box.y <= 0: start = [0, 128]
    elif spawn_box.y >= 640: start = [0, -128]
    elif spawn_box.x <= 0: start = [128, 0]
    elif spawn_box.x >= 640: start = [-128, 0]

    x = spawn_box.x
    y = spawn_box.y
    new_enemies = []
    for i in range(enemy_num):
        new_enemies.append(enemies.Wolf(x + 32, y + 32, grid, (x + 32 + start[0], y + 32 + start[1])))
        x += 64
        if not spawn_box.collidepoint(x, y):
            x = spawn_box.x
            y += 64

    all_enemies.add(new_enemies)
    all_sprites.add(new_enemies)

done = False
while not done:
    keys = pygame.key.get_pressed()                     # Retrieves all currently pressed keys as dict
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
        move = enemy.move()

        if move == True:                                             
            matrix[enemy.path[0][0]][enemy.path[0][1]] = 0              # Resets the current and next (i.e the one the enemy has just reached) point in the path on the matrix
            matrix[enemy.path[1][0]][enemy.path[1][1]] = 0
            enemy.path = enemy.find_path(player.rect.center, matrix)
            matrix[enemy.path[0][0]][enemy.path[0][1]] = 1              # Sets the current and next point in the path to obstacles on the matrix so enemies avoid each other
            matrix[enemy.path[1][0]][enemy.path[1][1]] = 1
        else:
            enemy.rect.center += move

        for fireball in bullets:                                        # Destroying enemies
            if fireball.origin == 'plr':
                if enemy.rect.colliderect(fireball.rect):
                    all_sprites.remove(enemy)
                    all_enemies.remove(enemy)
                    bullets.remove(fireball)
    
    if fireball_cooldown >= max_cooldown:
        fireball_cooldown = 0

    #if random.randint(1,100) == 69 and len(all_enemies.sprites()) < 10:
    #    spawn_enemies()

    player.rect.center += player.move()

    if fireball_cooldown > 0:
        fireball_cooldown += 1                                          # Increment cooldown until it hits max_cooldown
    else:
        fire_arrows()

    draw()

    tick += clock.tick(60)/1000                                         # Increment tick every second
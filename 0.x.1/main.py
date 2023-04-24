import pygame
import math
import random

shipstats={
    'ShipA':{
        'imagepath':{
            'still':'ShipA1.png',
            'active':'ShipA2.png'
        },
        'Power':3,
        'Max_speed':5,
        'Rotational_power':2,
        'Weight':2000
    }
}

asteroiddata={
    'C Ice S':{
        'imagepath':{
            'nums':1,
            1:'ACI1.png'
        },
        'health' : 30
    }
}

laserdata={
    'MininglaserA' : {
        'bullets' : {
            'speed' : 10,
            'imagepath' : 'laser.png',
            'type':'mining',
            'damage':5
        },
        'cooldown' : 1,
        'range' : 500
    }
}

class Key:
    def __init__(self):
        self.w = False
        self.a = False
        self.s = False
        self.d = False
        self.up = False
        self.left = False
        self.down = False
        self.right = False
        self.space = False
        
    def get_keys(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.w = True
                elif event.key == pygame.K_a:
                    self.a = True
                elif event.key == pygame.K_s:
                    self.s = True
                elif event.key == pygame.K_d:
                    self.d = True
                elif event.key == pygame.K_UP:
                    self.up = True
                elif event.key == pygame.K_LEFT:
                    self.left = True
                elif event.key == pygame.K_DOWN:
                    self.down = True
                elif event.key == pygame.K_RIGHT:
                    self.right = True
                elif event.key == pygame.K_SPACE:
                    self.space = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.w = False
                elif event.key == pygame.K_a:
                    self.a = False
                elif event.key == pygame.K_s:
                    self.s = False
                elif event.key == pygame.K_d:
                    self.d = False
                elif event.key == pygame.K_UP:
                    self.up = False
                elif event.key == pygame.K_LEFT:
                    self.left = False
                elif event.key == pygame.K_DOWN:
                    self.down = False
                elif event.key == pygame.K_RIGHT:
                    self.right = False
                elif event.key == pygame.K_SPACE:
                    self.space = False

class loop:
    def out(self, key, myship, screen_width, screen_height, asteroids):
        # Draw black background
        shooting = False
        screen.fill((0, 0, 0))
        if key.w:
            myship.thrust()
        if key.a:
            myship.rotate_left()
        if key.d:
            myship.rotate_right()
        if key.space:
            shooting = True
        coordinates = f"({int(myship.x)}, {int(myship.y)}, {myship.speed})"
        print(coordinates)
        view_x = myship.x - screen_width/2
        view_y = myship.y - screen_height/2
        myship.update(screen, view_x, view_y, shooting)
        self.check_collisions(asteroids)
        myship.draw(screen, view_x, view_y)
        for asteroid in asteroids:
            if asteroid.health <= 0:
                asteroids.remove(asteroid)
            else:
                asteroid.draw(screen, view_x, view_y)
        scaled_screen = pygame.transform.scale(screen, (screen_width * scale, screen_height * scale))
        
    def check_collisions(asteroids):
        for bullet in myship.weapon[0].bullets:
            for asteroid in asteroids:
                if (asteroid.rect).colliderect(bullet.rect):
                    asteroid.hit(bullet.damage)
                    myship.weapon[0].bullets.remove(bullet)
                    break
                    
        for bullet in myship.weapon[1].bullets:
            for asteroid in asteroids:
                if bullet.rect.colliderect(asteroid.rect):
                    asteroid.hit(bullet.damage)
                    myship.weapon[1].bullets.remove(bullet)
                    break

class ship(pygame.sprite.Sprite):
    def __init__(self, shipstats, scale, x, y, laserdata):
        super().__init__()
        
        self.st = shipstats
        
        #Ladda sprites
        self.image1 = pygame.image.load(self.st['imagepath']['still'])
        self.image2 = pygame.image.load(self.st['imagepath']['active'])
        self.width, self.height = self.image1.get_size()
        
        #Skala sprite
        self.image1 = pygame.transform.scale(self.image1, (self.width * scale, self.height * scale))
        self.image2 = pygame.transform.scale(self.image2, (self.width * scale, self.height * scale))

        #Initiella variabler
        self.x, self.y = x, y
        self.angle = 0
        self.speed = 0
        self.thrustactive = False
        
        #Gör bildväxling möjlig
        self.usedimage = 'still'
        self.rotated = False
        
        #Initiera vapen
        self.weapon = []
        self.weapon.append(laser(laserdata['MininglaserA'], 2, scale))
        self.weapon.append(laser(laserdata['MininglaserA'], -2, scale))
        
        #Hitta mittpinkt
        self.rect = self.image1.get_rect()

    def thrust(self):
        if self.speed < self.st['Max_speed']:
            self.speed += self.st['Power'] / ( self.st['Weight'] / 100 )
            if self.speed > self.st['Max_speed']:
                self.speed = self.st['Max_speed']
        if self.usedimage != 'active':
            self.image = pygame.image.load(self.st['imagepath']['active'])
            self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
        self.thrustactive = True

    def slow(self):
        if self.speed > 0.5:
            self.speed -= 0.5
        else:
            self.speed = 0
        if self.usedimage != 'still':
            self.image = pygame.image.load(self.st['imagepath']['still'])
            self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))

    def rotate_left(self):
        self.angle -= self.st['Rotational_power']
        self.angle %= 360
        self.rotated = True

    def rotate_right(self):
        self.angle += self.st['Rotational_power']
        self.angle %= 360
        self.rotated = True

    def update(self, surface, view_x, view_y, shooting):
        if self.speed != 0:
            self.x += math.sin(math.radians(self.angle)) * self.speed
            self.y -= math.cos(math.radians(self.angle)) * self.speed
        if not self.thrustactive:
            self.slow()
        for laser in self.weapon:
            if shooting:
                laser.shoot(self.angle, self.x, self.y)
            laser.update(surface, view_x, view_y)
        self.thrustactive = False
        self.rotated = False
        
    def draw(self, surface, view_x, view_y):
        # Rotate sprite
        if self.usedimage == 'still':
            rotated_image = pygame.transform.rotate(self.image1, - self.angle)
        else:
            rotated_image = pygame.transform.rotate(self.image2, - self.angle)
        
        # Get the rect object for the rotated image and calculate the center coordinates
        
        surface.blit(rotated_image, (self.x - view_x, self.y - view_y))
        self.rect = rotated_image.get_rect()

class asteroid(pygame.sprite.Sprite):
    def __init__(self, asteroiddata, scale, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.data = asteroiddata
        
        self.imagepath = self.data['imagepath'][random.randint(1,self.data['imagepath']['nums'])]
        self.image = pygame.image.load(self.imagepath)
        self.width, self.height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
        
        self.collideradius = 4
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.health = self.data['health']
    
    def hit(self, damage):
        self.health -= damage
        
    def draw(self, surface, view_x, view_y):
        surface.blit(self.image, (self.x - view_x, self.y - view_y))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class laser:
    def __init__(self, data, offset, scale):
        self.data = data
        self.offset = offset
        
        self.bullets = []
        self.lastshot = 0
        
        self.scale = scale
        
    def shoot(self, direction, x, y):
        if self.lastshot + ( 1000 * self.data['cooldown'] ) < pygame.time.get_ticks():
            shotbullet = lasershot(self.data['bullets'], direction, x, y, self.scale)
            self.bullets.append(shotbullet)
            self.lastshot = pygame.time.get_ticks()
            
    def update(self, surface, view_x, view_y):
        for lasershot in self.bullets:
            lasershot.update()
            lasershot.draw(surface, view_x, view_y)
            if lasershot.distance >= self.data['range']:
                self.bullets.remove(lasershot)
                
class lasershot(pygame.sprite.Sprite):
    def __init__(self, data, direction, x, y, scale):
        self.data = data
        self.angle = direction
        self.x = x
        self.y = y
        self.speed = data['speed']
        self.distance = 0
        self.image = pygame.image.load(self.data['imagepath'])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.damage = self.data['damage']
        
        self.angle %= 360
        self.width, self.height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
        
        self.rotated_image = pygame.transform.rotate(self.image, - self.angle)
    def update(self):
        self.x += math.sin(math.radians(self.angle)) * self.speed
        self.y -= math.cos(math.radians(self.angle)) * self.speed
        self.distance += self.speed
    
    def draw(self, surface, view_x, view_y):
        surface.blit(self.rotated_image, (self.x - view_x, self.y - view_y))
        self.rect = self.rotated_image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
scale = int(input('Scale? '))
clock = pygame.time.Clock()

#Initialise pygame
pygame.init()
screen_width = 1200
screen_height = 600
window_size = (1200, 600)
screen = pygame.display.set_mode(window_size)

shooting = False

key = Key()

running = True

myship = ship( shipstats['ShipA'], scale, 0, 0, laserdata )

asteroids = []
asteroids.append(asteroid( asteroiddata['C Ice S'], scale, 100, 100))

displayinfo = pygame.display.Info

while running:
    events = pygame.event.get() # Get all events since last loop
    for event in events:
        if event.type == pygame.QUIT:
            # User clicked the close button
            pygame.quit()
            running = False
    displayinfo = pygame.display.Info()
    screen_width=displayinfo.current_w
    screen_height=displayinfo.current_h
    key.get_keys(events)
    loop.out(loop, key, myship, screen_width, screen_height, asteroids)
    pygame.display.flip()
    print (screen_height, screen_width)
    clock.tick(60)
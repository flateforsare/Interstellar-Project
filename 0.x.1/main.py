import pygame
import math
import random

shipstats={
	'ShipA':{
		'imagepath':{
			'still':'ShipB1.png',
			'active':'ShipB1.png'
		},
		'Power':1,
		'Max_speed':6,
		'Rotational_power':2,
		'Weight':5,
		'Maxcargo' : 
	}
}

asteroiddata={
	'C Ice S':{
		'imagepath':{
			'nums':1,
			1:'ACI1.png'
		},
		'health' : 30,
		'Resources' : [
			{
			'type' : 'carbon',
			'amount' : (40,80)},
			{
			'type' : 'water',
			'amount' : (40,80)}
		]
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
		'cooldown' : 0,
		'range' : 500
	}
}

stationdata={
	'sales_curve' : 2,
	'speed_curve' : 2,
	'cargo_in' : {
		'water' : 1000,
		'carbon': 500
	},
	'cargo_out' : {
		'grains' : 500
		'organic produce' : 100
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
		self.esc = False
		self.ent = False
		
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
				elif event.key == pygame.K_ESCAPE:
					self.esc = True
				elif event.key == pygame.K_RETURN:
					self.ent = True
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
				elif event.key == pygame.K_RETURN:
					self.ent = False

class loop:
	def out(self, key, myship, screen_width, screen_height, asteroids):
		mystation.menub = False
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
		self.check_collisions(asteroids, cargo)
		myship.draw(screen, view_x, view_y)
		myship.draw_hud(screen)
		for asteroid in asteroids:
			if asteroid.health <= 0:
				asteroids.remove(asteroid)
			else:
				asteroid.draw(screen, view_x, view_y)
		for resource in cargo:
			resource.draw(screen, view_x, view_y)
		mystation.draw(screen, view_x, view_y)
		if mystation.menub:
			print('COLLISION')
			mystation.menuloop(key, myship, screen_width, screen_height)
		#scaled_screen = pygame.transform.scale(screen, (screen_width * scale, screen_height * scale))
	
	def check_collisions(asteroids, cargo):
		print('check')
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
					
		for resource in cargo:
			if resource.rect.colliderect(myship.rect):
				print('cargo collision')
				myship.collectcargo(resource.resource, resource.amount)
				cargo.remove(resource)
				break
				
		if mystation.rect.colliderect(myship.rect):
			print('station collision')
			mystation.menub = True

class ship(pygame.sprite.Sprite):
	def __init__(self, shipstats, scale, x, y, laserdata):
		super().__init__()
		
		self.st = shipstats
		self.cargo = {
			'carbon' : 0,
			'water' : 0
		}
		
		#Ladda sprites
		self.image1 = pygame.image.load(self.st['imagepath']['still'])
		self.image2 = pygame.image.load(self.st['imagepath']['active'])
		self.width, self.height = self.image1.get_size()
		self.money = 0
		
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
			self.speed += self.st['Power'] / ( self.st['Weight'] * 10 )
			if self.speed > self.st['Max_speed']:
				self.speed = self.st['Max_speed']
		if self.usedimage != 'active':
			self.image = pygame.image.load(self.st['imagepath']['active'])
			self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
		self.thrustactive = True

	def slow(self):
		if self.speed > 0.5:
			self.speed -= 0.2
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
		
		if self.usedimage == 'still':
			self.rect = self.image1.get_rect()
		else:
			self.rect = self.image2.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
		
	def draw(self, surface, view_x, view_y):
		# Rotate sprite
		if self.usedimage == 'still':
			rotated_image = pygame.transform.rotate(self.image1, - self.angle)
		else:
			rotated_image = pygame.transform.rotate(self.image2, - self.angle)
		
		# Get the rect object for the rotated image and calculate the center coordinates
		
		surface.blit(rotated_image, (self.x - view_x, self.y - view_y))
		self.rect = rotated_image.get_rect()
		
	def collectcargo(self, cargotype, amount):
		if cargotype in self.cargo:
			self.cargo[cargotype] += amount
		else:
			self.cargo[cargotype] = amount
		
	def draw_hud(self, surface):
		text = font.render(f"Speed: {int(self.speed*10)}", True, (255, 255, 255))
		screen.blit(text, (10, 10))
		text = font.render(f"x: {int(self.x)}, y: {int(self.y)}", True, (255, 255, 255))
		screen.blit(text, (10, 30))
		text = font.render(f"Money: {self.money}", True, (255,255,255))
		screen.blit(text, (10, 50))
		text = font.render(f"Cargo: {self.cargo}", True, (255,255,255))
		screen.blit(text, (10, 70))

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
		
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
		self.health = self.data['health']
		self.max_health = self.health
	
	def hit(self, damage):
		self.health -= damage
		if self.health <= 0:
			for resource in self.data['Resources']:
				cargo.append(resources(resource['type'], random.randint(resource['amount'][0], resource['amount'][1]), self.x, self.y))
		
	def draw_health_bar(self, surface, view_x, view_y):
		BAR_LENGTH = 30
		BAR_HEIGHT = 4
		fill = (self.health / self.max_health) * BAR_LENGTH
		border_rect = pygame.Rect(self.x - view_x - BAR_LENGTH // 2, self.y - view_y + self.height // 2 + 4, BAR_LENGTH, BAR_HEIGHT)
		fill_rect = pygame.Rect(self.x - view_x - BAR_LENGTH // 2, self.y - view_y + self.height // 2 + 4, fill, BAR_HEIGHT)
		pygame.draw.rect(surface, (255, 255, 255), border_rect, 1)
		pygame.draw.rect(surface, (255, 255, 255), fill_rect)
		
	def draw(self, surface, view_x, view_y):
		surface.blit(self.image, (self.x - view_x, self.y - view_y))
		self.draw_health_bar(surface, view_x - 4, view_y - 16)
		#self.rect = self.image.get_rect()
		#self.rect.x = self.x
		#self.rect.y = self.y

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
		
class resources(pygame.sprite.Sprite):
	def __init__(self, resource, amount, x, y):
		super().__init__
		self.resource = resource
		self.amount = amount
		self.x = x
		self.y = y
		
		self.image = pygame.transform.scale(pygame.image.load('Resource.png'), (32, 32))
		
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
	
	def draw(self, surface, view_x, view_y):
		surface.blit(self.image, (self.x - view_x, self.y - view_y))
		
class station(pygame.sprite.Sprite):
	def __init__(self, stationdata, x, y):
		super().__init__
		self.cargolist = {
			'carbon' : 0,
			'water' : 0
		}
		self.data = stationdata
		self.x = x
		self.y = y
		
		buylist = {}
		sellist = {}
		cargo = {}
		self.money = 3000
		
		self.image = pygame.transform.scale(pygame.image.load('FarmstationA1.png'), (64, 64))
		
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
		
		self.menub = False
		
		self.cm = [0]
		
		
	
	def menuloop(self, key, myship, screen_width, screen_height):
		self.get_prices()
		b = ["Sell Cargo", "Change Ship"]
		menu_surface.fill((200,200,200))
		print(self.cm)
		if len(self.cm) == 1:
			options = ["Sell Cargo", "Change ship"]
			i = 0
			texpos = (16,16)
			for option in options:
				if option == options[self.cm[0]]:
					text = font.render(option, True, (255, 255, 255))
					menu_surface.blit(text, (texpos[0],texpos[1]*(i+1)))
				else:
					text = font.render(option, True, (0, 0, 0))
					menu_surface.blit(text, (texpos[0],texpos[1]*(i+1)))
				i+=1
			if key.ent:
				self.cm.append(0)
			elif key.down:
				self.cm[0] += 1
				self.cm[0] %= len(options)
				
		#SÄLJ
		elif self.cm[0] == 0 and len(self.cm) == 2:
			options = list(self.data['cargo_in'].keys())
			i = 0
			texpos = (16,16)
			for option in options:
				if option == options[self.cm[1]]:
					text = font.render(f"  {option} ({self.cargolist[option]}) for {self.pricelist[option]}", True, (255, 255, 255))
					menu_surface.blit(text, (texpos[0],texpos[1]*(i+1)))
					if key.ent:
						self.cm.append(option)
						self.cm.append(0)
						break
				else:
					text = font.render(f"  {option} ({self.cargolist[option]}) for {self.pricelist[option]}", True, (0, 0, 0))
					menu_surface.blit(text, (texpos[0],texpos[1]*(i+1)))
				i+=1
				print(self.cm)
			if key.down:
				self.cm[1] += 1
				self.cm[1] %= len(options)
				
		elif self.cm[0] == 0 and len(self.cm) == 4:
			options = [f"Sell all (for)", 'Sell amount']
			i = 0
			texpos = (16,16)
			for option in options:
				if option == options[self.cm[3]]:
					text = font.render(option, True, (255, 255, 255))
					menu_surface.blit(text, (texpos[0],texpos[1]*(i+1)))
				else:
					text = font.render(option, True, (0, 0, 0))
					menu_surface.blit(text, (texpos[0],texpos[1]*(i+1)))
				i+=1
			if key.ent:
				option = self.cm[2]
				self.sellcargo(option, myship.cargo[option])
				myship.money += myship.cargo[option] * self.pricelist[option]
				myship.cargo[option] = 0
			if key.down:
				self.cm[3] += 1
				self.cm[3] %= len(options)
			
				
		if key.left and len(self.cm) > 1:
			self.cm.pop()
				
		screen.blit(menu_surface, menu_surface_rect)
		#while True:
		#	for event in pygame.event.get():
		#		if event.type == pygame.QUIT:
		#			pygame.quit(b)
		#			return
		#		if event.type == pygame.KEYDOWN:
		#			if event.key == pygame.K_UP:
		#				current_item = (current_item - 1) % len(b)
		#			elif event.key == pygame.K_DOWN:
		#				current_item = (current_item + 1) % len(b)
		#			elif event.key == pygame.K_RETURN:
		#				if current_item == 0:
		#					print("Leaving the station...")
		#					myship.x += 100
		#					return
		#				elif current_item == 1:
		#					b2 = ['Back', 'Sell all']
		#					while True:
		#						key.get_keys
		#						if key.up:
		#							current_item = (current_item - 1) % len(b)
		#						elif event.key == pygame.K_DOWN:
		#							current_item = (current_item + 1) % len(b)
		#						elif event.key == pygame.K_RETURN:
		#							if current_item == 0:
		#								print("Going back")
		#								return
		#							elif current_item == 1:
		#								b2 = ['Back', 'Sell all']
		#								while True:
		#									
		#							elif current_item == 2:
		#								print("You chose option 3")
		#								# Add code for option 3 here
		#				elif current_item == 2:
		#					print("You chose option 3")
		#					# Add code for option 3 here
		#	
		#	screen.fill((255, 255, 255))
		#	for i, item in enumerate(b):
		#		color = (0, 0, 255) if i == current_item else (0, 0, 0)
		#		text = font.render(item, True, color)
		#		text_rect = text.get_rect(center=(screen.get_width()/2, #(i+1)*50))
		#		screen.blit(text, text_rect)
		#	pygame.display.flip()
		#	clock.tick(60)
	
	def get_prices(self):
		self.pricelist = {
			'carbon' : 5,
			'water' : 8
		}
	def sellcargo(self, cargo, amount):
		self.money -= self.pricelist[cargo] * amount
		self.cargolist[cargo] += amount
		
	def update(self):	
		
	def draw(self, surface, view_x, view_y):
		surface.blit(self.image, (self.x - view_x, self.y - view_y))
	
scale = 2
clock = pygame.time.Clock()

#Initialise pygame
pygame.init()

shooting = False

key = Key()

running = True

myship = ship( shipstats['ShipA'], scale, 200, 200, laserdata )
mystation = station(stationdata, 0, 0)

asteroids = []
for i in range(30):
	asteroids.append(asteroid( asteroiddata['C Ice S'], scale, random.randint(-2000, 2000), random.randint(-2000, 2000)))
cargo = []

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

menu_surface = pygame.Surface((600,400))
menu_x = (screen_width - menu_surface.get_width()) // 2
menu_y = (screen_height - menu_surface.get_height()) // 2

menu_surface_rect = menu_surface.get_rect()
menu_surface_rect.x = menu_x
menu_surface_rect.y = menu_y

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 16)

# Set up the display with the FULLSCREEN flag
scaled_screen = pygame.transform.scale(screen, (screen_width * scale, screen_height * scale))
it = 0

while running:
	events = pygame.event.get() # Get all events since last loop
	for event in events:
		if event.type == pygame.QUIT:
			# User clicked the close button
			pygame.quit()
			running = False
	if key.esc:
		running = False
	it += 1
	if it <= 60:
		displayinfo = pygame.display.Info()
		screen_width=displayinfo.current_w
		screen_height=displayinfo.current_h
		it = 0
	key.get_keys(events)
	loop.out(loop, key, myship, screen_width, screen_height, asteroids)
	pygame.display.flip()
	fps = clock.get_fps()
	print (fps)
	key.ent=False
	key.left=False
	clock.tick(60)
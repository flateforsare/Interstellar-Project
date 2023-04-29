import pygame

# Set up Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.Font(None, 40)

cargo_in = {
	'Carbon' : 25,
	'Gold'  : 45,
	'Water' : 20
}

cargo_out = {
	'Grain' : 60,
	'Organic produce' : 120
}

prices = {
	'Carbon' : 25,
	'Grain' : 60,
	'Gold'  : 45,
	'Organic produce' : 120,
	'Water' : 20
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

def menu(cargo_in, cargo_out, prices, key):
	# Define the menu options
	menu_options = ["Leave", "Trade"]
	trade_selected_option = 1
	selected_option = 1
	keys = Key()
	while True:
		# Clear the screen
		screen.fill((0, 0, 0))
		# Display the menu options
		for i, option in enumerate(menu_options):
			color = (255, 255, 255) if i == selected_option else (128, 128, 128)
			text = font.render(option, True, color)
			screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - 50 + i*50))

		# Display the cargo and prices in the Trade menu
		if selected_option == 1:
			# Display the cargo items and their quantities in the Sell menu
			if trade_options[trade_selected_option] == "Sell":
				cargo_text = font.render("Cargo:", True, (255, 255, 255))
				screen.blit(cargo_text, (screen_width/2 - cargo_text.get_width()/2, screen_height/2 - 100))
				for i, item in enumerate(cargo_out.keys()):
					text = font.render(f"{item}: {cargo_out[item]} (Sell: {prices[item]})", True, (255, 255, 255))
					screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - 50 + i*50))

			# Display the "Buy" and "Sell" options
			trade_options = ["Buy", "Sell"]
			for i, option in enumerate(trade_options):
				color = (255, 255, 255) if i == trade_selected_option else (128, 128, 128)
				text = font.render(option, True, color)
				screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - 50 + i*50))

		# Update the screen
		pygame.display.flip()

		# Check for input
		events = pygame.event.get()
		keys.get_keys(events)
		if keys.esc:
			pygame.quit()
			return
		elif keys.up:
			if selected_option == 1:
				trade_selected_option -= 1
				trade_selected_option %= 2
			else:
				selected_option -= 1
				selected_option %= 2
		elif keys.down:
			if selected_option == 1:
				trade_selected_option += 1
				trade_selected_option %= 2
			else:
				selected_option += 1
				selected_option %= 2
		elif keys.ent:
			if selected_option == 0:
				pygame.quit()
				return
			elif selected_option == 1:
				if trade_options[trade_selected_option] == "Buy":
					pass  # Placeholder for buy code
				elif trade_options[trade_selected_option] == "Sell":
					pass  # Placeholder for selling code
								
def sell_menu(cargo_out, prices, key):
	# Set up Pygame
	pygame.init()
	screen_width, screen_height = 800, 600
	screen = pygame.display.set_mode((screen_width, screen_height))
	font = pygame.font.Font(None, 40)

	# Define the "Back" option
	menu_options = ["Back"]

	# Define the "Sell All" option
	sell_options = ["Sell All"]
	sell_all_selected = False

	# Add the cargo items to the sell options list
	for item in cargo_out.keys():
		sell_options.append(item)

	# Set the initial selected option
	selected_option = 0

	while True:
		# Clear the screen
		screen.fill((0, 0, 0))

		# Display the menu options
		for i, option in enumerate(menu_options + sell_options):
			color = (255, 255, 255) if i == selected_option else (128, 128, 128)
			text = font.render(option, True, color)
			screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - 50 + i*50))

		# Display the cargo items and their quantities
		if sell_all_selected:
			for i, item in enumerate(cargo_out.keys()):
				text = font.render(f"{item}: {cargo_out[item]}", True, (255, 255, 255))
				screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - 50 + i*50))
		else:
			selected_item = sell_options[selected_option]
			if selected_item != "Sell All":
				text = font.render(f"{selected_item}: {cargo_out[selected_item]}", True, (255, 255, 255))
				screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - 50))

		# Update the screen
		pygame.display.flip()

		# Check for input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
			elif event.type == pygame.KEYDOWN:
				if event.key == key['up']:
					selected_option -= 1
					if selected_option < 0:
						selected_option = len(menu_options + sell_options) - 1
				elif event.key == key['down']:
					selected_option += 1
					if selected_option > len(menu_options + sell_options) - 1:
						selected_option = 0
				elif event.key == key['ent']:
					selected_item = sell_options[selected_option]
					if selected_item == "Back":
						pygame.quit()
						return
					elif selected_item == "Sell All":
						total_price = 0
						for item, quantity in cargo_out.items():
							total_price += prices[item] * quantity
						# Add the total price to the player's funds
						# Set the cargo quantities to 0
						# Return to the previous menu
					else:
						sell_amount = cargo_out[selected_item]
						if sell_amount > 0:
							total_price = prices[selected_item] * sell_amount
							# Add the price to the player's funds
							# Set the cargo quantity to 0
							# Return to the previous menu
menu(cargo_in, cargo_out, prices, Key)
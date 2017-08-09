import sys
from time import sleep
from random import choice

import pygame
from bullet import Bullet
from long_bullet import LongBullet
from alien_bullet import AlienBullet
from alien import Alien
from health import Health
from shield import Shield
from ship import Ship

alien_list = []
			
def check_keydown_events(event, ai_settings, screen, stats, sb, play_button, ship,
			aliens, bullets, mouse_x, mouse_y, alien_bullets, long_bullets,
			health, shield):
	"""Respond to keypresses"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True	
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_z:
		stats.bullet_active = True
	elif event.key == pygame.K_RETURN: 
		check_play_button(ai_settings, screen, stats, sb, play_button, ship,
			aliens, bullets, mouse_x, mouse_y, alien_bullets, long_bullets,
			health, shield)
	elif event.key == pygame.K_q:
		save_high_score(stats)
		sys.exit() 
		
def check_keyup_events(event, ship):
	"""Respond to key releases"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False	
	
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
		bullets, alien_bullets, long_bullets, health, shield):
	# Watch for keyboard and mouse events.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			save_high_score(stats)
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()                                          #for the sake of filling in the parameter 
			check_keydown_events(event, ai_settings, screen, stats, sb, play_button, ship,
				aliens, bullets, mouse_x, mouse_y, alien_bullets, long_bullets,
				health, shield)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship,
				aliens, bullets, mouse_x, mouse_y, alien_bullets, long_bullets,
				health, shield)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
		aliens, bullets, mouse_x, mouse_y, alien_bullets, long_bullets,
		health, shield):
	"""Start a new game when the player clicks Play or press Enter"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	button_pressed = pygame.key.get_pressed()[pygame.K_RETURN]
	if (button_clicked or button_pressed) and not stats.game_active:
		#Reset the game settings
		ai_settings.initialize_dynamic_settings()
		
		#Hide the mouse cursor
		pygame.mouse.set_visible(False)
		
		#Reset the game statistics
		stats.reset_stats() 
		stats.game_active = True
		
		#Reset the scoreboard images
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		#Empty the list of aliens, bullets, long bullets, health
		aliens.empty()
		bullets.empty()
		long_bullets.empty()
		health.empty()
		shield.empty()
		
		#Create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens) 
		#create_alien_bullet(ai_settings, screen, aliens, alien_bullets)
		ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
		alien_bullets, play_button, long_bullets, health, shield):
	# Redraw the screen during each pass through of loop
	screen.fill(ai_settings.bg_color)
	#Redraw all bullets behind ship and aliens, but on top of screen
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	for long_bullet in long_bullets.sprites():
		long_bullet.draw_bullet()	
	ship.blitme()
	aliens.draw(screen)
	for alien_bullet in alien_bullets.sprites():
		alien_bullet.draw_alien_bullet()
	health.draw(screen) 
	shield.draw(screen)
	
	#Draw the score information
	sb.show_score()
	
	#Draw the play button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()
	
	# Make the most recently drawn screen visible.
	pygame.display.flip()


def create_alien_bullet(ai_settings, screen, alien_bullets):
	"""
	Create alien bullets which start position's based on the random 
	position of the fleet of aliens 
	"""
	while (len(alien_bullets) < ai_settings.alien_bullets_allowed):		
		alien_bullet = AlienBullet(ai_settings, screen)
		chosen_alien = choice(alien_list)
		alien_bullet.rect.x = chosen_alien.rect.x
		alien_bullet.y = float(chosen_alien.rect.y)
		alien_bullet.rect.y = alien_bullet.y
		alien_bullets.add(alien_bullet) 

def update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, 
		bullets, alien_bullets, long_bullets):
	create_alien_bullet(ai_settings, screen, alien_bullets)
	#Update bullet positions
	alien_bullets.update() 
	#Get rid of bullets that have disappeared	
	for alien_bullet in alien_bullets.copy():
		if alien_bullet.rect.top >= alien_bullet.screen_rect.bottom:
			alien_bullets.remove(alien_bullet)
	
	#Remove any bullets and alien bullets that have collided
	pygame.sprite.groupcollide(bullets, alien_bullets, True, True)
	pygame.sprite.groupcollide(long_bullets, alien_bullets, False, True)
	
	#Respond to alien-bullet and ship collision
	if pygame.sprite.spritecollideany(ship, alien_bullets): 
		if stats.shield_active:
			collision_list = pygame.sprite.spritecollide(ship, alien_bullets, True)
			stats.shield_hit += len(collision_list) 	
			
			#Respond to end of shield hit limit
			if stats.shield_hit >= ai_settings.shield_hit_limit:
				stats.shield_active = False
				stats.shield_hit = 0
				ship.image = pygame.image.load('images/ship.png').convert_alpha()
				ship = Ship(ai_settings, screen)					
		else:		
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit not reached yet."""
	#Create a new bullet and add it to the group 'bullets' using the add() method
	#Confirm the number of existing bullet is below the allowed number before creating a new bullet
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet) 

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets,
		long_bullets):
	"""Update position of bullets and get rid of old bullets"""
	#Update bullet positions
	bullets.update()
		
	#Get rid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
		aliens, bullets, long_bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
		aliens, bullets, long_bullets):
	"""Respond to bullet-alien and long_bullet-alien collisions"""
	#Remove any bullets and aliens that have collided
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	collisions1 = pygame.sprite.groupcollide(long_bullets, aliens, False, True)
	if collisions or collisions1:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
			stats.alien_kills += len(aliens)
		for aliens in collisions1.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()	
			stats.alien_kills += len(aliens)		
		check_high_score(stats, sb)
	
	if len(aliens) == 0:
		start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)

def create_long_bullet(ai_settings, screen, stats, long_bullets):
	"""Reload a long bullet for a certain amount of alien kills."""
	if (stats.alien_kills % ai_settings.long_bullet_reload_point == 0):
		if ai_settings.long_bullet_count < ai_settings.long_bullet_limit:
			ai_settings.long_bullet_count += 1
			
			#to prevent repetition of bullet creation at reload point;
			#add an inaccurate count for alien kills to close reload point once a bullet is reloaded;
			"""
			Attention! 	
			The reload point and all its multiple cannot be used for other drop points
			e.g. reload_point = 20; multiple: 40, 60, 80...
			"""			 
			stats.alien_kills += 1
	
def fire_long_bullet(ai_settings, screen, stats, ship, long_bullets):
	"""Fire a long bullet when key z is pressed."""
	if stats.bullet_active:
		if ai_settings.long_bullet_count > 0:
			new_long_bullet = LongBullet(ai_settings, screen, ship)
			long_bullets.add(new_long_bullet) 
			ai_settings.long_bullet_count -= 1
			stats.bullet_active = False	
		
		# To turn off the effect of bullet_active 
		# caused by key press of 'z' when long bullet count is 0
		stats.bullet_active = False 	

def update_long_bullets(ai_settings, screen, stats, sb, ship, aliens, 
		bullets, long_bullets):
	#Create long bullet for standby
	create_long_bullet(ai_settings, screen, stats, long_bullets)
	
	#Fire long bullet on trigger
	fire_long_bullet(ai_settings, screen, stats, ship, long_bullets)
	
	#Update long bullet positions
	long_bullets.update()
		
	#Get rid of long bullets that have disappeared
	for long_bullet in long_bullets.copy():
		if long_bullet.rect.bottom <= 0:
			long_bullets.remove(long_bullet)
	
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
		aliens, bullets, long_bullets)


def create_health(ai_settings, screen, stats, health):
	"""Add one health to the group health"""
	if (stats.alien_kills % ai_settings.health_drop_point == 0):
		if (len(health) < 1):
			new_health = Health(ai_settings, screen)
			health.add(new_health)	
			
def update_health(ai_settings, screen, stats, sb, ship, health):
	create_health(ai_settings, screen, stats, health)
	#Update health bubble position
	for new_health in health:
		new_health.update() 
		if new_health.rect.top >= ai_settings.screen_height:
			health.empty() 
	#Respond to health and ship collision
	if pygame.sprite.spritecollideany(ship, health):
		health.empty() 
		if (stats.ships_left < ai_settings.ship_limit + 2):
			#Increment ships_left
			stats.ships_left += 1
		#Update scoreboard
		sb.prep_ships()

def create_shield(ai_settings, screen, stats, shield):
	"""Add one shield to group Shield"""
	if (stats.alien_kills % ai_settings.shield_drop_point == 0):
		if (len(shield) < 1):
			new_shield = Shield(ai_settings, screen)
			shield.add(new_shield)	
			
def update_shield(ai_settings, screen, stats, ship, shield):
	create_shield(ai_settings, screen, stats, shield)
	#Update shield bubble position
	for new_shield in shield:
		new_shield.update() 
		if new_shield.rect.top >= ai_settings.screen_height:
			shield.empty() 
	#Respond to shield and ship collision
	if pygame.sprite.spritecollideany(ship, shield):
		shield.empty() 
		ship.image = pygame.image.load('images/ship_upgrade.png').convert_alpha()
		ship = Ship(ai_settings, screen)
		stats.shield_active = True
		stats.shield_hit = 0
		ai_settings.long_bullet_count = ai_settings.long_bullet_limit
		
	
def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets):
	#Destroy existing bullets, speed up game, and create new fleet
	bullets.empty()
	ai_settings.increase_speed()
		
	#Increase level
	stats.level += 1
	sb.prep_level()
		
	create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats, sb):
	"""Check to see if there's a new high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def save_high_score(stats):
	filename = 'high_score.txt'
	with open(filename, 'w') as file_object:
		file_object.write (str(stats.high_score))


def check_fleet_edges(ai_settings, aliens):
	"""Respond appropriately if any aliens have reached an edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break 

def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change the fleet's direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1 

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Respond to ship being hit by alien"""
	if stats.ships_left > 0:
		#Decrement ships_left
		stats.ships_left -= 1
		
		#Update scoreboard
		sb.prep_ships()
		
		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
		
		#Create a new fleet and center the ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		#Pause
		sleep(0.5)

	else:
		stats.game_active = False 
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Check if any aliens have reached the bottom of the screen."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if the ship got hit.
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
			break
	
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""
	Check if the fleet is at an edge,
	 and update the positions of all aliens in the fleet
	"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#Look for alien-ship collisions
	if pygame.sprite.spritecollideany(ship, aliens):
		if stats.shield_active:
			collision_list = pygame.sprite.spritecollide(ship, aliens, True)
			stats.score += ai_settings.alien_points * len(collision_list)
			sb.prep_score()
			stats.alien_kills += len(collision_list)
			stats.shield_hit += len(collision_list) 
			
			#Check special conditions: if there's high score or new level
			check_high_score(stats, sb)	
			if len(aliens) == 0:
				start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)	
			
			#Respond to end of shield hit limit
			if stats.shield_hit >= ai_settings.shield_hit_limit:
				stats.shield_active = False
				stats.shield_hit = 0
				ship.image = pygame.image.load('images/ship.png').convert_alpha()
				ship = Ship(ai_settings, screen)
					
		else:		
			ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
		
	#Look for aliens hitting the bottom of the screen
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets) 

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of aliens that fit in a row"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit on the screen."""
	available_space_y = (ai_settings.screen_height -
						(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in the row"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width 
	alien.x = alien_width + 2 * alien_width * alien_number 
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	# Add each alien into a list to choose random alien for alien bullet creation
	alien_list.append(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a full fleet of alines"""
	#Create an alien and find the number of aliens in a row
	#Spacing between each alien is equal to one alien width
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	#Create the fleet of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)




	




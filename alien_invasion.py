import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats 
from scoreboard import Scoreboard 
from button import Button 
from ship import Ship
import game_functions as gf
from health import Health
from shield import Shield

def run_game():
	# Initialize pygame, settings and screen object.
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	#Make the Play button 
	play_button = Button(ai_settings, screen, "Play")
		
	#Make a ship, a group of bullets, a group of alien bullets and a group of aliens
	ship = Ship(ai_settings, screen)
	bullets = Group()
	long_bullets = Group()
	alien_bullets = Group()
	aliens = Group()
	health = Group()
	shield = Group()
	
	#Create an instance to store game statistics and create a scoreboard
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats, ship)

	#Create the fleet of aliens
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	# Start the main loop for the game.
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
			aliens, bullets, alien_bullets, long_bullets, health, shield)
		
		if stats.game_active:
			ship.update() 
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, 
				long_bullets)
			gf.update_long_bullets(ai_settings, screen, stats, sb, ship, aliens, 
				bullets, long_bullets)
			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
			gf.update_alien_bullets(ai_settings, screen, stats, sb, ship, aliens, 
				bullets, alien_bullets, long_bullets)
			gf.update_health(ai_settings, screen, stats, sb, ship, health)
			gf.update_shield(ai_settings, screen, stats, ship, shield)
			
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, 
			bullets, alien_bullets, play_button, long_bullets, health, shield)

"""      
Program loophole:
Health/Shield/LongBullet reoccurences are based on a single selected game point 
(i.e. number of alien kills) and that point's multiples
Hence,
- if you shoot bullet, guarentee to get health, shield or long bullet reload
- if you shoot long_bullet, kill > 1 alien in one hit, selected game point may be skipped
Solution:
- Let it be. This will be one of the game's random element where you may get your health,
  shield, long bullet at different frequencies every time depending on how you play and
  also your luck
- You can also get > 1 consecutive goodies if you stay at a certain game point and stop 
  shooting aliens. Well, you can, but you can't stay like that forever!
- So, best piece of advice would be:
	~~Practice shooting bullets. Don't be overly dependant on long bullets~~

"""
       
run_game()



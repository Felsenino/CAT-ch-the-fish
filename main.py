import pygame as pg
import os
import random
import time

pg.font.init()
pg.mixer.init()

#general window attributes
TITLE = "CAT-ch the fish!" 
WIDTH, HEIGHT = 600, 900 #the way the code has been written allows to change the height of the screen from here
FPS = 60

#creating the window with the previous values
WIN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption(TITLE)

#score and health lists, used to track user's lifes and score
score = []
health = ["heart", "heart", "heart"]

#Load audio files
pg.mixer.music.load(os.path.join("Assets", "song.mp3"))
pg.mixer.music.set_volume(0.1)
click = pg.mixer.Sound(os.path.join("Assets", "click.wav"))
click.set_volume(0.4)
point = pg.mixer.Sound(os.path.join("Assets", "point.mp3"))
point.set_volume(0.7)
error = pg.mixer.Sound(os.path.join("Assets", "error.mp3"))
error.set_volume(0.2)
miao1 = pg.mixer.Sound(os.path.join("Assets", "miao1.mp3"))
miao1.set_volume(0.2)
miao2 = pg.mixer.Sound(os.path.join("Assets", "miao2.mp3"))
miao2.set_volume(0.4)
miao3 = pg.mixer.Sound(os.path.join("Assets", "miao3.mp3"))
miao3.set_volume(0.9)

#user interface attributes
BACKGROUND_IMAGE = pg.image.load(os.path.join("Assets", "background.jpg"))
BACKGROUND = pg.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
LOWER_BANNER = pg.image.load(os.path.join("Assets", "lower_banner.png"))
LOWER_GAME_OVER_BANNER = pg.image.load(os.path.join("Assets", "lower_game_over_banner.png"))
LOWER_GAME_STARTING_BANNER = pg.image.load(os.path.join("Assets", "lower_game_starting_banner.png"))
UPPER_BANNER = pg.image.load(os.path.join("Assets", "upper_banner.png"))
HEART_IMAGE = pg.image.load(os.path.join("Assets", "heart.png"))
HEART = pg.transform.scale(HEART_IMAGE, (50, 50))
A_BUTTON = pg.image.load(os.path.join("Assets", "a_button.png"))
D_BUTTON = pg.image.load(os.path.join("Assets", "d_button.png"))
GAME_OVER_IMAGE = pg.image.load(os.path.join("Assets", "game_over.png"))
GAME_OVER = pg.transform.scale(GAME_OVER_IMAGE, (WIDTH, 400))
SPACE_BUTTON = pg.image.load(os.path.join("Assets", "space_button.png"))
ESC_BUTTON = pg.image.load(os.path.join("Assets", "esc_button.png"))

#crates sprite attributes
CRATE_IMAGE = pg.image.load(os.path.join("Assets", "crate.png"))
CRATE_width, CRATE_height = 75, 75
CRATE = pg.transform.scale(CRATE_IMAGE, (CRATE_width, CRATE_height))
CRATE1_x = random.randint(0, WIDTH - CRATE_width)
CRATE2_x = random.randint(0, WIDTH - CRATE_width)
CRATE3_x = random.randint(0, WIDTH - CRATE_width)

#cat sprite attributes
CAT_IMAGE = pg.image.load(os.path.join("Assets", "kitty.png"))
CAT_width, CAT_height = 100, 80
IDLE_CAT_width, IDLE_CAT_height = 80, 80
CAT = pg.transform.scale(CAT_IMAGE, (CAT_width, CAT_height))
IDLE_CAT_IMAGE = pg.image.load(os.path.join("Assets", "idle_cat.png"))
IDLE_CAT = pg.transform.scale(IDLE_CAT_IMAGE, (IDLE_CAT_width, IDLE_CAT_height))

#fish sprite attributes
FISH_IMAGE = pg.image.load(os.path.join("Assets", "new_fish.png"))
FISH_width, FISH_height = 40, 80
FISH = pg.transform.scale(FISH_IMAGE, (FISH_width, FISH_height))
FISH1_x = random.randint(0, WIDTH - FISH_width)
FISH2_x = random.randint(0, WIDTH - FISH_width)
FISH3_x = random.randint(0, WIDTH - FISH_width)

#fishes go down with a vel/frame speed
def fish_movement(pesce1, pesce2, pesce3, vel):
	pesce1.y += vel 
	pesce2.y += vel 
	pesce3.y += vel 

#crates go down with a crate_speed/frame speed
def crate_movement(cassa1, cassa2, cassa3, crate_speed):
	cassa1.y += crate_speed 
	cassa2.y += crate_speed  
	cassa3.y += crate_speed  

#check if the user (cat sprite) collide with something
def collision_check(gatto, pesce1, pesce2, pesce3, cassa1, cassa2, cassa3):
	if gatto.colliderect(pesce1):
		pesce1.y = pesce3.y - HEIGHT/2
		pesce1.x = random.randint(0, WIDTH - FISH_width)
	elif gatto.colliderect(pesce2):
		pesce2.y = pesce1.y - HEIGHT/2
		pesce2.x = random.randint(0, WIDTH - FISH_width)
	elif gatto.colliderect(pesce3):
		pesce3.y = pesce2.y - HEIGHT/2
		pesce3.x = random.randint(0, WIDTH - FISH_width)

	if gatto.colliderect(cassa1):
		pg.mixer.Sound.play(error)
		health.pop()
		cassa1.y = cassa3.y - HEIGHT/2
		cassa1.x = random.randint(0, WIDTH - CRATE_width)
	elif gatto.colliderect(cassa2):
		pg.mixer.Sound.play(error)
		health.pop()
		cassa2.y = cassa1.y - HEIGHT/2
		cassa2.x = random.randint(0, WIDTH - CRATE_width)
	elif gatto.colliderect(cassa3):
		pg.mixer.Sound.play(error)
		health.pop()
		cassa3.y = cassa2.y - HEIGHT/2
		cassa3.x = random.randint(0, WIDTH - CRATE_width)


#if the user (cat sprite) collides with a fish his score increments by 1
def score_update(gatto, pesce1, pesce2, pesce3):
	if gatto.colliderect(pesce1) or gatto.colliderect(pesce2) or gatto.colliderect(pesce3):
		score.append("point")
		pg.mixer.Sound.play(point)

#if a fish gets to the bottom end of the screen the user loses a life
def health_bar_behavior(pesce1, pesce2, pesce3):
	if pesce1.y >= HEIGHT - 100 or pesce2.y >= HEIGHT - 100 or pesce3.y >= HEIGHT - 100:
		health.pop()

#fishes and crates' position gets resetted when they reach the bottom end of the screen
def screen_end_check(pesce1, pesce2, pesce3, cassa1, cassa2, cassa3):
	if pesce1.y >= HEIGHT - 100:
		pg.mixer.Sound.play(error)
		pesce1.y = pesce3.y - HEIGHT/2
		pesce1.x = random.randint(0, WIDTH - FISH_width)
	elif pesce2.y >= HEIGHT - 100:
		pg.mixer.Sound.play(error)
		pesce2.y = pesce1.y - HEIGHT/2
		pesce2.x = random.randint(0, WIDTH - FISH_width)
	elif pesce3.y >= HEIGHT - 100:
		pg.mixer.Sound.play(error)
		pesce3.y = pesce2.y - HEIGHT/2
		pesce3.x = random.randint(0, WIDTH - FISH_width)
	
	if cassa1.y >= HEIGHT - 100:
		cassa1.y = cassa3.y - HEIGHT/2
		cassa1.x = random.randint(0, WIDTH - CRATE_width)
	elif cassa2.y >= HEIGHT - 100:
		cassa2.y = cassa1.y - HEIGHT/2
		cassa2.x = random.randint(0, WIDTH - CRATE_width)
	elif cassa3.y >= HEIGHT - 100:
		cassa3.y = cassa2.y - HEIGHT/2
		cassa3.x = random.randint(0, WIDTH - CRATE_width)

#draw almost all of the sprites on the screen
def draw_window(gatto, pesce1, pesce2, pesce3, cassa1, cassa2, cassa3, keys_pressed):

	#score font's size gets smaller if it has 3 figures
	if len(score) < 100:
		font_size = 90
	elif len(score) >= 100:
		font_size = 80

	#font and text get defined
	font = pg.font.Font(os.path.join("Assets", "chary___.ttf"), font_size)
	text = font.render(str(len(score)), True, (170,170,170))

	#depending on the score figures number, the x coordinate of the score changes
	if len(score) < 10:
		text_x = 277
	elif len(score) < 100:
		text_x = 257
	elif len(score) < 1000:
		text_x = 245
	else:
		text_x = 240

	#background is displayed before everything
	WIN.blit(BACKGROUND,(0,0))

	#depending on the keys pressed the cat faces in a different direction
	if keys_pressed[pg.K_d]:
		WIN.blit(pg.transform.flip(CAT, True, False), (gatto.x, gatto.y))
	elif keys_pressed[pg.K_a]:
		WIN.blit(CAT, (gatto.x, gatto.y))
	else:
		WIN.blit(IDLE_CAT, (gatto.x, gatto.y))
	
	#the three fishes are displayed
	WIN.blit(FISH, (pesce1.x, pesce1.y))
	WIN.blit(FISH, (pesce2.x, pesce2.y))
	WIN.blit(FISH, (pesce3.x, pesce3.y))

	#the three crates are displayed
	WIN.blit(CRATE, (cassa1.x, cassa1.y))
	WIN.blit(CRATE, (cassa2.x, cassa2.y))
	WIN.blit(CRATE, (cassa3.x, cassa3.y))

	#ui component are displayed
	WIN.blit(LOWER_BANNER, (0, HEIGHT - 100))
	WIN.blit(UPPER_BANNER, (0, 0))
	WIN.blit(text, (text_x, 40))

	#a different number of hearts is displayed, depending on user's health
	for i in range (len(health)):
		WIN.blit(HEART, (20 + i*60, HEIGHT - 72.5))
	
	#buttons in the ui are "animated" if pressed
	if keys_pressed[pg.K_a]:
		WIN.blit(A_BUTTON, (353.5, HEIGHT - 83.5))
	if keys_pressed[pg.K_d]:
		WIN.blit(D_BUTTON, (474.5, HEIGHT - 83.5))

	pg.display.update()

#cat's sprite's x coordinate changes by VEL depending on the key pressed
def cat_handle_movement(keys_pressed, gatto, VEL):
	if keys_pressed[pg.K_a] and gatto.x - VEL > 0: #left
		gatto.x -= VEL
	if keys_pressed[pg.K_d]and gatto.x + VEL < WIDTH - CAT_width: #right
		gatto.x += VEL

#cat meowing a random meow file
def miao_sound():
	random_miao = random.randint(1,3)
	if random_miao == 1:
		pg.mixer.Sound.play(miao1)
	elif random_miao == 2:
		pg.mixer.Sound.play(miao2)
	elif random_miao == 3:
		pg.mixer.Sound.play(miao3)

#game over page
def game_over(keys_pressed, pesce1, pesce2, pesce3, cassa1, cassa2, cassa3):

	#":(" attributes, to display instead of score
	font = pg.font.Font(os.path.join("Assets", "chary___.ttf"), 85)
	text = font.render((":("), True, (170,170,170))
	text_x = 260

	#display user interface
	WIN.blit(BACKGROUND,(0,0))
	WIN.blit(LOWER_GAME_OVER_BANNER, (0, HEIGHT - 100))
	WIN.blit(UPPER_BANNER, (0, 0))
	WIN.blit(GAME_OVER, (0, 200))

	#"animates" the Space ui if pressed
	if keys_pressed[pg.K_SPACE]:
		WIN.blit(SPACE_BUTTON, (270.5, HEIGHT - 81.5))

	#":(" text is displayed
	WIN.blit(text, (text_x, 40))

	#reset fishes position
	pesce1.y =  - FISH_height
	pesce2.y =  - FISH_height - HEIGHT/2
	pesce3.y =  - FISH_height - HEIGHT

	#reset crates position
	cassa1.y =  - CRATE_height
	cassa2.y =  - CRATE_height - HEIGHT/2
	cassa3.y =  - CRATE_height - HEIGHT

	pg.display.update()

def game_starting(keys_pressed, pesce1, pesce2, pesce3, cassa1, cassa2, cassa3):

	#":)" attributes, to display instead of score
	font = pg.font.Font(os.path.join("Assets", "chary___.ttf"), 85)
	text = font.render((":)"), True, (170,170,170))
	text_x = 260

	#display user interface
	WIN.blit(BACKGROUND, (0, 0))
	WIN.blit(UPPER_BANNER, (0, 0))
	WIN.blit(LOWER_GAME_STARTING_BANNER, (0, HEIGHT - 100))

	#":)" text is displayed
	WIN.blit(text, (text_x, 40))

	font2 = pg.font.Font(os.path.join("Assets", "upheavtt.ttf"), 120)
	text2 = font2.render(("CAT-ch"), True, (25,25,25))
	WIN.blit(text2, (85, HEIGHT/2 - 125))

	font3 = pg.font.Font(os.path.join("Assets", "upheavtt.ttf"), 70)
	text3 = font3.render(("the fish"), True, (25,25,25))
	WIN.blit(text3, (135, HEIGHT/2 - 25))

	#"animates" the Space ui if pressed
	if keys_pressed[pg.K_SPACE]:
		WIN.blit(SPACE_BUTTON, (270.5, HEIGHT - 81.5))
	
	#reset fishes position
	pesce1.y =  - FISH_height
	pesce2.y =  - FISH_height - HEIGHT/2
	pesce3.y =  - FISH_height - HEIGHT

	#reset crates position
	cassa1.y =  - CRATE_height
	cassa2.y =  - CRATE_height - HEIGHT/2
	cassa3.y =  - CRATE_height - HEIGHT

	pg.display.update()

#main function
def main(running):

	timer_miao = 0
	random_timer_for_meow = random.randint(5, 12)*60

	#cat and fishes speed
	vel = 3
	VEL = 4
	crate_speed = 3

	#fishes, cat and crates rectangles are defined
	pesce1 = pg.Rect(FISH1_x, - FISH_height, FISH_width, FISH_height)
	pesce2 = pg.Rect(FISH2_x, - FISH_height - HEIGHT/2, FISH_width, FISH_height)
	pesce3 = pg.Rect(FISH3_x, - FISH_height - HEIGHT, FISH_width, FISH_height)
	gatto = pg.Rect(WIDTH/2 - CAT_width/2, HEIGHT - 200, CAT_width, CAT_height)
	cassa1 = pg.Rect(CRATE1_x, - CRATE_height - HEIGHT/4, CRATE_width, CRATE_height)
	cassa2 = pg.Rect(CRATE2_x, - CRATE_height - HEIGHT/2 - HEIGHT/4, CRATE_width, CRATE_height)
	cassa3 = pg.Rect(CRATE3_x, - CRATE_height - HEIGHT - HEIGHT/4, CRATE_width, CRATE_height)

	clock = pg.time.Clock()
	run = True

	while run:
		clock.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				run = False
		
		keys_pressed = pg.key.get_pressed()
		
		#music loop
		music_queue = pg.mixer.music.get_busy()
		if music_queue == False:
			pg.mixer.music.play()

		#accelerations
		vel = vel + 0.002
		VEL = VEL + 0.0015
		crate_speed = crate_speed + 0.0025
		
		#the "the running" variable is used to define which scene has to be run
		#running = 1 ---- start scene
		#running = 2 ---- main game
		#running = 3 ---- game over scene

		#if user's health is 0 (or < 0 in case of weird errors) go to game over scene
		if len(health) <= 0:
				running = 3

		#if user plays esc starting scene gets displayed
		if keys_pressed[pg.K_ESCAPE]:
			running = 1
			pg.mixer.Sound.play(click)
			WIN.blit(ESC_BUTTON, (9, 7.5))
			pg.display.update()
			time.sleep(0.2)

			#reset user attributes
			for i in range(3 - len(health)):	
				health.append("heart")
			for i in range(len(score)):
				score.pop()
		
		#game starting page
		if running == 1:
			game_starting(keys_pressed, pesce1, pesce2, pesce3, cassa1, cassa2, cassa3)
			#cat and fishes speed
			vel = 3
			VEL = 4
			crate_speed = 3
		

			if keys_pressed[pg.K_SPACE]:
				pg.mixer.Sound.play(click)
				time.sleep(0.2) #sleep is used to let the user see the Space button "animation" in the game starting screen
				running = 2

		#main game scene
		elif running == 2:
			cat_handle_movement(keys_pressed, gatto, VEL)
			fish_movement(pesce1, pesce2, pesce3, vel)
			crate_movement(cassa1, cassa2, cassa3, crate_speed)
			draw_window(gatto, pesce1, pesce2, pesce3, cassa1, cassa2, cassa3, keys_pressed)
			score_update(gatto, pesce1, pesce2, pesce3)
			collision_check(gatto, pesce1, pesce2, pesce3, cassa1, cassa2, cassa3)
			health_bar_behavior(pesce1, pesce2, pesce3)
			screen_end_check(pesce1, pesce2, pesce3, cassa1, cassa2, cassa3)

		#game over scene
		elif running == 3:
			game_over(keys_pressed, pesce1, pesce2, pesce3, cassa1, cassa2, cassa3)

			#cat and fishes speed
			vel = 3
			VEL = 4
			crate_speed = 3

			#if the user presses "Space" during game over reset stats and re-run the game
			if keys_pressed[pg.K_SPACE]:
				pg.mixer.Sound.play(click)
				time.sleep(0.2) #sleep is used to let the user see the Space button "animation" in the game over screen
				for i in range(3):	
					health.append("heart")
				for i in range(len(score)):
					score.pop()
				running = 2
		
		#in a random time between 5 and 12 seconds the cat meows
		timer_miao += 1

		if timer_miao == random_timer_for_meow:
			miao_sound()
			timer_miao = 0
			random_timer_for_meow = random.randint(5, 12)*60

	pg.quit()

if __name__ == "__main__":
	running = 1
	main(running)
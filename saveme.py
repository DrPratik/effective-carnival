import pygame
import sys
import random
pygame.init()

width = 800
height = 600
RED=(204,206,204)
BLUE=(49,193,20)
YELLOW=(255,255,0)
BACKGROUND=(38,111,206)
player_size=50
player_pos=[width/2,height-2*player_size]
DISPLAYSURF = pygame.display.set_mode((width, height))

enemy_size = 50
enemy_pos = [random.randint(0,width-enemy_size),0]
enemy_list = [enemy_pos]
speed=10

screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('Save me!')
game_over = False
score = 0
clock= pygame.time.Clock()


myFont = pygame.font.SysFont("monospace",35)

def set_level(score,speed):
	if score < 20:
		speed=5
	elif score <40:
		speed=8
	elif score<60:
		speed=10
	else:
		speed=15
	#speed = score/5+1
	return speed;
def drop_enemies(enemy_list):
	delay = random.random() 
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos=random.randint(0,width-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos,y_pos])
		
def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen,BLUE,(enemy_pos[0],enemy_pos[1],enemy_size,enemy_size))

def update_enemy_pos(enemy_list,score):
	for idx,enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < height:
			enemy_pos[1]+= speed
		else:
			enemy_list.pop(idx)
			score += 1
	return score
			
def collision_check(enemy_list,player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos,player_pos):
			return True
	return False

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, RED)
    overSurf = gameOverFont.render('Over', True, RED)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (width / 2, 10)
    overRect.midtop = (height / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
   # drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    #checkForKeyPress() # clear out any key presses in the event queue

    while True:
   #     if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
            
            
def detect_collision(player_pos,enemy_pos):
	p_x=player_pos[0]
	p_y=player_pos[1]
	
	e_x=enemy_pos[0]
	e_y=enemy_pos[1]
	
	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >=e_y and p_y < (e_y+enemy_size)):
			return True
	return False
while not game_over:
	
	for event in pygame.event.get():
	
		if event.type == pygame.QUIT:
			sys.exit()
		
		if event.type == pygame.KEYDOWN:

			x=player_pos[0]
			y=player_pos[1]
			
			if event.key == pygame.K_LEFT:
				x -= player_size
			elif event.key == pygame.K_RIGHT:
				x += player_size
			
			player_pos = [x,y]
	
	screen.fill(BACKGROUND)
	
	#update position of enemy
	
	#if enemy_pos[1] >= 0 and enemy_pos[1] < height:
	#	enemy_pos[1]+= speed
	#else:
	#	enemy_pos[0] = random.randint(0,width-enemy_size)
	#	enemy_pos[1] = 0
	
	
	drop_enemies(enemy_list)
	score=update_enemy_pos(enemy_list,score)
	speed = set_level(score,speed)
	text = "Score:" + str(score)
	label = myFont.render(text,1,YELLOW)
	screen.blit(label,(width-200,height-40))
	if collision_check(enemy_list,player_pos):
		game_over= True
		showGameOverScreen()
		break
	draw_enemies(enemy_list)
	
	pygame.draw.rect(screen,RED,(player_pos[0],player_pos[1],player_size,player_size))
	
	clock.tick(30)
	pygame.display.update()


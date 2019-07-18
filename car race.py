import pygame
import random
import sys 

pygame.init()

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(loops=0, start=0.0)

RED = (255,255,255)
YELLOW = (255,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

SIZE = WIDTH, HEIGHT = 800, 600


player_size = 52
player_pos = [(WIDTH/2), (HEIGHT-2*player_size)]
x, y = (WIDTH/2), (HEIGHT-2*player_size)

carImg = pygame.image.load("newcar.png")


enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size),0]
enemy_list = [enemy_pos]

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

BACKGROUND_COLOR = pygame.image.load("bg.jpg")
BACKGROUND_COLOR = pygame.transform.scale(BACKGROUND_COLOR, SIZE)

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, SPEED):
	if score < 20:
		SPEED = 5
	elif score < 40:
		SPEED = 7
	elif score < 70:
		SPEED = 10
	elif score < 100:
		SPEED = 13
	elif score < 200:
		SPEED = 15
	elif score < 300:
		SPEED = 19
	else:
		SPEED = 22
	return SPEED 

def car(x,y):
    screen.blit(carImg, (x,y))

def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0, WIDTH - enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED 
		else:
			enemy_list.pop(idx)
			score += 1
	return score

def collision_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True 
		return False


def detect_collision(player_pos, enemy_pos):
	p_x = player_pos[0] 
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
			return True 
		return False

while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:

			x = player_pos[0]
			y = player_pos[1]

			if event.key == pygame.K_LEFT:
				x -= player_size
			elif event.key == pygame.K_RIGHT:
				x += player_size

			player_pos = [x,y]

	
	screen.fill(BLACK)
	screen.blit(BACKGROUND_COLOR,(0,0))
	screen.blit(carImg,(x, y))

	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score)
	SPEED = set_level(score, SPEED)

	text = "Score:" + str(score)
	label = myFont.render(text, 1, YELLOW)
	screen.blit(label, (WIDTH-200, HEIGHT-40))

	if collision_check(enemy_list, (x,y)):
		game_over = True 
		break
		
	car(x,y)
	draw_enemies(enemy_list)
	pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
	
	clock.tick(30)

	pygame.display.update()	


import pygame, sys
from scenes import *
pygame.init()

WINDOW_WIDTH  = 1200
WINDOW_HEIGHT = 800

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("MoldovaInc")
clock = pygame.time.Clock()

while True:
	for event in pygame.event.get():

		Map.pressed = pygame.mouse.get_pressed()[0]
		Map.motion = event.type == pygame.MOUSEMOTION
	
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEWHEEL:
			Map.scroll = event.y
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				GameState.upgrade_menu = False
				GameState.play = False
				GameState.pause = True
			elif event.key == pygame.K_SPACE:
				if GameState.statistic:
					GameState.statistic = False
					Statistic.one_plot = True
					Statistic.delete_plot()
					GameState.play = True
				else:
					GameState.play = False
					GameState.statistic = True


	window.fill((255,255,255))
	GameState.update(window)
	
	pygame.display.update()
	clock.tick(60)
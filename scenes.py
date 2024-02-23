import pygame, os, sys
import matplotlib.pyplot as plt
import numpy as np
from objects import *
from logic import *
pygame.init()

class GameState:
    main_menu = True
    play = False
    pause = False
    settings = False
    statistic = False
    country_statistic = False
    upgrade_menu = False

    @classmethod
    def update(cls, window):
        if GameState.main_menu:
            MainMenu.update(window)
        elif GameState.pause:
            Pause.update(window)
        elif GameState.country_statistic:
            CountryStatistic.update(window)
        elif GameState.upgrade_menu:
            UpgradeMenu.update(window)
        elif GameState.play:
            Map.update(window)
        if GameState.statistic:
            Statistic.update(window)
        if GameState.settings:
            Settings.update(window)


class MainMenu:
    buttons = [
        Button("start", "images/ButtonsAsset/png/in-use/Play.png", (500, 200)),
        Button("settings", image_path=None, position=(500, 400)),
        Button("exit", "images/ButtonsAsset/png/in-use/Exit.png", (500, 500)),
    ]

    background = pygame.transform.scale(pygame.image.load("images/wine-field.jpg"), (1200, 800))
    background.set_alpha(100)

    panel_surface = pygame.Surface((300, 400), pygame.SRCALPHA)
    panel_for_buttons = pygame.draw.rect(panel_surface, (55, 55, 55) + (120,), panel_surface.get_rect(), border_radius=10)


    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_title(window)
        cls.dispay_panel_for_buttons(window)
        cls.display_buttons(window)
        cls.check_collisions()
    
    @classmethod
    def display_buttons(cls, window):
        for button in MainMenu.buttons:
            window.blit(button.image, button.rect)
    
    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if button.name == "start":
                    GameState.main_menu = False
                    GameState.play = True
                elif button.name == "settings":
                    Settings.back_is = "main_menu"
                    GameState.main_menu = False
                    GameState.settings = True
                elif button.name == "exit":
                    sys.exit()
    
    @classmethod
    def display_background(cls, window):
        window.blit(cls.background, cls.background.get_rect())
    
    @classmethod
    def dispay_panel_for_buttons(cls, window):
        window.blit(cls.panel_surface, (450, 200))
    
    @classmethod
    def display_title(cls, window):
        font_path = "images/font/evil-empire.ttf"
        font_size = 36
        font_color = (0, 0, 0)
        font = pygame.font.Font(font_path, font_size)

        text = "Moldova Inc"
        text_surface = font.render(text, True, font_color)  # White color
        window.blit(text_surface, (470, 150))
    
    @classmethod
    def set_window(cls, window):
        print(window.get_size())
        cls.window = window
        cls.background = pygame.transform.scale(pygame.image.load("images/wine-field.jpg"), window.get_size())
        cls.background.set_alpha(100)


class Pause:
    buttons = [
        Button("resume", "images/buttons/resume-btn.png", (400, 350)),
        Button("settings", image_path=None , position=(400, 450)),
        Button("exit", "images/buttons/exit-btn.png", (400, 550)),
    ]

    @classmethod
    def update(cls, window):
        cls.display_buttons(window)
        cls.check_collisions()

    @classmethod
    def display_buttons(cls, window):
        for button in Pause.buttons:
            window.blit(button.image, button.rect)
        
    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if button.name == "resume":
                    GameState.pause = False
                    GameState.play = True
                elif button.name == "settings":
                    Settings.back_is = "pause"
                    GameState.pause = False
                    GameState.settings = True
                elif button.name == "exit":
                    sys.exit()

class Statistic:
    one_plot = True  # To generate one plot per space button (not each frame)

    @classmethod
    def update(cls, window):
        cls.display_plot(window)

    @classmethod
    def display_plot(cls, window):
        if Statistic.one_plot:
            x = np.linspace(0, 10, 100) 
            y = np.sin(x)  
            plt.plot(x, y)
            plt.title('Wine Selled')
            plt.savefig('plot.png')

            plot = pygame.image.load('plot.png')
            rect = plot.get_rect()
            window.blit(plot, rect)
            Statistic.one_plot = False
        else:
            plot = pygame.image.load('plot.png')
            rect = plot.get_rect()
            window.blit(plot, rect)
    
    @classmethod
    def delete_plot(self):
        os.remove('plot.png')

class UpgradeMenu:
    # Soon here will be buttons for gameplay, but for now just...
    buttons = [
        Button("world-icon", "images/buttons/world-icon-btn.png", (1150,750), (100, 100))
    ]

    upgrade_buttons = [
        Button("taste-up", image_path=None, position=(500, 500)),
        Button("naturality-up", image_path=None, position=(500, 600)),
        Button("advertisement-up", image_path=None, position=(500, 700)),

        Button("taste-down", image_path=None, position=(400, 500)),
        Button("naturality-down", image_path=None, position=(400, 600)),
        Button("advertisement-down", image_path=None, position=(400, 700)), 
    ]

    image = pygame.transform.scale(pygame.image.load('images/cellar.jpg'),  (1200,800))
    image.set_alpha(50)
    rect = image.get_rect()
    pressed_1 = False
    pressed_2 = False

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_buttons(window)
        cls.display_upgrade_buttons(window)
        cls.display_wine_data(window)
        cls.check_collisions()

    @classmethod
    def display_background(cls, window):
        window.fill((0, 0, 0))
        window.blit(cls.image, cls.rect)

        transparent_gray = (55, 55, 55) + (120,)
        transparent_surface = pygame.Surface((window.get_size()[0]-60, window.get_size()[1]-60), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, transparent_gray, transparent_surface.get_rect(), border_radius=10)
        window.blit(transparent_surface, (30, 30))


    @classmethod
    def display_buttons(cls, window):
        for button in UpgradeMenu.buttons:
            window.blit(button.image, button.rect)

    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    if not cls.pressed_1:
                        cls.pressed_1 = True
                        if button.name == "world-icon":
                            GameState.upgrade_menu = False
                            GameState.play = True
                else:
                    cls.pressed_1 = False
        
        for button in cls.upgrade_buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    if not cls.pressed_2:
                        cls.pressed_2 = True
                        if pygame.mouse.get_pressed()[0]:
                            if button.name == "taste-up":
                                Wine.taste += 1
                            elif button.name == "taste-down":
                                if Wine.taste > 0:
                                    Wine.taste -= 1
                            elif button.name == "naturality-up":
                                Wine.naturality += 1
                            elif button.name == "naturality-down":
                                if Wine.naturality > 0:
                                    Wine.naturality -= 1
                            elif button.name == "advertisement-up":
                                Wine.advertisement += 1
                            elif button.name == "advertisement-down":
                                if Wine.naturality > 0:
                                    Wine.naturality -= 1
                else:
                    cls.pressed_2 = False

    @classmethod
    def display_wine_data(cls, window):
        font = pygame.font.Font("images/font/evil-empire.ttf", 18)
        text = f"Taste: {Wine.taste}, Naturality: {Wine.naturality}, Advertisement: {Wine.advertisement}"
        text_render = font.render(text, True, (255, 255, 255))
        window.blit(text_render, (100, 100))


    @classmethod
    def display_upgrade_buttons(cls, window):
        for button in cls.upgrade_buttons:
            window.blit(button.image, button.rect)
class CountryStatistic:
    buttons = [
        Button("back", image_path=None, position=(500,500))
    ]

    focus_country = None

    @classmethod
    def update(cls, window):
        cls.display_country_statistics(window)
        cls.display_buttons(window)
        cls.check_collisions()

    @classmethod
    def display_buttons(cls, window):
        for button in cls.buttons:
            window.blit(button.image, button.rect)

    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if button.name == "back":
                    GameState.country_statistic = False
                    GameState.play = True

    @classmethod
    def display_country_statistics(cls, window):
        if cls.focus_country != None:
            window.blit(cls.focus_country.image, cls.focus_country.rect)


class Settings:
    buttons = [
        Button("back", image_path=None, position=(500,100))
    ]

    back_is = None

    @classmethod
    def update(cls, window):
        cls.display_buttons(window)
        cls.check_collisions()

    @classmethod
    def display_buttons(cls, window):
        for button in cls.buttons:
            window.blit(button.image, button.rect)
    
    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if button.name == "back":
                    GameState.settings = False
                    if Settings.back_is == "main_menu":
                        GameState.main_menu = True
                    elif Settings.back_is == "pause":
                        GameState.pause = True
                    


class Map:
    buttons = [
        Button("upgrade_menu", "images/buttons/cellar-icon-btn.png", (1150,750), (100, 100)),
        Button("statistics", image_path=None, position=(800,480)),
    ]

    image = pygame.transform.scale(pygame.image.load("images/map.png"), (1200, 800))
    initial_image = pygame.image.load("images/map.png")
    
    width = image.get_width()
    height = image.get_height()

    rect = image.get_rect()
    rect.center = (width // 2, height // 2)

    # mainly for to_scale() method
    scale = 1
    old_scale = 1
    scroll = 0  # 1 for up, -1 for down, 0 for ne

    # for to_drag() method
    initial_map_center = rect.center
    initial_click = None
    pressed = 0
    motion = 0 

    pressed = False
    motion = False

    pressed_icon = False  # for check_collisions() method

    @classmethod
    def update(cls, window):
        Country.one_time_activation() 
        Map.personal_update(window)
        ToSellButton.check_collisions()  # put it here, before Country.update(), because of collisions of clicking on it and on country itslef
        Country.update(window, Map, GameState, CountryStatistic)
        ToSellButton.update(window, Map)
        Tranport.update(window, Map)

    @classmethod
    def personal_update(cls, window):
        window.blit(cls.image, cls.rect)
        cls.display_buttons(window)
        cls.to_scale()
        cls.to_drag()
        cls.check_collisions()

    @classmethod
    def to_drag(cls):
        if cls.scale == 1:
            return
        mouse_pos = pygame.mouse.get_pos()
        if cls.pressed and cls.motion:
            if cls.initial_click is None:
                cls.initial_click = mouse_pos
            offset_x = mouse_pos[0] - cls.initial_click[0]
            offset_y = mouse_pos[1] - cls.initial_click[1]
            cls.rect.center = cls.rect.centerx + offset_x, cls.rect.centery + offset_y
            cls.initial_click = mouse_pos
        elif not cls.pressed:
            cls.initial_click = None

    @classmethod
    def to_scale(cls):  # don't zoom on mouse pos :(
        cls.old_scale = cls.scale
        cls.last_pos = cls.rect.center

        if cls.scroll == 1:  
            if cls.scale >= 2.9:
                cls.scale = 3
            else:
                cls.scale += 0.2
        elif cls.scroll == -1:  
            if cls.scale <= 1.1:
                cls.scale = 1
            else:  
                cls.scale -= 0.2
        cls.scroll = 0

        cls.image = pygame.transform.scale(cls.initial_image, (cls.scale*cls.width, cls.scale*cls.height))
        cls.rect = cls.image.get_rect()

        if cls.scale == 1:
            cls.rect.topleft = (0,0)
        else:
            cls.rect.center = cls.last_pos

    @classmethod
    def display_buttons(cls, window):
        for button in cls.buttons:
            window.blit(button.image, button.rect)

    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    if not cls.pressed_icon:
                        cls.pressed_icon = True
                        if button.name == "upgrade_menu":
                            GameState.play = False
                            GameState.upgrade_menu = True
                        elif button.name == "statistics":
                            GameState.play = False
                            GameState.statistic = True
                else:
                    cls.pressed_icon = False

    @classmethod
    def set_window(cls, window):
        cls.window = pygame.transform.scale(pygame.image.load("images/map2.png"), (window.get_size()[0] / cls.initial_image.get_size()[0],
                                                                                    window.get_size()[1] / cls.initial_image.get_size()[1]))
pygame.quit()
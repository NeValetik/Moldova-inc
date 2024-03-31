import pygame, os, sys, datetime, copy
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.dirname(__file__))  # To avoid the error of neighbour files
from objects import *
from logic import *

pygame.init()
pygame.mixer.init()

class GameState:
    main_menu = True
    play = False
    pause = False
    settings = False
    statistic = False
    country_statistic = False
    upgrade_menu = False

    mouse_button_pressed = None
    mouse_position = None

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
            graph.check_new_contracts()
            Map.update(window)
            Timer.update(window)
            News.update(window)
        if GameState.statistic:
            Statistic.update(window)
        if GameState.settings:
            Settings.update(window)


class MainMenu:

    buttons = [
        Button("start", "assets/stuff/buttons/png/in-use/Play.png", (500, 300)),
        Button("settings", image_path=None, position=(500, 400)),
        Button("exit", "assets/stuff/buttons/png/in-use/Exit.png", (500, 500)),
    ]

    background = pygame.transform.scale(pygame.image.load("assets/background/wine-field.jpg"), (1200, 800))
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
        Button.dislpay_text_on_buttons(window, cls.buttons)
    
    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                Music.play_click_sound()
                if button.name == "start":
                    GameState.main_menu = False
                    GameState.play = True
                elif button.name == "settings":
                    Settings.back_is = "main_menu"
                    GameState.main_menu = False
                    GameState.settings = True
                elif button.name == "exit":
                    sys.exit()
            else:
                Music.is_clicked = False
    
    @classmethod
    def display_background(cls, window):
        window.blit(cls.background, cls.background.get_rect())
    
    @classmethod
    def dispay_panel_for_buttons(cls, window):
        window.blit(cls.panel_surface, (450, 200))
    
    @classmethod
    def display_title(cls, window):
        font_path = "assets/font/evil-empire.ttf"
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
        cls.background = pygame.transform.scale(pygame.image.load("assets/background/wine-field.jpg"), window.get_size())
        cls.background.set_alpha(100)


class Pause:
    buttons = [
        Button("resume", "assets/buttons/resume-btn.png", (400, 350)),
        Button("settings", image_path=None , position=(400, 450)),
        Button("exit", "assets/buttons/exit-btn.png", (400, 550)),
    ]

    @classmethod
    def update(cls, window):
        cls.display_buttons(window)
        cls.check_collisions()

    @classmethod
    def display_buttons(cls, window):
        for button in Pause.buttons:
            window.blit(button.image, button.rect)
        Button.dislpay_text_on_buttons(window, cls.buttons)
        
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
    # don't touch (to generate one plot per space button, not each frame)
    _one_plot = True

    @classmethod

    def update(cls, window):
        cls.display_plot(window)

    @classmethod
    def display_plot(cls, window):
        if Statistic._one_plot:
            x = np.linspace(0, 10, 100) 
            y = np.sin(x)  
            plt.plot(x, y)
            plt.title('Wine Selled')
            plt.savefig('plot.png')

            plot = pygame.image.load('plot.png')
            rect = plot.get_rect()
            window.blit(plot, rect)
            Statistic._one_plot = False
        else:
            plot = pygame.image.load('plot.png')
            rect = plot.get_rect()
            window.blit(plot, rect)
    
    @classmethod
    def delete_plot(self):
        os.remove('plot.png')

class UpgradeMenu:
    buttons = [
        Button("world-icon", "assets/buttons/world-icon-btn.png", (1150,750), (100, 100))
    ]

    upgrade_buttons = [
        Button("taste-up", image_path=None, position=(500, 500)),
        Button("naturality-up", image_path=None, position=(500, 600)),
        Button("advertisement-up", image_path=None, position=(500, 700)),

        Button("taste-down", image_path=None, position=(400, 500)),
        Button("naturality-down", image_path=None, position=(400, 600)),
        Button("advertisement-down", image_path=None, position=(400, 700)), 
    ]

    image = pygame.transform.scale(pygame.image.load('assets/background/cellar.jpg'),  (1200,800))
    image.set_alpha(50)
    rect = image.get_rect()
    pressed_1 = True
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
        Button.dislpay_text_on_buttons(window, cls.buttons)

    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    Music.play_click_sound()
                    if not cls.pressed_1:
                        cls.pressed_1 = True
                        if button.name == "world-icon":
                            GameState.upgrade_menu = False
                            GameState.play = True
                else:
                    cls.pressed_1 = False
                    Music.is_clicked = False
        
        for button in cls.upgrade_buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    Music.play_click_sound()
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
                                if Wine.advertisement > 0:
                                    Wine.advertisement -= 1
                else:
                    cls.pressed_2 = False
                    Music.is_clicked = False

    @classmethod
    def display_wine_data(cls, window):
        font = pygame.font.Font("assets/font/evil-empire.ttf", 18)
        text = f"Taste: {Wine.taste}, Naturality: {Wine.naturality}, Advertisement: {Wine.advertisement}"
        text_render = font.render(text, True, (255, 255, 255))
        window.blit(text_render, (100, 100))


    @classmethod
    def display_upgrade_buttons(cls, window):
        for button in cls.upgrade_buttons:
            window.blit(button.image, button.rect)
class CountryStatistic:
    buttons = [
        Button("back", image_path=None, position=(990,700))
    ]

    focus_country = None

    @classmethod
    def update(cls, window):
        cls.display_country(window)
        cls.display_statistics(window)
        cls.display_buttons(window)
        cls.display_title(window)
        cls.check_collisions()

    @classmethod
    def display_buttons(cls, window):
        for button in cls.buttons:
            window.blit(button.image, button.rect)
        Button.dislpay_text_on_buttons(window, cls.buttons)

    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                Music.play_click_sound()
                if button.name == "back":
                    GameState.country_statistic = False
                    GameState.play = True
            else:
                Music.is_clicked = False

    @classmethod
    def display_country(cls, window):
        if cls.focus_country != None:
            country = copy.copy(cls.focus_country)

            # This scaling should be adjusted more
            scale_factor = max([country.scaled_width // 200, country.scaled_height // 200])
            scale_factor = 3 - scale_factor

            scale_factor *= country.initial_scale_factor
            country.image = pygame.transform.scale(country.initial_not_scaled_image, (country.not_scaled_width * scale_factor,
                                                                                    country.not_scaled_height * scale_factor))
            country.rect = country.image.get_rect()
            country.rect.center = (395, 380)  # center of remain space
            window.blit(country.image, country.rect)
            del country

    @classmethod
    def display_statistics(cls, window):
        transparent_gray = (55, 55, 55) + (120,)
        transparent_surface = pygame.Surface((400, 780), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, transparent_gray, transparent_surface.get_rect(), border_radius=10)
        window.blit(transparent_surface, (790, 10))

    @classmethod
    def display_title(cls, window):
        font = pygame.font.Font("assets/font/evil-empire.ttf", 36)
        text = font.render(cls.focus_country.name, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (990, 40)
        window.blit(text, text_rect)
class Settings:
    buttons = [
        Button("back", image_path=None, position=(500,100))
    ]

    image_path = "assets/background/settings.png"
    initial_image = pygame.image.load(image_path)

    image = pygame.transform.scale(pygame.image.load(image_path), (1200, 800))
    image.set_alpha(50)
    rect = image.get_rect()

    back_is = None

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_buttons(window)
        cls.check_collisions()

    @classmethod
    def display_background(cls, window):
        window.fill((0, 0, 0))
        window.blit(cls.image, cls.rect)
        transparent_gray = (55, 55, 55) + (120,)
        transparent_surface = pygame.Surface((window.get_size()[0] - 60, window.get_size()[1] - 60), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, transparent_gray, transparent_surface.get_rect(), border_radius=10)
        window.blit(transparent_surface, (30, 30))

    @classmethod
    def display_buttons(cls, window):
        for button in UpgradeMenu.buttons:
            window.blit(button.image, button.rect)
        Button.dislpay_text_on_buttons(window, cls.buttons)

    @classmethod
    def display_buttons(cls, window):
        for button in cls.buttons:
            window.blit(button.image, button.rect)
        Button.dislpay_text_on_buttons(window, cls.buttons)
    
    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                Music.play_click_sound()
                if button.name == "back":
                    GameState.settings = False
                    if Settings.back_is == "main_menu":
                        GameState.main_menu = True
                    elif Settings.back_is == "pause":
                        GameState.pause = True
                    


class Map:
    buttons = [
        Button("upgrade_menu", "assets/buttons/cellar-icon-btn.png", (1150,750), (100, 100)),
        Button("statistics", image_path=None, position=(900,700)),
    ]

    stats_bars = [
        ProgressBar(0, 100, 200, 30, (100, 10, 10), (255, 255, 255), (30, 700), getter=BarsGetters.get_world_progress),
    ]

    image = pygame.transform.scale(pygame.image.load("assets/background/oceans-8k.png"), (1200, 800))
    initial_image = pygame.image.load("assets/background/oceans-8k.png")

    background_image = pygame.image.load("assets/background/oceans-8k.png")
    background_rect = background_image.get_rect()
    background_rect.center = (600, 400)
    
    width = image.get_width()
    height = image.get_height()

    rect = image.get_rect()
    rect.center = (width // 2, height // 2)

    # mainly for to_scale() method
    scale = 1
    old_scale = 1
    min_scale = 1
    max_scale = 2
    scale_step = 0.2
    scroll = 0  # 1 for up, -1 for down, 0 for neutral


    # for to_drag() method
    initial_map_center = rect.center
    initial_click = None
    pressed = 0
    motion = 0 

    # general information
    pressed = False
    motion = False

    # for check_collisions() method
    pressed_icon = False  

    @classmethod
    def update(cls, window):
        window.blit(cls.background_image, cls.background_image.get_rect())
        window.blit(cls.image, cls.rect)
        Country.update(window, Map, GameState, CountryStatistic)
        Tranport.update(window, Map)
        Map.personal_update(window)

    @classmethod
    def personal_update(cls, window):
        cls.display_buttons(window)
        cls.dislpay_stats_bars(window)
        cls.to_scale()
        cls.to_drag(window)
        cls.check_collisions()


    @classmethod
    def to_drag(cls, window):
        if cls.scale == 1:
            return
        mouse_pos = pygame.mouse.get_pos()
        if cls.pressed and cls.motion:
            if cls.initial_click is None:
                cls.initial_click = mouse_pos
            offset_x = mouse_pos[0] - cls.initial_click[0]
            offset_y = mouse_pos[1] - cls.initial_click[1]
            # Bounding the map
            if cls.rect.topleft >= (0, 0) and offset_x > 0 and offset_y > 0:
                offset_x = 0
                offset_y = 0
            if cls.rect.top > 0 and offset_y > 0:
                offset_y = 0
            if cls.rect.left > 0 and offset_x > 0:
                offset_x = 0
            if cls.rect.bottomright <= window.get_size() and offset_x < 0 and offset_y < 0:
                offset_x = 0
                offset_y = 0
            if cls.rect.bottom < window.get_size()[1] and offset_y < 0:
                offset_y = 0
            if cls.rect.right < window.get_size()[0] and offset_x < 0:
                offset_x = 0
            cls.rect.center = cls.rect.centerx + offset_x, cls.rect.centery + offset_y
            cls.initial_click = mouse_pos
        elif not cls.pressed:
            cls.initial_click = None

    @classmethod
    def to_scale(cls):  # don't zoom on mouse pos :(
        cls.old_scale = cls.scale
        cls.last_pos = cls.rect.center

        if cls.scroll == 1:  
            if cls.scale >= cls.max_scale-0.1:
                cls.scale = cls.max_scale
            else:
                cls.scale += cls.scale_step
        elif cls.scroll == -1:  
            if cls.scale <= cls.min_scale+0.1:
                cls.scale = cls.min_scale
            else:  
                cls.scale -= cls.scale_step
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
        Button.dislpay_text_on_buttons(window, cls.buttons)

    @classmethod
    def dislpay_stats_bars(cls, window):
        for bar in cls.stats_bars:
            bar.update(window)

    @classmethod
    def check_collisions(cls):
        if Map.pressed and Map.motion:
            return
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    Music.play_click_sound()
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
                    Music.is_clicked = False
        
class Timer:
    start_time = datetime.datetime(1950, 12, 30, 12, 0, 0)
    current_time = start_time
    frame = 1

    @classmethod
    def update(cls, window):
        cls.update_timer()
        cls.display_timer(window)
    
    @classmethod
    def display_timer(cls, window):
        time = cls.get_time()

        border_rect = pygame.Rect(1040, 20, 100, 20)
        pygame.draw.rect(window, (255, 255, 255), border_rect, border_radius=40)

        font = pygame.font.Font("assets/font/evil-empire.ttf", 20)
        text = font.render(time, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1090, 30)
        window.blit(text, text_rect)

    @classmethod
    def update_timer(cls):
        if cls.frame >= 60:
            cls.frame = 1
            cls.current_time += datetime.timedelta(weeks=1)
        else:
            cls.frame += 1

    @classmethod
    def get_time(cls):
        return f"{cls.current_time.day}/{cls.current_time.month}/{cls.current_time.year}"

class News:
    buttons = [
        Button("okay", image_path=None, position=(600, 750))
    ]

    stored_notifications = []
    current_notification = None

    @classmethod
    def update(cls, window):
        cls.check_data()
        cls.display_notification()
        cls.store_notification()

    @classmethod
    def check_data(cls):
        '''
        Method wich will look at countries data,
        and notify about presetted events
        '''
        pass

    @classmethod
    def display_notification(cls):
        '''
        Method wich will display current_notification on window
        '''
        pass

    @classmethod
    def store_notification(cls):
        if cls.current_notification is not None:
            cls.store_notification.append(cls.current_notification)
            cls.current_notification = None
            if len(cls.store_notification) > 10:
                cls.store_notification = cls.store_notification[-10:]
    
class Music:
    click_sound = pygame.mixer.Sound("assets/sound/click-menu.ogg")
    is_clicked = False

    @classmethod
    def initiate_background_music(cls):
        pygame.mixer.init()
        pygame.mixer.music.load('assets/sound/theme.ogg')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)

    @classmethod
    def play_click_sound(cls):
        if not cls.is_clicked:
            cls.click_sound.play()
            cls.is_clicked = True
        

pygame.quit()
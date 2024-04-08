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
        Button("start", (400, 450)),
        Button("settings", (400, 550)),
        Button("exit", (400, 650)),
    ]

    background = pygame.transform.scale(pygame.image.load("assets/background/main-background.png"), (1920, 1020))
    stripe = pygame.transform.scale(pygame.image.load("assets/background/stripe.png"), (600, 1080))
    stripe_rect = stripe.get_rect()
    stripe_rect.center = (400, 510)


    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_title(window)
        cls.display_buttons(window)
        cls.check_collisions(window)

    @classmethod
    def display_background(cls, window):
        window.blit(cls.background, cls.background.get_rect())
        window.blit(cls.stripe, cls.stripe_rect)
    
    @classmethod
    def display_title(cls, window):
        font_path = "assets/font/evil-empire.ttf"
        font_size = 72
        font_color = (0, 0, 0)
        font = pygame.font.Font(font_path, font_size)

        text = "Moldova Inc."
        text_surface = font.render(text, True, font_color)
        window.blit(text_surface, (230, 150))

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)
    
    @classmethod
    def check_collisions(cls, window):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                Button.frame_rect.center = button.rect.center
                window.blit(Button.frame, Button.frame_rect)
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
    
class Pause:
    buttons = [
        Button("resume", (400, 450)),
        Button("settings", (400, 550)),
        Button("exit", (400, 650)),
    ]

    background = pygame.transform.scale(pygame.image.load("assets/background/pause-background.png"), (1920, 1020))
    stripe = pygame.transform.scale(pygame.image.load("assets/background/stripe.png"), (600, 1080))
    stripe_rect = stripe.get_rect()
    stripe_rect.center = (400, 510)

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_buttons(window)
        cls.check_collisions(window)

    @classmethod
    def display_background(cls, window):
        window.blit(cls.background, cls.background.get_rect())
        window.blit(cls.stripe, cls.stripe_rect)

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)
        
    @classmethod
    def check_collisions(cls, window):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                Button.frame_rect.center = button.rect.center
                window.blit(Button.frame, Button.frame_rect)
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
    _one_plot = True  # (to generate one plot per space button, not each frame)

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
        Button("world-icon", (1750, 900), dimension=(100, 100))
    ]

    upgrade_buttons = [
        Button("naturality", (500, 600), image_path="assets/icons/grey-circle.png", dimension=(50,50)),
    ]

    image = pygame.transform.scale(pygame.image.load('assets/background/besi-background.png'),  (1920, 1080))
    rect = image.get_rect()

    grape = pygame.image.load("assets/stuff/grape.png")
    grape = pygame.transform.scale(grape, (grape.get_width()/3, grape.get_height()/3))
    grape_rect = grape.get_rect()
    grape_rect.center = (842, 487)

    pressed_1 = True
    pressed_2 = False

    naturality = 0
    advertisment = 0
    taste = 0


    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_the_grape(window)
        cls.display_grape_bubbles(window)
        cls.display_info_panel(window)
        cls.display_buttons(window)
        cls.display_upgrade_buttons(window)
        cls.display_wine_data(window)
        cls.check_collisions()

    @classmethod
    def display_background(cls, window):
        window.blit(cls.image, cls.rect)

    @classmethod
    def display_the_grape(cls, window):
        window.blit(cls.grape, cls.grape_rect)

    @classmethod
    def display_grape_bubbles(cls, window):
        for bubble in cls.upgrade_buttons:
            window.blit(bubble.image, bubble.rect)

    @classmethod
    def display_info_panel(cls, window):
        panel = pygame.transform.scale(pygame.image.load("assets/stuff/info-panel.png"), (400, 800))
        panel_rect = panel.get_rect()
        panel_rect.center = (1600, 450)
        window.blit(panel, panel_rect)

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)

    @classmethod
    def display_wine_data(cls, window):
        pass

    @classmethod
    def display_upgrade_buttons(cls, window):
        for button in cls.upgrade_buttons:
            window.blit(button.image, button.rect)

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
                            if button.name == "naturality":
                                cls.naturality += 1
                else:
                    cls.pressed_2 = False
                    Music.is_clicked = False

class CountryStatistic:
    buttons = [
        Button("Back", (1700, 900))
    ]

    focus_country = None

    @classmethod
    def update(cls, window):
        cls.display_country(window)
        cls.display_statistics(window)
        cls.display_title(window)
        cls.display_buttons(window)
        cls.check_collisions()

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
            country.rect.center = (500, 500)  # center of remain space
            window.blit(country.image, country.rect)
            del country
    
    @classmethod
    def display_statistics(cls, window):
        transparent_gray = (55, 55, 55, 120)
        transparent_surface = pygame.Surface((400, 980), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, transparent_gray, transparent_surface.get_rect(), border_radius=10)
        window.blit(transparent_surface, (1500, 10))

    @classmethod
    def display_title(cls, window):
        font = pygame.font.Font("assets/font/evil-empire.ttf", 36)
        text = font.render(cls.focus_country.name, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1700, 40)
        window.blit(text, text_rect)

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)

    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                Music.play_click_sound()
                if button.name == "Back":
                    GameState.country_statistic = False
                    GameState.play = True
            else:
                Music.is_clicked = False

class Settings:
    buttons = [
        Button("Back", (960,900))
    ]

    image_path = "assets/background/pause-background.png"
    initial_image = pygame.image.load(image_path)

    background = pygame.transform.scale(pygame.image.load(image_path), (1920, 1020))
    background.set_alpha(50)
    background_rect = background.get_rect()

    back_is = None

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_buttons(window)
        cls.check_collisions()

    @classmethod
    def display_background(cls, window):
        window.fill((0, 0, 0))
        window.blit(cls.background, cls.background_rect)
        color = (55, 55, 55, 120)
        transparent_surface = pygame.Surface((window.get_size()[0] - 60, 950), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, color, transparent_surface.get_rect(), border_radius=10)
        window.blit(transparent_surface, (30, 30))

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)
    
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
        Button("upgrade_menu", (1750,900), dimension=(100, 100)),
        Button("statistics", (170, 900),),
    ]

    stats_bars = [
        # ProgressBar(0, Profit.TARGET_PROFIT, 200, 30, (100, 10, 10), (255, 255, 255), (30, 700), getter=BarsGetters.get_world_progress),
    ]

    image = pygame.transform.scale(pygame.image.load("assets/background/oceans-4k.png"), (1920, 1080))
    initial_background = pygame.image.load("assets/background/oceans-4k.png")
    background_rect = initial_background.get_rect()
    background_rect.center = (960, 540)
    
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
        window.blit(cls.initial_background, cls.background_rect)
        window.blit(cls.image, cls.rect)
        Country.update(window, Map, GameState, CountryStatistic)
        Tranport.update(window, Map)
        Map.personal_update(window)

    @classmethod
    def personal_update(cls, window):
        cls.display_buttons(window)
        cls.display_stats_bars(window)
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

        cls.image = pygame.transform.scale(cls.initial_background, (cls.scale*cls.width, cls.scale*cls.height))
        cls.rect = cls.image.get_rect()

        if cls.scale == 1:
            cls.rect.topleft = (0,0)
        else:
            cls.rect.center = cls.last_pos

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)

    @classmethod
    def display_stats_bars(cls, window):
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
    def update_timer(cls):
        if cls.frame >= 60:
            cls.frame = 1
            cls.current_time += datetime.timedelta(weeks=1)
        else:
            cls.frame += 1

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
    def get_time(cls):
        return f"{cls.current_time.day}/{cls.current_time.month}/{cls.current_time.year}"

class News:
    buttons = [
        Button("okay", (600, 750))
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
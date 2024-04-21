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

    mouse_button_was_pressed = None
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
            graph.update()
            Map.update(window)
            Timer.update(window)
            News.update(window)
        if GameState.statistic:
            Statistic.update(window)
        if GameState.settings:
            Settings.update(window)
        
        cls.mouse_button_was_pressed = pygame.mouse.get_pressed()[0]


class MainMenu:
    buttons = [
        Button('start', (300, 270)),
        Button('settings', (300, 360)),
        Button('exit', (300, 450)),
    ]

    background = pygame.transform.scale(pygame.image.load('assets/background/main-background.png'), (1280, 720))
    stripe = pygame.transform.scale(pygame.image.load('assets/background/stripe.png'), (400, 720))
    stripe_rect = stripe.get_rect()
    stripe_rect.center = (300, 360)


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
        font_path = 'assets/font/evil-empire.ttf'
        font_size = 56
        font_color = (0, 0, 0)
        font = pygame.font.Font(font_path, font_size)

        text = 'Moldova Inc.'
        text_surface = font.render(text, True, font_color)
        window.blit(text_surface, (165, 100))

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
            if button.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                Music.play_click_sound()
                if button.name == 'start':
                    GameState.main_menu = False
                    GameState.play = True
                elif button.name == 'settings':
                    Settings.back_is = 'main_menu'
                    GameState.main_menu = False
                    GameState.settings = True
                elif button.name == 'exit':
                    sys.exit()
            else:
                Music.is_clicked = False
    
class Pause:
    buttons = [
        Button('resume', (300, 270)),
        Button('settings', (300, 360)),
        Button('exit', (300, 450)),
    ]

    background = pygame.transform.scale(pygame.image.load('assets/background/pause-background.png'), (1280, 720))
    stripe = pygame.transform.scale(pygame.image.load('assets/background/stripe.png'), (400, 720))
    stripe_rect = stripe.get_rect()
    stripe_rect.center = (300, 360)

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_buttons(window)
        cls.check_collisions()

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
            if button.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                if button.name == 'resume':
                    GameState.pause = False
                    GameState.play = True
                elif button.name == 'settings':
                    Settings.back_is = 'pause'
                    GameState.pause = False
                    GameState.settings = True
                elif button.name == 'exit':
                    sys.exit()


class Statistic:
    _one_plot = True  # to generate one plot per space button, not each frame

    buttons = [
        Button('Back', (640, 600))
    ]

    image_path = 'assets/background/pause-background.png'
    initial_image = pygame.image.load(image_path)

    background = pygame.transform.scale(pygame.image.load(image_path), (1280, 720))
    background.set_alpha(50)

    back_is = None

    @classmethod
    def update(cls, window):
        cls.display_buttons(window)
        cls.display_plot(window)
        cls.check_collisions()

    @classmethod
    def display_plot(cls, window):
        if Statistic._one_plot:
            x = np.linspace(0, 10, 100) 
            y = np.sin(x)  
            plt.plot(x, y)
            plt.title('Wine Selled')
            plt.savefig('plot.png')

            plot = pygame.image.load('plot.png')
            window.blit(plot, (0,0))
            Statistic._one_plot = False
        else:
            plot = pygame.image.load('plot.png')
            window.blit(plot, (0,0))
    
    @classmethod
    def delete_plot(self):
        os.remove('plot.png')
        pass

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)
    
    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                Music.play_click_sound()
                if button.name == 'Back':
                    GameState.statistic = False
                    GameState.play = True

class UpgradeMenu:
    buttons = [
        Button('map', (976, 609), image_path='assets/upgrade-elements/besi-button.png', dimension=None),
        Button('soon', (1120, 609), image_path='assets/upgrade-elements/besi-button.png', dimension=None),
    ]   

    upgrade_buttons = [
        Button('naturality', (316, 249), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('heart', (420, 249), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('Coming Soon', (265, 340), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('advertisment', (368, 340), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('taste', (474, 340), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('Coming Soon', (210, 432), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('Coming Soon', (316, 432), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('time', (423, 432), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('Coming Soon', (159, 524), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('Coming Soon', (264, 524), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('Coming Soon', (369, 524), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
        Button('Coming Soon', (474, 524), image_path='assets/upgrade-elements/grey-circle.png', dimension=None),
    ]

    skills_icons = [
        ['assets/upgrade-elements/quality-skill.png', (316, 247.5)],
        ['assets/upgrade-elements/coming-soon-skill.png', (420, 251)],
        ['assets/upgrade-elements/coming-soon-skill.png', (264, 340)],
        ['assets/upgrade-elements/money-skill.png', (369, 337)],
        ['assets/upgrade-elements/am-skill.png', (476, 337)],
        ['assets/upgrade-elements/coming-soon-skill.png', (212, 432)],
        ['assets/upgrade-elements/coming-soon-skill.png', (319, 432)],
        ['assets/upgrade-elements/coming-soon-skill.png', (419, 429.5)],
        ['assets/upgrade-elements/coming-soon-skill.png', (160, 524)],
        ['assets/upgrade-elements/coming-soon-skill.png', (264, 524)],
        ['assets/upgrade-elements/coming-soon-skill.png', (369, 524)],
        ['assets/upgrade-elements/coming-soon-skill.png', (477, 524)],
    ]

    naturality_prices = [10_000, 12_000, 15_000, 15_000, 15_000, 15_000, 15_000, 15_000, 15_000, 15_000]
    naturality_index = 0
    taste_prices = [5_000, 6_000, 7_000, 7_000, 7_000, 7_000, 7_000, 7_000, 7_000, 7_000]
    taste_index = 0
    advertisment_prices = [2_000, 3_000, 4_000, 4_000, 4_000, 4_000, 4_000, 4_000, 4_000, 4_000]
    advertisment_index = 0

    skill_description = {
        'naturality' : ['Add naturality +1', f'Cost: {naturality_prices[naturality_index]}'],
        'taste' : ['Add taste +1', f'Cost: {taste_prices[taste_index]}'],
        'advertisment' : ['Add advertisment +1', f'Cost: {advertisment_prices[advertisment_index]}'],
    }

    stats_bars = [
        ProgressBar(0, 10000, 200, 30, (100, 10, 10), (255, 255, 255), (30, 650), getter=BarsGetters.get_wine_naturality),
        ProgressBar(0, 10000, 200, 30, (100, 10, 10), (255, 255, 255), (330, 650), getter=BarsGetters.get_wine_advertisment),
        ProgressBar(0, 10000, 200, 30, (100, 10, 10), (255, 255, 255), (630, 650), getter=BarsGetters.get_wine_taste),
    ]


    image = pygame.transform.scale(pygame.image.load('assets/background/besi-background.png'),  (1280, 720))
    rect = image.get_rect()

    grape = pygame.image.load('assets/upgrade-elements/grape.png')
    grape_rect = grape.get_rect()
    grape_rect.center = (448, 352)

    pressed_1 = True
    pressed_2 = False
    focus = None

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_the_grape(window)
        cls.display_grape_bubbles(window)
        cls.display_icon_skills(window)
        cls.display_info_panel(window)
        cls.display_title(window)
        cls.display_buttons(window)
        cls.display_stats_bars(window)
        cls.check_collisions(window)

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
    def display_icon_skills(cls, window):
        for icon_data in cls.skills_icons:
            icon = pygame.image.load(icon_data[0])
            icon_rect = icon.get_rect()
            icon_rect.center = icon_data[1]
            window.blit(icon, icon_rect)

    @classmethod
    def display_info_panel(cls, window):
        panel = pygame.image.load('assets/upgrade-elements/info-panel.png')
        panel_rect = panel.get_rect()
        panel_rect.center = (1046.50, 360)
        window.blit(panel, panel_rect)

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)
    
    @classmethod
    def display_stats_bars(cls, window):
        for bar in cls.stats_bars:
            bar.update(window)
    
    @classmethod
    def display_title(cls, window):
        if cls.focus == None:
            text = 'Skill'
        else:
            text = cls.focus.name

        font = pygame.font.Font('assets/font/evil-empire.ttf', 36)
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1046.50, 140)
        window.blit(text, text_rect)

    @classmethod
    def check_collisions(cls , window):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                    Music.play_click_sound()
                    if not cls.pressed_1:
                        cls.pressed_1 = True
                        if button.name == 'map':
                            GameState.upgrade_menu = False
                            GameState.play = True
                else:
                    cls.pressed_1 = False
                    Music.is_clicked = False
        
        for button in cls.upgrade_buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                cls.display_info_about_skill(window, button)
                cls.focus = button
                if pygame.mouse.get_pressed()[0]:
                    Music.play_click_sound()
                    if not cls.pressed_2:
                        cls.pressed_2 = True
                        if pygame.mouse.get_pressed()[0]:
                            if button.name == 'naturality':
                                if cls.naturality_index == -1:  # If it's full marked, skip interaction with this button
                                    return
                                if Graph.total_income >= cls.naturality_prices[cls.naturality_index]:
                                    Graph.total_income -= cls.naturality_prices[cls.naturality_index]
                                    cls.naturality_index += 1
                                    Wine.naturality += 100
                                    if cls.naturality_index == 9:
                                        button.image = pygame.image.load('assets/upgrade-elements/purple-circle.png')
                                        cls.naturality_index = -1  # Mark full upgraded skill

                            elif button.name == 'advertisment':
                                if cls.advertisment_index == -1:  # If it's full marked, skip interaction with this button
                                    return
                                if Graph.total_income >= cls.advertisment_prices[cls.advertisment_index]:
                                    Graph.total_income -= cls.advertisment_prices[cls.advertisment_index]
                                    cls.advertisment_index += 1
                                    Wine.advertisment += 100
                                    if cls.advertisment_index == 9:
                                        button.image = pygame.image.load('assets/upgrade-elements/purple-circle.png')
                                        cls.advertisment_index = -1  # Mark full upgraded skill

                            elif button.name == 'taste':
                                if cls.taste_index == -1:  # If it's full marked, skip interaction with this button
                                    return
                                if Graph.total_income >= cls.taste_prices[cls.taste_index]:
                                    Graph.total_income -= cls.taste_prices[cls.taste_index]
                                    cls.taste_index += 1
                                    Wine.taste += 100
                                    if cls.taste_index == 9:
                                        button.image = pygame.image.load('assets/upgrade-elements/purple-circle.png')
                                        cls.taste_index = -1  # Mark full upgraded skill
                else:
                    cls.pressed_2 = False
                    Music.is_clicked = False

    @classmethod
    def display_info_about_skill(cls, window, button):
        font = pygame.font.SysFont(None, 40)
        cls.update_info_skills()
        try:
            first_text = cls.skill_description[button.name][0]
            second_text = cls.skill_description[button.name][1]
        except:
            first_text = 'Soon'
            second_text = ''

        first_text_surface = font.render(first_text, True, (0, 0, 0))
        first_text_rect = first_text_surface.get_rect()       
        first_text_rect.topleft = (1100, 200)

        second_text_surface = font.render(second_text, True, (0, 0, 0))
        second_text_rect = first_text_surface.get_rect()       
        second_text_rect.topleft = (1100, 250)

        rect = pygame.Rect(830, 100, 270, 450)  # info panel (830, 100) 270x450

        # Set the opacity of the rectangle to 0 (completely transparent)
        rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        rect_surface.fill((255, 255, 255, 0))

        pygame.draw.rect(rect_surface, (0, 0, 0), rect, 2)
        window.blit(rect_surface, rect)

        first_text_rect.clamp_ip(rect)
        second_text_rect.clamp_ip(rect)
        window.blit(first_text_surface, first_text_rect)
        window.blit(second_text_surface, second_text_rect)

    @classmethod
    def update_info_skills(cls):
        cls.skill_description = {
        'naturality' : ['Add naturality +1', f'Cost: {cls.naturality_prices[cls.naturality_index]}'],
        'taste' : ['Add taste +1', f'Cost: {cls.taste_prices[cls.taste_index]}'],
        'advertisment' : ['Add advertisment +1', f'Cost: {cls.advertisment_prices[cls.advertisment_index]}'],
    }

class CountryStatistic:
    buttons = [
        Button('back', (1046, 609), image_path='assets/stuff/button.png', dimension=None),
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
            country.rect.center = (400, 360)  # center of remain space
            window.blit(country.image, country.rect)
            del country
    
    @classmethod
    def display_statistics(cls, window):
        panel = pygame.image.load('assets/stuff/info-panel.png')
        panel_rect = panel.get_rect()
        panel_rect.center = (1046.50, 360)
        window.blit(panel, panel_rect)

    @classmethod
    def display_title(cls, window):
        font = pygame.font.Font('assets/font/evil-empire.ttf', 36)
        text = font.render(cls.focus_country.name, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1046.50, 140)
        window.blit(text, text_rect)

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)

    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                Music.play_click_sound()
                if button.name == 'back':
                    GameState.country_statistic = False
                    GameState.play = True
            else:
                Music.is_clicked = False

class Settings:
    buttons = [
        Button('back', (640, 600))
    ]

    image_path = 'assets/background/pause-background.png'
    initial_image = pygame.image.load(image_path)

    background = pygame.transform.scale(pygame.image.load(image_path), (1280, 720))
    background.set_alpha(50)

    back_is = None

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_buttons(window)
        cls.check_collisions()

    @classmethod
    def display_background(cls, window):
        window.fill((0, 0, 0))
        window.blit(cls.background, cls.background.get_rect())

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)
    
    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                Music.play_click_sound()
                if button.name == 'back':
                    GameState.settings = False
                    if Settings.back_is == 'main_menu':
                        GameState.main_menu = True
                    elif Settings.back_is == 'pause':
                        GameState.pause = True
                    
class Map:
    buttons = [
        Button('upgrade_menu', (1100, 600), dimension=(100,100)),
        Button('statistics', (170, 600)),
    ]

    stats_bars = [
        ProgressBar(0, 100_000, 200, 30, (100, 10, 10), (255, 255, 255), (71, 500), getter=BarsGetters.get_world_progress),
    ]

    image = pygame.transform.scale(pygame.image.load('assets/background/oceans-4k.png'), (1280, 720))
    initial_background = pygame.image.load('assets/background/new-ocean-full-hd.png')

    background_rect = initial_background.get_rect()
    background_rect.center = (640, 360)
    
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

        # Look like a mess because I avoided in this way double click/missclick of Button and Country
        Country.update(window, Map, GameState, CountryStatistic)
        Country.display_countries(window, Map)
        
        Contract.display_contracts(window,Map)

        ToSellButton.display_buttons(window, Map)
        Map.display_buttons(window)
        Tranport.update(window, Map)

        if Map.personal_update(window) != 'changed':  # Checking the Country collision only if map Button were not pressed
            Country.check_collisions(Map, GameState, CountryStatistic)

    @classmethod
    def personal_update(cls, window):
        cls.display_stats_bars(window)
        cls.to_scale()
        cls.to_drag(window)
        if cls.check_collisions() == 'changed':
            return 'changed'


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

        cls.image = pygame.transform.scale(cls.image, (cls.scale*cls.width, cls.scale*cls.height))
        cls.image.set_alpha(255)
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
                if not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                    Music.play_click_sound()
                    if not cls.pressed_icon:
                        cls.pressed_icon = True
                        if button.name == 'upgrade_menu':
                            GameState.play = False
                            GameState.upgrade_menu = True
                        elif button.name == 'statistics':
                            GameState.play = False
                            GameState.statistic = True
                        return 'changed'
                else:
                    cls.pressed_icon = False
                    Music.is_clicked = False
        

class News:
    buttons = [
        Button('okay', (600, 750))
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
    click_sound = pygame.mixer.Sound('assets/sound/click-menu.ogg')
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
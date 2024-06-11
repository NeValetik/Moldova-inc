import pygame, os, sys, datetime, copy
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.dirname(__file__))  # To avoid the error of neighbour files
from objects import *
from logic import *

Wine.init_wines()  # initialization of wines

pygame.init()
pygame.mixer.init()

class ScenesInit:
    @staticmethod    
    def buttons_init():
        directory = "components/saved_game"
        files = os.listdir(directory)
        if len(files) > 1:
            return [
                Button('continue', (300, 270), dimension=(230, 80)),
                Button('start', (300, 360), dimension=(230, 80)),
                Button('settings', (300, 450), dimension=(230, 80)),
                Button('exit', (300, 540), dimension=(230, 80)),
            ]
        else:
            return [
                Button('start', (300, 270), dimension=(230, 80)),
                Button('settings', (300, 360), dimension=(230, 80)),
                Button('exit', (300, 450), dimension=(230, 80)),
            ]
    @staticmethod    
    def upgrade_buttons_init():
            UpgradeMenu.upgrade_buttons = [
                Button('naturality', (316, 249), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('taste', (420, 249), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('Coming Soon', (265, 340), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('advertisment', (368, 340), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('Coming Soon', (474, 340), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('Coming Soon', (210, 432), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('Coming Soon', (316, 432), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('Coming Soon', (423, 432), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('Coming Soon', (159, 524), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('Coming Soon', (264, 524), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('Coming Soon', (369, 524), image_path='assets/upgrade-elements/grey-circle.png'),
                Button('Coming Soon', (474, 524), image_path='assets/upgrade-elements/grey-circle.png'),
            ]
            try:
                with open("components/saved_game/winedata.csv", mode='r') as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        for button in UpgradeMenu.upgrade_buttons:
                            if row.get(button.name+"_index") is not None:
                                if int(row[button.name+"_index"]) == -1:
                                    button.image = pygame.image.load('assets/upgrade-elements/purple-circle.png')
            except:
                pass

class GameState:
    main_menu = True
    play = False
    pause = False
    settings = False
    statistic = False
    country_statistic = False
    upgrade_menu = False
    bar = False
    end_game = False

    mouse_button_was_pressed = None
    mouse_position = None

    @classmethod
    def __init__(cls,minimal_amount,maximal_amount):
        cls.win_condition = maximal_amount
        cls.lose_condtion = minimal_amount

    @classmethod
    def check_end_game(cls,window):
        if BarsGetters.get_world_progress() >= cls.win_condition and EndGameWindow.initialized == False:
            cls.play = False
            EndGameWindow("Victory")
            cls.end_game = True   
        elif BarsGetters.get_world_progress() < cls.lose_condtion and EndGameWindow.initialized == False:
            cls.play = False
            EndGameWindow("Defeat")
            cls.end_game = True   
        

    @classmethod
    def update(cls, window):
        if GameState.main_menu:
            MainMenu.update(window)
        elif GameState.pause:
            Pause.update(window)
        elif GameState.country_statistic:
            Map.update(window)
            CountryStatistic.update(window)
        elif GameState.upgrade_menu:
            UpgradeMenu.update(window)
        elif GameState.bar:
            Bar.update(window)
        elif GameState.play:
            graph.update()
            Map.update(window)
            Timer.update(window)
            cls.check_end_game(window)
            News.update(window)
        
        if GameState.end_game:
            Map.update(window)
            EndGameWindow.update(cls,window)
        if GameState.statistic:
            Statistic.update(window)
        if GameState.settings:
            Settings.update(window)
        
        cls.mouse_button_was_pressed = pygame.mouse.get_pressed()[0]

class MainMenu:
    buttons = ScenesInit.buttons_init()

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
                    exit_game()
                elif button.name == 'continue':
                    ScenesInit.upgrade_buttons_init()
                    GraphInit._initialize()
                    ObjectInit._initialize()
                    GameState.main_menu = False
                    GameState.play = True


            else:
                Music.is_clicked = False
    
class Pause:
    buttons = [
        Button('resume', (300, 270), dimension=(230, 80)),
        Button('settings', (300, 360), dimension=(230, 80)),
        Button('exit', (300, 450), dimension=(230, 80)),
    ]

    background = pygame.transform.scale(pygame.image.load('assets/background/pause-background.png'), (1280, 720))
    stripe = pygame.transform.scale(pygame.image.load('assets/background/stripe.png'), (400, 720))
    stripe_rect = stripe.get_rect()
    stripe_rect.center = (300, 360)

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
            if button.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                if button.name == 'resume':
                    GameState.pause = False
                    GameState.play = True
                elif button.name == 'settings':
                    Settings.back_is = 'pause'
                    GameState.pause = False
                    GameState.settings = True
                elif button.name == 'exit':
                    exit_game()

class Statistic:
    _one_plot = True  # to generate one plot per space button, not each frame

    buttons = [
        Button('Back', (640, 700), dimension=(230, 80))
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
            x = graph.x
            plt.figure(figsize=(12,6))

            y = graph.y
            plt.plot(x, y)
            plt.title('Wine sold')
            plt.xlabel("Date")
            plt.ylabel("Deal")
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
        Button('map', (976, 609), image_path='assets/upgrade-elements/besi-button.png'),
        Button('bar', (1120, 609), image_path='assets/upgrade-elements/besi-button.png'),
    ]   

    upgrade_buttons = {trandmark:[
        Button('naturality', (316, 249), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('taste', (420, 249), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('Coming Soon', (265, 340), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('advertisment', (368, 340), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('Coming Soon', (474, 340), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('Coming Soon', (210, 432), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('Coming Soon', (316, 432), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('Coming Soon', (423, 432), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('Coming Soon', (159, 524), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('Coming Soon', (264, 524), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('Coming Soon', (369, 524), image_path='assets/upgrade-elements/grey-circle.png'),
        Button('Coming Soon', (474, 524), image_path='assets/upgrade-elements/grey-circle.png'),
    ] for trandmark in Wine.trandmarks
    }

    skills_icons = [
        ['assets/upgrade-elements/quality-skill.png', (316, 247.5)],
        ['assets/upgrade-elements/coming-soon-skill.png', (476, 337)],
        ['assets/upgrade-elements/coming-soon-skill.png', (264, 340)],
        ['assets/upgrade-elements/money-skill.png', (369, 337)],
        ['assets/upgrade-elements/am-skill.png', (420, 251)],
        ['assets/upgrade-elements/coming-soon-skill.png', (212, 432)],
        ['assets/upgrade-elements/coming-soon-skill.png', (319, 432)],
        ['assets/upgrade-elements/coming-soon-skill.png', (419, 429.5)],
        ['assets/upgrade-elements/coming-soon-skill.png', (160, 524)],
        ['assets/upgrade-elements/coming-soon-skill.png', (264, 524)],
        ['assets/upgrade-elements/coming-soon-skill.png', (369, 524)],
        ['assets/upgrade-elements/coming-soon-skill.png', (477, 524)],
    ]

    naturality_prices = {
        trademark: [10_000, 12_000, 15_000, 15_000, 15_000, 15_000, 15_000, 15_000, 15_000, 15_000, 15_000]
        for trademark in Wine.trandmarks
    }

    taste_prices = {
        trademark: [5_000, 6_000, 7_000, 7_000, 7_000, 7_000, 7_000, 7_000, 7_000, 7_000, 7_000]
        for trademark in Wine.trandmarks
    }

    advertisment_prices = {
        trademark: [2_000, 3_000, 4_000, 4_000, 4_000, 4_000, 4_000, 4_000, 4_000, 4_000, 7_000]
        for trademark in Wine.trandmarks
    }

    skill_description = {
        # wine.name: {
            'naturality': [
                'Add naturality +1',
                f'Cost: {naturality_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.naturality_index]}'
            ],
            'taste': [
                'Add taste +1',
                f'Cost: {taste_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.taste_index]}'
            ],
            'advertisment': [
                'Add advertisement +1',
                f'Cost: {advertisment_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.advertisment_index]}'
            ]
        }
        # for wine in Wine.wines
    # }

    stats_bars = {wine.name:{
        'naturality':      ProgressBar(0, 10_000, 200, 30, (100, 10, 10), (255, 255, 255), (955, 520), getter=BarsGetters.get_wine_naturality,getter_attributes=wine),
        'advertisment':    ProgressBar(0, 10_000, 200, 30, (100, 10, 10), (255, 255, 255), (955, 520), getter=BarsGetters.get_wine_advertisment,getter_attributes=wine),
        'taste':           ProgressBar(0, 10_000, 200, 30, (100, 10, 10), (255, 255, 255), (955, 520), getter=BarsGetters.get_wine_taste,getter_attributes=wine),
    }for wine in Wine.wines
    }
    

    image = pygame.transform.scale(pygame.image.load('assets/background/besi-background.png'),  (1280, 720))
    rect = image.get_rect()

    grape = pygame.image.load('assets/upgrade-elements/grape.png')
    grape_rect = grape.get_rect()
    grape_rect.center = (448, 352)

    pressed_1 = True
    pressed_2 = False
    focus =     None

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_the_grape(window)
        cls.display_grape_bubbles(window)
        cls.display_icon_skills(window)
        cls.display_info_panel(window)
        cls.display_buttons(window)
        cls.check_collisions(window)

    @classmethod
    def display_background(cls, window):
        window.blit(cls.image, cls.rect)

    @classmethod
    def display_the_grape(cls, window):
        window.blit(cls.grape, cls.grape_rect)

    @classmethod
    def display_grape_bubbles(cls, window):
        for bubble in cls.upgrade_buttons[Wine.focus_on_wine.name]:
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
        try:
            cls.stats_bars[Wine.focus_on_wine.name][cls.focus.name].update(window)
        except:
            pass
    
    @classmethod
    def display_title(cls, window):
        if cls.focus == None:
            text = 'Skill'
        else:
            text = cls.focus.name

        font = pygame.font.Font('assets/font/lexend.ttf', 36)
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
                        elif button.name == 'bar':
                            GameState.upgrade_menu = False
                            GameState.bar = True
                else:
                    cls.pressed_1 = False
                    Music.is_clicked = False
        
        for button in cls.upgrade_buttons[Wine.focus_on_wine.name]:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                cls.focus = button
                cls.display_info_about_skill(window, button)
                cls.display_title(window)
                cls.display_stats_bars(window)

                if pygame.mouse.get_pressed()[0]:
                    Music.play_click_sound()
                    if not cls.pressed_2:
                        cls.pressed_2 = True
                        if pygame.mouse.get_pressed()[0]:
                            if button.name == 'naturality':
                                if Wine.focus_on_wine.naturality_index == -1:  # If it's full marked, skip interaction with this button
                                    return
                                if Graph.total_income >= cls.naturality_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.naturality_index]:
                                    Graph.total_income -= cls.naturality_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.naturality_index]
                                    Wine.focus_on_wine.naturality_index += 1
                                    Wine.focus_on_wine.naturality += 1000
                                    if Wine.focus_on_wine.naturality_index == 10:
                                        button.image = pygame.image.load('assets/upgrade-elements/purple-circle.png')
                                        Wine.focus_on_wine.naturality_index = -1  # Mark full upgraded skill

                            elif button.name == 'advertisment':
                                if Wine.focus_on_wine.advertisment_index == -1:  # If it's full marked, skip interaction with this button
                                    return
                                if Graph.total_income >= cls.advertisment_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.advertisment_index]:
                                    Graph.total_income -= cls.advertisment_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.advertisment_index]
                                    Wine.focus_on_wine.advertisment_index += 1
                                    Wine.focus_on_wine.advertisment += 1000
                                    if Wine.focus_on_wine.advertisment_index == 10:
                                        button.image = pygame.image.load('assets/upgrade-elements/purple-circle.png')
                                        Wine.focus_on_wine.advertisment_index = -1  # Mark full upgraded skill

                            elif button.name == 'taste':
                                if Wine.focus_on_wine.taste_index == -1:  # If it's full marked, skip interaction with this button
                                    return
                                if Graph.total_income >= cls.taste_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.taste_index]:
                                    Graph.total_income -= cls.taste_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.taste_index]
                                    Wine.focus_on_wine.taste_index += 1
                                    Wine.focus_on_wine.taste += 1000
                                    if Wine.focus_on_wine.taste_index == 10:
                                        button.image = pygame.image.load('assets/upgrade-elements/purple-circle.png')
                                        Wine.focus_on_wine.taste_index = -1  # Mark full upgraded skill
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
        first_text_rect.topleft = (900, 200)

        second_text_surface = font.render(second_text, True, (0, 0, 0))
        second_text_rect = first_text_surface.get_rect()       
        second_text_rect.topleft = (900, 250)

        window.blit(first_text_surface, first_text_rect)
        window.blit(second_text_surface, second_text_rect)

    @classmethod
    def update_info_skills(cls):
        cls.skill_description = {
            'naturality': [
                'Add naturality +1',
                f'Cost: {cls.naturality_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.naturality_index]}'
            ],
            'taste': [
                'Add taste +1',
                f'Cost: {cls.taste_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.taste_index]}'
            ],
            'advertisment': [
                'Add advertisement +1',
                f'Cost: {cls.advertisment_prices[Wine.focus_on_wine.name][Wine.focus_on_wine.advertisment_index]}'
            ]
    }

class CountryStatistic:
    buttons = [
        Button('back', (1046, 609), image_path='assets/stuff/button.png'),
    ]

    focus_country = None

    @classmethod
    def initialize_statistics(cls):
        cls.country_description = {country.name: ["Naturality low" if country.naturality_coef < 0.4 else("Naturality middle" if 0.6>country.naturality_coef > 0.4 else "Naturality high"),
                                          "Advertisment low" if country.advertisment_coef < 0.4 else("Advertisment middle" if 0.6>country.advertisment_coef > 0.4 else "Advertisment high"),
                                          "Taste low" if country.taste_coef < 0.4 else("Taste middle" if 0.6>country.taste_coef > 0.4 else "Taste high"),
                                          f"Naturality needed {int(country.contract_condition_naturality)}",
                                          f"Advertisment needed {int(country.contract_condition_advertisment)}",
                                          f"Taste needed {int(country.contract_condition_taste)}"] for country in Country.countries}

    @classmethod
    def update(cls, window):
        cls.initialize_statistics()
        cls.transparent_background(window)
        cls.display_country(window)
        cls.display_statistics(window)
        cls.display_title(window)
        cls.display_buttons(window)
        cls.display_info_about_country(window,cls.focus_country)
        cls.check_collisions()

    @classmethod
    def transparent_background(cls, window):
        background = pygame.Surface((1280, 720))
        background.fill((255, 255, 255))
        background.set_alpha(230)
        window.blit(background, (0, 0))

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
            country.rect.center = (400, 360)
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
        font = pygame.font.Font('assets/font/lexend-bold.ttf', 36)
        text = font.render(cls.focus_country.name, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1046.50, 140)
        window.blit(text, text_rect)

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)

    @classmethod
    def display_info_about_country(cls, window, country):
        font = pygame.font.Font('assets/font/lexend.ttf', 23)
        try:
            first_text = cls.country_description[country.name][0]
            second_text = cls.country_description[country.name][1]
            third_text = cls.country_description[country.name][2]
            fourth_text = cls.country_description[country.name][3]
            fifth_text = cls.country_description[country.name][4]
            sixth_text = cls.country_description[country.name][5]
        except:
            first_text = 'Soon'
            second_text = ''

        first_text_surface = font.render(first_text, True, (0, 0, 0))
        first_text_rect = first_text_surface.get_rect()       
        first_text_rect.topleft = (900, 200)

        second_text_surface = font.render(second_text, True, (0, 0, 0))
        second_text_rect = first_text_surface.get_rect()       
        second_text_rect.topleft = (900, 250)

        third_text_surface = font.render(third_text, True, (0, 0, 0))
        third_text_rect = first_text_surface.get_rect()       
        third_text_rect.topleft = (900, 300)

        fourth_text_surface = font.render(fourth_text, True, (0, 0, 0))
        fourth_text_rect = first_text_surface.get_rect()       
        fourth_text_rect.topleft = (900, 350)

        fifth_text_surface = font.render(fifth_text, True, (0, 0, 0))
        fifth_text_rect = first_text_surface.get_rect()       
        fifth_text_rect.topleft = (900, 400)

        sixth_text_surface = font.render(sixth_text, True, (0, 0, 0))
        sixth_text_rect = first_text_surface.get_rect()       
        sixth_text_rect.topleft = (900, 450)

        window.blit(first_text_surface, first_text_rect)
        window.blit(second_text_surface, second_text_rect)
        window.blit(third_text_surface, third_text_rect)
        window.blit(fourth_text_surface, fourth_text_rect)
        window.blit(fifth_text_surface, fifth_text_rect)
        window.blit(sixth_text_surface, sixth_text_rect)

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

    music_state = Button('off', (720, 280), size=(60, 49))
    sound_effect_state = Button('off', (720, 330), size=(60, 49))

    
    image_path = 'assets/background/pause-background.png'
    initial_image = pygame.image.load(image_path)

    background = pygame.transform.scale(pygame.image.load(image_path), (1280, 720))
    background.set_alpha(50)

    back_is = None

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.dislplay_text(window)
        cls.display_buttons(window)
        cls.check_collisions()

    @classmethod
    def display_background(cls, window):
        window.fill((0, 0, 0))
        window.blit(cls.background, cls.background.get_rect())

    @classmethod
    def dislplay_text(cls, window):
        font = pygame.font.Font('assets/font/lexend.ttf', 48)
        text = 'Music is ' + cls.music_state.name
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect = (500, 250)
        window.blit(text_surface, text_rect)

        font = pygame.font.Font('assets/font/lexend.ttf', 48)
        text = 'Sound effect is ' + cls.sound_effect_state.name
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect = (340, 300)

        window.blit(text_surface, text_rect)

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
        if cls.music_state.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                Music.play_click_sound()
                if cls.music_state.name == 'on':
                    pygame.mixer.music.set_volume(0)
                    cls.music_state.name = 'off'
                elif cls.music_state.name == 'off':
                    pygame.mixer.music.set_volume(0.5)
                    cls.music_state.name = 'on'
        elif cls.sound_effect_state.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                Music.play_click_sound()
                if cls.sound_effect_state.name == 'on':
                    cls.sound_effect_state.name = 'off'
                    Music.click_sound_is_allowed = False
                elif cls.sound_effect_state.name == 'off':
                    Music.click_sound_is_allowed = True
                    cls.sound_effect_state.name = 'on'
                    
                    
class Map:
    buttons = [
        Button('upgrade_menu', (1100, 670), image_path='assets/stuff/menu-button.png'),
        Button('statistics', (170, 670), image_path='assets/stuff/menu-button.png'),
    ]

    stats_bars = [
        ProgressBar(0, 1_000_000, 200, 30, (100, 10, 10), (255, 255, 255), (71, 600), getter=BarsGetters.get_world_progress),
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

        GameState(cls.stats_bars[0].start_value,cls.stats_bars[0].max_value)
        # Looks like a mess because I avoided in this way double click/missclick of Button and Country
        Country.update(window, Map, GameState, CountryStatistic)
        Country.display_countries(window, Map)
        
        Contract.display_contracts(window,Map)

        ToSellButton.display_buttons(window, Map)
        Map.display_buttons(window)
        Transport.update(window, Map, graph)

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
        
    
class Music:
    click_sound = pygame.mixer.Sound('assets/sound/click-menu.ogg')
    is_clicked = False
    click_sound_is_allowed = False

    @classmethod
    def initiate_background_music(cls):
        pygame.mixer.init()
        pygame.mixer.music.load('assets/sound/theme.ogg')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0)

    @classmethod
    def play_click_sound(cls):
        if not cls.is_clicked and cls.click_sound_is_allowed:
            cls.click_sound.play()
            cls.is_clicked = True        

class Bar:
    buttons = [
        Button('map', (976, 609), image_path='assets/upgrade-elements/besi-button.png'),
        Button('upgrade', (1120, 609), image_path='assets/upgrade-elements/besi-button.png'),
    ]   

    # Static elements will not collide with anything
    static_elements = [
        Button('assets/upgrade-wine/rect.png', (1046, 357), image_path='assets/upgrade-wine/rect.png'),
        Button('assets/upgrade-wine/rect.png', (1046, 583.5), image_path='assets/upgrade-wine/table.png'),

        Button('assets/upgrade-wine/rect.png', (204.00, 263.5), image_path='assets/upgrade-wine/small-white-wine.png'),
        Button('assets/upgrade-wine/rect.png', (204, 500.5), image_path='assets/upgrade-wine/small-red-wine.png'),
        Button('assets/upgrade-wine/rect.png', (565.00,263.5), image_path='assets/upgrade-wine/small-pink-wine.png'),
        Button('assets/upgrade-wine/rect.png', (565, 500.5), image_path='assets/upgrade-wine/small-sparkling-wine.png'),
    ]

    # Elements that will (check collision and) change big wine glass
    dynamic_elements = [
        Button('support-rect-1', (213, 264), image_path='assets/upgrade-wine/support-rect.png'),
        Button('support-rect-2', (568, 264), image_path='assets/upgrade-wine/support-rect.png'),
        Button('support-rect-3', ( 213, 501), image_path='assets/upgrade-wine/support-rect.png'),
        Button('support-rect-4', (568, 501), image_path='assets/upgrade-wine/support-rect.png'),

        Button('tag-1', (320.5, 261.5), image_path='assets/upgrade-wine/tag.png'),
        Button('tag-2', (684.5, 261.5), image_path='assets/upgrade-wine/tag.png'),
        Button('tag-3', (320.5, 498.5), image_path='assets/upgrade-wine/tag.png'),
        Button('tag-4', (684.5, 498.5), image_path='assets/upgrade-wine/tag.png'),
    ]

    image = pygame.image.load('assets/upgrade-wine/background.png')
    rect = image.get_rect()

    pressed_1 = True
    pressed_2 = False
    focus =     None

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        cls.display_static_and_dynamic_elements(window)
        cls.display_buttons(window)
        cls.display_title(window)
        cls.display_wine_information(window)
        cls.check_collisions(window)  # check collisions + load and display big wine glass

    @classmethod
    def display_background(cls, window):
        window.blit(cls.image, cls.rect)

    @classmethod
    def display_static_and_dynamic_elements(cls, window):
        for button in cls.dynamic_elements:
            window.blit(button.image, button.rect)
        for button in cls.static_elements:
            window.blit(button.image, button.rect)

    @classmethod
    def display_buttons(cls, window):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)

    
    @classmethod
    def display_title(cls, window):
        if Wine.focus_on_wine.name == 'red-wine':
            text = 'Red Wine'
        if Wine.focus_on_wine.name == 'pink-wine':
            text = 'Pink Wine'
        if Wine.focus_on_wine.name == 'sparkling-wine':
            text = 'Sparkling Wine'
        if Wine.focus_on_wine.name == 'white-wine':
            text = 'White Wine'

        font = pygame.font.Font('assets/font/lexend.ttf', 36)
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1046.50, 140)
        window.blit(text, text_rect)
    
    @classmethod
    def display_wine_information(cls, window):
        pass

    @classmethod
    def check_collisions(cls , window):
        if Wine.focus_on_wine.name == 'red-wine':
            big_wine = pygame.image.load('assets/upgrade-wine/big-red-wine.png')
        elif Wine.focus_on_wine.name == 'sparkling-wine':
            big_wine = pygame.image.load('assets/upgrade-wine/big-sparkling-wine.png')
        elif Wine.focus_on_wine.name == 'pink-wine':
            big_wine = pygame.image.load('assets/upgrade-wine/big-pink-wine.png')
        elif Wine.focus_on_wine.name == 'white-wine':
            big_wine = pygame.image.load('assets/upgrade-wine/big-white-wine.png')

        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                    Music.play_click_sound()
                    if not cls.pressed_1:
                        cls.pressed_1 = True
                        if button.name == 'map':
                            GameState.bar = False
                            GameState.play = True
                        elif button.name == 'upgrade':
                            GameState.bar = False
                            GameState.upgrade_menu = True
                else:
                    cls.pressed_1 = False
                    Music.is_clicked = False

        # Displaying big glass of wine and change the selling wine on click
        for button in cls.dynamic_elements:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                cls.focus = button
                
                if not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                    Music.play_click_sound()
                    if not cls.pressed_1:
                        cls.pressed_1 = True
                        if cls.focus.name == 'tag-1' or cls.focus.name == 'support-rect-1':
                                Wine.change_focus('white-wine')
                        elif cls.focus.name == 'tag-2' or cls.focus.name == 'support-rect-2':
                                Wine.change_focus('pink-wine')
                        elif cls.focus.name == 'tag-3' or cls.focus.name == 'support-rect-3':
                                Wine.change_focus('red-wine')
                        elif cls.focus.name == 'tag-4' or cls.focus.name == 'support-rect-4':
                                Wine.change_focus('sparkling-wine')
                else:
                    cls.pressed_1 = False
                    Music.is_clicked = False

        big_wine_rect = big_wine.get_rect()
        big_wine_rect.center = (1041.5, 396)
        window.blit(big_wine, big_wine_rect)


class News:

    # Elements that will (check collision and) change 'big' wine 
    image = NewsItem.make_surface(size = (450,50))
    rect = image.get_rect()
    rect.center = (640,670)

    @classmethod
    def update(cls, window):
        cls.display_background(window)
        NewsItem.update(window)
        # cls.display_static_and_dynamic_elements(window)

    @classmethod
    def display_background(cls, window):
        window.blit(cls.image, cls.rect)

           

pygame.quit()
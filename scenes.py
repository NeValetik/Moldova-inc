import pygame, random, os, sys, math
import matplotlib.pyplot as plt
import numpy as np
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
        if GameState.play:
            ToSellButton.one_time_activation()
            Map.update(window)
            Plane.display_planes(window)
        # if GameState.country_statistic:
        #     CountryStatistic.update()
        if GameState.statistic:
            Statistic.update(window)
        if GameState.upgrade_menu:
            UpgradeMenu.update(window)
        if GameState.pause:
            Pause.update(window)
        if GameState.settings:
            Settings.update(window)

class Button(pygame.sprite.Sprite):
    def __init__(self, name, image_path, position, rescale=None):
        super().__init__()
        self.name = name
        if rescale == None:
            self.image = pygame.image.load(os.path.join(os.getcwd(),image_path))
        else:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(),image_path)), rescale)
        self.rect = self.image.get_rect()
        self.rect.center = position

class MainMenu:
    buttons = [
        Button("start", "images/buttons/start-btn.png", (400, 350)),
        # Button("settings", "images/buttons/settings-btn.png", (400, 450)),
        Button("exit", "images/buttons/exit-btn.png", (400, 550)),
    ]

    @classmethod
    def update(cls, window):
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
                    pass
                elif button.name == "exit":
                    sys.exit()

class Pause:
    buttons = [
        Button("resume", "images/buttons/resume-btn.png", (400, 350)),
        # Button("settings", "images/buttons/settings-btn.png", (400, 450)),
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
                    pass
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

    image = pygame.transform.scale(pygame.image.load('images/cellar.jpg'),  (1200,800))
    rect = image.get_rect()
    pressed = False

    @classmethod
    def update(cls, window):
        window.blit(cls.image, cls.rect)
        cls.display_buttons(window)
        cls.check_collisions()

    @classmethod
    def display_buttons(cls, window):
        for button in UpgradeMenu.buttons:
            window.blit(button.image, button.rect)

    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    if not cls.pressed:
                        cls.pressed = True
                        if button.name == "world-icon":
                            GameState.upgrade_menu = False
                            GameState.play = True
                else:
                    cls.pressed = False
            


class Settings:
    buttons = [
        # soon
    ]

    @classmethod
    def update(cls, window):
        cls.display_buttons(window)

    @classmethod
    def display_buttons(cls, window):
        for button in cls.buttons:
            window.blit(button.image, button.rect)

class Map:
    buttons = [
        Button("upgrade_menu", "images/buttons/cellar-icon-btn.png", (1150,750), (100, 100)),
        # Button("statistics", "images/stats.png", (630,480)),
        # Button("settings", "images/settings.png", (620,480)),
    ]

    image = pygame.image.load("images/map.jpg")
    initial_image = pygame.image.load("images/map.jpg")

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
        window.blit(cls.image, cls.rect)
        cls.display_buttons(window)
        cls.to_scale()
        cls.to_drag()
        cls.check_collisions()
        ToSellButton.display_buttons(window)
        ToSellButton.check_collisions()

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
            if cls.scale >= 1.9:
                cls.scale = 2
            else:
                cls.scale += 0.1
        elif cls.scroll == -1:  
            if cls.scale <= 1.1:
                cls.scale = 1
            else:  
                cls.scale -= 0.1
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
                else:
                    cls.pressed_icon = False


class ToSellButton(pygame.sprite.Sprite):
    coor = {
        "Canada": (230,230),
        "Republic of Moldova": (685,316),
        "China": (948,371),
        "USA": (228,349),
    }

    initiated = False  # For first and last initiation
    buttons = []
    

    def __init__(self, name, pos):
        super().__init__()
        self.name = name
        self.pos = pos
        self.is_available = False
        self.image = pygame.transform.scale(pygame.image.load("images/wine.png"), (50, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos[0], self.pos[1])


    @classmethod
    def one_time_activation(cls):
        if not cls.initiated:
            cls.initiated = True
            for country, coor in cls.coor.items():
                cls.buttons.append(ToSellButton(country, coor))


    @classmethod
    def display_buttons(cls, window):
        cls.random_availability()

        for button in [button for button  in cls.buttons if button.is_available]:
            button.rect.center = (Map.rect.topleft[0] + Map.scale*button.pos[0],
                                Map.rect.topleft[1] + Map.scale*button.pos[1])

            if button.is_available:
                window.blit(button.image, button.rect)

    @classmethod
    def random_availability(cls):
        for button in cls.buttons:
            if random.randint(1, 100) == 1:
                button.is_available = True

    @classmethod
    def check_collisions(cls):
        for button in cls.buttons:
            if button.is_available and button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    button.is_available = False
                    if button.pos != (685,316):
                        Plane(button.pos)



class Plane(pygame.sprite.Sprite):
    planes = []

    def __init__(self, destination):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/plane.png"), (30,30)).convert_alpha()
        self.initial_image = pygame.transform.scale(pygame.image.load("images/plane.png"), (30,30)).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
         
        self.origin = (685,316)  # Moldova
        self.destination = destination
        self.rect.center = self.origin

        self.before_middle_point = True
        self.path = Plane.get_path(self.origin, self.destination)
        self.middle_point = self.path[len(self.path) // 2]
        Plane.planes.append(self)

    @classmethod
    def display_planes(cls, window):
        for plane in Plane.planes:
            if len(plane.path) <= 1:
                del plane
            else:
                plane.rect.center = (Map.rect.topleft[0] + Map.scale*plane.path[0][0],
                                    Map.rect.topleft[1] + Map.scale*plane.path[0][1])

                # Look at middle point (before middle point), look at destination (after middle point)
                if plane.before_middle_point and plane.path[0] != plane.middle_point:
                    plane.before_middle_point = False
                    plane.image = pygame.transform.rotate(plane.image, -120 + Plane.angle_between_points(plane.origin, plane.middle_point))
                elif plane.path[0] == plane.middle_point:
                    plane.image = pygame.transform.rotate(plane.image, -150 + Plane.angle_between_points(plane.middle_point, plane.destination))
                

                window.blit(plane.image, plane.rect)
                del plane.path[0]
        
    @classmethod
    def get_path(cls, c1, c2):
        middle_point = (min([c1[0], c2[0]]) + (abs(c1[0] - c2[0]) / 2), min([c1[1], c2[1]]) + (abs(c1[1] - c2[1]) / 2))
        direction_vector = (c2[0] - c1[0], c2[1] - c1[1])

        perp_vect = (-direction_vector[1], direction_vector[0])
        magnitude = math.sqrt(sum(component**2 for component in perp_vect))
        normalized_perp_vector = (perp_vect[0] / magnitude, perp_vect[1] / magnitude)

        distance = 100
        third_point = (middle_point[0] + normalized_perp_vector[0]*distance, middle_point[1] + normalized_perp_vector[1]*distance)
        

        x_values = [c1[0], third_point[0], c2[0]]
        y_values = [c1[1], third_point[1], c2[1]]
            
        x = np.array(x_values)
        y = np.array(y_values)
        coefficients = np.polyfit(x, y, 2)  # Fit a quadratic polynomial (degree 2)
        curve_x = np.linspace(int(min(x)), int(max(x)), int(max(x)-min(x)+1))
        curve_y = np.polyval(coefficients, curve_x)
        coordinates = [(x_val, y_val) for x_val, y_val in zip(curve_x, curve_y)]

        if c1[0] > c2[0]:
            coordinates.sort(reverse=True)
        return coordinates
    
    @classmethod
    def angle_between_points(cls, point1, point2):
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        angle = math.degrees(math.atan2(dy, dx))
        angle_degrees = angle % 360
        return angle_degrees
                

class Ship(pygame.sprite.Sprite):
    ships = []

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/ship.png"), (30,30)).convert_alpha()
        self.initial_image = pygame.transform.scale(pygame.image.load("images/ship.png"), (30,30)).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = None
        Ship.ships.append(self)

    @classmethod
    def display_ships(cls, window):
        for ship in Plane.ships:
            ship.rect.center = (Map.rect.topleft[0] + Map.scale*ship.pos[0],
                                Map.rect.topleft[1] + Map.scale*ship.pos[1])

            window.blit(ship.image, ship.rect)

pygame.quit()
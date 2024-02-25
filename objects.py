import pygame, random, math, os
import numpy as np

pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, name, image_path, position, rescale=None, text=None):
        super().__init__()
        self.name = name
        if type(image_path) is str:
            if rescale == None:
                self.image = pygame.image.load(os.path.join(os.getcwd(),image_path))
            else:
                self.image = pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(),image_path)), rescale)
        else:
            self.image = Button.make_surface(position)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.text = text
    
    @classmethod
    def make_surface(cls, position, size=(70,40), color=(70,70,70)):
        box = pygame.Surface(size)
        box.fill(color)
        # font = pygame.font.Font("images/font/evil-empire.ttf", 12)

        # text = font.render(text, True, (255,255,255))
        # text_rect = text.get_rect()
        # text_rect.center = position

        # box.blit(text, text_rect)
        return  box


class ToSellButton(pygame.sprite.Sprite):
    coor = {
        "Canada": (230,230),
        "Republic of Moldova": (685,316),
        "China": (948,371),
        "USA": (228,349),
    }

    initiated = False  # For first and last initiation
    buttons = []
    
    @classmethod
    def update(cls, window, Map):
        ToSellButton.display_buttons(window, Map)
        ToSellButton.check_collisions()

    def __init__(self, name, pos):
        super().__init__()
        self.name = name
        self.pos = pos
        self.is_available = False
        self.image = pygame.transform.scale(pygame.image.load("images/Icons/Circle.png"), (20, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos[0], self.pos[1])
        self.mask = pygame.mask.from_surface(self.image)


    @classmethod
    def one_time_activation(cls):
        if not cls.initiated:
            cls.initiated = True
            for country, coor in cls.coor.items():
                cls.buttons.append(ToSellButton(country, coor))


    @classmethod
    def display_buttons(cls, window, Map):
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
                    relative_x = pygame.mouse.get_pos()[0] - button.rect.x
                    relative_y = pygame.mouse.get_pos()[1] - button.rect.y
                    if button.mask.get_at((relative_x, relative_y)):
                        button.is_available = False
                        if button.pos != (685,316):
                            Plane(button.pos)


class Tranport:
    @classmethod
    def update(cls, window, Map):
        Plane.update(window, Map)
        Ship.update(window, Map)


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
    def update(cls, window, Map):
        Plane.display_planes(window, Map)

    @classmethod
    def display_planes(cls, window, Map):
        for plane in Plane.planes:
            if len(plane.path) <= 1:
                del plane
            else:
                plane.rect.center = (Map.rect.topleft[0] + Map.scale*plane.path[0][0],
                                    Map.rect.topleft[1] + Map.scale*plane.path[0][1])

                # Look at middle point (before middle point), look at destination (after middle point)
                if plane.before_middle_point and plane.path[0] != plane.middle_point:
                    # Look to which side should be made additional rotation
                    plane.before_middle_point = False
                    if plane.origin[1] - plane.destination[1]>0:
                        if plane.origin[0] - plane.destination[0]>0:
                            plane.image = pygame.transform.rotate(plane.image, Plane.angle_between_points(plane.origin, plane.middle_point))
                        elif plane.origin[0] - plane.destination[0]<=0:
                            plane.image = pygame.transform.rotate(plane.image, -Plane.angle_between_points(plane.origin, plane.middle_point))
                    elif plane.origin[1] - plane.destination[1]<=0:
                        if plane.origin[0] - plane.destination[0]>0:
                            plane.image = pygame.transform.rotate(plane.image,180 - Plane.angle_between_points(plane.origin, plane.middle_point))
                        elif plane.origin[0] - plane.destination[0]<=0:
                            plane.image = pygame.transform.rotate(plane.image,180 + Plane.angle_between_points(plane.origin, plane.middle_point))
                elif plane.path[0] == plane.middle_point:
                        if plane.origin[1] - plane.destination[1]>0:
                            plane.image = pygame.transform.rotate(plane.image,  Plane.angle_between_points(plane.middle_point, plane.destination))
                        else:
                            plane.image = pygame.transform.rotate(plane.image,  90 - Plane.angle_between_points(plane.origin, plane.middle_point) + Plane.angle_between_points(plane.middle_point, plane.destination))

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
        print(curve_x)
        curve_y = np.polyval(coefficients, curve_x)
        print(curve_y)
        coordinates = [(x_val, y_val) for x_val, y_val in zip(curve_x, curve_y)]

        if c1[0] > c2[0]:
            coordinates.sort(reverse=True)
        return coordinates
    
    @classmethod
    def angle_between_points(cls, point1, point2):
        direction_vector = (point2[0] - point1[0], point2[1] - point1[1])
        if point2[1]-point1[1] > 0:    
            perp_vect = (-direction_vector[1], direction_vector[0])
        else:
            perp_vect = (direction_vector[1], direction_vector[0])
        magnitude = math.sqrt(sum(component**2 for component in perp_vect))
        normalized_perp_vector = (perp_vect[0] / magnitude, perp_vect[1] / magnitude)
        distance = 100

        dy = math.sqrt((normalized_perp_vector[0]*distance)**2+(normalized_perp_vector[1]*distance)**2)
        if point2[1]-point1[1]<0:
            dx = math.sqrt((point2[0]-point1[0])**2+(point2[1]+dy-point1[1])**2)
        else:
            dx = math.sqrt((point2[0]-point1[0])**2+(point2[1]-dy-point1[1])**2)
        c = math.sqrt((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)
        angle = math.degrees(math.acos((dy**2 +c**2 - dx**2)/(2*dy*c)))
        print(angle)
        return angle
                

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
    def update(cls, window, Map):
        Ship.display_ships(window, Map)

    @classmethod
    def display_ships(cls, window, Map):
        for ship in Ship.ships:
            ship.rect.center = (Map.rect.topleft[0] + Map.scale*ship.pos[0],
                                Map.rect.topleft[1] + Map.scale*ship.pos[1])

            window.blit(ship.image, ship.rect)


class Country(pygame.sprite.Sprite):
    countries = []

    activated = False
    initiation = {
        "USA" : ["images/countries/10242.png", (250,350)]
    }


    def __init__(self, name, image_path, pos):
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (180,180))
        self.initial_image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (180,180))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.name = name
        self.pos = pos
        self.rect.center = self.pos
        self.focused = False
        self.deal = ["Moldova"]
        # self.deal = []
        Country.countries.append(self)

    @classmethod
    def update(cls, window, Map, GameState, CountryStatistic):
        cls.scale_on_focus()
        cls.display_countries(window, Map)
        cls.check_collisions(GameState, CountryStatistic)

    @classmethod
    def display_countries(cls, window, Map):
        for country in Country.countries:
            country.image = pygame.transform.scale(country.image, (Map.scale*country.image.get_size()[0],
                                                                    Map.scale*country.image.get_size()[1]))
            country.rect.center = (Map.rect.topleft[0] + Map.scale*country.pos[0],
                                   Map.rect.topleft[1] + Map.scale*country.pos[1])

            window.blit(country.image, country.rect)

    @classmethod
    def scale_on_focus(cls):
        for country in Country.countries:
            if country.rect.collidepoint(pygame.mouse.get_pos()):
                relative_x = pygame.mouse.get_pos()[0] - country.rect.x
                relative_y = pygame.mouse.get_pos()[1] - country.rect.y
                if country.mask.get_at((relative_x, relative_y)): 
                    if not country.focused:
                        country.image = pygame.transform.scale(country.image, (0.9*country.image.get_size()[0],
                                                                                0.9*country.image.get_size()[1]))
                        country.focused = True
            else:
                country.image = country.initial_image
                country.focused = False
    
    @classmethod
    def check_collisions(cls, GameState, CountryStatistic):
        for country in cls. countries:
            if country.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                GameState.country_statistic = True
                GameState.play = False
                CountryStatistic.focus_country = country
    
    @classmethod
    def one_time_activation(cls):
        if not cls.activated:
            cls.activated = True
            for key, value in cls.initiation.items():
                Country(key, value[0], value[1])


class Wine:
    name = "Traminer"

    taste = 0
    naturality = 0
    advertisement = 0

    # trandmarks = []

    # def __init__(self, name):
    #     self.name = name
    #     self.total_sold = 0

    #     self.taste = 0
    #     self.naturality = 0
    #     self.advertisement = 0


pygame.quit()
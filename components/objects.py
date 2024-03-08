import pygame, random, math, os, datetime, csv, sqlite3
from PIL import Image
import numpy as np
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, name, image_path=None, position=None, rescale=None):
        super().__init__()
        self.name = name
        if image_path:
            if rescale is None:
                self.image = pygame.image.load(image_path)
            else:
                self.image = pygame.transform.scale(pygame.image.load(image_path), rescale)
            self.have_icon = True
        else:
            self.image = pygame.image.load("assets/stuff/buttons/png/Rect-Dark-Default.png")
            self.have_icon = False
        self.rect = self.image.get_rect()
        if position:
            self.rect.center = position

    @classmethod
    def make_surface(cls, size=(70,40), color=(70,70,70)):
        box = pygame.Surface(size)
        box.fill(color)
        return box

    @classmethod
    def dislpay_text_on_buttons(cls, window, buttons):
        for button in buttons:
            if not button.have_icon:
                font = pygame.font.Font("assets/font/evil-empire.ttf", 12)
                text = font.render(button.name, True, (255,255,255))
                text_rect = text.get_rect()
                text_rect.center = button.rect.center
                window.blit(text, text_rect)

class ProgressBar:
    def __init__(self, start_value, max_value, bar_width, bar_height, bar_color, background_color, position, getter):
        self.start_value = start_value
        self.max_value = max_value
        self.current_value = start_value
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.bar_color = bar_color
        self.background_color = background_color
        self.position = position
        self.getter = getter

    def update(self, window, new_value=0):
        self.update_progress_bar(new_value)
        self.display_progress_bar(window)

    def display_progress_bar(self, window):
        bar_x, bar_y = self.position
        progress_width = int((self.current_value / self.max_value) * self.bar_width)

        pygame.draw.rect(window, (0, 0, 0), (bar_x - 1, bar_y - 1, self.bar_width + 2, self.bar_height + 2), 1)
        pygame.draw.rect(window, self.background_color, (bar_x, bar_y, self.bar_width, self.bar_height))
        pygame.draw.rect(window, self.bar_color, (bar_x, bar_y, progress_width, self.bar_height))

        font = pygame.font.Font("assets/font/evil-empire.ttf", 24)
        percent_text = f"{int((self.current_value / self.max_value) * 100)}%"
        text = font.render(percent_text, True, (0, 0, 0))
        text_rect = text.get_rect()

        text_rect.center = (bar_x + self.bar_width // 2, bar_y + self.bar_height // 2)
        window.blit(text, text_rect)

    def update_progress_bar(self, getter):  # ?
        self.current_value = min(self.getter(), self.max_value)


class ToSellButton(pygame.sprite.Sprite):
    buttons = []
    
    def __init__(self, country):
        super().__init__()
        self.is_available = False
        self.have_coordinates = False
        self.is_positioned = False

        self.country = country
        self.image = pygame.transform.scale(pygame.image.load("assets/icons/Circle.png"), (20, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = country.rect.center
        self.rect.center = self.pos

        ToSellButton.buttons.append(self)

    @classmethod
    def update(cls, window, Map):
        ToSellButton.display_buttons(window, Map)

    @classmethod
    def display_buttons(cls, window, Map):
        cls.random_availability()
        for button in [button for button  in cls.buttons if button.is_available]:
            if button.have_coordinates:
                if button.is_positioned:
                    # button.rect.center = (Map.rect.topleft[0] + button.rect.center[0],
                                        #   Map.rect.topleft[1] + button.rect.center[1])
                    window.blit(button.image, button.rect)
                    continue
                button.is_positioned = True
                button.rect.center = (Map.rect.topleft[0] + Map.scale*button.rect.center[0],
                                      Map.rect.topleft[1] + Map.scale*button.rect.center[1])
                window.blit(button.image, button.rect)
                continue
            country_width = button.country.rect.topright[0] - button.country.rect.topleft[0]
            country_height = button.country.rect.bottomright[1] - button.country.rect.topright[1]
            random_point = (random.randint(1, country_width-2), random.randint(1, country_height-2))

            while not button.country.mask.get_at(random_point):
                random_point = (random.randint(1, country_width-2), random.randint(1, country_height-2))
            button.rect.center = button.country.rect.topleft[0] + random_point[0], -15 + button.country.rect.topleft[1] + random_point[1]
            window.blit(button.image, button.rect)
            button.have_coordinates = True
            button.is_positioned = False

    @classmethod
    def random_availability(cls):
        for button in cls.buttons:
            if button.country.name == "Moldova":
                pass
            elif random.randint(1, 200) == 1:
                button.is_available = True


class Tranport:
    @classmethod
    def update(cls, window, Map):
        Plane.update(window, Map)
        Ship.update(window, Map)


class Plane(pygame.sprite.Sprite):
    planes = []
    def __init__(self, destination):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/icons/plane.png"), (30,30)).convert_alpha()
        self.initial_image = pygame.transform.scale(pygame.image.load("assets/icons/plane.png"), (30,30)).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.origin = Country.moldova.rect.center
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
        curve_y = np.polyval(coefficients, curve_x)
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
        return angle
                

class Ship(pygame.sprite.Sprite):
    ships = []

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/icons/ship.png"), (30,30)).convert_alpha()
        self.initial_image = pygame.transform.scale(pygame.image.load("assets/icons/ship.png"), (30,30)).convert_alpha()
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
    contracts = []  # The deal will be added here, after which logic part will handle this list entirely
    moldova = None

    activated = False  # First initiation
    # initiate_from = 'csv'
    initiate_from = 'sqlite3'
    old_map_scale = 1  # To rescale the map only after Map.scale modification
    initial_scale_factor  = 0.325  # Optimal scale for countries

    def __init__(self, name, image_path, pos, continent):
        self.initial_scale_factor = 0.325
        self.not_scaled_width = Image.open(image_path).size[0]
        self.not_scaled_height = Image.open(image_path).size[1]
        self.not_scaled_size = (self.not_scaled_width, self.not_scaled_height)

        self.scaled_width = Country.initial_scale_factor * Image.open(image_path).size[0]
        self.scaled_height = Country.initial_scale_factor * Image.open(image_path).size[1]
        self.scaled_size = (self.scaled_width, self.scaled_height)

        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), self.scaled_size)
        self.initial_image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), self.scaled_size)
        self.initial_not_scaled_image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), self.not_scaled_size)

        self.rect = self.image.get_rect()
        self.scaled_x_pos = Country.initial_scale_factor * (pos[0] - 230)
        self.scaled_y_pos = Country.initial_scale_factor * pos[1]
        self.pos = (self.scaled_x_pos, self.scaled_y_pos)
        self.rect.center = self.pos
        self.mask = pygame.mask.from_surface(self.image)

        self.name = name
        self.continent = continent
        self.focused = False
        self.buy_from = []
        self.sell_to = []
        self.to_sell_button = ToSellButton(self)
        self.old_map_scale = 1

        Country.countries.append(self)
        if name == "Moldova":
            Country.moldova = self

    @classmethod
    def update(cls, window, Map, GameState, CountryStatistic):
        cls.one_time_activation()
        cls.display_countries(window, Map)
        ToSellButton.display_buttons(window, Map)
        cls.check_collisions(Map, GameState, CountryStatistic)

    @classmethod
    def display_countries(cls, window, Map):
        for country in Country.countries:
            if country.old_map_scale != Map.scale:  # To avoid inifinte scaling
                country.old_map_scale = Map.scale
                # Scaling the size of country
                country.image = pygame.transform.scale(country.initial_not_scaled_image, (Map.scale * country.not_scaled_width * cls.initial_scale_factor,
                                                                                          Map.scale * country.not_scaled_height * cls.initial_scale_factor))
                country.rect = country.image.get_rect()
                country.mask = pygame.mask.from_surface(country.image)
            # Changing the coordinates of the country
            country.rect.center = (Map.rect.topleft[0] + Map.scale*country.pos[0], Map.rect.topleft[1] + Map.scale*country.pos[1])
            window.blit(country.image, country.rect)


    @classmethod
    def check_collisions(cls, Map, GameState, CountryStatistic):
        if Map.pressed and Map.motion:
            return
        for country in cls. countries:
            # Checking collisions with rectangle of the country
            if country.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                #Checking collisions with rectangle of the sell button
                if country.to_sell_button.rect.collidepoint(pygame.mouse.get_pos()):
                    relative_x = pygame.mouse.get_pos()[0] - country.to_sell_button.rect.x
                    relative_y = pygame.mouse.get_pos()[1] - country.to_sell_button.rect.y
                    # Checking cllisions with mask of the sell button
                    if country.to_sell_button.mask.get_at((relative_x, relative_y)) and country.to_sell_button.is_available :
                        country.to_sell_button.is_available = False
                        country.to_sell_button.have_coordinates = False
                        country.to_sell_button.is_positioned = False
                        if country != Country.moldova:  # Do not send plane from Moldova to Moldova
                            Plane(country.to_sell_button.pos)  # Generate a plane
                            # Logistic stuff:
                            cls.contracts.append([Country.moldova, country])
                            Country.moldova.sell_to.append(country)
                            country.buy_from.append(Country.moldova)
                # Checking collisions with mask of the country
                else:
                    relative_x = pygame.mouse.get_pos()[0] - country.rect.x
                    relative_y = pygame.mouse.get_pos()[1] - country.rect.y
                    if country.mask.get_at((relative_x, relative_y)):
                        GameState.country_statistic = True
                        GameState.play = False
                        CountryStatistic.focus_country = country

    @classmethod
    def one_time_activation(cls):
        if not cls.activated:
            cls.activated = True
            if cls.initiate_from == 'csv':
                with open('components/countries_data/countries_data.csv', mode='r') as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        Country(row['country'], row['image_path'], (float(row['x_position']), float(row['y_position'])), str(row['continent']))
            elif cls.initiate_from == 'sqlite3':
                db_file = 'components/countries_data/countries_data.db'
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM countries")
                for row in cursor.fetchall():
                    Country(row[0], row[1], (row[2], row[3]), row[4])


    def __repr__(self):
        return self.name

class Wine:

    wine_color = (89, 16, 56)
    trandmarks = []

    taste = 0
    naturality = 0
    advertisement = 0

    def __init__(self, name):
        self.name = name
        self.total_sold = 0

        self.taste = 0
        self.naturality = 0
        self.advertisement = 0

class Woman:
    def __init__(self, id, wash_dishes_speed, her_owner):
        self.id = id
        self.name = None

        self.beautiful = random.randint(1, 10)
        self.blow_mind = random.randint(0,1)
        self.required_attention_per_day = datetime.timedelta(hours=24)
        self.required_money_per_day = her_owner.get_salary() / 30
        self.wash_dishes_speed = wash_dishes_speed
        self.social_rating = wash_dishes_speed
        self.rights = random.choice(["No rights", "No rights"])
        self.can_cook = random.choice(["Hopefully", "Let Her Cook"])
        self.have_driving_license = False

    def get_size(self):
        return '\u2620'
    
    def start_cook(self):
        return "mby we'll order smth?"
    
    def get_mood(self):
        return (1 - self.her_owner.get_mood())
    
    def get_cause_of_sadness(self):
        return None
    
    def get_driving_license(self):
        return False

pygame.quit()
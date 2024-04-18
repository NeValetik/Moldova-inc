import pygame, random, math, os, datetime, csv, sqlite3
from PIL import Image
import numpy as np

pygame.init()


class Button(pygame.sprite.Sprite):
    frame = pygame.transform.scale(pygame.image.load("assets/stuff/button-frame.png"), (230, 80))
    frame_rect = frame.get_rect()

    def __init__(self, name, position, image_path=None, dimension=(230, 80), size = (200, 80), font_size=36):
        super().__init__()
        self.name = name

        self.text = Button.get_text_object(name,font_size)
        self.text_rect = self.text.get_rect()

        if image_path == None:
            self.image = Button.make_surface(size = size)
        elif dimension == None:
            self.image = pygame.image.load(image_path)
        else:
            self.image = pygame.transform.scale(pygame.image.load(image_path), dimension)

        self.rect = self.image.get_rect()
        self.rect.center = position

    @classmethod
    def get_text_object(cls, name, font_size):
        font = pygame.font.Font("assets/font/evil-empire.ttf", font_size)
        text = font.render(name, True, (0, 0, 0))
        return text

    @classmethod
    def make_surface(cls, size=(200, 80), color=(255, 255, 255, 128)):
        box = pygame.Surface(size, pygame.SRCALPHA)
        box.fill(color)
        pygame.draw.rect(box, (255, 255, 255, 255), (0, 0, *size))
        return box

    @classmethod
    def display_text_on_buttons(cls, from_class, window):
        for button in from_class.buttons:
            button.text_rect.center = button.rect.center
            window.blit(button.text, button.text_rect)
    
    @classmethod
    def display_buttons(cls, from_class, window):
        for button in from_class.buttons:
            window.blit(button.image, button.rect)
        

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

        border_radius = self.bar_height // 2

        border_rect = pygame.Rect(bar_x - 1, bar_y - 1, self.bar_width + 2, self.bar_height + 2)
        pygame.draw.rect(window, (255, 255, 255), border_rect, border_radius=border_radius)

        progress_rect = pygame.Rect(bar_x, bar_y, progress_width, self.bar_height)
        pygame.draw.rect(window, (*self.bar_color, 128), progress_rect, border_radius=border_radius)

        font = pygame.font.Font("assets/font/evil-empire.ttf", 24)
        percent_text = f"{int(self.current_value)}"
        text = font.render(percent_text, True, (0, 0, 0))
        text_rect = text.get_rect()

        text_rect.center = (bar_x + self.bar_width // 2, bar_y + self.bar_height // 2)
        window.blit(text, text_rect)

    def update_progress_bar(self, getter):  # ?
        self.current_value = min(self.getter(), self.max_value)


class Contract(pygame.sprite.Sprite): 
    buttons = []
    positions = []

    def __init__(self,position):
        super().__init__()
        self.position = position
        Contract.buttons.append(Button("accept", (self.position[0]-40, self.position[1]),size=(70,30),font_size=16))
        Contract.positions.append((self.position[0]-40, self.position[1]))
        Contract.buttons.append(Button("decline", (self.position[0]+40, self.position[1]),size=(70,30),font_size=16))
        Contract.positions.append((self.position[0]+40, self.position[1]))
        # self.name = "Vladimir"

        # self.text = Contract.get_text_object(self.name,36)
        # self.text_rect = self.text.get_rect()

        # self.position = (700,400)
        # self.image = self.make_surface()
        # self.rect = self.image.get_rect()
        # self.rect.center = self.position
        


    @classmethod
    def display_contracts(cls, window, Map):
        Button.display_buttons(cls, window)
        Button.display_text_on_buttons(cls, window)
        # window.blit(cls.image, cls.rect)
        for iterator in range(len(cls.buttons)):#The buttons are driving away anyway(Will fix it later)
            #NEEDS FIX
            cls.buttons[iterator].rect.center = (
            Map.rect.topleft[0] + Map.scale * cls.positions[iterator][0], Map.rect.topleft[1] + Map.scale * cls.positions[iterator][1])
    

    # @classmethod
    # def display_text_on_contracts(cls, from_class, window):
    #     cls.text_rect.center = cls.rect.center
    #     window.blit(cls.text, cls.text_rect)

    # @classmethod
    # def get_text_object(cls, name, font_size):
    #     font = pygame.font.Font("assets/font/evil-empire.ttf", font_size)
    #     text = font.render(name, True, (0, 0, 0))
    #     return text


    # @classmethod
    # def make_surface(cls, size=(400, 200), color=(255, 255, 255, 128)):
    #     box = pygame.Surface(size, pygame.SRCALPHA)
    #     box.fill(color)
    #     pygame.draw.rect(box, (255, 255, 255, 255), (0, 0, *size))
    #     return box

class ToSellButton(pygame.sprite.Sprite):
    buttons = []

    def __init__(self, country):
        super().__init__()
        self.is_available = False
        self.have_coordinates = False

        self.country = country
        self.image = pygame.transform.scale(pygame.image.load("assets/icons/Circle.png"), (20, 30))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = None
        self.rect.center = (-100, -100)

        ToSellButton.buttons.append(self)

    @classmethod
    def update(cls, window, Map):
        ToSellButton.display_buttons(window, Map)

    @classmethod
    def display_buttons(cls, window, Map):
        cls.random_availability()
        for button in [button for button in cls.buttons if button.is_available]:
            if not button.have_coordinates:
                country_width = button.country.rect.topright[0] - button.country.rect.topleft[0]
                country_height = button.country.rect.bottomright[1] - button.country.rect.topright[1]
                random_point = (random.randint(1, country_width - 1), random.randint(1, country_height - 1))
                while not button.country.mask.get_at(random_point):
                    random_point = (random.randint(1, country_width - 1), random.randint(1, country_height - 1))
                button.pos = (button.country.rect.topleft[0] + random_point[0],
                              button.country.rect.topleft[1] + random_point[1] - 15)  # -15 for bottom to be at center
                button.have_coordinates = True

            # Somewhere in the branch below we need to adjust scaling on zooming
            elif button.have_coordinates:
                button.rect.center = (
                    Map.rect.topleft[0] + Map.scale * button.pos[0], Map.rect.topleft[1] + Map.scale * button.pos[1])
                
            window.blit(button.image, button.rect)

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
        self.image = pygame.transform.scale(pygame.image.load("assets/icons/plane.png"), (30, 30)).convert_alpha()
        self.initial_image = pygame.transform.scale(pygame.image.load("assets/icons/plane.png"),
                                                    (30, 30)).convert_alpha()
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
                # if plane.before_middle_point and plane.path[0] != plane.middle_point:
                if plane.before_middle_point:

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
                # elif plane.path[0] == plane.middle_point:
                #         if plane.origin[1] - plane.destination[1]>0:
                #             plane.image = pygame.transform.rotate(plane.image,  Plane.angle_between_points(plane.middle_point, plane.destination))
                #         else:
                #             plane.image = pygame.transform.rotate(plane.image,  90 - Plane.angle_between_points(plane.origin, plane.middle_point) + Plane.angle_between_points(plane.middle_point, plane.destination))

                window.blit(plane.image, plane.rect)
                del plane.path[0]

    @classmethod
    def get_path(cls, c1, c2):
        # middle_point = (min([c1[0], c2[0]]) + (abs(c1[0] - c2[0]) / 2), min([c1[1], c2[1]]) + (abs(c1[1] - c2[1]) / 2))
        
        # direction_vector = (c2[0] - c1[0], c2[1] - c1[1])
        # perp_vect = (-direction_vector[1], direction_vector[0])
        # magnitude = math.sqrt(sum(component**2 for component in perp_vect))
        # normalized_perp_vector = (perp_vect[0] / magnitude, perp_vect[1] / magnitude)

        # distance = 20
        # third_point = (middle_point[0] + normalized_perp_vector[0]*distance, middle_point[1] + normalized_perp_vector[1]*distance)
        
        x_values = [c1[0], c2[0]]
        y_values = [c1[1], c2[1]]
            
        x = np.array(x_values)
        y = np.array(y_values)
        coefficients = np.polyfit(x, y, 1)  # Fit a quadratic polynomial (degree 2)
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
        distance = 20

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
        self.image = pygame.transform.scale(pygame.image.load("assets/icons/ship.png"), (30, 30)).convert_alpha()
        self.initial_image = pygame.transform.scale(pygame.image.load("assets/icons/ship.png"),
                                                    (30, 30)).convert_alpha()
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
            ship.rect.center = (Map.rect.topleft[0] + Map.scale * ship.pos[0],
                                Map.rect.topleft[1] + Map.scale * ship.pos[1])

            window.blit(ship.image, ship.rect)


class Country(pygame.sprite.Sprite):
    countries = []
    contracts = []  # The deal will be added here, after which logic part will handle this list entirely
    moldova = None

    activated = False  # First initiation
    initiate_from = 'csv'
    # initiate_from = 'sqlite3'
    old_map_scale = 1  # To rescale the map only after Map.scale modification
    initial_scale_factor = 0.325    # Optimal scale for countries for 1200x800

    def __init__(self, name, image_path, pos, continent,naturality,advertisment,taste,contract_condition_naturality,contract_condition_advertisment,contract_condition_taste):
        self.initial_scale_factor = 0.325  # Optimal scale for countries for 1200x800
        self.not_scaled_width = Image.open(image_path).size[0]
        self.not_scaled_height = Image.open(image_path).size[1]
        self.not_scaled_size = (self.not_scaled_width, self.not_scaled_height)

        self.scaled_width = Country.initial_scale_factor * Image.open(image_path).size[0]
        self.scaled_height = Country.initial_scale_factor * Image.open(image_path).size[1]
        self.scaled_size = (self.scaled_width, self.scaled_height)

        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), self.scaled_size)
        self.initial_image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), self.scaled_size)
        self.initial_not_scaled_image = pygame.image.load(image_path).convert_alpha()

        self.rect = self.image.get_rect()
        self.scaled_x_pos = Country.initial_scale_factor * pos[0]
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

        #Here is read from database base the initial data for each country which states the effect of each characteristic on the income
        self.naturality_coef = naturality
        self.advertisment_coef = advertisment
        self.taste_coef = taste
        
        #Here is read from database base the initial data for each country which states the needed amount of progress to make the contract
        self.contract_condition_naturality = contract_condition_naturality
        self.contract_condition_advertisment = contract_condition_advertisment
        self.contract_condition_taste = contract_condition_taste

        Country.countries.append(self)
        if name == "Moldova":
            Country.moldova = self

    @classmethod
    def update(cls, window, Map, GameState, CountryStatistic):
        cls.one_time_activation()
        # Contract.display_buttons(window)
        # All this stuff now is in Map.update()upgrade-elements/quality-skill.png"
        # cls.display_countries(window, Map)
        # ToSellButton.display_buttons(window, Map)
        # cls.check_collisions(Map, GameState, CountryStatistic)

    @classmethod
    def display_countries(cls, window, Map):
        for country in Country.countries:
            if country.old_map_scale != Map.scale:  # To avoid inifinte scaling
                country.old_map_scale = Map.scale
                # Scaling the size of country
                country.image = pygame.transform.scale(country.initial_not_scaled_image,
                                                       (Map.scale * country.not_scaled_width * cls.initial_scale_factor,
                                                        Map.scale * country.not_scaled_height * cls.initial_scale_factor))
                country.rect = country.image.get_rect()
                country.mask = pygame.mask.from_surface(country.image)

            # Changing the coordinates of the country
            country.rect.center = (
                Map.rect.topleft[0] + Map.scale * country.pos[0], Map.rect.topleft[1] + Map.scale * country.pos[1])
            window.blit(country.image, country.rect)

    @classmethod
    def check_collisions(cls, Map, GameState, CountryStatistic):
        if Map.pressed and Map.motion:
            return
        # Checking only to sell buttons 
        for to_sell_button in [country.to_sell_button for country in cls.countries if country.to_sell_button.is_available]:
            if to_sell_button.rect.collidepoint(pygame.mouse.get_pos())  and not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                relative_x = pygame.mouse.get_pos()[0] - to_sell_button.rect.x
                relative_y = pygame.mouse.get_pos()[1] - to_sell_button.rect.y
                if to_sell_button.mask.get_at((relative_x, relative_y)):
                    to_sell_button.is_available = False
                    to_sell_button.have_coordinates = False
                    to_sell_button.is_positioned = False
                    # Logistic stuff:
                    if to_sell_button.country != Country.moldova:  # Do not send plane from Moldova to Moldova
                        Plane(to_sell_button.pos)  # Generate a plane
                        to_sell_button.country.start_time = Timer.get_time_in_years() # Gives the time of the contract activation
                        Contract(to_sell_button.pos)
                        cls.contracts.append([Country.moldova, to_sell_button.country])
                        Country.moldova.sell_to.append(to_sell_button.country)
                        to_sell_button.country.buy_from.append(Country.moldova)
                    return
        # Checking only countries
        for country in cls.countries:
            if country.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0] and GameState.mouse_button_was_pressed:
                relative_x = pygame.mouse.get_pos()[0] - country.rect.x
                relative_y = pygame.mouse.get_pos()[1] - country.rect.y
                if country.mask.get_at((relative_x, relative_y)):
                    GameState.country_statistic = True
                    GameState.play = False
                    CountryStatistic.focus_country = country
                    return

    @classmethod
    def one_time_activation(cls):
        if not cls.activated:
            cls.activated = True
            if cls.initiate_from == 'csv':
                with open('components/countries_data/countries_data.csv', mode='r') as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        Country(row['country'], row['image_path'], (float(row['x_position']), float(row['y_position'])),
                                str(row['continent']),float(row["naturality"]),float(row["advertisment"]),float(row["taste"]),float(row["contract_condition_naturality"]),float(row["contract_condition_advertisment"]),float(row["contract_condition_taste"]))
            elif cls.initiate_from == 'sqlite3':
                db_file = 'components/countries_data/countries_data.db'
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM countries")
                for row in cursor.fetchall():
                    Country(row[0], row[1], (row[2], row[3]), row[4])
                conn.close()

    def __repr__(self):
        return (str(self.name), self.naturality_coef, self.advertisment_coef, self.taste_coef)


class Wine:
    wine_color = (89, 16, 56)
    trandmarks = []

    naturality = 1000
    advertisment = 5
    taste = 100

    def __init__(self, name, taste=0, naturality=0, advertisement=0):
        self.name = name
        self.total_sold = 0

        self.taste = taste
        self.naturality = naturality
        self.advertisement = advertisement

    def set_taste(self, taste):
        self.taste = taste

    def set_naturality(self, naturality):
        self.taste = naturality

    def set_advertisement(self, advertisement):
        self.advertisement = advertisement
    
    def return_taste(self, taste):
        return self.taste

    def return_naturality(self, naturality):
        return self.naturality

    def return_advertisement(self, advertisement):
        return self.advertisement    

class Woman:
    def __init__(self, id, wash_dishes_speed, her_owner):
        self.id = id
        self.name = None

        self.beautiful = random.randint(1, 10)
        self.blow_mind = random.randint(0, 1)
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

class Timer:
    start_time = datetime.datetime(1950, 12, 30, 12, 0, 0)
    current_time = start_time
    frame = 1
    
    #Counts years from the start of the game
    years_from_start = current_time.year-start_time.year

    @classmethod
    def update(cls, window):
        cls.update_timer()
        cls.display_timer(window)
        cls.update_time_difference()
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
    
    @classmethod
    def get_time_in_years(cls):
        return cls.current_time.day/31+cls.current_time.month/12 + cls.current_time.year
    
    @classmethod
    def update_time_difference(cls):
        cls.years_from_start = cls.current_time.year-cls.start_time.year

pygame.quit()

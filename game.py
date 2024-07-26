import pygame
import sys
import random

# Ініціалізація Pygame
pygame.init()

# Встановлення розмірів екрану та розміру плитки
screen_width = 800
screen_height = 600
tile_size = 40
fullscreen_res = (1920, 1080)
windowed_res = (screen_width, screen_height)
screen = pygame.display.set_mode(windowed_res)
pygame.display.set_caption("SimCity 2D")

# Визначення кольорів
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Визначення вартості будівництва
costs = {
    'residential': 100,
    'commercial': 200,
    'industrial': 300,
    'road': 50
}

# Визначення доходу від комерційних і промислових будівель за рівнем
income_per_level_commercial = [5, 10, 15, 20, 25]
income_per_level_industrial = [20, 40, 60, 80, 100]

# Визначення вмістимості житлових будівель за рівнем
capacity_per_level_residential = [2, 4, 6, 8, 10]

# Витрати на утримання будівель
maintenance_costs = {
    'residential': 10,
    'commercial': 20,
    'industrial': 30
}

# Завантаження зображень фону та їх масштабування
grass_images = [
    pygame.transform.scale(pygame.image.load('grass_1.png'), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load('grass_2.png'), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load('grass_3.png'), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load('grass_4.png'), (tile_size, tile_size))
]

# Клас для комерційних будівель
class CommercialBuilding:
    def __init__(self, pos):
        self.pos = pos
        self.level = 1

    def upgrade(self):
        if self.level < 5:
            self.level += 1

    def earn_income(self):
        if current_population > 0 and len(roads) > 0 and len(residential_buildings) > 0:
            return income_per_level_commercial[self.level - 1]
        return 0

    def maintenance_cost(self):
        return maintenance_costs['commercial']

# Клас для промислових будівель
class IndustrialBuilding:
    def __init__(self, pos):
        self.pos = pos
        self.level = 1

    def upgrade(self):
        if self.level < 5:
            self.level += 1

    def earn_income(self):
        if len(roads) > 0:
            return income_per_level_industrial[self.level - 1]
        return 0

    def maintenance_cost(self):
        return maintenance_costs['industrial']

# Клас для житлових будівель
class ResidentialBuilding:
    def __init__(self, pos):
        self.pos = pos
        self.level = 1

    def upgrade(self):
        if self.level < 5:
            self.level += 1

    def get_capacity(self):
        return capacity_per_level_residential[self.level - 1]

    def maintenance_cost(self):
        return maintenance_costs['residential']

# Основні змінні
clock = pygame.time.Clock()
residential_buildings = []
commercial_buildings = []
industrial_buildings = []
roads = []
current_tool = 'road'
current_building_type = 'residential'
balance = 1000
total_capacity = 0
current_population = 0
population_added = False

# Налаштування податків
tax_rates = {
    'residential': 0.1,  # 10% податку на житлові будівлі
    'commercial': 0.2,  # 20% податку на комерційні будівлі
    'industrial': 0.3   # 30% податку на промислові будівлі
}

def calculate_tax(building, tax_rate):
    if isinstance(building, ResidentialBuilding):
        return int(building.get_capacity() * tax_rate)
    elif isinstance(building, CommercialBuilding):
        return int(building.earn_income() * tax_rate)
    elif isinstance(building, IndustrialBuilding):
        return int(building.earn_income() * tax_rate)
    return 0

def earn_income():
    global balance
    total_income = 0
    for building in commercial_buildings:
        if current_population > 0 and len(roads) > 0 and len(residential_buildings) > 0:
            income = building.earn_income()
            tax = calculate_tax(building, tax_rates['commercial'])
            total_income += income - tax - building.maintenance_cost()
    for building in industrial_buildings:
        if len(roads) > 0:
            income = building.earn_income()
            tax = calculate_tax(building, tax_rates['industrial'])
            total_income += income - tax - building.maintenance_cost()
    for building in residential_buildings:
        tax = calculate_tax(building, tax_rates['residential'])
        total_income -= building.maintenance_cost()
    balance += total_income

# Змінні для роздільної здатності
fullscreen = False
current_res = windowed_res

# Генерація розміщення фону
def generate_background():
    global background_tiles
    background_tiles = []
    for x in range(0, current_res[0] // tile_size):
        row = []
        for y in range(0, current_res[1] // tile_size):
            img = random.choice(grass_images)
            row.append(img)
        background_tiles.append(row)

generate_background()

# Функція для малювання фону
def draw_background():
    for x in range(len(background_tiles)):
        for y in range(len(background_tiles[x])):
            screen.blit(background_tiles[x][y], (x * tile_size, y * tile_size))

# Функція для оновлення загальної вмістимості
def update_total_capacity():
    global total_capacity
    total_capacity = sum(building.get_capacity() for building in residential_buildings)

# Функція для оновлення населення
def update_population():
    global current_population
    if current_population > total_capacity:
        current_population = total_capacity

# Функція для додавання населення
def add_population():
    global current_population, population_added
    if len(residential_buildings) > 0 and not population_added:
        total_capacity = sum(building.get_capacity() for building in residential_buildings)
        current_population = min(total_capacity, current_population + 10)  # Додаємо нових людей
        population_added = True

# Функція для перемикання роздільної здатності
def toggle_fullscreen():
    global screen, fullscreen, current_res
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode(fullscreen_res, pygame.FULLSCREEN)
        current_res = fullscreen_res
    else:
        screen = pygame.display.set_mode(windowed_res)
        current_res = windowed_res
    generate_background()

# Функція для скидання гри
def reset_game():
    global residential_buildings, commercial_buildings, industrial_buildings, roads, balance, total_capacity, current_population, population_added
    residential_buildings = []
    commercial_buildings = []
    industrial_buildings = []
    roads = []
    balance = 1000
    total_capacity = 0
    current_population = 0
    population_added = False
    generate_background()

# Основний цикл гри
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            grid_pos = (pos[0] // tile_size * tile_size, pos[1] // tile_size * tile_size)
            if current_tool == 'road':
                if grid_pos not in roads:
                    roads.append(grid_pos)
                    balance -= costs['road']
            elif current_tool == 'building':
                if current_building_type == 'residential':
                    if balance >= costs['residential']:
                        residential_buildings.append(ResidentialBuilding(grid_pos))
                        balance -= costs['residential']
                elif current_building_type == 'commercial':
                    if balance >= costs['commercial']:
                        commercial_buildings.append(CommercialBuilding(grid_pos))
                        balance -= costs['commercial']
                elif current_building_type == 'industrial':
                    if balance >= costs['industrial']:
                        industrial_buildings.append(IndustrialBuilding(grid_pos))
                        balance -= costs['industrial']
            elif current_tool == 'remove':
                for building in residential_buildings:
                    if building.pos == grid_pos:
                        residential_buildings.remove(building)
                        update_total_capacity()
                        update_population()
                        break
                for building in commercial_buildings:
                    if building.pos == grid_pos:
                        commercial_buildings.remove(building)
                        break
                for building in industrial_buildings:
                    if building.pos == grid_pos:
                        industrial_buildings.remove(building)
                        break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_fullscreen()
            elif event.key == pygame.K_F5:
                reset_game()
            elif event.key == pygame.K_r:
                current_tool = 'road'
            elif event.key == pygame.K_b:
                current_tool = 'building'
            elif event.key == pygame.K_1:
                current_building_type = 'residential'
            elif event.key == pygame.K_2:
                current_building_type = 'commercial'
            elif event.key == pygame.K_3:
                current_building_type = 'industrial'

    # Заробляння доходу від податків і будівель
    earn_income()
    add_population()

    # Малювання фону
    draw_background()

    # Малювання будівель
    for building in residential_buildings:
        pygame.draw.rect(screen, GREEN, (building.pos[0], building.pos[1], tile_size, tile_size))
    for building in commercial_buildings:
        pygame.draw.rect(screen, BLUE, (building.pos[0], building.pos[1], tile_size, tile_size))
    for building in industrial_buildings:
        pygame.draw.rect(screen, YELLOW, (building.pos[0], building.pos[1], tile_size, tile_size))
    
    # Малювання доріг
    for road in roads:
        pygame.draw.rect(screen, GRAY, (road[0], road[1], tile_size, tile_size))

    # Відображення поточного інструменту та балансу
    font = pygame.font.SysFont(None, 24)
    tool_text = font.render(f'Tool: {current_tool}', True, (0, 0, 0))
    screen.blit(tool_text, (10, 10))

    building_text = font.render(f'Building: {current_building_type}', True, (0, 0, 0))
    screen.blit(building_text, (10, 30))

    balance_text = font.render(f'Balance: ${balance}', True, (0, 0, 0))
    screen.blit(balance_text, (10, 50))

    population_text = font.render(f'Population: {current_population}/{total_capacity}', True, (0, 0, 0))
    screen.blit(population_text, (10, 70))

    # Відображення вартості будівництва
    costs_text = font.render('Costs: R: 100, C: 200, I: 300, Rd: 50', True, (0, 0, 0))
    screen.blit(costs_text, (10, 90))

    # Відображення податкових ставок та доходів
    tax_rates_text = font.render(f'Tax Rates: Res: {int(tax_rates["residential"]*100)}%, Com: {int(tax_rates["commercial"]*100)}%, Ind: {int(tax_rates["industrial"]*100)}%', True, (0, 0, 0))
    screen.blit(tax_rates_text, (10, 110))

    # Відображення рівня будівлі при наведенні миші
    pos = pygame.mouse.get_pos()
    grid_pos = (pos[0] // tile_size * tile_size, pos[1] // tile_size * tile_size)
    for building in residential_buildings:
        if building.pos == grid_pos:
            level_text = font.render(f'Level: {building.level}', True, (0, 0, 0))
            screen.blit(level_text, (pos[0] + 10, pos[1] + 10))
    for building in commercial_buildings:
        if building.pos == grid_pos:
            level_text = font.render(f'Level: {building.level}', True, (0, 0, 0))
            screen.blit(level_text, (pos[0] + 10, pos[1] + 10))
    for building in industrial_buildings:
        if building.pos == grid_pos:
            level_text = font.render(f'Level: {building.level}', True, (0, 0, 0))
            screen.blit(level_text, (pos[0] + 10, pos[1] + 10))

    # Оновлення екрану
    pygame.display.flip()
    clock.tick(30)

# Завершення Pygame
pygame.quit()
sys.exit()

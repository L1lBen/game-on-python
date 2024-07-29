import pygame
import sys
import os
import random

# Ініціалізація Pygame
pygame.init()

# Параметри вікна
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
GRID_SIZE = 40

# Створення вікна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Місто будівництво")

# Основні кольори
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Завантаження текстур
texture_path = "texture"
textures = {
    "grass_1": pygame.image.load(os.path.join(texture_path, "grass_1.png")),
    "grass_2": pygame.image.load(os.path.join(texture_path, "grass_2.png")),
    "grass_3": pygame.image.load(os.path.join(texture_path, "grass_3.png")),
    "grass_4": pygame.image.load(os.path.join(texture_path, "grass_4.png")),
    "grass_5": pygame.image.load(os.path.join(texture_path, "grass_5.png")),
    "road_vertical": pygame.image.load(os.path.join(texture_path, "road_vertical.png")),
    "road_vertical_right": pygame.image.load(os.path.join(texture_path, "road_vertical_right.png")),
    "road_vertical_left": pygame.image.load(os.path.join(texture_path, "road_vertical_left.png")),
    "road_vertical_horizontal": pygame.image.load(os.path.join(texture_path, "road_vertical_horizontal.png")),
    "road_horizontal": pygame.image.load(os.path.join(texture_path, "road_horizontal.png")),
    "road_horizontal_right": pygame.image.load(os.path.join(texture_path, "road_horizontal_right.png")),
    "road_horizontal_left": pygame.image.load(os.path.join(texture_path, "road_horizontal_left.png")),
    "road_1": pygame.image.load(os.path.join(texture_path, "road_1.png")),
    "road_2": pygame.image.load(os.path.join(texture_path, "road_2.png")),
    "road_3": pygame.image.load(os.path.join(texture_path, "road_3.png")),
    "road_4": pygame.image.load(os.path.join(texture_path, "road_4.png")),
    "shop": pygame.image.load(os.path.join(texture_path, "shop.png")),
    "office": pygame.image.load(os.path.join(texture_path, "office.png")),
    "factory": pygame.image.load(os.path.join(texture_path, "factory.png")),
    "house": pygame.image.load(os.path.join(texture_path, "house.png")),
    "delete": pygame.image.load(os.path.join(texture_path, "delete.png")),  # Завантаження текстури видалення
    "power_plant": pygame.image.load(os.path.join(texture_path, "power_plant.png")),
    "water_tower": pygame.image.load(os.path.join(texture_path, "water_tower.png")),
    "waste_facility": pygame.image.load(os.path.join(texture_path, "waste_facility.png"))
}

# Масштабування текстур до розміру сітки
for key in textures:
    textures[key] = pygame.transform.scale(textures[key], (GRID_SIZE, GRID_SIZE))

# Генерація карти
def generate_map():
    map_data = []
    for y in range(0, WINDOW_HEIGHT - 100, GRID_SIZE):  # Віднімаємо 100 пікселів для панелі інструментів
        row = []
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            texture_key = random.choice(list(textures.keys())[:5])  # Вибираємо тільки текстури трави
            row.append(texture_key)
        map_data.append(row)
    return map_data

# Малювання карти
def draw_map(map_data, buildings):
    for y, row in enumerate(map_data):
        for x, texture_key in enumerate(row):
            screen.blit(textures[texture_key], (x * GRID_SIZE, y * GRID_SIZE))
    
    for building in buildings:
        if building["type"] == "road":
            texture_key = building["texture"]
            screen.blit(textures[texture_key], (building["x"] * GRID_SIZE, building["y"] * GRID_SIZE))
        else:
            texture_key = building["texture"]
            screen.blit(textures[texture_key], (building["x"] * GRID_SIZE, building["y"] * GRID_SIZE))

# Малювання сітки
def draw_grid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT - 100))
    for y in range(0, WINDOW_HEIGHT - 100, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))

# Малювання панелі інструментів
def draw_toolbar(selected_tool, selected_road_texture):
    pygame.draw.rect(screen, DARK_GRAY, (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100))
    font = pygame.font.SysFont(None, 36)
    text = font.render("Toolbar", True, WHITE)
    screen.blit(text, (10, WINDOW_HEIGHT - 80))

    # Відображення іконок будівель
    building_tools = [
        {"texture": "house", "rect": pygame.Rect(10, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "house"},
        {"texture": "factory", "rect": pygame.Rect(60, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "factory"},
        {"texture": "shop", "rect": pygame.Rect(110, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "shop"},
        {"texture": "office", "rect": pygame.Rect(160, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "office"}
    ]

    road_tools = [
        {"texture": "road_vertical", "rect": pygame.Rect(220, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"},
        {"texture": "road_vertical_right", "rect": pygame.Rect(270, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"},
        {"texture": "road_vertical_left", "rect": pygame.Rect(320, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"},
        {"texture": "road_vertical_horizontal", "rect": pygame.Rect(370, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"},
        {"texture": "road_horizontal", "rect": pygame.Rect(420, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"},
        {"texture": "road_horizontal_right", "rect": pygame.Rect(470, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"},
        {"texture": "road_horizontal_left", "rect": pygame.Rect(520, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"},
        {"texture": "road_1", "rect": pygame.Rect(570, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"},
        {"texture": "road_2", "rect": pygame.Rect(620, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"},
        {"texture": "road_3", "rect": pygame.Rect(670, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"},
        {"texture": "road_4", "rect": pygame.Rect(720, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "road"}
    ]

    delete_tool = {"texture": "delete", "rect": pygame.Rect(780, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "delete"}

    # Інструменти для електрики, води та утилізації відходів
    utility_tools = [
        {"texture": "power_plant", "rect": pygame.Rect(840, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "power_plant"},
        {"texture": "water_tower", "rect": pygame.Rect(890, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "water_tower"},
        {"texture": "waste_facility", "rect": pygame.Rect(940, WINDOW_HEIGHT - 60, GRID_SIZE, GRID_SIZE), "type": "waste_facility"}
    ]

    for tool in building_tools:
        rect = tool["rect"]
        if selected_tool == tool["type"]:
            pygame.draw.rect(screen, WHITE, rect.inflate(4, 4))  # Рамка для вибраного інструменту
        screen.blit(textures[tool["texture"]], rect.topleft)

    for tool in road_tools:
        rect = tool["rect"]
        if selected_road_texture == tool["texture"]:
            pygame.draw.rect(screen, WHITE, rect.inflate(4, 4))  # Рамка для вибраного інструменту
        screen.blit(textures[tool["texture"]], rect.topleft)

    rect = delete_tool["rect"]
    if selected_tool == delete_tool["type"]:
        pygame.draw.rect(screen, WHITE, rect.inflate(4, 4))  # Рамка для вибраного інструменту
    screen.blit(textures[delete_tool["texture"]], rect.topleft)

    for tool in utility_tools:
        rect = tool["rect"]
        if selected_tool == tool["type"]:
            pygame.draw.rect(screen, WHITE, rect.inflate(4, 4))  # Рамка для вибраного інструменту
        screen.blit(textures[tool["texture"]], rect.topleft)

    return building_tools, road_tools, delete_tool, utility_tools

# Економічна система
class Economy:
    def __init__(self):
        self.budget = 50000
        self.income = 0
        self.expenses = 0
        self.building_costs = {
            "house": 5000,
            "factory": 10000,
            "shop": 2000,
            "office": 3000,
            "road": 500,
            "power_plant": 20000,
            "water_tower": 15000,
            "waste_facility": 18000
        }
        self.maintenance_costs = {
            "house": 10,
            "factory": 50,
            "shop": 20,
            "office": 30,
            "road": 5,
            "power_plant": 100,
            "water_tower": 75,
            "waste_facility": 90
        }
        self.tax_rates = {
            "house": 0.05,
            "factory": 0.10,
            "shop": 0.07,
            "office": 0.08
        }

    def update_budget(self, buildings):
        self.income = 0
        self.expenses = 0
        for building in buildings:
            if building["type"] in self.tax_rates:
                self.income += self.building_costs[building["type"]] * self.tax_rates[building["type"]]
            self.expenses += self.maintenance_costs.get(building["type"], 0)
        self.budget += self.income - self.expenses

    def can_build(self, building_type):
        return self.budget >= self.building_costs.get(building_type, 0)

    def build(self, building_type):
        if self.can_build(building_type):
            self.budget -= self.building_costs[building_type]

    def draw_economy(self):
        font = pygame.font.SysFont(None, 36)
        budget_text = font.render(f"Budget: ${self.budget}", True, WHITE)
        income_text = font.render(f"Income: ${self.income}", True, WHITE)
        expenses_text = font.render(f"Expenses: ${self.expenses}", True, WHITE)
        screen.blit(budget_text, (800, 10))
        screen.blit(income_text, (800, 40))
        screen.blit(expenses_text, (800, 70))

# Система населення
class Population:
    def __init__(self):
        self.population = 0
        self.employed = 0
        self.housing_capacity = {
            "house": 4
        }
        self.employment_capacity = {
            "factory": 10,
            "shop": 5,
            "office": 8
        }

    def update_population(self, buildings):
        self.population = 0
        self.employed = 0
        for building in buildings:
            self.population += self.housing_capacity.get(building["type"], 0)
            self.employed += self.employment_capacity.get(building["type"], 0)

    def draw_population(self):
        font = pygame.font.SysFont(None, 36)
        population_text = font.render(f"Population: {self.population}", True, WHITE)
        employed_text = font.render(f"Employed: {self.employed}", True, WHITE)
        screen.blit(population_text, (800, 100))
        screen.blit(employed_text, (800, 130))

# Система потреб
class Needs:
    def __init__(self):
        self.electricity = 0
        self.water = 0
        self.waste = 0
        self.electricity_capacity = 0
        self.water_capacity = 0
        self.waste_capacity = 0

    def update_needs(self, buildings):
        self.electricity = 0
        self.water = 0
        self.waste = 0
        self.electricity_capacity = 0
        self.water_capacity = 0
        self.waste_capacity = 0

        for building in buildings:
            if building["type"] == "house":
                self.electricity += 1
                self.water += 1
                self.waste += 1
            elif building["type"] == "factory":
                self.electricity += 5
                self.water += 3
                self.waste += 5
            elif building["type"] == "shop":
                self.electricity += 2
                self.water += 1
                self.waste += 2
            elif building["type"] == "office":
                self.electricity += 3
                self.water += 2
                self.waste += 3
            elif building["type"] == "power_plant":
                self.electricity_capacity += 10
            elif building["type"] == "water_tower":
                self.water_capacity += 10
            elif building["type"] == "waste_facility":
                self.waste_capacity += 10

    def draw_needs(self):
        font = pygame.font.SysFont(None, 36)
        electricity_text = font.render(f"Electricity: {self.electricity}/{self.electricity_capacity}", True, WHITE)
        water_text = font.render(f"Water: {self.water}/{self.water_capacity}", True, WHITE)
        waste_text = font.render(f"Waste: {self.waste}/{self.waste_capacity}", True, WHITE)
        screen.blit(electricity_text, (800, 160))
        screen.blit(water_text, (800, 190))
        screen.blit(waste_text, (800, 220))

# Основний цикл гри
def main():
    map_data = generate_map()
    buildings = []
    selected_tool = None
    selected_road_texture = None
    show_grid = False
    economy = Economy()
    population = Population()
    needs = Needs()  # Додаємо систему потреб
    paused = False  # Змінна для відстеження стану паузи

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if mouse_y >= WINDOW_HEIGHT - 100:
                    # Вибір інструменту
                    building_tools, road_tools, delete_tool, utility_tools = draw_toolbar(selected_tool, selected_road_texture)
                    for tool in building_tools:
                        if tool["rect"].collidepoint(mouse_x, mouse_y):
                            selected_tool = tool["type"]
                            selected_road_texture = None
                    for tool in road_tools:
                        if tool["rect"].collidepoint(mouse_x, mouse_y):
                            selected_tool = tool["type"]
                            selected_road_texture = tool["texture"]
                    if delete_tool["rect"].collidepoint(mouse_x, mouse_y):
                        selected_tool = "delete"
                        selected_road_texture = None
                    for tool in utility_tools:
                        if tool["rect"].collidepoint(mouse_x, mouse_y):
                            selected_tool = tool["type"]
                            selected_road_texture = None
                else:
                    # Розміщення або видалення будівлі
                    if selected_tool:
                        grid_x = mouse_x // GRID_SIZE
                        grid_y = mouse_y // GRID_SIZE
                        if selected_tool == "house" and economy.can_build("house"):
                            buildings.append({"x": grid_x, "y": grid_y, "texture": "house", "type": "house"})
                            economy.build("house")
                        elif selected_tool == "factory" and economy.can_build("factory"):
                            buildings.append({"x": grid_x, "y": grid_y, "texture": "factory", "type": "factory"})
                            economy.build("factory")
                        elif selected_tool == "shop" and economy.can_build("shop"):
                            buildings.append({"x": grid_x, "y": grid_y, "texture": "shop", "type": "shop"})
                            economy.build("shop")
                        elif selected_tool == "office" and economy.can_build("office"):
                            buildings.append({"x": grid_x, "y": grid_y, "texture": "office", "type": "office"})
                            economy.build("office")
                        elif selected_tool == "road" and selected_road_texture and economy.can_build("road"):
                            buildings.append({"x": grid_x, "y": grid_y, "texture": selected_road_texture, "type": "road"})
                            economy.build("road")
                        elif selected_tool == "power_plant" and economy.can_build("power_plant"):
                            buildings.append({"x": grid_x, "y": grid_y, "texture": "power_plant", "type": "power_plant"})
                            economy.build("power_plant")
                        elif selected_tool == "water_tower" and economy.can_build("water_tower"):
                            buildings.append({"x": grid_x, "y": grid_y, "texture": "water_tower", "type": "water_tower"})
                            economy.build("water_tower")
                        elif selected_tool == "waste_facility" and economy.can_build("waste_facility"):
                            buildings.append({"x": grid_x, "y": grid_y, "texture": "waste_facility", "type": "waste_facility"})
                            economy.build("waste_facility")
                        elif selected_tool == "delete":
                            for building in buildings:
                                if building["x"] == grid_x and building["y"] == grid_y:
                                    buildings.remove(building)
                                    break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    show_grid = not show_grid
                if event.key == pygame.K_SPACE:
                    paused = not paused

        screen.fill(BLACK)

        draw_map(map_data, buildings)
        if show_grid:
            draw_grid()
        building_tools, road_tools, delete_tool, utility_tools = draw_toolbar(selected_tool, selected_road_texture)

        # Оновлення економіки, населення та потреб, якщо гра не на паузі
        if not paused:
            economy.update_budget(buildings)
            population.update_population(buildings)
            needs.update_needs(buildings)  # Оновлюємо потреби

        economy.draw_economy()
        population.draw_population()
        needs.draw_needs()  # Малюємо потреби

        # Відображення статусу паузи
        if paused:
            font = pygame.font.SysFont(None, 36)
            pause_text = font.render("Пауза", True, WHITE)
            screen.blit(pause_text, (10, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()

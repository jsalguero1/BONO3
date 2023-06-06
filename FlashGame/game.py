import pygame
import random

# Dimensiones de la ventana del juego
WIDTH = 900
HEIGHT = 600

# Tamaño de la ciudad y tamaño de cada celda en la matriz
CITY_SIZE = 9
CELL_SIZE = 50

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

# Inicializar Pygame
pygame.init()

# Crear la ventana del juego
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FlashDay Game")

clock = pygame.time.Clock()

class City:
    def __init__(self, _tam):
        self.size = _tam 
        self.grid = [[None for i in range(_tam)] for i in range(_tam)]
        self.hamburguesas = []
        self.villanos = []

    def generate_points(self, _numHamburguesas, _numVillanos):
        self.hamburguesas = random.sample(range(self.size*self.size), _numHamburguesas)
        self.villanos = random.sample(range(self.size*self.size), _numVillanos)
        for hamburguesa in self.hamburguesas:
            row = hamburguesa // self.size
            col = hamburguesa % self.size
            self.grid[row][col] = "H"
        for villain in self.villanos:
            row = villain // self.size
            col = villain % self.size
            if self.grid[row][col] != "H":
                self.grid[row][col] = "V"



class FlashGame:
    def __init__(self, city):
        self.city = city
        self.energy = 5
        self.position = (random.randint(0, city.size-1), random.randint(0, city.size-1))
        self.visited = set()
        self.game_over = False
        self.game_won = False    


    def move(self, direction):
        if self.game_over or self.game_won:
            return

        new_position = None
        if direction == "up":
            if self.position[0]-1 < 0:
                return
            else:
                new_position = (self.position[0] - 1, self.position[1])
        elif direction == "down":
            if self.position[0]+1 >= self.city.size:
                return
            else:
                new_position = (self.position[0] + 1, self.position[1])
        elif direction == "left":
            if self.position[1]-1 < 0:
                return
            else:
                new_position = (self.position[0], self.position[1] - 1)
        elif direction == "right":
            if self.position[1]+1 >= self.city.size:
                return
            else:
                new_position = (self.position[0], self.position[1] + 1)

        if new_position is None or new_position in self.visited:
            return


        row, col = new_position
        if 0 <= row < self.city.size and 0 <= col < self.city.size:
            point = self.city.grid[row][col]
            if point == "H":
                self.energy += random.randint(1, 8)
                self.city.grid[row][col] = None
                self.city.hamburguesas.remove(row * self.city.size + col)
                if len(self.city.hamburguesas) == 0 and len(self.city.villanos) == 0:
                    self.game_won = True
            elif point == "V":
                self.energy -= random.randint(1, 3)
                self.city.grid[row][col] = None
                self.city.villanos.remove(row * self.city.size + col)
                if self.energy <= 0:
                    self.game_over = True
                if len(self.city.hamburguesas) == 0 and len(self.city.villanos) == 0:
                    self.game_won = True
            else:
                self.energy -= 1
                if self.energy <= 0:
                    self.game_over = True
                if len(self.city.hamburguesas) == 0 and len(self.city.villanos) == 0:
                    self.game_won = True
        
        if len(self.city.hamburguesas) == 0 and len(self.city.villanos) == 0:
            self.game_won = True

        self.visited.add(new_position)
        
        self.position = new_position

    def is_game_over(self):
        return self.game_over or self.game_won

class FlashGameGUI:
    def __init__(self, city, cell_size):
        self.city = city
        self.cell_size = cell_size
        self.game = FlashGame(city)
        self.hamburguesa_image = pygame.image.load("hamburguesa.png")
        self.ladron_image = pygame.image.load("ladron.png")
        self.hamburguesa_image = pygame.transform.scale(self.hamburguesa_image, (self.cell_size, self.cell_size))
        self.ladron_image = pygame.transform.scale(self.ladron_image, (self.cell_size, self.cell_size))
        self.flash_image = pygame.image.load("flash.png")
        self.flash_image = pygame.transform.scale(self.flash_image, (self.cell_size, self.cell_size))
        self.rayo_image = pygame.image.load("rayo.png")
        self.rayo_image = pygame.transform.scale(self.rayo_image, (self.cell_size, self.cell_size))


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_flash("up")
                    elif event.key == pygame.K_DOWN:
                        self.move_flash("down")
                    elif event.key == pygame.K_LEFT:
                        self.move_flash("left")
                    elif event.key == pygame.K_RIGHT:
                        self.move_flash("right")

            self.draw_city()
            self.draw_flash()
            self.draw_info()

            if self.game.is_game_over():
                self.show_game_over_message()

            pygame.display.update()
            clock.tick(60)

        pygame.quit()

    def move_flash(self, direction):
        self.game.move(direction)

    def draw_city(self):
        window.fill(BLANCO)
        for row in range(self.city.size):
            for col in range(self.city.size):
                cell_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(window, NEGRO, cell_rect, 1)
                if self.city.grid[row][col] == "H":
                    window.blit(self.hamburguesa_image, cell_rect)
                    #pygame.draw.circle(window, VERDE, (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2), self.cell_size // 4)
                elif self.city.grid[row][col] == "V":
                    window.blit(self.ladron_image, cell_rect)
                elif (row, col) in self.game.visited:
                    window.blit(self.rayo_image,cell_rect)

    def draw_flash(self):
        flash_rect = pygame.Rect(self.game.position[1] * self.cell_size, self.game.position[0] * self.cell_size, self.cell_size, self.cell_size)
        window.blit(self.flash_image, flash_rect)

    def draw_info(self):
        font = pygame.font.Font(None, 30)
        energy_text = font.render("Energía: {}".format(self.game.energy), True, NEGRO)
        position_text = font.render("Posición: {}".format(self.game.position), True, NEGRO)
        window.blit(energy_text, (WIDTH - energy_text.get_width() - 10, HEIGHT - energy_text.get_height() - 10))
        window.blit(position_text, (WIDTH - position_text.get_width() - 10, HEIGHT - energy_text.get_height() - position_text.get_height() - 20))

    def show_game_over_message(self):
        font = pygame.font.Font(None, 50)
        if self.game.game_won:
            game_over_text = font.render("¡Has ganado!", True, VERDE)
        else:
            game_over_text = font.render("¡Game Over!", True, ROJO)
        window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

# Crear una ciudad de tamaño CITY_SIZE y generar puntos
city = City(CITY_SIZE)
city.generate_points(10, 5)

# Crear y ejecutar la interfaz gráfica del juego
game_gui = FlashGameGUI(city, CELL_SIZE)
game_gui.run()

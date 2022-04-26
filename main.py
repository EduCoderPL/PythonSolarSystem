import pygame
import math

pygame.init()
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

FONT = pygame.font.SysFont("comicsans", 16)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)


targetScale = 1


def lerp(start, stop, interpolation):
    return start + (stop - start) * interpolation


class Button:
    def __init__(self, text, width, height, pos, elevation):
        self.pressed = False
        self.clicked = False

        self.elevation = elevation
        self.dynamicElevation = elevation
        self.originalYPosition = pos[1]

        self.topRect = pygame.Rect(pos, (width, height))
        self.topColor = "#475F77"

        self.bottomRect = pygame.Rect(pos, (width, height))
        self.bottomColor = "#354B5E"

        self.textSurf = FONT.render(f"  {text}  ", True, "#FFFFFF")
        self.textRect = self.textSurf.get_rect(center=self.topRect.center)

    def draw(self):
        self.topRect.y = self.originalYPosition - self.dynamicElevation
        self.textRect.center = self.topRect.center

        self.bottomRect.midtop = self.topRect.midtop
        self.bottomRect.height = self.topRect.height + self.dynamicElevation

        pygame.draw.rect(WIN, self.bottomColor, self.bottomRect, border_radius=3)
        pygame.draw.rect(WIN, self.topColor, self.topRect, border_radius=3)
        WIN.blit(self.textSurf, self.textRect)
        self.check_click()

    def check_click(self):
        mousePos = pygame.mouse.get_pos()
        if self.topRect.collidepoint(mousePos):
            self.topColor = '#D74B4B'
            if self.clicked:
                self.clicked = False
            if pygame.mouse.get_pressed()[0]:
                self.dynamicElevation = 0
                if not self.pressed:
                    self.clicked = True
                self.pressed = True
            elif self.pressed:
                self.pressed = False
            else:
                self.dynamicElevation = self.elevation
        else:

            self.topColor = "#475F77"


class Planet:
    offsetX = 0
    offsetY = 0
    AU = 146.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 3600 * 24

    listOfPlanets = []

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distanceToSun = 0

        self.xVel = 0
        self.yVel = 0

        Planet.listOfPlanets.append(self)

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2 + self.offsetX
                y = y * self.SCALE + HEIGHT / 2 + self.offsetY
                updated_points.append((x, y))

            pygame.draw.aalines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius * Planet.SCALE / (250 / Planet.AU))

        if not self.sun:
            distance_text = FONT.render(f"{math.trunc(self.distanceToSun)} km", True, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        self.distanceToSun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self):
        total_fx = total_fy = 0
        for planet in Planet.listOfPlanets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.xVel += total_fx / self.mass * self.TIMESTEP
        self.yVel += total_fy / self.mass * self.TIMESTEP

        self.x += self.xVel * self.TIMESTEP
        self.y += self.yVel * self.TIMESTEP

        self.orbit.append((self.x, self.y))
        if len(self.orbit) > 100:
            self.orbit.pop(0)


mousePos = [0, 0]


def change_timestep(change):
    Planet.TIMESTEP *= change


def main():
    button1 = Button("Double Speed", 200, 30, (10, 40), 6)
    button2 = Button("Half Speed", 200, 30, (10, 80), 6)
    button3 = Button("Reset Position", 200, 30, (10, 120), 6)

    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30)
    sun.sun = True
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24)
    earth.yVel = 29.783 * 1000
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 1.98892 * 10 ** 23)
    mars.yVel = 24.783 * 1000
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23)
    mercury.yVel = -47.783 * 1000
    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24)
    venus.yVel = -35.02 * 1000
    jupiter = Planet(5.203 * Planet.AU, 0, 25, RED, 1.90 * 10 ** 27)
    jupiter.yVel = -13.1 * 1000
    saturn = Planet(9.539 * Planet.AU, 0, 23, YELLOW, 5.69 * 10 ** 26)
    saturn.yVel = -9.7 * 1000
    uranus = Planet(19.18 * Planet.AU, 0, 21, BLUE, 8.68 * 10 ** 25)
    uranus.yVel = -6.8 * 1000
    neptune = Planet(30.06 * Planet.AU, 0, 22, WHITE, 1.02 * 10 ** 26)
    neptune.yVel = -5.4 * 1000
    pluto = Planet(39.53 * Planet.AU, 0, 6, DARK_GREY, 1.29 * 10 ** 22)
    pluto.yVel = -4.67 * 1000

    targetScale = 250/Planet.AU

    while run:

        textsurface = FONT.render(f"Speed scale: {Planet.SCALE}", False, WHITE)

        clock.tick(60)
        WIN.fill((0, 0, 0))

        WIN.blit(textsurface, (100, 0))

        button1.draw()
        button2.draw()
        button3.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[1]:
                Planet.offsetX -= (mousePos[0] - pygame.mouse.get_pos()[0])
                Planet.offsetY -= (mousePos[1] - pygame.mouse.get_pos()[1])

            if event.type == pygame.MOUSEWHEEL:
                targetScale *= 1.4 ** event.y
                # Planet.SCALE *= 1.4 ** event.y

        for planet in Planet.listOfPlanets:
            planet.update_position()
            planet.draw(WIN)

        if button1.clicked:
            change_timestep(2)
        if button2.clicked:
            change_timestep(1 / 2)
        if button3.clicked:
            Planet.offsetY = Planet.offsetX = 0

        Planet.SCALE = lerp(Planet.SCALE, targetScale, 0.1)

        mousePos[0] = pygame.mouse.get_pos()[0]
        mousePos[1] = pygame.mouse.get_pos()[1]

        pygame.display.update()


    pygame.quit()


main()

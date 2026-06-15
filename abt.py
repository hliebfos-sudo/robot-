import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
FPS = 60
ROBOT_RADIUS = 15
ROBOT_SPEED = 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Розумний робот-пилосос")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (0, 200, 0)
GRAY = (120, 120, 120)
RED = (220, 50, 50)
BLUE = (0, 100, 255)
LIGHT_GREEN = (200, 255, 200)

dirt = []
for _ in range(150):
    dirt.append([
        random.randint(20, WIDTH - 20),
        random.randint(20, HEIGHT - 20)
    ])

obstacles = [
    pygame.Rect(250, 150, 100, 250),
    pygame.Rect(500, 100, 150, 80),
    pygame.Rect(450, 350, 200, 100)
]

robot_x = 100
robot_y = 100
angle = 0

battery = 100.0

base_x = 50
base_y = 50

trail = []
visited = set()

font = pygame.font.SysFont(None, 28)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    battery -= 0.003

    if battery <= 0:
        battery = 0

    if battery < 20:
        angle = math.atan2(
            base_y - robot_y,
            base_x - robot_x
        )
    elif dirt:
        nearest = min(
            dirt,
            key=lambda d: math.hypot(
                robot_x - d[0],
                robot_y - d[1]
            )
        )

        angle = math.atan2(
            nearest[1] - robot_y,
            nearest[0] - robot_x
        )

    new_x = robot_x + math.cos(angle) * ROBOT_SPEED
    new_y = robot_y + math.sin(angle) * ROBOT_SPEED

    collision = False

    if (
        new_x < ROBOT_RADIUS or
        new_x > WIDTH - ROBOT_RADIUS or
        new_y < ROBOT_RADIUS or
        new_y > HEIGHT - ROBOT_RADIUS
    ):
        collision = True

    robot_rect = pygame.Rect(
        new_x - ROBOT_RADIUS,
        new_y - ROBOT_RADIUS,
        ROBOT_RADIUS * 2,
        ROBOT_RADIUS * 2
    )

    for obstacle in obstacles:
        if robot_rect.colliderect(obstacle):
            collision = True
            break

    if collision:
        angle += random.uniform(
            math.pi / 2,
            math.pi
        )
    else:
        robot_x = new_x
        robot_y = new_y

    if (
        battery < 20 and
        math.hypot(
            robot_x - base_x,
            robot_y - base_y
        ) < 25
    ):
        battery += 0.2
        if battery > 100:
            battery = 100

    trail.append((robot_x, robot_y))

    if len(trail) > 5000:
        trail.pop(0)

    cell = (
        int(robot_x // 20),
        int(robot_y // 20)
    )
    visited.add(cell)

    cleaned = []

    for d in dirt:
        if math.hypot(
            robot_x - d[0],
            robot_y - d[1]
        ) < ROBOT_RADIUS + 5:
            cleaned.append(d)

    for d in cleaned:
        dirt.remove(d)

    coverage = (
        len(visited) /
        ((WIDTH // 20) * (HEIGHT // 20))
    ) * 100

    screen.fill(WHITE)

    for point in trail:
        pygame.draw.circle(
            screen,
            LIGHT_GREEN,
            (int(point[0]), int(point[1])),
            2
        )

    for d in dirt:
        pygame.draw.circle(
            screen,
            RED,
            d,
            4
        )

    for obstacle in obstacles:
        pygame.draw.rect(
            screen,
            GRAY,
            obstacle
        )

    pygame.draw.rect(
        screen,
        BLUE,
        (base_x - 20, base_y - 20, 40, 40)
    )

    pygame.draw.circle(
        screen,
        GREEN,
        (int(robot_x), int(robot_y)),
        ROBOT_RADIUS
    )

    pygame.draw.line(
        screen,
        BLACK,
        (robot_x, robot_y),
        (
            robot_x + math.cos(angle) * 25,
            robot_y + math.sin(angle) * 25
        ),
        3
    )

    battery_text = font.render(
        f"Battery: {battery:.0f}%",
        True,
        BLACK
    )

    dirt_text = font.render(
        f"Сміття: {len(dirt)}",
        True,
        BLACK
    )

    coverage_text = font.render(
        f"Покриття: {coverage:.1f}%",
        True,
        BLACK
    )

    screen.blit(battery_text, (10, 10))
    screen.blit(dirt_text, (10, 40))
    screen.blit(coverage_text, (10, 70))

    pygame.display.flip()

pygame.quit()
import pygame
import heapq
from tkinter import messagebox

grid_size = 60
cols, rows = 15, 10
width, height = cols * grid_size, rows * grid_size

WEIGHTS = {
    "obstacle": float('inf'),
    "road": 1,
    "ground": 2,
    "sand": 3,
    "end": 0,
    "start": 0
}

COLORS = {
    "obstacle": (0, 0, 0),
    "road": (200, 200, 200),
    "ground": (139, 69, 19),
    "sand": (255, 255, 102),
    "start": (0, 255, 0),
    "end": (255, 0, 0),
    "path": (0, 0, 255),
}

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("A* Pathfinding")

grid = [["road" for _ in range(cols)] for _ in range(rows)]
start, end = None, None


def draw_grid():
    for y in range(rows):
        for x in range(cols):
            cell = grid[y][x]
            color = COLORS[cell]
            pygame.draw.rect(screen, color, (x * grid_size, y * grid_size, grid_size, grid_size))
            pygame.draw.rect(screen, (0, 0, 0), (x * grid_size, y * grid_size, grid_size, grid_size), 1)


def get_cell(pos):
    x, y = pos
    return x // grid_size, y // grid_size


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, end, weights):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score[end]

        neighbors = [(current[0] + dr, current[1] + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        neighbors = [(x, y) for x, y in neighbors if 0 <= x < cols and 0 <= y < rows]

        for neighbor in neighbors:
            x, y = neighbor
            if grid[y][x] == "obstacle":
                continue
            tentative_g_score = g_score[current] + weights[grid[y][x]]
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


running = True
messagebox.showinfo("Горячие клавиши",
                    "ЛКМ - стена \n ПКМ - удалить объект \n P - песочек \n Z - земля \n R - рестарт \n "
                    "E - конечная точка \n  S - начальная точка \n space - построить путь")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0]:
            x, y = get_cell(pygame.mouse.get_pos())
            grid[y][x] = "obstacle"

        if pygame.mouse.get_pressed()[2]:
            x, y = get_cell(pygame.mouse.get_pos())
            grid[y][x] = "road"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                grid = [["road" for _ in range(cols)] for _ in range(rows)]
                start, end = None, None

            if event.key == pygame.K_s:
                x, y = get_cell(pygame.mouse.get_pos())
                start = (x, y)
                grid[y][x] = "start"

            if event.key == pygame.K_e:
                x, y = get_cell(pygame.mouse.get_pos())
                end = (x, y)
                grid[y][x] = "end"

            if event.key == pygame.K_z:
                x, y = get_cell(pygame.mouse.get_pos())
                grid[y][x] = "ground"

            if event.key == pygame.K_p:
                x, y = get_cell(pygame.mouse.get_pos())
                grid[y][x] = "sand"

            if event.key == pygame.K_SPACE and start and end:
                path, path_len = a_star(grid, start, end, WEIGHTS)
                if path:
                    for x, y in path:
                        grid[y][x] = "path"
                    grid[end[1]][end[0]] = "end"
                    grid[start[1]][start[0]] = "start"
                    print("Путь : ", *path)
                    messagebox.showinfo(" ", f"Длина пути:{path_len}")
                else:
                    messagebox.showinfo("Oшибка", "Нету пути")

    screen.fill((255, 255, 255))
    draw_grid()
    pygame.display.flip()

pygame.quit()

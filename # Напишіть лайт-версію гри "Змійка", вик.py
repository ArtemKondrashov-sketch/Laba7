# Напишіть лайт-версію гри "Змійка", використовуючи Pygame. Змійка їсть червоні яблука,
# які з'являються у випадкових позиціях у межах ігрового поля, та додає у довжині після
# кожного яблука. При зіткненні з хвостом чи межею вікна гра закінчується.
import pygame
import random

pygame.init()
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")
green = (0, 255, 0)
red = (255, 0, 0)
font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

# Основні параметри гри
cell_size = 17
snake_speed = 6
snake_length = 1
snake_body = [pygame.Rect(screen_width // 2, screen_height // 2, cell_size, cell_size)]

# Створюємо змію та визначаємо напрям її руху
for i in range(snake_length):
    snake_body.append(pygame.Rect(screen_width // 2, screen_height // 2, cell_size, cell_size))
snake_direction = "RIGHT"
new_direction = "RIGHT"

# Визначаємо випадкове положення для яблука
apple_position = pygame.Rect(
    random.randint(0, (screen_width - cell_size) // cell_size) * cell_size,
    random.randint(0, (screen_height - cell_size) // cell_size) * cell_size,
    cell_size,
    cell_size
)

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        # Визначаємо новий напрямок руху змії
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                new_direction = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                new_direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                new_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                new_direction = "RIGHT"

    # Керування змією
    snake_direction = new_direction
    head = snake_body[0]
    if snake_direction == "UP":
        new_head = pygame.Rect(head.x, head.y - cell_size, cell_size, cell_size)
    elif snake_direction == "DOWN":
        new_head = pygame.Rect(head.x, head.y + cell_size, cell_size, cell_size)
    elif snake_direction == "LEFT":
        new_head = pygame.Rect(head.x - cell_size, head.y, cell_size, cell_size)
    elif snake_direction == "RIGHT":
        new_head = pygame.Rect(head.x + cell_size, head.y, cell_size, cell_size)

    # Перевіряємо, чи з'їла змія яблуко
    if snake_body[0].colliderect(apple_position):
        apple_position = pygame.Rect(
            random.randint(0, (screen_width - cell_size) // cell_size) * cell_size,
            random.randint(0, (screen_height - cell_size) // cell_size) * cell_size,
            cell_size,
            cell_size
        )
        snake_body.insert(0, new_head)  # Збільшуємо змію
    else:
        snake_body.insert(0, new_head)  # Додаємо нову голову
        snake_body.pop()  # Видаляємо хвіст

    # Перевірка на зіткнення зі стінками
    if new_head.x < 0 or new_head.x >= screen_width or new_head.y < 0 or new_head.y >= screen_height:
        game_over = True

    # Перевірка на зіткнення голови змії із власним тілом
    if new_head in snake_body[1:]:
        game_over = True

    screen.fill((0, 0, 0))
    # Малюємо змію
    for segment in snake_body:
        pygame.draw.rect(screen, green, segment)

    # Малюємо яблуко
    pygame.draw.circle(screen, red, apple_position.center, cell_size // 2)

    # Друкуємо кількість з'їдених яблук
    score_text = font.render(f"Score: {len(snake_body) - 1}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.update()

    clock.tick(snake_speed)

pygame.quit()

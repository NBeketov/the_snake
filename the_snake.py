import sys
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Константа для центра экрана.
DEFAULT_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Базовый класс для игровых объектов
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=DEFAULT_POSITION, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заготовка метода отрисовки."""
        raise NotImplementedError(
            f'Переопредели метод draw в классе {self.__class__.__name__}'
        )

    def draw_cell(self, position):
        """Отрисовывает одну ячейку игрового объекта на экране.

        Args:
            position (tuple[int, int]): Координаты ячейки (x, y) в пикселях.
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)

        if occupied_positions is None:
            occupied_positions = []

        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию, не занятую змейкой."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1

        self.positions = [self.position]

        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def update_direction(self, next_direction):
        """Применяет следующее направление движения (если оно задано)."""
        if next_direction:
            self.direction = next_direction

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки.

        Returns:
            tuple[int, int]: Координаты головы змейки (x, y) в пикселях.
        """
        return self.positions[0]

    def draw(self):
        """Отрисовывает змейку."""
        self.draw_cell(self.get_head_position())

        # Рисуем остальное тело
        for position in self.positions[1:]:
            self.draw_cell(position)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Перемещает змейку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        self.last = None

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и возвращает новое направление.

    Args:
        game_object: Экземпляр класса Snake.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_UP and game_object.direction != DOWN:
                return UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                return DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                return LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                return RIGHT
    return None


def main():
    """Запускает игру и содержит основной игровой цикл."""
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)

    snake = Snake()

    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)

        next_direction = handle_keys(snake)
        snake.update_direction(next_direction)

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_positions=snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(occupied_positions=snake.positions)

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()

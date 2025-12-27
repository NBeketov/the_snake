from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов.

    Атрибуты:
        position: Координаты объекта на игровом поле (x, y).
        body_color: Цвет объекта (RGB).
    """
    def __init__(self, position=CENTER_POSITION, body_color=None):
        """Инициализирует базовые атрибуты игрового объекта.

        Args:
            position: Начальная позиция объекта. Если не задана — центр экрана.
        """
        self.position = position
        self.body_color = body_color

    
    def draw_cell(self, position=None, body_color=None):
        """Рисует одну ячейку сетки.

        Args:
            position: Координаты верхнего левого угла клетки.
            body_color: Цвет заливки клетки (RGB).
        """
        position = position if position is not None else self.position
        body_color = body_color if body_color is not None else self.body_color
                
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
    

    def draw(self):
        """Заготовка метода отрисовки (переопределяется в наследниках)."""
        raise NotImplementedError(
            f'draw() is not implemented in {self.__class__.__name__}'
        )


class Apple(GameObject):
    """Класс яблока.

    Яблоко появляется в случайной клетке игрового поля.
    """

    def __init__(self, body_color=APPLE_COLOR):
        """Создаёт яблоко, задаёт цвет и начальную позицию."""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self, occupied=None):
        """Устанавливает яблоку случайную позицию в пределах игрового поля."""
        occupied = occupied or set()
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in occupied:
                self.position = position
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        self.draw_cell()


class Snake(GameObject):
    """Класс змейки.

    Хранит тело змейки в списке positions и управляет движением/отрисовкой.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует змейку в центре поля и задаёт начальные параметры."""
        super().__init__(position=CENTER_POSITION, body_color=body_color)
        self.reset(direction=RIGHT)

    def reset(self, direction=None):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length = 1
        self.position = CENTER_POSITION
        self.positions = [self.position]
        self.direction = (
            direction if direction is not None
            else choice([UP, DOWN, LEFT, RIGHT])
            )
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Применяет следующее направление движения (если оно задано)."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    
    def get_next_head_position(self):
        """Возвращает координаты следующей позиции головы (без движения)."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        return (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
    

    def draw(self):
        """Отрисовывает змейку и затирает хвостовой сегмент (если нужно)."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Перемещает змейку на одну клетку с переходом через границы поля."""
        new_head = self.get_next_head_position()
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None


def handle_keys(game_object):
    """Обрабатывает события pygame и меняет направление движения змейки.

    Args:
        game_object: Экземпляр класса Snake.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запускает игру и содержит основной игровой цикл."""
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple()
    apple.randomize_position(set(snake.positions))

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        next_head = snake.get_next_head_position()
        if next_head == apple.position:
            snake.length += 1
        snake.move()
        if snake.get_head_position() == apple.position:
            apple.randomize_position(set(snake.positions))
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(set(snake.positions))
        apple.draw()
        snake.draw()


        pygame.display.update()


if __name__ == '__main__':
    main()

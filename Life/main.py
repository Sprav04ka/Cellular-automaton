import sys
import time
import pygame

# Цвета фона и клетки
BACKGROUND_COLOR = (63, 63, 63)
CELL_COLOR = (255, 255, 255)

# Шиина и высота экрана
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
# Размер клетки и сетки
CELL_SIZE = 10

FIELD_WIDTH = SCREEN_WIDTH // CELL_SIZE
FIELD_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Интервал (период), через который будет происходить вычисление следующего поколения клеткок. В секундах
# Скорость регулируется колесом мыши. Раз в 2 секунды - медленно, раз в 0.1 секунду - быстро
GAME_SPEED_MIN = 2.0
GAME_SPEED_MAX = 0.1

# Изменение скорости за 1 событие прокрутки колеса мышки
GAME_SPEED_INCREMENT_DECREMENT = 0.05


def generation(cells: list, surface: pygame.Surface) -> None:
    """
    Метод (функция), которая будет просчитывать что происходит с клетками
    :param cells: Список живых клеток
    :param surface: Объект типа pygame.Surface для отрисовки рождённых или умерших клеток
    """
    cells_to_delete = []
    cells_to_create = []
    # Пробегаем всё поле по X
    for x in range(FIELD_WIDTH):
        # Пробегаем всё поле по Y
        for y in range(FIELD_HEIGHT):
            # Считаем живые клетки
            alive_cells_counter = 0
            for x_zone_x in range(x - 1, x + 2):
                for y_zone_y in range(y - 1, y + 2):

                    x_zone_x_fixed = x_zone_x
                    y_zone_y_fixed = y_zone_y
                    if x_zone_x_fixed >= FIELD_WIDTH:
                        # 64 - 64 = 0
                        x_zone_x_fixed = FIELD_WIDTH - x_zone_x_fixed
                    elif x_zone_x_fixed < 0:
                        # 64 + (-1) = 63
                        x_zone_x_fixed = FIELD_WIDTH + x_zone_x_fixed

                    if y_zone_y_fixed >= FIELD_HEIGHT:
                        # 64 - 64 = 0
                        y_zone_y_fixed = FIELD_HEIGHT - y_zone_y_fixed
                    elif y_zone_y_fixed < 0:
                        # 64 + (-1) = 63
                        y_zone_y_fixed = FIELD_HEIGHT + y_zone_y_fixed
                    if x_zone_x_fixed != x or y_zone_y_fixed != y:
                        if [x_zone_x_fixed, y_zone_y_fixed] in cells:
                            alive_cells_counter += 1
            if [x, y] in cells:
                if alive_cells_counter > 3 or alive_cells_counter < 2:
                    # cell_modify(cells, surface, x, y, False)
                    cells_to_delete.append([x, y])

            elif alive_cells_counter == 3:
                # cell_modify(cells, surface, x, y, True)
                cells_to_create.append([x, y])
    for cell in cells_to_delete:
        cell_modify(cells, surface, cell[0], cell[1], False)
    for cell in cells_to_create:
        cell_modify(cells, surface, cell[0], cell[1], True)
    del cells_to_delete
    del cells_to_create


def cell_modify(cells: list, surface: pygame.Surface, x: float or int, y: float or int, create: bool) -> None:
    """
    Метод (функция), которая создаёт или удаляет клетки
    :param cells: Список живых клеток
    :param surface: Объект типа pygame.Surface для отрисовки рождённых или умерших клеток
    :param x: X - координата клетки (от 0 до SCREEN_WIDTH // CELL_SIZE - 1)
    :param y: Y - координата клетки (от 0 до SCREEN_HEIGHT // CELL_SIZE - 1)
    :param create: True чтобы создать клетку, False чтобы удалить
    """
    # Создание клетки
    if create:
        # Отрисовка клетки
        pygame.draw.rect(surface, CELL_COLOR, pygame.Rect(
            x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()

        # Добавление клетки в список
        cells.append([x, y])
        print("Создаем")

    # Удаление клетки
    else:
        # удаляем по индексу
        del cells[cells.index([x, y])]

        # Закрашиваем её место цветом фона
        pygame.draw.rect(surface, BACKGROUND_COLOR, pygame.Rect(
            x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        print("Удаляем")


def main() -> None:
    """
    Основной метод (функция) программы
    """
    # Инициализация библиотеки PyGame
    pygame.init()

    # Инициализация и создание окна
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Игра жизни")

    # Заполнение фона
    surface.fill(BACKGROUND_COLOR)
    pygame.display.flip()

    # Список клеток (двухмерный)
    cells = []

    # Если True то игра на паузе, если False то нет
    space_to_pause = False

    # Скорость игры. Начнём с середины
    game_speed = (GAME_SPEED_MIN + GAME_SPEED_MAX) / 2

    # Переменная которая будет хранить время предыдущего вызова метода. Таймер чтобы регулировать скорость игры
    generation_time_last = time.time()

    # Основной цикл
    while True:
        # Просмотр всех эвентов от pygame
        for event in pygame.event.get():
            # Событие отжатия мыши и проверка что это левая кнопка -> генераация новой клетки
            # 1 - left click
            # 2 - middle click
            # 3 - right click
            # 4 - scroll up
            # 5 - scroll down
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Получаем координаты нажатия
                x, y = event.pos

                # Выравниваем по сетке
                # Например у нас X это 11.5 а размер сетки 10. Тогда 11.5 // 10 даст 1 (// это целочисленое деление)
                x = x // CELL_SIZE
                y = y // CELL_SIZE

                # Проверяем нет ли такой клетки
                if [x, y] in cells:
                    # Удаляем
                    cell_modify(cells, surface, x, y, False)

                # Клетки нет
                else:
                    # Создаём
                    cell_modify(cells, surface, x, y, True)
            # Событие прокрутки колёсика мышки
            elif event.type == pygame.MOUSEWHEEL:
                # Движение колёсика вверх
                if event.y > 0:
                    # Проверка, можно ли уменьшить интервал еще больше (увеличить скорость)
                    if game_speed > GAME_SPEED_MAX:
                        game_speed -= GAME_SPEED_INCREMENT_DECREMENT
                    else:
                        print("Скорость и так уже слишком высокая")

                # Движение колёсика вниз
                elif event.y < 0:
                    # Проверка, можно ли увеличить интервал еще больше (уменьшить скорость)
                    if game_speed < GAME_SPEED_MIN:
                        game_speed += GAME_SPEED_INCREMENT_DECREMENT
                    else:
                        print("Скорость и так уже слишком низкая")

            # Событие паузы по нажатию пробела
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if space_to_pause == False:
                    space_to_pause = True
                    print("Включена пауза")
                else:
                    space_to_pause = False
                    print("Пауза выключена")

            # Событие выхода -> завершаем всё и выходим из всего
            elif event.type == pygame.QUIT:
                print("Выход")
                pygame.quit()
                sys.exit()

        # После просмотра всех эвентов от pygame проверяем не на паузе ли наша игра
        # И прошло ли достаточно времени чтобы обновить клетки
        if not space_to_pause and time.time() - generation_time_last >= game_speed:
            # Запоминаем время для следующего цикла
            generation_time_last = time.time()

            # Вызываем функцию обновления клеток
            generation(cells, surface)


if __name__ == "__main__":
    main()

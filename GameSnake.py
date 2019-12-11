import pygame, random, os
pygame.init()



#===== КЛАССЫ =====#
# Точка
class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def equal(self, other):
        if self.x == other.x and self.y == other.y: return True
        else: return False

# Размер
class Size:
    def __init__(self, x = 0, y = None):
        self.x = x

        if y == None: self.y = x
        else: self.y = y



#===== ПЕРЕМЕННЫЕ =====#
direction = 'None' # Клавиша, нажатая последней
score = 0 # Число сегментов и кол-во очков
snakeSegments = [] # Список координат сегментов змейки
millisecondLeft = 0 # Времени прошло



#===== ФУНКЦИИ =====#
# Вывод информации об игре в консоль
def info():
    os.system("cls") # Очистка консоли
    print('Времени прошло: ' + str(millisecondLeft // 1000) + ' секунд') # Вывод очков в консоль
    print('Счет: ' + str(score)) # Вывод очков в консоль

# Генерация координат яблока
def appleGenerate():
    point = Point(random.randrange(0, coordSize.x), random.randrange(0, coordSize.y))
    return point

# Управление
def move(key):
    if   key == pygame.K_w and (score < 1 or direction != 'Down'):    return 'Up'
    elif key == pygame.K_s and (score < 1 or direction != 'Up'):      return 'Down'
    elif key == pygame.K_a and (score < 1 or direction != 'Right'):   return 'Left'
    elif key == pygame.K_d and (score < 1 or direction != 'Left'):    return 'Right'
    return direction

# Конец игры
def gameEnd():
    # Столкновение со стеной
    if (position.x < 0) or (position.x > coordSize.x) or (position.y < 0) or (position.y > coordSize.y):
        print('Причина смерти: Столкновение со стеной') #Вывод в консоль
        exit(0)

    # Столкновение с телом
    for segment in snakeSegments:
        if (position.equal(segment)):
            print('Причина смерти: Столкновение с телом') #Вывод в консоль
            exit(0)


#===== РАЗМЕРЫ И КООРДИНАТЫ =====#
cellSize = 25 # Размер клетки
screenSize = Size(900, 700) # Размер окна
coordSize = Size(screenSize.x // cellSize, screenSize.y // cellSize) # Размер сетки

position = Point(coordSize.x // 2, coordSize.y // 2) # Координаты змейки
appleCoords = appleGenerate()



#===== РАБОТА С ПОВЕРХНОСТЯМИ =====#
# Отрисовка элементов
def draw():
    screenGame.fill((60, 174, 11)) # Заливка фона

    pygame.draw.circle(screenGame, (255, 6, 6), (appleCoords.x * cellSize + cellSize // 2, appleCoords.y * cellSize + cellSize // 2), 12)  # Отрисовка яблока

    screenGame.blit(snakeHead, (position.x * cellSize, position.y * cellSize)) # Отрисовка головы
    # Отрисовка тела
    for i in range (0, score):
        screenGame.blit(snakeBody, (snakeSegments[i].x * cellSize, snakeSegments[i].y * cellSize)) # Отрисовка сегмента тела
    
    screenGame.blit(textScore, (700, 0)) # Отрисовка очков


screenGame = pygame.display.set_mode((screenSize.x, screenSize.y)) # Установка экрана игры

font = pygame.font.Font(None, 37) # Установка шрифта
textScore = font.render('Счет: ', 0, (0, 0, 0)) # Строка "Счет"

snakeHead = pygame.Surface((cellSize, cellSize)) # Создание головы
snakeHead.fill((249, 180, 6)) # Заливка головы

snakeBody = pygame.Surface((cellSize, cellSize)) # Создание тела
snakeBody.fill((252, 210, 106)) # Заливка тела


# Игра
while 1:
    for event in pygame.event.get(): # Получение события с модуля
        if event.type == pygame.QUIT: exit(0) # Выход
        elif event.type == pygame.KEYDOWN: direction = move(event.key) # Если была нажата клавиша

    # Смещение сегментов тела
    if (len(snakeSegments) > 0):
        snakeSegments.insert(0, Point(position.x, position.y))
        snakeSegments.pop()

    #===== ДВИЖЕНИЕ =====#
    if   direction == 'Up':     position.y -= 1 # Вверх
    elif direction == 'Down':   position.y += 1 # Вниз
    elif direction == 'Left':   position.x -= 1 # Влево
    elif direction == 'Right':  position.x += 1 # Вправо
    #====================#

    gameEnd() # Проверка на завершении игры
    draw() # Отрисовка элементов

    # Если змейка съела яблоко
    if position.equal(appleCoords):
        # Добавление сегмента в список
        if len(snakeSegments) == 0: snakeSegments.append(Point(position.x, position.y))
        else: snakeSegments.append(snakeSegments[len(snakeSegments) - 1])

        appleCoords = appleGenerate(); # Создание нового яблока

        score += 1 #Увеличение очков
        textScore = font.render('Счет: ' + str(score), 0, (0, 0, 0)) # Обновление счета
    
    pygame.display.update() # Обновление экрана
    pygame.time.delay(100) # Пауза

    millisecondLeft += 100 # Увеличение пройденных мс
    info() # Вывод информации об игре в консоль

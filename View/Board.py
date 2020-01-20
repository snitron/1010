import pygame
import random

class Figure:
    x, y = 0, 0
    w, h = 0, 0
    type = ""

    def __init__(self, x, y, w, h, type):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.type = type

    def isClicked(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True


        return False


class Board:
    width = 10
    height = 10
    cell_size = 30
    little_left = 30
    little_top = 30

    x_start, y_start = 0, 0 #начальные координаты сетки
    first = True

    checked = False
    checked_figure = Figure(0, 0, 0, 0, "")

    to_choose = list() #список фигур, предлагаемых игроку для установки ()

    playing_desk = list()  # матрица размерами W*H (10 * 10)
                                  # 0 - поле пустое, 1 - оранжевый, 2 - зелёный, 3 - голубой
    # создание поля игры
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.border = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 50
        self.top = 50
        self.cell_size = 300

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, w, h):
        last_x, last_y = 0, 0
        for i in range(self.width):
            if(self.first):
                self.playing_desk.append(list())

            for j in range(self.height):
                color = pygame.Color("#FFFFFF")
                if(not self.first):
                    if(self.playing_desk[i][j].type == "0"):
                        color = pygame.Color("#FFFFFF")
                    elif(self.playing_desk[i][j].type == "1"):
                        color = pygame.Color("#e67e22")
                    elif(self.playing_desk[i][j].type == "2"):
                        color = pygame.Color("#27ae60")
                    else:
                        color = pygame.Color("#3498db")

                pygame.draw.rect(screen, color, (1 / 6 * w + j * self.left, 1 / 16 * h + i * self.top, self.top - 2.5, self.left - 2.5), 1)

                if(self.first):
                    self.playing_desk[i].append(Figure(1 / 6 * w + j * self.left, 1 / 16 * h + i * self.top, self.top - 2.5, self.left - 2.5, "0"))
                if(i == 9 and j == 0):
                    last_x, last_y = 1 / 6 * w + j * self.left, 1 / 16 * h + i * self.top

                if(i == 0 and j == 0):
                    self.x_start = 1 / 6 * w, 1 / 16 * h

        if(len(self.to_choose) == 0):
            for i in range(3):
                if(i == 0):
                    last_x, last_y = self.renderByRandom(screen, last_x + 50, last_y + 100)
                else:
                    last_x, last_y = self.renderByRandom(screen, last_x + 120, last_y)
            self.first = False
        else:
            for i in self.to_choose:
                if(i.type == "square2"):
                    self.renderSquare(screen, i.x, i.y, 2)
                elif(i.type == "square3"):
                    self.renderSquare(screen, i.x, i.y, 3)
                elif(i.type == "downLine2"):
                    self.renderDownLine(screen, i.x, i.y, 2)
                elif(i.type == "downLine3"):
                    self.renderDownLine(screen, i.x, i.y, 3)
                elif(i.type == "upperLine2"):
                    self.renderUpperLine(screen, i.x, i.y, 2)
                elif(i.type == "upperLine3"):
                    self.renderUpperLine(screen, i.x, i.y, 3)
                elif(i.type == "corner2"):
                    self.renderCorner(screen, i.x, i.y, 2)
                else:
                    self.renderCorner(screen, i.x, i.y, 3)

    def check_for_full_lines(self):
        toDeleteByWidth = list()
        toDeleteByHeight = list()

        for i in range(len(self.playing_desk)):
            wasZero = False
            for j in self.playing_desk[i]:
                if(j == 0):
                    wasZero = True

            if(not wasZero):
                toDeleteByWidth.append(i)

        for i in range(len(self.playing_desk)):
            wasZero = False
            for j in range(len(self.playing_desk[i])):
                if(self.playing_desk[j][i] == 0):
                    wasZero = True

            if(not wasZero):
                toDeleteByHeight.append(i)

    def renderSquare(self, screen, x, y, n):
        last_x, last_y = 0, 0

        for i in range(n):
            for j in range(n):
                const = 0

                if(i == 0 and j == 0):
                    const = 0
                else:
                    const = 1

                pygame.draw.rect(screen, pygame.Color("#27ae60"),
                                 (x + j * self.little_left, y + i * self.little_top, self.little_top, self.little_left), const)

                if(i == 0 and j == n - 1):
                    last_x, last_y = x + j * self.little_left, y + i * self.little_top

        if (self.first):
            self.to_choose.append(Figure(x, y, 30, 30, "square" + str(n)))
        return (last_x, last_y)

    def renderDownLine(self, screen, x, y, n): #горизонтальная линия (длина 2-3)
        last_x, last_y = 0, 0
        for i in range(n):
            const = 0

            if (i == 0):
                const = 0
            else:
                const = 1

            pygame.draw.rect(screen, pygame.Color("#e67e22"),
                             (x + i * self.little_left, y, self.little_top, self.little_left), const)
            if(i == n - 1):
                last_x, last_y = x + i * self.little_left, y

        if(self.first):
            self.to_choose.append(Figure(x, y, 30, 30, "downLine" + str(n)))
        return (last_x, last_y)

    def renderUpperLine(self, screen, x, y, n):
        last_x, last_y = 0, 0

        for i in range(n):
            const = 0

            if (i == 0):
                const = 0
            else:
                const = 1

            pygame.draw.rect(screen, pygame.Color("#e67e22"),
                             (x, y + i * self.little_top, self.little_top, self.little_left), const)
            if (i == 0):
                last_x, last_y = x, y + i * self.little_top

        if (self.first):
            self.to_choose.append(Figure(x, y, 30, 30, "upperLine" + str(n)))

        return (last_x, last_y)

    def renderCorner(self, screen, x, y, n):
        last_x, last_y = 0, 0

        for i in range(n):
            for j in range(n):
                if(j == 0):
                    const = 0

                    if (i == 0 and j == 0):
                        const = 0
                    else:
                        const = 1
                    pygame.draw.rect(screen, pygame.Color("#3498db"),
                                     (x + j * self.little_left, y + i * self.little_top, self.little_top,
                                      self.little_left), const)
                elif(i == n - 1):
                    pygame.draw.rect(screen, pygame.Color("#3498db"),
                                     (x + j * self.little_left, y + i * self.little_top, self.little_top,
                                      self.little_left), 1)

                elif(i == 0 and j == n - 1):
                    last_x, last_y = x + j * self.little_left, y + i * self.little_top

                else:
                    continue

        if (self.first):
            self.to_choose.append(Figure(x, y, 30, 30, "corner" + str(n)))
        return (last_x, last_y)

    def renderByRandom(self, screen, x, y):
        rand = random.randint(0, 3)

        l_x, l_y = 0, 0

        if(rand == 0):
            l_x, l_y = self.renderSquare(screen, x, y, random.randint(2, 3))
            print("renderSquare", l_x, l_y)
        elif(rand == 1):
            l_x, l_y = self.renderDownLine(screen, x, y, random.randint(2, 3))
            print("renderDownLine", l_x, l_y)
        elif(rand == 2):
            l_x, l_y = self.renderUpperLine(screen, x, y, random.randint(2, 3))
            print("renderUpperLine", l_x, l_y)
        elif(rand == 3):
            l_x, l_y = self.renderCorner(screen, x, y, random.randint(2, 3))
            print("renderCorner", l_x, l_y)
        else:
            pass

        return (l_x, l_y)

    def checkClick(self, pos, screen):
        if(self.checked):
            for i in range(10):
                for j in range(10):
                    if(self.playing_desk[i][j].isClicked(pos)):
                        elem = self.playing_desk[i][j]
                        if (self.checked_figure.type == "square2"):
                            if(i <= 8 and j <= 8):
                                if(elem.type == "0" and self.playing_desk[i][j + 1].type == "0" and self.playing_desk[i + 1][j].type == "0" and self.playing_desk[i + 1][j + 1] == "0"):
                                    self.playing_desk[i][j].type = "2"
                                    self.playing_desk[i][j + 1].type = "2"
                                    self.playing_desk[i + 1][j].type = "2"
                                    self.playing_desk[i + 1][j + 1].type = "2"

                                    self.check_for_full_lines()
                                    self.to_choose.remove(self.checked_figure)

                                    self.render(screen, 800, 800)

                                self.checked = False
                        elif (self.checked_figure.type == "square3"):
                            if (i <= 7 and j <= 7):
                                if (elem.type == "0" and self.playing_desk[i][j + 1].type == "0" and self.playing_desk[i][j + 2].type == "0" and
                                        self.playing_desk[i + 1][j].type == "0" and self.playing_desk[i + 1][j + 1] == "0" and self.playing_desk[i + 1][j + 2] == "0" and self.playing_desk[i + 2][j] == "0" and self.playing_desk[i + 2][j + 1] == "0" and self.playing_desk[i + 2][j + 2] == "0"):
                                    self.playing_desk[i][j].type = "2"
                                    self.playing_desk[i][j + 1].type = "2"
                                    self.playing_desk[i][j + 2].type = "2"
                                    self.playing_desk[i + 1][j].type = "2"
                                    self.playing_desk[i + 1][j + 1].type = "2"
                                    self.playing_desk[i + 1][j + 2].type = "2"
                                    self.playing_desk[i + 2][j].type = "2"
                                    self.playing_desk[i + 2][j + 1].type = "2"
                                    self.playing_desk[i + 2][j + 2].type = "2"

                                    self.check_for_full_lines()
                                    self.to_choose.remove(self.checked_figure)

                                    self.render(screen, 800, 800)

                                self.checked = False
                        elif (self.checked_figure.type == "downLine2"):
                            if(j <= 8):
                                if(elem.type == "0" and self.playing_desk[i][j + 1].type == "0"):
                                    self.playing_desk[i][j].type = "1"
                                    self.playing_desk[i][j + 1].type = "1"

                                    self.check_for_full_lines()
                                    self.to_choose.remove(self.checked_figure)

                                    self.render(screen, 800, 800)

                                self.checked = False
                        elif (self.checked_figure.type == "downLine3"):
                            if (j <= 7):
                                if (elem.type == "0" and self.playing_desk[i][j + 1].type == "0" and self.playing_desk[i][j + 2].type == "0"):
                                    self.playing_desk[i][j].type = "1"
                                    self.playing_desk[i][j + 1].type = "1"
                                    self.playing_desk[i][j + 2].type = "1"

                                    self.check_for_full_lines()
                                    self.to_choose.remove(self.checked_figure)

                                    self.render(screen, 800, 800)

                                self.checked = False
                        elif (self.checked_figure.type == "upperLine2"):
                            if(i <= 8):
                                if(elem.type == "0" and self.playing_desk[i + 1][j].type == "0"):
                                    self.playing_desk[i][j].type = "1"
                                    self.playing_desk[i + 1][j].type = "1"

                                    self.check_for_full_lines()
                                    self.to_choose.remove(self.checked_figure)

                                    self.render(screen, 800, 800)

                                self.checked = False

                        elif (self.checked_figure.type == "upperLine3"):
                            if (i <= 7):
                                if (elem.type == "0" and self.playing_desk[i + 1][j].type == "0"):
                                    self.playing_desk[i][j].type = "1"
                                    self.playing_desk[i + 1][j].type = "1"
                                    self.playing_desk[i + 2][j].type = "1"

                                    self.check_for_full_lines()
                                    self.to_choose.remove(self.checked_figure)

                                    self.render(screen, 800, 800)

                                self.checked = False
                        elif (self.checked_figure.type == "corner2"):
                            if (i <= 8 and j <= 8):
                                if (elem.type == "0" and self.playing_desk[i + 1][j].type == "0" and self.playing_desk[i + 1][
                                            j + 1] == "0"):
                                    self.playing_desk[i][j].type = "3"
                                    self.playing_desk[i + 1][j].type = "3"
                                    self.playing_desk[i + 1][j + 1].type = "3"

                                    self.check_for_full_lines()
                                    self.to_choose.remove(self.checked_figure)

                                    self.render(screen, 800, 800)

                                self.checked = False
                        else:
                            if (i <= 7 and j <= 7):
                                if (elem.type == "0" and self.playing_desk[i + 1][j].type == "0" and self.playing_desk[i + 2][j] == "0" and self.playing_desk[i + 2][
                                            j + 1] == "0" and self.playing_desk[i + 2][j + 2] == "0"):
                                    self.playing_desk[i][j].type = "3"
                                    self.playing_desk[i + 1][j].type = "3"
                                    self.playing_desk[i + 2][j].type = "3"
                                    self.playing_desk[i + 2][j + 1].type = "3"
                                    self.playing_desk[i + 2][j + 2].type = "3"

                                    self.check_for_full_lines()
                                    self.to_choose.remove(self.checked_figure)

                                    self.render(screen, 800, 800)

                                self.checked = False
        else:
            for i in self.to_choose:
                if(i.isClicked(pos)):
                    self.checked = True
                    self.checked_figure = i

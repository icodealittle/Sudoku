import time

import pygame

pygame.font.init()


class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, xAxis, yAxis, w, h, win):
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.cubes = [[Cube(self.board[i][j], i, j, w, h) for j in range(yAxis)] for i in range(xAxis)]
        self.w = w
        self.h = h
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.yAxis)] for i in range(self.xAxis)]

    def location(self, val):
        x, y = self.selected

        # Loop start
        if self.cubes[x][y].value == 0:
            self.cubes[x][y].set(val)
            self.update_model()

            # 1st inside loop
            if validity(self.model, val, (x, y)) and self.solve():
                return True
            else:
                self.cubes[x][y].set(0)
                self.cubes[x][y].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        x, y = self.selected
        self.cubes[x][y].set_temp(val)

    def draw(self):

        space = self.w / 9
        for i in range(self.xAxis + 1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * space), (self.w, i * space), thickness)
            pygame.draw.line(self.win, (0, 0, 0), (i * space, 0), (i * space, self.h), thickness)

        for i in range(self.xAxis):
            for j in range(self.yAxis):
                self.cubes[i][j].draw(self.win)

    def select(self, x, y):

        for i in range(self.xAxis):
            for j in range(self.yAxis):
                self.cubes[i][j].selected = False

        self.cubes[x][y].selected = True
        self.selected = (x, y)

    def game_clear(self):

        x, y = self.selected

        if self.cubes[x][y].value == 0:
            self.cubes[x][y].temp(0)

    def clear(self, position):

        if position[0] < self.w and position[1] < self.h:
            space = self.w / 9
            x = position[0] // space
            y = position[1] // space
            return (int(y), int(x))
        else:
            return None

    def over(self):

        for i in range(self.xAxis):
            for j in range(self.yAxis):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):

        find = empty(self.model)
        if not find:
            return True
        else:
            x, y = find

        for i in range(1, 10):
            if validity(self.model, i, (x, y)):
                self.model[x][y] = i

                if self.solve():
                    return True

                self.model[x][y] = 0

        return False

    def gui_sol(self):

        find = empty(self.model)
        if not find:
            return True
        else:
            x, y = find

        for i in range(1, 10):
            if validity(self.model, i, (x, y)):
                self.model[x][y] = i
                self.cubes[x][y].set(i)
                self.cubes[x][y].draw_change(self.w, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.gui_sol():
                    return True

                self.model[x][y] = 0
                self.cubes[x][y].set(0)
                self.update_model()
                self.cubes[x][y].draw_change(self.w, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    row = 9
    columns = 9

    def __init__(self, value, xAxis, yAxis, w, h):
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.w = w
        self.h = h
        self.selected = False
        self.value = value
        self.temp = 0

    def draw(self, win):

        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.w / 9
        x = self.columns * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):

        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.w / 9
        x = self.columns * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def temp(self, val):
        self.temp = val


def empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


def validity(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True

def redraw(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + run_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw()


def run_time(secs):
    sec = secs % 60
    min = secs // 60
    hour = min // 60

    mat = " " + str(min) + ":" + str(sec)
    return mat

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.gui_sol()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.location(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.over():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
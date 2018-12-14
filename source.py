import pygame
from random import choice
# one block = 100px


class Square(pygame.sprite.Sprite):
    global screen, all_squares, blocks_on_x, blocks_on_y, gb_score

    def __init__(self, *location):
        self.x, self.y = location
        pygame.sprite.Sprite.__init__(self)
        self.score = 3
        self.size_square = 100
        self.surface_image = pygame.surface.Surface([self.size_square, self.size_square])
        self.surface_image.fill([200, 200, 200])
        self.image = self.surface_image.convert()   # convert Surface -> image
        self.font = pygame.font.Font(None, 48)
        self.surf_font = self.font.render(str(self.score), 1, (255, 255, 255))
        self.image.blit(self.surf_font, [self.size_square/2 - self.surf_font.get_width()/2,
                        self.size_square/2 - self.surf_font.get_height()/2])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.x*100, self.y*100

    def get_rect(self):
        return self.rect

    def get_image(self):
        return self.image

    def move(self, event):
        if event.key == pygame.K_LEFT:
            if self.rect.left <= 0:
                self.rect.left = 0

            elif all_squares[self.y][self.x-1] is None:
                self.rect.right -= 100
                all_squares[self.y][self.x] = None
                all_squares[self.y][self.x-1] = self
                self.x -= 1
            else:
                if self.score != 3072:
                    self.rect.left -= 5
                    if self.collision(all_squares[self.y][self.x-1]):
                        self.rect.left += 5
                        if self.rect.left != 0:
                            self.rect.left -= 100
                        self.score *= 2
                        self.change_score()
                        all_squares[self.y][self.x-1] = self
                        all_squares[self.y][self.x] = None
                        self.x -= 1
                    else:
                        self.rect.left += 5

        elif event.key == pygame.K_RIGHT:
            if self.rect.right >= screen.get_width():
                self.rect.right = screen.get_width()

            elif all_squares[self.y][self.x+1] is None:
                self.rect.right += 100
                all_squares[self.y][self.x] = None
                all_squares[self.y][self.x+1] = self
                self.x += 1
            else:
                if self.score != 3072:
                    self.rect.right += 5
                    if self.collision(all_squares[self.y][self.x+1]):
                        self.rect.right -= 5
                        self.score *= 2
                        self.change_score()
                        all_squares[self.y][self.x+1] = self
                        all_squares[self.y][self.x] = None
                        self.rect.right += 100
                        self.x += 1
                    else:
                        self.rect.right -= 5

        elif event.key == pygame.K_UP:
            if self.rect.top <= 0:
                self.rect.top = 0

            elif all_squares[self.y-1][self.x] is None:
                self.rect.top -= 100
                all_squares[self.y][self.x] = None
                all_squares[self.y-1][self.x] = self
                self.y -= 1
            else:
                if self.score != 3072:
                    self.rect.top -= 5
                    if self.collision(all_squares[self.y-1][self.x]):
                        self.rect.top += 5
                        if self.rect.top != 0:
                            self.rect.top -= 100
                        self.score *= 2
                        self.change_score()
                        all_squares[self.y-1][self.x] = self
                        all_squares[self.y][self.x] = None
                        self.y -= 1
                    else:
                        self.rect.top += 5

        elif event.key == pygame.K_DOWN:
            if self.rect.bottom >= screen.get_height():
                self.rect.bottom = screen.get_height()

            elif all_squares[self.y+1][self.x] is None:
                self.rect.bottom += 100
                all_squares[self.y][self.x] = None
                all_squares[self.y+1][self.x] = self
                self.y += 1
            else:
                if self.score != 3072:
                    self.rect.bottom += 5
                    if self.collision(all_squares[self.y+1][self.x]):
                        self.rect.bottom -= 5
                        self.score *= 2
                        self.change_score()
                        all_squares[self.y+1][self.x] = self
                        all_squares[self.y][self.x] = None
                        self.rect.bottom += 100
                        self.y += 1
                    else:
                        self.rect.bottom -= 5

    def change_color(self):
        if self.score == 6:
            return [50, 200, 50]
        elif self.score == 12:
            return [50, 50, 200]
        elif self.score == 24:
            return [200, 50, 50]
        elif self.score == 48:
            return [100, 150, 100]
        elif self.score == 96:
            return [150, 100, 100]
        elif self.score == 192:
            return[100, 100, 150]
        elif self.score == 384:
            return [0, 250, 20]
        elif self.score == 768:
            return [50, 50, 200]
        elif self.score == 1536:
            return [250, 0, 0]
        elif self.score >= 3072:
            return [0, 250, 0]

    def pos_in_all_squares(self):
        return (self.y, self.x)    # сначала возвратит Y, затем X   [[x,x,x], [x,x,x]]

    def location(self):
        return (self.rect.left, self.rect.top)

    def change_score(self):
        self.image.fill(self.change_color())
        self.surf_font = self.font.render(str(self.score), 1, (255, 255, 255))
        self.image.blit(self.surf_font, [self.size_square/2 - self.surf_font.get_width()/2,
                        self.size_square/2 - self.surf_font.get_height()/2])

    def collision(self, another_obj):
        if self.rect.colliderect(another_obj.rect):   # check on collision
            if another_obj.score == self.score:
                return True
            return False


'''
class BgDivisions(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite().__init__(self)
        div_on_horizontal = self.screen.get_width()
        div_on_vertical = self.screen.get_height()
        self.image = pygame.surface.Sufrace()
        pygame.draw.rect(screen, [0,0,0], [20, 20, 20, 20])
'''


def random_appear():
    global all_squares, gb_score
    empty_place = []
    for i in range(len(all_squares)):
        accum = []
        # first number in array - it's first index in second dimension array
        if None in all_squares[i]:
            accum.append(i)
            for j in range(len(all_squares[i])):
                if all_squares[i][j] is None:
                    accum.append(j)
            empty_place.append(accum)

    if empty_place == []:
        return 'End Game'

    y = choice(list(range(len(empty_place))))
    x = choice(list(empty_place[y][1:]))
    real_y = empty_place[y][0]
    real_x = x
    all_squares[real_y].pop(x)
    all_squares[real_y].insert(x, Square(real_x, real_y))
    gb_score += 3


def main_board(x=4, y=4):
    global all_squares

    for i in range(y):
        accum = []
        for j in range(x):
            accum.append(None)
        all_squares.append(accum)

    x = x*100
    y = y*100
    screen = pygame.display.set_mode([x, y])
    screen.fill([255, 255, 255])

    return screen


print()
print('Для управления используйте \u2190 \u2191 \u2192 \u2193. Для выхода ESC')
print()
print('Для установки поля по умолчанию 4x4 просто нажмите Enter')

try:
    inp = input('Введите максимальное число квадратов x, y: ')
    inp = inp.split(',')
    blocks_on_x = int(inp[0])
    blocks_on_y = int(inp[1])
except Exception:
    blocks_on_x = 4
    blocks_on_y = 4

pygame.init()
pygame.display.set_caption('3072')

all_squares = []
screen = main_board(blocks_on_x, blocks_on_y)
clock = pygame.time.Clock()

gb_score = 0
gb_score_font = pygame.font.Font(None, 34)
gb_score_pos = (10, 10)

running = True

random_appear()
while running:
    clock.tick(60)
    screen.fill([255, 255, 255])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

            for i in range(max(blocks_on_x, blocks_on_y)):
                for set_square in all_squares:
                    for square in set_square:
                        if square is None:
                            continue
                        square.move(event)
            r = random_appear()
            if r == 'End Game':
                screen.fill([255, 255, 255])
                font = pygame.font.Font(None, 92)
                surf_font = font.render('GAME OVER', 1, (0, 0, 0))
                screen.blit(surf_font, [screen.get_width()/2 - surf_font.get_width()/2,
                            screen.get_height()/2 - surf_font.get_height()/2])
                pygame.display.flip()
                pygame.time.delay(3000)
                running = False
                break

    if running is False:
        break

    for set_square in all_squares:
        for square in set_square:
            if square is None:
                continue
            screen.blit(square.get_image(), square.get_rect())

    gb_score_surf = gb_score_font.render(str(gb_score), 1, (30, 30, 30))
    screen.blit(gb_score_surf, gb_score_pos)
    pygame.display.flip()

import pygame
from View import Button, Board


def draw():
    screen.fill((0, 0, 0))
    fontBig = pygame.font.Font(None, 80)
    text = fontBig.render("1010!", 1, (255, 255, 255))
    text_x = width // 2 - text.get_width() // 2
    text_y = 3 / 8 * height - text.get_height() // 2


    fontLittle = pygame.font.Font(None, 40)

    text2 = fontLittle.render("An incredible PyGame-based project by Nitron Apps", 1, (255, 255, 255))
    text_x2 = width // 2 - text2.get_width() // 2
    text_y2 = height // 2 - text2.get_height() // 2

    fontButton = pygame.font.Font(None, 50)

    textButton = fontButton.render("START", 1, (255, 255, 255))

    screen.blit(text, (text_x, text_y))
    screen.blit(text2, (text_x2, text_y2))
    #screen.blit(textButton, (textButton_x, textButton_y))


    #pygame.draw.rect(screen, (255, 255, 255), (textButton_x - 10, textButton_y - 10,
     #                                      textButton.get_width() + 20, textButton.get_height() + 20), 1)

#init my frame
pygame.init()

size = width, height = 800, 800
screen = pygame.display.set_mode(size)

draw()

textButton = pygame.font.Font(None, 50).render("START", 1, (255, 255, 255))
textButton_x = width // 2 - textButton.get_width() // 2
textButton_y = 2 / 3 * height - textButton.get_height() // 2
textButton_width = textButton.get_width()
textButton_height = textButton.get_height()

button = Button.Button(pygame.Color("#FFFFFF"), textButton_x, textButton_y, textButton_width,
                       textButton_height, 'START')

button.draw(screen)

pygame.display.flip()

running = True
# ожидание закрытия окна:
board = Board.Board(10, 10)
while running:
    for i in pygame.event.get():
        if (i.type == pygame.QUIT):
            running = False
        if (i.type == pygame.MOUSEBUTTONDOWN):
            if(button.isOver(i.pos)):
                screen.fill((0, 0, 0))
                board.render(screen, width, height)
                pygame.display.flip()

            board.checkClick(i.pos, screen)

# завершение работы:
pygame.quit()

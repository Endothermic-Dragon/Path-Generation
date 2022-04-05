from time import sleep
import pygame
from Path import Path, Translate
from DriveCharacterization import DriveCharacterization

robotCharacteristics = DriveCharacterization(1, 1, 1, 1)
path = Path(robotCharacteristics)

pygame.init()

#blit to make it resizable
screen = pygame.display.set_mode([1200, 800])

screen.fill((0, 0, 0))
field = pygame.Rect(0, 0, 1200, 600)
pygame.draw.rect(screen, (94, 219, 94), field)
pygame.display.flip()

breakLoop = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            breakLoop = True
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()
            if field.collidepoint(mousePos):
                pygame.draw.circle(screen, (0, 0, 0), mousePos, 5, 5)
                path.append(Translate.toNative(field, mousePos))
            else:
                breakLoop = True
    if breakLoop:
        break
    pygame.display.flip()

coords = path.drawPath()

for i in range(len(coords)):
    coords[i] = Translate.toPygame(field, coords[i])

pygame.draw.lines(screen, (0, 0, 0), False, coords)
pygame.display.flip()

while True:
    sleep(0.1)
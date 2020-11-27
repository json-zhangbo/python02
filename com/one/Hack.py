import random

import pygame

FONT_PX = 15

pygame.init()

winSur = pygame.display.set_mode((640, 480))

font = pygame.font.SysFont("fangsong", 20)

bg_suface = pygame.Surface((640, 480), flags=pygame.SRCALPHA)

pygame.Surface.convert(bg_suface)

bg_suface.fill(pygame.Color(0, 0, 0, 13))

winSur.fill((0, 0, 0))

# 相关参数
list1 = ['$', '¥', '€', 'R$','￡','฿','₩','฿']
texts = [font.render(str(i), True, (0, 255, 0)) for i in list1]
colums = int(640 / FONT_PX)
drops = [0 for i in range(colums)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    pygame.time.delay(63)

    winSur.blit(bg_suface, (0, 0))

    for i in range(len(drops)):
        text = random.choice(texts)
        winSur.blit(text, (i * FONT_PX, drops[i] * FONT_PX))

        drops[i] += 1
        if drops[i] * 10 > 480 or random.random() > 0.95:
            drops[i] = 0
    pygame.display.flip()

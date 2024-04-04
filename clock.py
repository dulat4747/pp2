import pygame
import time
pygame.init()

# Загрузите изображения циферблата и стрелок
base = pygame.image.load("mickeyclock.png")
h1 = pygame.image.load("hand-1.png")  # Предположим, что это часовая стрелка
h2 = pygame.image.load("hand-2.png")  # Минутная стрелка
h3 = pygame.image.load("hand-2.png")  # Секундная стрелка

window = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("MickeyClock")

check = True
while check:
    window.fill((255, 255, 255))  # Заполнение фона белым цветом
    window.blit(base, (0, 0))  # Отображение циферблата

    # Получение текущего времени
    c_time = time.localtime()
    hours = c_time.tm_hour % 12 + c_time.tm_min / 60  # Корректное время для часовой стрелки
    minutes = c_time.tm_min
    seconds = c_time.tm_sec

    # Расчет углов для стрелок
    # Предполагается, что стрелки изначально направлены вверх. Если это не так, скорректируйте начальный угол
    hours_angle = (hours / 12) * 360
    minutes_angle = (minutes / 60) * 360
    seconds_angle = (seconds / 60) * 360

    # Поворот и размещение стрелок
    for hand, angle in [(h1, hours_angle), (h2, minutes_angle), (h3, seconds_angle)]:
        rotated_hand = pygame.transform.rotate(hand, -angle)
        hand_rect = rotated_hand.get_rect(center=(500, 375))  # Центрирование стрелки
        window.blit(rotated_hand, hand_rect.topleft)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check = False

    time.sleep(1)  # Пауза в 1 секунду перед следующим обновлением экрана

pygame.quit()

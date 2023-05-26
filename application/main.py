import pygame

white_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6']

black_labels = ['Db4', 'Eb4', 'Gb4', 'Ab4', 'Bb4', 'Db5', 'Eb5', 'Gb5', 'Ab5', 'Bb5']

active_whites = []
active_blacks = []

pygame.init()

font = pygame.font.Font('assets/Terserah.ttf', 48)
medium_font = pygame.font.Font('assets/Terserah.ttf', 28)
small_font = pygame.font.Font('assets/Terserah.ttf', 16)
real_small_font = pygame.font.Font('assets/Terserah.ttf', 10)
fps = 60
timer = pygame.time.Clock()
WIDTH = 15 * 50
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
left_oct = 4
right_oct = 5
pygame.display.set_caption("Application")

def draw_piano(whites, blacks):

    white_rects = []
    for i in range(15):
        rect = pygame.draw.rect(screen, 'white', [i * 50, HEIGHT - 200, 50, 200], 0, 2) #Touches Blanches
        white_rects.append(rect)
        pygame.draw.rect(screen, 'black', [i * 50, HEIGHT - 200, 50, 200], 2, 2) #Separation entre les touches blanches
        key_label = small_font.render(white_notes[i], True, 'black')
        screen.blit(key_label, (i * 50 + 3, HEIGHT - 20)) #Label de la note blanche

    # Contour quand touche utilisée
    for i in range(len(whites)):
        if whites[i][1] > 0:
            j = whites[i][0]
            pygame.draw.rect(screen, 'magenta', [j * 50, HEIGHT - 200, 50, 200], 0, 2)
            whites[i][1] -= 1

    skip_count = 0
    last_skip = 3
    skip_track = 0
    black_rects = []
    for i in range(10):
        rect = pygame.draw.rect(screen, 'black', [35 + (i * 50) + (skip_count * 50), HEIGHT - 200, 30, 100], 0, 2)

        # Contour quand touche utilisée
        for q in range(len(blacks)):
            if blacks[q][0] == i:
                if blacks[q][1] > 0:
                    pygame.draw.rect(screen, 'cyan', [35 + (i * 50) + (skip_count * 50), HEIGHT - 200, 30, 100], 0, 2)
                    blacks[q][1] -= 1

        key_label = real_small_font.render(black_labels[i], True, 'white')
        screen.blit(key_label, (39 + (i * 50) + (skip_count * 50), HEIGHT - 115))
        black_rects.append(rect)
        skip_track += 1
        if last_skip == 2 and skip_track == 3:
            last_skip = 3
            skip_track = 0
            skip_count += 1
        elif last_skip == 3 and skip_track == 2:
            last_skip = 2
            skip_track = 0
            skip_count += 1

    return white_rects, black_rects, whites, blacks

run = True
while run:

    timer.tick(fps)
    screen.fill('gray')
    white_keys, black_keys, active_whites, active_blacks = draw_piano(active_whites, active_blacks)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            black_key = False
            for i in range(len(black_keys)):
                if black_keys[i].collidepoint(event.pos):
                    black_key = True
                    active_blacks.append([i, 30])
            for i in range(len(white_keys)):
                if white_keys[i].collidepoint(event.pos) and not black_key:
                    active_whites.append([i, 30])
    pygame.display.flip()
pygame.quit()
import pygame
from pygamevideo import Video

window = pygame.display.set_mode((640, 360))

video = Video("video.mp4")

# start video
video.play()

# main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # выход из игры
            run = False
    # draw video to display surface
    # this function must be called every tick
    video.draw_to(window, (0, 0))
    pygame.display.update()

    # set window title to current duration of video as hour:minute:second
    #t = video.current_time.format("%h:%m:%s")
    #pygame.display.set_caption(t)

    # start video
video.play()

# main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # выход из игры
            run = False
    # draw video to display surface
    # this function must be called every tick
    video.draw_to(window, (0, 0))
    pygame.display.update()

    # set window title to current duration of video as hour:minute:second
    #t = video.current_time.format("%h:%m:%s")
    #pygame.display.set_caption(t)
    # start video
video.play()

# main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # выход из игры
            run = False
    # draw video to display surface
    # this function must be called every tick
    video.draw_to(window, (0, 0))
    pygame.display.update()

    # set window title to current duration of video as hour:minute:second
    #t = video.current_time.format("%h:%m:%s")
    #pygame.display.set_caption(t)
    # start video
video.play()

# main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # выход из игры
            run = False
    # draw video to display surface
    # this function must be called every tick
    video.draw_to(window, (0, 0))
    pygame.display.update()

    # set window title to current duration of video as hour:minute:second
    #t = video.current_time.format("%h:%m:%s")
    #pygame.display.set_caption(t)
    
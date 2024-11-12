import random
from pico2d import *
import game_framework
import time
import game_world
from grass import Grass
from boy import Boy
from ball import Ball
from zombie import Zombie

# boy = None
game_over = False
game_over_time = 0

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)

    # fill here
    zombies = [Zombie() for _ in range(3)]
    for zombie in zombies:
        game_world.add_object(zombie, 1)
        game_world.add_collision_pair('boy:zombie', boy, zombie)

    for zombie in zombies:
        for ball in boy.balls:
            game_world.add_collision_pair('zombie:ball', zombie, ball)

def finish():
    game_world.clear()
    pass

def update():
    global game_over, game_over_time

    if game_over:

        if time.time() - game_over_time > 3:
            game_framework.quit()
        return

    game_world.update()

    for zombie in [obj for obj in game_world.world[1] if isinstance(obj, Zombie)]:
        if game_world.collide(boy, zombie):
            game_world.remove_object(boy)
            game_over = True
            game_over_time = time.time()
            return

    for zombie in [obj for obj in game_world.world[1] if isinstance(obj, Zombie)]:
        for ball in boy.balls[:]:
            if game_world.collide(zombie, ball):
                zombie.shrink_or_remove()

                game_world.remove_object(ball)
                boy.balls.remove(ball)
                break

def draw():
    clear_canvas()
    game_world.render()
    if game_over:

        font = load_font('ENCR10B.TTF', 200)
        font.draw(300, 300, "GAME OVER", (255, 0, 0))
    update_canvas()

def pause():
    pass

def resume():
    pass

import numpy as np
import pygame as pg
import pygame.freetype
import constants as ct
import navigation as nav
import physics as phy
import control as ctr

# INITIALIZATION
pg.init()
screen = pg.display.set_mode((ct.WIDTH, ct.HEIGHT))
pg.display.set_caption('Simulator')
clock = pg.time.Clock()
myfont = pg.freetype.SysFont('Consolas', 20)

toogle_trail = ct.trail
toogle_distance = ct.distance
toogle_forces = ct.forces
t = 0

ship = nav.Body(ID='ship', x=700, y=700, size=5, mass=10)
star = nav.Body(ID='star', x=0, y=0, size=5, mass=100000)
#planetA = nav.Body(ID='A', x=-2000, y=-2000, size=10, mass=6 * 10**3)
#planetB = nav.Body(ID='B', x=2000, y=2000, size=10, mass=6 * 10**3)

flight = ctr.Flight(ship)

bodies = pg.sprite.Group()
trails = pg.sprite.Group()
bodies.add(ship)
bodies.add(star)
# bodies.add(planetA)
# bodies.add(planetB)


# GAME LOOP
running = True

while running:

    # 0. run the loop at the desired frame rate
    clock.tick(ct.FPS)

    # 1. process input
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_t:
                toogle_trail = not(toogle_trail)
            if event.key == pg.K_d:
                toogle_distance = not(toogle_distance)
            if event.key == pg.K_p:
                ship.prop = 0
                print('Prop OFF')
            if event.key == pg.K_f:
                toogle_forces = not(toogle_forces)

    # 2. update
    if t > 100:
        t = 1
    else:
        t += 1
    ship.g_force = ship.g_force + phy.g_force(star, ship)
    flight.update()
    bodies.update()

    if toogle_trail:
        if t % 50 == 0:
            trail = nav.Body(x=ship.pos[0], y=ship.pos[1], size=1, color=ct.GREY)
            trails.add(trail)
            trails.update()

    # 3. render
    screen.fill((0, 0, 0))

    # draw
    if toogle_distance:
        pg.draw.line(screen, ct.BLUE, phy.trans(ship.pos), phy.trans(flight.target))
    if toogle_forces:
        pg.draw.line(screen, ct.YELLOW, phy.trans(ship.pos), phy.trans(ship.pos) + phy.trans(ship.f_total, center=False) * 20 * ct.SCALE / 5)
    if toogle_trail:
        trails.draw(screen)
    else:
        trails.empty()

    bodies.draw(screen)
    #pg.draw.circle(screen, ct.YELLOW, (int(phy.trans(star.pos)[0]), int(phy.trans(star.pos)[1])), 14)
    # text
    text, rect = myfont.render(f'F total: {round(phy.distance((0,0),ship.f_total), 4)} N', (255, 255, 255))
    screen.blit(text, (5, 5))
    text, rect = myfont.render(f'Grav: {round(phy.distance((0,0),phy.g_force(star, ship)), 4)} N', (255, 255, 255))
    screen.blit(text, (5, 25))
    text, rect = myfont.render(f'Prop: {round(ship.prop_mag, 4)} N', (255, 255, 255))
    screen.blit(text, (5, 45))
    text, rect = myfont.render(f'Distance: {round(flight.distance, 0)} u', (255, 255, 255))
    screen.blit(text, (5, 65))

    pg.display.flip()

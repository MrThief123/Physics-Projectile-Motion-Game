# Import the pygame module
import pygame
import math
import random

print('bye')


plat_height = random.randint(30, 130)  # height of paltform
plat_height = plat_height * 5 + 5



loop = []
loop_x = []
loop_y = []
max_dist = []
max_height = []
max_speed = []
bullet_x = 100
bullet_y = plat_height

cannon_ip = ''
angle_ip = ''
input1 = False

cannon_pwr = random.randint(50, 50) * 20

# Initialize pygame
pygame.init()


fps = 1

width, height = 1500, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Super Shooter")

white = (255, 255, 255)
blue = (173, 216, 230)
red = (188, 39, 50)
green = (0, 154, 23)
yellow = (255, 255, 0)

x_dist = random.randint(60, 270) * 5
x_dist1 = x_dist - 100
x_dist2 = x_dist

bullet_weight = random.randint(0, 20)
bullet_weight = ((bullet_weight * 50) + 500) / 1000

wind_angle = random.randint(50, 210)
if wind_angle > 130:
    wind_angle = wind_angle - 130 + 230


wind_pos = False

if 0 < wind_angle < 180:
    wind_pos = True
else:
    wind_pos = False

wind_strength = random.randint(1, 10) / 2

wind_trig = (wind_angle * math.pi) / 180
wind_x = (((math.sin(wind_trig)) * wind_strength) / bullet_weight / fps)
wind_y = (((math.cos(wind_trig)) * wind_strength) / bullet_weight / fps)
y_accel = -9.8 / fps + wind_y


cloud = pygame.image.load("c:\Pictures\cloud.png")
cloud = pygame.transform.scale(cloud, (200, 120))
cloudx = 750
cloudy = 200
cloud2x = 0
cloud2y = 50

cloud_speed = wind_x / 2


font = pygame.font.SysFont("comicsans", 22)


def pre_flight():
    alt = (plat_height - 800) * -1 - 50  # altitiude cal
    alt_text = font.render(f"Altitude: {alt} meters", 1, white)
    win.blit(alt_text, (1200, 50))

    h_text = font.render(f"Horizontal Distance: {x_dist1} meters", 1, white)
    win.blit(h_text, (1080, 100))

    bullet_text = font.render(f"Bullet Weight: {bullet_weight} Kg", 1, white)
    win.blit(bullet_text, (1150, 150))

    wind_text = font.render(f"Wind: {wind_angle} °T {wind_strength} N", 1, white)
    win.blit(wind_text, (1150, 200))

    pygame.draw.circle(win, (0, 0, 0), (bullet_x, plat_height - 3), 3)  # bullet


def basic():
    global cloudx, cloudy, cloud_pos, cloud2x, cloud2y
    pygame.draw.rect(win, (255, 0, 0), (x_dist - 5, 740, 10, 10))  # target
    pygame.draw.rect(win, green, (0, 750, 1500, 50))  # ground
    pygame.draw.rect(win, red, (0, plat_height, 120, 800))  # platform

    if wind_pos == True:
        cloudx += cloud_speed
        cloud2x += cloud_speed
        if cloudx > 1450:
            cloudx = -350
            cloudy = random.randint(0, 300)
        if cloud2x > 1450:
            cloud2x = -350
            cloud2y = random.randint(0, 300)
        win.blit(cloud, (cloudx, cloudy))
        win.blit(cloud, (cloud2x, cloud2y))
    if wind_pos == False:
        cloudx += cloud_speed
        cloud2x += cloud_speed
        if cloudx < -300:
            cloudx = 1500
            cloudy = random.randint(0, 300)
        if cloud2x < -300:
            cloud2x = 1500
            cloud2y = random.randint(0, 300)
        win.blit(cloud, (cloudx, cloudy))
        win.blit(cloud, (cloud2x, cloud2y))




scale_y = 1
scale_x = 1


def basic_final():
    global finish, scale_y, scale_x, cloudx, cloudy, cloud_pos, cloud2x, cloud2y
    finish = True
    max_height.sort()
    max_dist.sort()
    if max_height[0] < 0 and max_dist[-1] <= 1500:  # too high in range
        scale_ry = round(((max_height[0] * -1 + 800) / 750) ** -1, 3)
        if scale_ry <= scale_y:
            scale_y -= 0.002
        pygame.draw.rect(win, green, (0, 750, 1500, 50))
        pygame.draw.rect(win, (255, 0, 0), (x_dist - 5, 747 + 10 * scale_y, 10, 10 * scale_y))
        for i in range(len(loop)):
            loop[i] = (loop_x[i], 750 - ((loop_y[i] * -1 + 750) * scale_y))
        pygame.draw.rect(win, red, (0, 750 - ((loop_y[0] * -1 + 750) * scale_y), 120, 800))
        pygame.draw.lines(win, white, False, loop, 2)

    elif max_dist[-1] > 1500 and max_height[0] >= 0:  # too long in height
        scale_rx = round(1480 / max_dist[-1], 3)
        if scale_rx <= scale_x:
            scale_x -= 0.002
        pygame.draw.rect(win, green, (0, 750, 15000, 50))
        pygame.draw.rect(win, (255, 0, 0), ((x_dist - 5) * scale_x, 740, 10, 10))
        for i in range(len(loop)):
            loop[i] = (loop_x[i] * scale_x, loop_y[i])
        pygame.draw.rect(win, red, (0, plat_height, 120 * scale_x, 800))
        pygame.draw.lines(win, white, False, loop, 2)

    if max_height[0] < 0 and max_dist[-1] >= 1500:
        scale_ry = round(((max_height[0] * -1 + 800) / 750) ** -1, 3)
        scale_rx = round(1480 / max_dist[-1], 3)
        if scale_ry <= scale_y:
            scale_y -= 0.002
        if scale_rx <= scale_x:
            scale_x -= 0.002
        pygame.draw.rect(win, green, (0, 750, 15000, 50))
        pygame.draw.rect(win, (255, 0, 0), ((x_dist - 5) * scale_x, 747 + 10 * scale_y, 10, 10 * scale_y))
        for i in range(len(loop)):
            loop[i] = (loop_x[i] * scale_x, 750 - ((loop_y[i] * -1 + 750) * scale_y))
        pygame.draw.rect(win, red, (0, 750 - ((loop_y[0] * -1 + 750) * scale_y), 120 * scale_x, 800))
        pygame.draw.lines(win, white, False, loop, 2)

    if max_dist[-1] <= 1500 and max_height[0] >= 0:
        scale_y = 1
        pygame.draw.rect(win, green, (0, 750 * scale_y, 1500, 50))
        pygame.draw.rect(win, (255, 0, 0), (x_dist - 5, 740, 10, 10))
        pygame.draw.rect(win, red, (0, plat_height, 120, 800))
        pygame.draw.lines(win, white, False, loop, 2)

    bullet_text = font.render(f"Maximum Speed: {round(max_speed[-1])} m/s", 1, white)
    win.blit(bullet_text, (1200, 100))
    high_text = font.render(f"Maximum Height: {round(max_height[0]) * -1 + 800} m", 1, white)
    win.blit(high_text, (1200, 150))
    dist_text = font.render(f"Maximum Distance: {round(max_dist[-1])} m", 1, white)
    win.blit(dist_text, (1200, 200))

    if wind_pos == True:
        cloudx += cloud_speed
        cloud2x += cloud_speed
        if cloudx > 1450:
            cloudx = -350
            cloudy = random.randint(0, 300)
        if cloud2x > 1450:
            cloud2x = -350
            cloud2y = random.randint(0, 300)
        win.blit(cloud, (cloudx, cloudy))
        win.blit(cloud, (cloud2x, cloud2y))
    if wind_pos == False:
        cloudx += cloud_speed
        cloud2x += cloud_speed
        if cloudx < -300:
            cloudx = 1500
            cloudy = random.randint(0, 300)
        if cloud2x < -300:
            cloud2x = 1500
            cloud2y = random.randint(0, 300)
        win.blit(cloud, (cloudx, cloudy))
        win.blit(cloud, (cloud2x, cloud2y))

def fly():
    global bullet_x, bullet_y, vel_x, vel_y
    max_height.append(bullet_y)
    max_dist.append(bullet_x)

    vel_x = x_int + wind_x * time
    vel_y = y_int + y_accel * time

    x_change = (x_int * time) + (0.5 * wind_x * (time ** 2))
    y_change = ((y_int * time) + 0.5 * y_accel * (time ** 2))

    bullet_x = 100 + x_change
    bullet_y = plat_height - y_change
    pygame.draw.circle(win, (0, 0, 0), (bullet_x, bullet_y), 3)


def line_draw():
    if len(loop) > 1:
        for i in loop:
            pygame.draw.lines(win, white, False, loop, 2)
    loop.append((bullet_x, bullet_y))
    loop_x.append(bullet_x)
    loop_y.append(bullet_y)

    alt = round((bullet_y - 800) * -1 - 50)  # altitiude cal
    if alt < 0:
        alt = 0
    alt_text = font.render(f"Altitude: {alt} m", 1, white)
    win.blit(alt_text, (1200, 50))

    x_dist3 = round(x_dist2 - bullet_x)
    h_text = font.render(f"Horizontal Distance: {x_dist3} m", 1, white)
    win.blit(h_text, (1080, 100))

    speed = round(math.sqrt(vel_x ** 2 + (vel_y ** 2)))

    if alt == 0:
        speed = 0
    pwr_text = font.render(f"Velocity X:{round(vel_x)} m/s  Y:{round(vel_y)} m/s", 1, white)
    win.blit(pwr_text, (1100, 150))

    max_speed.append(speed)
    max_speed.sort()
    bullet_text = font.render(f"Maximum Speed: {max_speed[-1]} m/s", 1, white)
    win.blit(bullet_text, (1150, 200))

    wind_text = font.render(f"Wind: {wind_angle} °T {wind_strength} N", 1, white)
    win.blit(wind_text, (1150, 250))


cannon_box = pygame.draw.rect(win, red, (1150, 300, 230, 35))
angle_box = pygame.draw.rect(win, red, (1150, 350, 230, 35))
go_box = pygame.draw.rect(win, red, (1150, 400, 230, 35))
active = False
active2 = False
active3 = False


def reset():
    global flight, input_angle, bullet_y, finish, bullet_x, dist, loop, loop_y, loop_x, \
        max_dist, max_height, vel_x, vel_y, scale_x, scale_y, max_speed, active, active2, \
        getting_input, cannon_ip, angle_ip, fps, time
    basic()
    finish = False
    flight = False
    loop = []
    loop_x = []
    loop_y = []
    max_dist = []
    max_height = []
    max_speed = []
    bullet_x = 100
    bullet_y = plat_height
    vel_x = (cannon_pwr / bullet_weight * math.cos((input_angle * math.pi) / 180)) / fps
    vel_y = (cannon_pwr / bullet_weight * math.sin((input_angle * math.pi) / 180)) / fps
    scale_x = 1
    scale_y = 1
    time = 0
    getting_input = True


# Variable to keep the main loop running

flight = False
finish = False
getting_input = False
clock = pygame.time.Clock()

time = 0

def main():
    global flight, input_angle, bullet_y, finish, bullet_x, dist, loop, loop_y, loop_x, \
        max_dist, max_height, vel_x, vel_y, scale_x, scale_y, max_speed, active, cannon_box, \
        getting_input, cannon_ip, active2, angle_ip, active3, cannon_pwr, fps, clock, time, x_int, y_int

    run = True
      # limit frame rate

    while run:
        clock.tick(25)

        win.fill(blue)
        if finish == False:
            basic()
            if flight == False:
                pre_flight()
            elif bullet_y >= 750:
                if x_dist - 10 <= bullet_x <= x_dist + 10:
                    print("you win")
                    print(time)
                else:
                    print("you loose")
                    print(time)
                basic_final()
            else:
                line_draw()
                fly()
                time += 0.04

        else:
            basic_final()

        if getting_input == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = bool(cannon_box.collidepoint(event.pos))
                active2 = bool(angle_box.collidepoint(event.pos))
                if go_box.collidepoint(event.pos):
                    active3 = True
                    input_angle = int(angle_ip)
                    cannon_pwr = int(cannon_ip)
                    if 0 <= input_angle <= 360:
                        if 0 <= cannon_pwr <= 5000:
                            vel_x = (math.cos(input_angle / 180 * math.pi) * cannon_pwr / bullet_weight / fps)
                            x_int = vel_x
                            print(vel_x)
                            vel_y = (math.sin(input_angle / 180 * math.pi) * cannon_pwr / bullet_weight / fps)
                            y_int = vel_y
                            print(vel_y)
                            flight = True
                            getting_input = False
                            active3 = False
                    else:
                        active3 = False
                else:
                    active3 = False

            if active:
                color = pygame.Color('red')
            else:
                color = pygame.Color('blue')
            pygame.draw.rect(win, color, cannon_box, 20)
            cannon_text = font.render(f"Power: {cannon_ip} N", 1, white)
            win.blit(cannon_text, (1155, 300))

            if active2:
                color = pygame.Color('red')
            else:
                color = pygame.Color('blue')
            pygame.draw.rect(win, color, angle_box, 20)
            angle_text = font.render(f"Angle: {angle_ip} Degrees", 1, white)
            win.blit(angle_text, (1155, 350))

            if active3 == True:
                color = pygame.Color('red')
            else:
                color = pygame.Color('blue')
            pygame.draw.rect(win, color, go_box, 20)
            go_text = font.render("LANUCH", 1, white)
            win.blit(go_text, (1220, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:  # end here
                    getting_input = True

                if active:
                    if event.key == pygame.K_DOWN:
                        active = False
                        active2 = True
                    if event.key == pygame.K_BACKSPACE:
                        cannon_ip = cannon_ip[:-1]
                    else:
                        if event.unicode.isdigit():
                            cannon_ip += event.unicode
                            cannon_text = font.render(f"Power: {cannon_ip} N", 1, white)
                            win.blit(cannon_text, (1155, 300))
                        if event.key == pygame.K_RETURN:
                            active = False

                if active2:
                    if event.key == pygame.K_UP:
                        active = True
                        active2 = False
                    if event.key == pygame.K_BACKSPACE:
                        angle_ip = angle_ip[:-1]
                    else:
                        if event.unicode.isdigit():
                            angle_ip += event.unicode
                        if event.key == pygame.K_RETURN:
                            active2 = False

        pygame.display.update()
    pygame.quit()


main()


import pygame, sys, math, random

pygame.init()
W, H = 680, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 20)

# --- Stars ---
stars = [(random.randint(0,W), random.randint(0,H), random.uniform(0.1,0.4)) for _ in range(80)]

# --- Ship ---
ship = {"x": W//2, "y": 400, "w": 28, "h": 32, "speed": 5, "invincible": 0}

bullets = []
meteors = []
particles = []
score = 0
lives = 3
level = 1
shoot_cooldown = 0
meteor_timer = 0
meteor_interval = 90
state = "playing"

def spawn_meteor():
    x = random.randint(20, W-20)
    size = random.randint(12, 30)
    speed = random.uniform(1, 2.5) + level * 0.3
    vx = random.uniform(-1.5, 1.5)
    sides = random.randint(6, 9)
    meteors.append({"x": x, "y": -size, "size": size, "speed": speed,
                    "vx": vx, "sides": sides, "rot": 0,
                    "rot_speed": random.uniform(-0.03, 0.03)})

def draw_meteor(m):
    pts = []
    for i in range(m["sides"]):
        angle = m["rot"] + (i / m["sides"]) * math.pi * 2
        r = m["size"] * (0.8 + math.sin(i * 2.3) * 0.2)
        pts.append((m["x"] + math.cos(angle)*r, m["y"] + math.sin(angle)*r))
    pygame.draw.polygon(screen, (90, 74, 58), pts)
    pygame.draw.polygon(screen, (138, 122, 106), pts, 2)

def draw_ship():
    x, y = ship["x"], ship["y"]
    if ship["invincible"] > 0 and (ship["invincible"] // 6) % 2 == 0:
        return
    pts = [(x, y-16), (x+14, y+16), (x+7, y+10), (x-7, y+10), (x-14, y+16)]
    pygame.draw.polygon(screen, (79, 195, 247), pts)
    pygame.draw.polygon(screen, (129, 212, 250), pts, 2)
    if pygame.time.get_ticks() // 100 % 2 == 0:
        flame = [(x-8, y+16), (x, y+28), (x+8, y+16)]
        pygame.draw.polygon(screen, (255, 112, 67), flame)

def spawn_particles(x, y, color, count):
    for _ in range(count):
        angle = random.uniform(0, math.pi*2)
        speed = random.uniform(1, 4)
        particles.append({
            "x": x, "y": y,
            "vx": math.cos(angle)*speed, "vy": math.sin(angle)*speed,
            "life": 1.0, "color": color, "size": random.randint(2, 4)
        })

def reset():
    global bullets, meteors, particles, score, lives, level
    global shoot_cooldown, meteor_timer, meteor_interval, state
    bullets.clear(); meteors.clear(); particles.clear()
    score=0; lives=3; level=1; state="playing"
    shoot_cooldown=0; meteor_timer=0; meteor_interval=90
    ship["x"]=W//2; ship["y"]=400; ship["invincible"]=0

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and state != "playing":
                reset()

    keys = pygame.key.get_pressed()

    if state == "playing":
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ship["x"] = max(ship["w"]//2, ship["x"] - ship["speed"])
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship["x"] = min(W - ship["w"]//2, ship["x"] + ship["speed"])
        if keys[pygame.K_SPACE] and shoot_cooldown == 0:
            bullets.append({"x": ship["x"], "y": ship["y"]-20, "speed": 10})
            shoot_cooldown = 12
        if shoot_cooldown > 0: shoot_cooldown -= 1
        if ship["invincible"] > 0: ship["invincible"] -= 1

        level = 1 + score // 300
        meteor_interval = max(30, 90 - (level-1)*8)
        meteor_timer += 1
        if meteor_timer >= meteor_interval:
            spawn_meteor(); meteor_timer = 0

        bullets = [b for b in bullets if b["y"] > -10]
        for b in bullets: b["y"] -= b["speed"]

        to_remove_meteors = []
        to_remove_bullets = []
        for m in meteors:
            m["x"] += m["vx"]; m["y"] += m["speed"]; m["rot"] += m["rot_speed"]
            if m["y"] > H + m["size"]:
                to_remove_meteors.append(m); continue
            for b in bullets:
                dx, dy = b["x"]-m["x"], b["y"]-m["y"]
                if math.sqrt(dx*dx+dy*dy) < m["size"]+4:
                    score += 10
                    spawn_particles(m["x"], m["y"], (233,69,96), 8)
                    to_remove_meteors.append(m)
                    to_remove_bullets.append(b)
                    break
            if ship["invincible"] == 0:
                dx, dy = ship["x"]-m["x"], ship["y"]-m["y"]
                if math.sqrt(dx*dx+dy*dy) < m["size"]+14:
                    lives -= 1
                    ship["invincible"] = 90
                    spawn_particles(ship["x"], ship["y"], (245,166,35), 12)
                    to_remove_meteors.append(m)
                    if lives <= 0: state = "dead"

        meteors = [m for m in meteors if m not in to_remove_meteors]
        bullets = [b for b in bullets if b not in to_remove_bullets]

        for p in particles:
            p["x"] += p["vx"]; p["y"] += p["vy"]; p["vy"] += 0.05; p["life"] -= 0.04
        particles = [p for p in particles if p["life"] > 0]

        for s in stars:
            stars[stars.index(s)] = (s[0], (s[1] + s[2]) % H, s[2])

    # --- Draw ---
    screen.fill((10, 10, 26))

    for sx, sy, _ in stars:
        pygame.draw.circle(screen, (180, 180, 220), (int(sx), int(sy)), 1)

    for m in meteors: draw_meteor(m)

    for b in bullets:
        pygame.draw.rect(screen, (0, 229, 255), (b["x"]-2, b["y"], 4, 14), border_radius=2)

    for p in particles:
        alpha = max(0, int(p["life"] * 255))
        s = pygame.Surface((p["size"]*2, p["size"]*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*p["color"], alpha), (p["size"], p["size"]), p["size"])
        screen.blit(s, (int(p["x"])-p["size"], int(p["y"])-p["size"]))

    draw_ship()

    screen.blit(font.render(f"Score: {score}  Level: {level}  Lives: {'♥'*lives}", True, (255,255,255)), (10,10))

    if state == "dead":
        msg = font.render("GAME OVER  -  Press SPACE to restart", True, (255,80,80))
        screen.blit(msg, (W//2 - msg.get_width()//2, H//2))

    pygame.display.flip()

pygame.quit()
sys.exit()
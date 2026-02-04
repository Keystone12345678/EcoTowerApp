import pygame
import sys
import random
import os
import math

# --- LOGIK-DATEN DIREKT IM CODE (Falls game_logic fehlt) ---
UPGRADES_DATA = [
    {"name": "Moos-Teppich", "base_cost": 15, "yield": 0.5},
    {"name": "Algen-Behälter", "base_cost": 100, "yield": 2.0},
    {"name": "Solar-Fenster", "base_cost": 500, "yield": 8.0},
    {"name": "Wind-Ventilator", "base_cost": 1200, "yield": 25.0},
    {"name": "Büro-Botaniker", "base_cost": 3500, "yield": 70.0}
]

def get_cost(base, count):
    return int(base * (1.15 ** count))

# --- INITIALISIERUNG ---
pygame.init()
WIDTH, HEIGHT = 400, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eco-Tower: Neo-Seoul (Vector Edition)")
clock = pygame.time.Clock()

# FARBEN
CYAN = (0, 255, 247)
MAGENTA = (255, 0, 255)
NEON_GREEN = (57, 255, 20)
GOLD = (255, 215, 0)
BG_DARK = (10, 10, 25)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("monospace", 16, bold=True)
big_font = pygame.font.SysFont("monospace", 28, bold=True)

# SPIELVARIABLEN
energy = 0
upgrade_counts = [0] * len(UPGRADES_DATA)
certificates = 0
drone_active = False
drone_x, drone_y = -100, 0
multiplier = 1
multiplier_timer = 0
click_effects = []

def draw_ufo(surface, x, y):
    # Gezeichnetes UFO statt Bild
    pygame.draw.ellipse(surface, (100, 100, 120), (x-40, y-10, 80, 30)) # Körper
    pygame.draw.ellipse(surface, CYAN, (x-20, y-20, 40, 25), 2) # Kuppel
    # Lichter
    for i in range(-2, 3):
        pygame.draw.circle(surface, NEON_GREEN, (x + i*15, y+5), 3)

# --- HAUPTSCHLEIFE ---
running = True
while running:
    # LOGIK
    eps = sum(upgrade_counts[i] * UPGRADES_DATA[i]["yield"] for i in range(len(UPGRADES_DATA)))
    energy += (eps / 60) * (1 + certificates * 0.1)
    
    if multiplier_timer > 0:
        multiplier_timer -= 1/60
    else:
        multiplier = 1

    if not drone_active and random.randint(1, 800) == 1:
        drone_active = True
        drone_x, drone_y = -50, random.randint(150, 300)

    if drone_active:
        drone_x += 4
        if drone_x > WIDTH + 50: drone_active = False

    # RENDERING
    screen.fill(BG_DARK)
    
    # UI
    screen.blit(big_font.render(f"{int(energy)} kWh", True, NEON_GREEN), (20, 30))
    screen.blit(font.render(f"RATE: {eps:.1f}/s", True, CYAN), (20, 70))

    # Spielfeld (Ersatz für Hintergrundbild)
    view_rect = pygame.Rect(20, 110, 360, 250)
    pygame.draw.rect(screen, (20, 30, 60), view_rect, border_radius=10)
    pygame.draw.rect(screen, CYAN, view_rect, 2, border_radius=10)
    
    # "Cyber-Stadt" Silhouetten zeichnen
    for i in range(5):
        pygame.draw.rect(screen, (10, 15, 40), (40 + i*60, 250, 40, 110))

    if drone_active:
        ufo_wave = math.sin(pygame.time.get_ticks() * 0.01) * 10
        draw_ufo(screen, drone_x, drone_y + ufo_wave)

    # UPGRADES
    for i, upg in enumerate(UPGRADES_DATA):
        cost = get_cost(upg["base_cost"], upgrade_counts[i])
        box_y = 380 + (i * 45)
        pygame.draw.rect(screen, (30, 30, 50), (20, box_y, 360, 35), border_radius=5)
        color = NEON_GREEN if energy >= cost else (100, 100, 100)
        screen.blit(font.render(upg["name"], True, WHITE), (30, box_y + 8))
        screen.blit(font.render(f"{cost} E", True, color), (280, box_y + 8))

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            # UFO Treffer
            if drone_active and math.hypot(mx - drone_x, my - drone_y) < 50:
                drone_active = False
                multiplier = 10
                multiplier_timer = 15
            # Klick im Feld
            elif view_rect.collidepoint(mx, my):
                energy += 1 * multiplier
            # Upgrade Klick
            for i in range(len(UPGRADES_DATA)):
                if 20 < mx < 380 and 380 + (i*45) < my < 415 + (i*45):
                    cost = get_cost(UPGRADES_DATA[i]["base_cost"], upgrade_counts[i])
                    if energy >= cost:
                        energy -= cost
                        upgrade_counts[i] += 1

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
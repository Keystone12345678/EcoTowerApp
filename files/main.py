import pygame
import sys
import random
import math
import time

# Versuche game_logic zu importieren, falls vorhanden
try:
    from game_logic import UPGRADES_DATA, get_cost, save_game, load_game
    HAS_GAME_LOGIC = True
except ImportError:
    HAS_GAME_LOGIC = False
    # Fallback: Lokale Daten
    UPGRADES_DATA = [
        {"name": "Moos-Teppich", "base_cost": 15, "yield": 0.5},
        {"name": "Algen-Behälter", "base_cost": 100, "yield": 2.0},
        {"name": "Solar-Fenster", "base_cost": 500, "yield": 8.0},
        {"name": "Wind-Ventilator", "base_cost": 1200, "yield": 25.0},
        {"name": "Büro-Botaniker", "base_cost": 3500, "yield": 70.0},
        {"name": "Regen-Turbine", "base_cost": 9000, "yield": 150.0},
        {"name": "Bio-Reaktor", "base_cost": 25000, "yield": 300.0},
        {"name": "CO2-Sauger", "base_cost": 75000, "yield": 600.0},
        {"name": "Quanten-Photo", "base_cost": 200000, "yield": 1500.0},
        {"name": "Fusion-Zelle", "base_cost": 500000, "yield": 3500.0}
    ]
    
    def get_cost(base, count):
        return int(base * (1.15 ** count))
    
    def save_game(e, c, cert):
        pass
    
    def load_game():
        return {"energy": 0, "counts": [0] * len(UPGRADES_DATA), "certificates": 0}, 0

# --- INITIALISIERUNG ---
pygame.init()
WIDTH, HEIGHT = 400, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eco-Tower: Neo-Seoul")
clock = pygame.time.Clock()

# FARBEN
CYAN = (0, 255, 247)
MAGENTA = (255, 0, 255)
NEON_GREEN = (57, 255, 20)
GOLD = (255, 215, 0)
BG_DARK = (10, 10, 25)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

font = pygame.font.SysFont("monospace", 16, bold=True)
big_font = pygame.font.SysFont("monospace", 28, bold=True)
small_font = pygame.font.SysFont("monospace", 12, bold=True)

# SPIELVARIABLEN LADEN
game_data, offline_gain = load_game()
energy = game_data["energy"]
upgrade_counts = game_data["counts"]
certificates = game_data["certificates"]

drone_active = False
drone_x, drone_y = -100, 0
multiplier = 1
multiplier_timer = 0
last_save_time = time.time()
scroll_offset = 0

# Offline-Gewinn anzeigen?
show_offline_message = offline_gain > 0
offline_message_timer = 5.0  # 5 Sekunden anzeigen

def draw_ufo(surface, x, y):
    """Zeichnet ein UFO"""
    pygame.draw.ellipse(surface, (100, 100, 120), (x-40, y-10, 80, 30))
    pygame.draw.ellipse(surface, CYAN, (x-20, y-20, 40, 25), 2)
    for i in range(-2, 3):
        pygame.draw.circle(surface, NEON_GREEN, (x + i*15, y+5), 3)

def format_number(num):
    """Formatiert große Zahlen lesbar"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return f"{int(num)}"

# --- HAUPTSCHLEIFE ---
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta-Zeit in Sekunden
    
    # LOGIK
    eps = sum(upgrade_counts[i] * UPGRADES_DATA[i]["yield"] for i in range(len(UPGRADES_DATA)))
    bonus_mult = 1 + (certificates * 0.1)
    energy += (eps * bonus_mult) * dt
    
    # Multiplier Timer
    if multiplier_timer > 0:
        multiplier_timer -= dt
        if multiplier_timer <= 0:
            multiplier = 1
    
    # UFO/Drohne Logik
    if not drone_active and random.randint(1, 800) == 1:
        drone_active = True
        drone_x, drone_y = -50, random.randint(150, 300)
    
    if drone_active:
        drone_x += 4
        if drone_x > WIDTH + 50:
            drone_active = False
    
    # Auto-Save alle 10 Sekunden
    if time.time() - last_save_time > 10:
        if HAS_GAME_LOGIC:
            save_game(energy, upgrade_counts, certificates)
        last_save_time = time.time()
    
    # Offline-Nachricht Timer
    if show_offline_message:
        offline_message_timer -= dt
        if offline_message_timer <= 0:
            show_offline_message = False
    
    # RENDERING
    screen.fill(BG_DARK)
    
    # Offline-Nachricht
    if show_offline_message:
        msg_surface = pygame.Surface((360, 60))
        msg_surface.fill((20, 40, 20))
        pygame.draw.rect(msg_surface, NEON_GREEN, (0, 0, 360, 60), 2)
        text1 = small_font.render("Willkommen zurück!", True, WHITE)
        text2 = small_font.render(f"Offline-Gewinn: +{format_number(offline_gain)} kWh", True, NEON_GREEN)
        msg_surface.blit(text1, (10, 10))
        msg_surface.blit(text2, (10, 30))
        screen.blit(msg_surface, (20, 400))
    
    # UI Header
    screen.blit(big_font.render(f"{format_number(energy)} kWh", True, NEON_GREEN), (20, 30))
    screen.blit(font.render(f"RATE: {format_number(eps * bonus_mult)}/s", True, CYAN), (20, 70))
    if certificates > 0:
        screen.blit(small_font.render(f"Zertifikate: {certificates} (+{int(certificates*10)}%)", True, GOLD), (20, 95))
    
    if multiplier > 1:
        screen.blit(font.render(f"BOOST x{multiplier}!", True, MAGENTA), (250, 30))
    
    # Spielfeld
    view_rect = pygame.Rect(20, 120, 360, 230)
    pygame.draw.rect(screen, (20, 30, 60), view_rect, border_radius=10)
    pygame.draw.rect(screen, CYAN, view_rect, 2, border_radius=10)
    
    # "Cyber-Stadt" Silhouetten
    for i in range(6):
        height = random.randint(80, 140) if i % 2 == 0 else random.randint(60, 100)
        pygame.draw.rect(screen, (10, 15, 40), (30 + i*55, 350-height, 40, height))
    
    # UFO mit Animation
    if drone_active:
        ufo_wave = math.sin(pygame.time.get_ticks() * 0.005) * 10
        draw_ufo(screen, drone_x, drone_y + ufo_wave)
    
    # UPGRADES (scrollbar)
    upgrade_area_y = 360
    upgrade_area_height = HEIGHT - upgrade_area_y
    visible_upgrades = upgrade_area_height // 45
    max_scroll = max(0, len(UPGRADES_DATA) - visible_upgrades)
    
    # Upgrade-Liste
    for i in range(len(UPGRADES_DATA)):
        display_index = i - scroll_offset
        if display_index < 0 or display_index >= visible_upgrades:
            continue
        
        upg = UPGRADES_DATA[i]
        cost = get_cost(upg["base_cost"], upgrade_counts[i])
        box_y = upgrade_area_y + (display_index * 45)
        
        # Box
        box_rect = pygame.Rect(20, box_y, 360, 40)
        pygame.draw.rect(screen, (30, 30, 50), box_rect, border_radius=5)
        
        # Highlight wenn kaufbar
        if energy >= cost:
            pygame.draw.rect(screen, NEON_GREEN, box_rect, 2, border_radius=5)
            color = NEON_GREEN
        else:
            pygame.draw.rect(screen, GRAY, box_rect, 1, border_radius=5)
            color = GRAY
        
        # Text
        name_text = font.render(upg["name"], True, WHITE)
        screen.blit(name_text, (30, box_y + 5))
        
        count_text = small_font.render(f"x{upgrade_counts[i]}", True, CYAN)
        screen.blit(count_text, (30, box_y + 23))
        
        cost_text = font.render(f"{format_number(cost)}", True, color)
        screen.blit(cost_text, (280, box_y + 12))
    
    # Scrollbar (falls nötig)
    if len(UPGRADES_DATA) > visible_upgrades:
        scrollbar_height = (visible_upgrades / len(UPGRADES_DATA)) * upgrade_area_height
        scrollbar_y = upgrade_area_y + (scroll_offset / len(UPGRADES_DATA)) * upgrade_area_height
        pygame.draw.rect(screen, CYAN, (385, scrollbar_y, 5, scrollbar_height), border_radius=2)
    
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Speichern vor Beenden
            if HAS_GAME_LOGIC:
                save_game(energy, upgrade_counts, certificates)
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            # Scroll mit Mausrad
            if event.button == 4:  # Scroll up
                scroll_offset = max(0, scroll_offset - 1)
            elif event.button == 5:  # Scroll down
                scroll_offset = min(max_scroll, scroll_offset + 1)
            elif event.button == 1:  # Linksklick
                # UFO Treffer
                if drone_active and math.hypot(mx - drone_x, my - drone_y) < 50:
                    drone_active = False
                    multiplier = 10
                    multiplier_timer = 15
                
                # Klick im Spielfeld
                elif view_rect.collidepoint(mx, my):
                    energy += 1 * multiplier
                
                # Upgrade Klick
                elif my >= upgrade_area_y:
                    for i in range(len(UPGRADES_DATA)):
                        display_index = i - scroll_offset
                        if display_index < 0 or display_index >= visible_upgrades:
                            continue
                        
                        box_y = upgrade_area_y + (display_index * 45)
                        if 20 < mx < 380 and box_y < my < box_y + 40:
                            cost = get_cost(UPGRADES_DATA[i]["base_cost"], upgrade_counts[i])
                            if energy >= cost:
                                energy -= cost
                                upgrade_counts[i] += 1
                                # Sofort speichern nach Kauf
                                if HAS_GAME_LOGIC:
                                    save_game(energy, upgrade_counts, certificates)
    
    pygame.display.flip()

# Finales Speichern
if HAS_GAME_LOGIC:
    save_game(energy, upgrade_counts, certificates)
pygame.quit()
sys.exit()

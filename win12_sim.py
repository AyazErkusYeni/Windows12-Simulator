import pygame
import sys
import math
from datetime import datetime

# Pygame Başlatma
pygame.init()
pygame.font.init()

# FULLSCREEN (Tam Ekran) Ayarları
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Windows 12 Pro Simulator - XS TEAM")

CLOCK = pygame.time.Clock()
FPS = 60

# Renk Paletleri
WALLPAPERS = [
    {"name": "Cyber Purple", "bg": (15, 12, 29), "accent": (168, 85, 247), "glow": (88, 28, 135)},
    {"name": "Midnight Blue", "bg": (10, 15, 30), "accent": (56, 189, 248), "glow": (30, 58, 138)},
    {"name": "Sunset Gold", "bg": (28, 15, 12), "accent": (251, 146, 60), "glow": (154, 52, 18)},
    {"name": "Emerald Matrix", "bg": (6, 24, 18), "accent": (52, 211, 153), "glow": (6, 78, 59)}
]
current_wp_index = 0

# Modern UI Renkleri
GLASS_BG = (22, 27, 38, 220)
HEADER_BG = (15, 20, 30)
WHITE = (248, 250, 252)
GRAY = (148, 163, 184)
DARK_GRAY = (30, 41, 59)
RED = (239, 68, 68)

FONT = pygame.font.SysFont("Segoe UI", 16)
BOLD_FONT = pygame.font.SysFont("Segoe UI", 18, bold=True)
TITLE_FONT = pygame.font.SysFont("Segoe UI", 26, bold=True)

class InputBox:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.placeholder = placeholder
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN and len(self.text) < 45:
                self.text += event.unicode

    def draw(self, surface):
        accent = WALLPAPERS[current_wp_index]["accent"]
        color = accent if self.active else GRAY
        pygame.draw.rect(surface, DARK_GRAY, self.rect, border_radius=10)
        pygame.draw.rect(surface, color, self.rect, 2, border_radius=10)
        
        display_txt = self.text if self.text else self.placeholder
        txt_color = WHITE if self.text else GRAY
        txt_surface = FONT.render(display_txt, True, txt_color)
        surface.blit(txt_surface, (self.rect.x + 15, self.rect.y + 8))

class Window:
    def __init__(self, title, x, y, w, h, content_type):
        self.title = title
        self.rect = pygame.Rect(x, y, w, h)
        self.content_type = content_type
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.is_open = False
        self.close_btn = pygame.Rect(self.rect.right - 40, self.rect.y + 8, 28, 22)
        
        if content_type == "browser":
            self.search_box = InputBox(x + 15, y + 45, w - 30, 36, "https://google.com veya arama yap...")

    def update_close_btn(self):
        self.close_btn = pygame.Rect(self.rect.right - 40, self.rect.y + 8, 28, 22)

    def draw(self, surface, music_playing, anim_timer):
        if not self.is_open:
            return

        accent = WALLPAPERS[current_wp_index]["accent"]

        # Yarı Saydam Buzlu Cam Gövde
        win_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        win_surf.fill((20, 26, 40, 235))
        surface.blit(win_surf, (self.rect.x, self.rect.y))
        pygame.draw.rect(surface, accent, self.rect, width=2, border_radius=14)

        # Başlık Çubuğu
        header_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 38)
        pygame.draw.rect(surface, HEADER_BG, header_rect, border_top_left_radius=14, border_top_right_radius=14)

        # Başlık Yazısı
        t_txt = BOLD_FONT.render(self.title, True, WHITE)
        surface.blit(t_txt, (self.rect.x + 15, self.rect.y + 8))

        # Kapat Butonu
        self.update_close_btn()
        pygame.draw.rect(surface, RED, self.close_btn, border_radius=6)
        x_txt = BOLD_FONT.render("✕", True, WHITE)
        surface.blit(x_txt, (self.close_btn.x + 8, self.close_btn.y + 1))

        content_rect = pygame.Rect(self.rect.x + 15, self.rect.y + 50, self.rect.width - 30, self.rect.height - 65)

        # 🌐 WEB TARAYICISI
        if self.content_type == "browser":
            self.search_box.rect.x = self.rect.x + 15
            self.search_box.rect.y = self.rect.y + 48
            self.search_box.rect.width = self.rect.width - 30
            self.search_box.draw(surface)

            web_area = pygame.Rect(self.rect.x + 15, self.rect.y + 95, self.rect.width - 30, self.rect.height - 110)
            pygame.draw.rect(surface, (12, 16, 26), web_area, border_radius=10)

            query = self.search_box.text.lower()
            if "youtube" in query:
                surface.blit(TITLE_FONT.render("▶ YouTube - XS TEAM Channel", True, RED), (web_area.x + 25, web_area.y + 20))
                
                # Video Kartı 1
                pygame.draw.rect(surface, DARK_GRAY, (web_area.x + 25, web_area.y + 70, 220, 110), border_radius=8)
                surface.blit(BOLD_FONT.render("🎬 gLiTcH wOrLd", True, WHITE), (web_area.x + 35, web_area.y + 110))
                surface.blit(FONT.render("Official Teaser", True, GRAY), (web_area.x + 35, web_area.y + 135))
                
                # Video Kartı 2
                pygame.draw.rect(surface, DARK_GRAY, (web_area.x + 265, web_area.y + 70, 220, 110), border_radius=8)
                surface.blit(BOLD_FONT.render("⛏️ MapleSMP Trailer", True, WHITE), (web_area.x + 275, web_area.y + 110))
                surface.blit(FONT.render("Minecraft Server", True, GRAY), (web_area.x + 275, web_area.y + 135))

            elif query:
                surface.blit(BOLD_FONT.render(f"🔍 '{self.search_box.text}' sonuçları:", True, accent), (web_area.x + 25, web_area.y + 20))
                pygame.draw.rect(surface, DARK_GRAY, (web_area.x + 25, web_area.y + 60, web_area.width - 50, 60), border_radius=8)
                surface.blit(BOLD_FONT.render("XS TEAM Official Portal", True, accent), (web_area.x + 40, web_area.y + 70))
                surface.blit(FONT.render("https://xsteam.dev/projects/win12", True, GRAY), (web_area.x + 40, web_area.y + 92))
            else:
                surface.blit(TITLE_FONT.render("🌐 Edge 12 - Web'de Ara", True, WHITE), (web_area.x + 25, web_area.y + 25))
                surface.blit(FONT.render("Yukarıdaki adrese 'youtube' yazarak videoları keşfedebilirsin.", True, GRAY), (web_area.x + 25, web_area.y + 70))

        # 🎵 MÜZİK ÇALAR
        elif self.content_type == "music":
            # Dönen Plak Efekti
            cx, cy = content_rect.x + 65, content_rect.y + 65
            pygame.draw.circle(surface, DARK_GRAY, (cx, cy), 55)
            angle = anim_timer * 0.05 if music

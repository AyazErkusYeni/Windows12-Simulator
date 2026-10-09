import pygame
import sys
import math
from datetime import datetime

# Pygame Başlatma
pygame.init()
pygame.font.init()

# Ekran Ayarları
WIDTH, HEIGHT = 1024, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Windows 12 Simulator - Concept Edition (XS TEAM)")

CLOCK = pygame.time.Clock()
FPS = 60

# Renk Paletleri & Duvar Kağıtları
WALLPAPERS = [
    {"name": "Midnight Blue", "bg": (15, 23, 42), "accent": (56, 189, 248)},
    {"name": "Cyber Purple", "bg": (30, 10, 50), "accent": (192, 132, 252)},
    {"name": "Sunset Orange", "bg": (45, 15, 20), "accent": (251, 146, 60)},
    {"name": "Emerald Matrix", "bg": (6, 30, 20), "accent": (52, 211, 153)}
]
current_wp_index = 0

# Arayüz Renkleri
TASKBAR_GLASS = (30, 41, 59)
WHITE = (248, 250, 252)
GRAY = (148, 163, 184)
DARK_GRAY = (51, 65, 85)
RED = (239, 68, 68)

FONT = pygame.font.SysFont("Segoe UI", 15)
BOLD_FONT = pygame.font.SysFont("Segoe UI", 17, bold=True)
TITLE_FONT = pygame.font.SysFont("Segoe UI", 22, bold=True)

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
            elif event.key != pygame.K_RETURN and len(self.text) < 30:
                self.text += event.unicode

    def draw(self, surface):
        color = WALLPAPERS[current_wp_index]["accent"] if self.active else GRAY
        pygame.draw.rect(surface, DARK_GRAY, self.rect, border_radius=8)
        pygame.draw.rect(surface, color, self.rect, 2, border_radius=8)
        
        display_txt = self.text if self.text else self.placeholder
        txt_color = WHITE if self.text else GRAY
        txt_surface = FONT.render(display_txt, True, txt_color)
        surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 7))

class Window:
    def __init__(self, title, x, y, w, h, content_type):
        self.title = title
        self.rect = pygame.Rect(x, y, w, h)
        self.content_type = content_type
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.is_open = False
        self.close_btn = pygame.Rect(self.rect.right - 35, self.rect.y + 5, 25, 20)
        
        if content_type == "browser":
            self.search_box = InputBox(x + 10, y + 40, w - 20, 32, "https://google.com veya arama yap...")

    def update_close_btn(self):
        self.close_btn = pygame.Rect(self.rect.right - 35, self.rect.y + 5, 25, 20)

    def draw(self, surface, music_playing, anim_timer):
        if not self.is_open:
            return

        accent = WALLPAPERS[current_wp_index]["accent"]

        # Pencere Gövdesi
        pygame.draw.rect(surface, TASKBAR_GLASS, self.rect, border_radius=12)
        pygame.draw.rect(surface, accent, self.rect, width=2, border_radius=12)

        # Başlık Çubuğu
        header_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 32)
        pygame.draw.rect(surface, DARK_GRAY, header_rect, border_top_left_radius=12, border_top_right_radius=12)

        # Başlık Yazısı
        t_txt = BOLD_FONT.render(self.title, True, WHITE)
        surface.blit(t_txt, (self.rect.x + 12, self.rect.y + 6))

        # Kapat Butonu
        self.update_close_btn()
        pygame.draw.rect(surface, RED, self.close_btn, border_radius=4)
        x_txt = FONT.render("X", True, WHITE)
        surface.blit(x_txt, (self.close_btn.x + 8, self.close_btn.y + 1))

        content_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 40, self.rect.width - 20, self.rect.height - 50)

        # 🌐 1. WEB TARAYICISI (EDGE 12)
        if self.content_type == "browser":
            self.search_box.rect.x = self.rect.x + 10
            self.search_box.rect.y = self.rect.y + 40
            self.search_box.draw(surface)

            web_area = pygame.Rect(self.rect.x + 10, self.rect.y + 80, self.rect.width - 20, self.rect.height - 90)
            pygame.draw.rect(surface, (20, 25, 35), web_area, border_radius=8)

            query = self.search_box.text.lower()
            if "youtube" in query:
                surface.blit(TITLE_FONT.render("▶ YouTube - XS TEAM Channel", True, RED), (web_area.x + 20, web_area.y + 20))
                surface.blit(FONT.render("• gLiTcH wOrLd Official Teaser Trailer", True, WHITE), (web_area.x + 20, web_area.y + 70))
                surface.blit(FONT.render("• MapleSMP Server Gameplay & Devlog", True, WHITE), (web_area.x + 20, web_area.y + 100))
            elif query:
                surface.blit(BOLD_FONT.render(f"🔍 '{self.search_box.text}' için Arama Sonuçları:", True, accent), (web_area.x + 20, web_area.y + 20))
                surface.blit(FONT.render("1. XS TEAM Resmi Topluluk Portalı", True, WHITE), (web_area.x + 20, web_area.y + 60))
                surface.blit(FONT.render("2. Python Pygame & Win12 OS Proje Sayfası", True, WHITE), (web_area.x + 20, web_area.y + 90))
            else:
                surface.blit(BOLD_FONT.render("🌐 Windows 12 Start Web Page", True, WHITE), (web_area.x + 20, web_area.y + 20))
                surface.blit(FONT.render("Arama yapmak için yukarıdaki adrese yazıp Enter'a basabilirsiniz.", True, GRAY), (web_area.x + 20, web_area.y + 50))

        # 🎵 2. MÜZİK ÇALAR (XS SOUND)
        elif self.content_type == "music":
            pygame.draw.rect(surface, DARK_GRAY, (content_rect.x, content_rect.y, 110, 110), border_radius=12)
            surface.blit(TITLE_FONT.render("🎵", True, accent), (content_rect.x + 40, content_rect.y + 35))

            surface.blit(BOLD_FONT.render("Lumi Athena - Scenecore Mix", True, WHITE), (content_rect.x + 130, content_rect.y + 10))
            surface.blit(FONT.render("Çalan: Track #01 (XS Sound Core)", True, GRAY), (content_rect.x + 130, content_rect.y + 35))

            # Ses Dalga Efekti (Spectrum)
            for i in range(16):
                h = math.sin(anim_timer * 0.1 + i) * 20 + 25 if music_playing else 5
                pygame.draw.rect(surface, accent, (content_rect.x + 130 + (i * 12), content_rect.y + 95 - h, 8, h), border_radius=3)

            # Oynat Butonu Rehberi
            status_txt = "▶ Çalıyor..." if music_playing else "⏸ Duraklatıldı (SPACE ile Oynat)"
            surface.blit(FONT.render(status_txt, True, accent if music_playing else RED), (content_rect.x + 130, content_rect.y + 110))

        # 🖼️ 3. DUVAR KAĞIDI DEĞİŞTİRİCİ
        elif self.content_type == "wallpaper":
            surface.blit(BOLD_FONT.render("Masaüstü Temasını Seçin:", True, WHITE), (content_rect.x, content_rect.y))
            
            bx = content_rect.x
            for idx, wp in enumerate(WALLPAPERS):
                btn_rect = pygame.Rect(bx, content_rect.y + 35, 80, 50)
                pygame.draw.rect(surface, wp["bg"], btn_rect, border_radius=8)
                border_c = WHITE if idx == current_wp_index else GRAY
                pygame.draw.rect(surface, border_c, btn_rect, width=2, border_radius=8)
                
                txt = FONT.render(f"Tema {idx+1}", True, WHITE)
                surface.blit(txt, (btn_rect.x + 12, btn_rect.y + 15))
                bx += 90

        # 📁 4. DOSYA GEZGİNİ
        elif self.content_type == "explorer":
            surface.blit(FONT.render("📁 C:\\Users\\AyazPC\\Desktop", True, WHITE), (content_rect.x, content_rect.y))
            items = ["ssdymus.py", "win12_sim.py", "README.md", "MapleSMP_Config"]
            iy = content_rect.y + 35
            for item in items:
                pygame.draw.rect(surface, DARK_GRAY, (content_rect.x, iy, content_rect.width, 30), border_radius=6)
                surface.blit(FONT.render(f"📄 {item}", True, WHITE), (content_rect.x + 10, iy + 5))
                iy += 38

# Uygulama Pencereleri
windows = {
    "browser": Window("Edge 12 - Web Browser", 100, 60, 600, 380, "browser"),
    "music": Window("XS Sound - Music Player", 220, 120, 480, 230, "music"),
    "wallpaper": Window("Kişiselleştirme - Duvar Kağıdı", 260, 150, 420, 200, "wallpaper"),
    "explorer": Window("Dosya Gezgini", 180, 90, 450, 300, "explorer")
}

start_menu_open = False
music_playing = True
anim_timer = 0

running = True
while running:
    CLOCK.tick(FPS)
    anim_timer += 1
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        windows["browser"].search_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and windows["music"].is_open:
                music_playing = not music_playing

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Başlat Menüsü
            start_btn_rect = pygame.Rect(WIDTH // 2 - 140, HEIGHT - 52, 40, 40)
            if start_btn_rect.collidepoint(mouse_pos):
                start_menu_open = not start_menu_open

            # Görev Çubuğu İkonları
            icons = {
                "browser": pygame.Rect(WIDTH // 2 - 80, HEIGHT - 52, 40, 40),
                "music": pygame.Rect(WIDTH // 2 - 20, HEIGHT - 52, 40, 40),
                "wallpaper": pygame.Rect(WIDTH // 2 + 40, HEIGHT - 52, 40, 40),
                "explorer": pygame.Rect(WIDTH // 2 + 100, HEIGHT - 52, 40, 40)
            }

            for key, rect in icons.items():
                if rect.collidepoint(mouse_pos):
                    windows[key].is_open = True

            # Duvar Kağıdı Değiştirme Tıklamaları
            if windows["wallpaper"].is_open:
                w_rect = windows["wallpaper"].rect
                bx = w_rect.x + 10
                for idx in range(len(WALLPAPERS)):
                    btn_r = pygame.Rect(bx, w_rect.y + 75, 80, 50)
                    if btn_r.collidepoint(mouse_pos):
                        current_wp_index = idx
                    bx += 90

            # Pencere Taşıma ve Kapatma
            for w in windows.values():
                if w.is_open:
                    if w.close_btn.collidepoint(mouse_pos):
                        w.is_open = False
                    elif pygame.Rect(w.rect.x, w.rect.y, w.rect.width, 32).collidepoint(mouse_pos):
                        w.is_dragging = True
                        w.drag_offset_x = w.rect.x - mouse_pos[0]
                        w.drag_offset_y = w.rect.y - mouse_pos[1]

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for w in windows.values():
                w.is_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            for w in windows.values():
                if w.is_dragging:
                    w.rect.x = mouse_pos[0] + w.drag_offset_x
                    w.rect.y = mouse_pos[1] + w.drag_offset_y

    # --- ÇİZİMLER ---
    accent = WALLPAPERS[current_wp_index]["accent"]

    # Dinamik Arka Plan
    screen.fill(WALLPAPERS[current_wp_index]["bg"])
    pygame.draw.circle(screen, DARK_GRAY, (200, 150), 280)
    pygame.draw.circle(screen, TASKBAR_GLASS, (800, 420), 200)

    # Pencereler
    for w in windows.values():
        w.draw(screen, music_playing, anim_timer)

    # Yüzen Görev Çubuğu (Windows 12 Dock)
    tb_rect = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 60, 320, 50)
    pygame.draw.rect(screen, TASKBAR_GLASS, tb_rect, border_radius=16)
    pygame.draw.rect(screen, accent, tb_rect, width=1, border_radius=16)

    # İkonlar
    pygame.draw.rect(screen, accent, (WIDTH // 2 - 140, HEIGHT - 52, 40, 40), border_radius=10)
    screen.blit(BOLD_FONT.render("W12", True, TASKBAR_GLASS), (WIDTH // 2 - 136, HEIGHT - 43))

    pygame.draw.rect(screen, DARK_GRAY, (WIDTH // 2 - 80, HEIGHT - 52, 40, 40), border_radius=10)
    screen.blit(FONT.render("🌐", True, WHITE), (WIDTH // 2 - 70, HEIGHT - 44))

    pygame.draw.rect(screen, DARK_GRAY, (WIDTH // 2 - 20, HEIGHT - 52, 40, 40), border_radius=10)
    screen.blit(FONT.render("🎵", True, WHITE), (WIDTH // 2 - 10, HEIGHT - 44))

    pygame.draw.rect(screen, DARK_GRAY, (WIDTH // 2 + 40, HEIGHT - 52, 40, 40), border_radius=10)
    screen.blit(FONT.render("🖼️", True, WHITE), (WIDTH // 2 + 50, HEIGHT - 44))

    pygame.draw.rect(screen, DARK_GRAY, (WIDTH // 2 + 100, HEIGHT - 52, 40, 40), border_radius=10)
    screen.blit(FONT.render("📁", True, WHITE), (WIDTH // 2 + 110, HEIGHT - 44))

    # Sağ Üst Saat
    now = datetime.now().strftime("%H:%M:%S")
    screen.blit(BOLD_FONT.render(now, True, WHITE), (WIDTH - 100, 20))

    # Başlat Menüsü
    if start_menu_open:
        sm_rect = pygame.Rect(WIDTH // 2 - 180, HEIGHT - 370, 360, 300)
        pygame.draw.rect(screen, TASKBAR_GLASS, sm_rect, border_radius=16)
        pygame.draw.rect(screen, accent, sm_rect, width=2, border_radius=16)

        screen.blit(TITLE_FONT.render("Windows 12 Pro", True, WHITE), (sm_rect.x + 20, sm_rect.y + 20))
        screen.blit(BOLD_FONT.render("👤 AyazXS (Admin)", True, accent), (sm_rect.x + 20, sm_rect.y + 55))

        pygame.draw.line(screen, GRAY, (sm_rect.x + 20, sm_rect.y + 85), (sm_rect.right - 20, sm_rect.y + 85))
        screen.blit(FONT.render("• XS TEAM OS Core v12.0", True, GRAY), (sm_rect.x + 20, sm_rect.y + 110))

    pygame.display.flip()

pygame.quit()
sys.exit()

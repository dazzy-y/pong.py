# menu.py
# Главное меню Pong — полностью исправлено верхнее меню

import pygame
import sys
import os
import webbrowser
from pong import PongGame

pygame.init()

WIDTH, HEIGHT = 800, 600

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong — Главное меню")
        self.clock = pygame.time.Clock()

        # Шрифты
        self.font_title = pygame.font.SysFont("Arial", 80, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 40)
        self.font_menu = pygame.font.SysFont("Arial", 24)
        self.font_info = pygame.font.SysFont("Arial", 28)
        self.font_small = pygame.font.SysFont("Arial", 20)
        self.font_link = pygame.font.SysFont("Arial", 24)

        # Текущая сложность и тема
        self.difficulty = "Средне"
        self.ai_speeds = {"Легко": 6, "Средне": 10, "Сложно": 14}
        self.theme = "Тёмная"
        self.update_colors()

        # Результат игры
        self.last_result = None

        # Сообщения
        self.message = None
        self.message_timer = 0

        # Модальное окно
        self.modal = None
        self.link_rects = []

        # Загруженное фото
        self.custom_image = None

        # Кнопки главного меню
        self.buttons = [
            {"text": "Играть (с ИИ)", "action": lambda: self.start_game("ai"), "rect": pygame.Rect(300, 180, 200, 70)},
            {"text": "Игра на 2", "action": lambda: self.start_game("two_player"), "rect": pygame.Rect(300, 270, 200, 70)},
            {"text": "Игра по сети", "action": lambda: self.start_game("network"), "rect": pygame.Rect(300, 360, 200, 70)},
            {"text": "Выход", "action": sys.exit, "rect": pygame.Rect(300, 450, 200, 70)},
        ]

        # Верхнее меню
        self.menu_bar_height = 40
        self.menu_items = [
            {"text": "Файл", "x": 10, "width": 80, "submenu": [
                {"text": "Загрузить фото", "action": self.load_custom_image},
                {"text": "Сохранить результат в Excel", "action": self.save_result_to_excel},
                {"text": "Выход", "action": sys.exit},
            ]},
            {"text": "Настройки", "x": 100, "width": 120, "submenu": [
                {"text": "Сложность: Легко", "action": lambda: self.set_difficulty("Легко")},
                {"text": "Сложность: Средне", "action": lambda: self.set_difficulty("Средне")},
                {"text": "Сложность: Сложно", "action": lambda: self.set_difficulty("Сложно")},
                {"text": "—", "action": None},
                {"text": "Тема: Тёмная", "action": lambda: self.set_theme("Тёмная")},
                {"text": "Тема: Светлая", "action": lambda: self.set_theme("Светлая")},
            ]},
            {"text": "Справка", "x": 230, "width": 100, "submenu": [
                {"text": "Об авторе", "action": lambda: self.show_modal("author")},
                {"text": "О приложении", "action": lambda: self.show_modal("about")},
            ]},
        ]

        self.active_submenu = None
        self.hovered_button = None

    def update_colors(self):
        if self.theme == "Тёмная":
            self.bg_color = (15, 25, 50)
            self.button_color = (0, 100, 200)
            self.button_hover = (0, 150, 255)
            self.text_color = (255, 255, 255)
            self.menu_bar_color = (40, 40, 60)
            self.submenu_color = (220, 220, 220)
            self.selected_color = (255, 255, 100)
            self.message_color = (255, 100, 100)
            self.modal_bg = (30, 40, 70)
            self.modal_border = (100, 150, 255)
            self.link_color = (100, 200, 255)
        else:
            self.bg_color = (240, 240, 240)
            self.button_color = (0, 150, 255)
            self.button_hover = (0, 100, 200)
            self.text_color = (0, 0, 0)
            self.menu_bar_color = (200, 200, 200)
            self.submenu_color = (255, 255, 255)
            self.selected_color = (255, 215, 0)
            self.message_color = (200, 0, 0)
            self.modal_bg = (255, 255, 255)
            self.modal_border = (0, 100, 200)
            self.link_color = (0, 100, 255)

    def set_theme(self, theme):
        self.theme = theme
        self.update_colors()

    def set_difficulty(self, level):
        self.difficulty = level

    def get_ai_speed(self):
        return self.ai_speeds[self.difficulty]

    def show_message(self, text, duration=3000):
        self.message = text
        self.message_timer = pygame.time.get_ticks() + duration

    def load_custom_image(self):
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(
                title="Выберите фото",
                filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp *.gif")]
            )
            if file_path:
                self.custom_image = pygame.image.load(file_path)
                self.show_message("Фото загружено!")
        except Exception as e:
            self.show_message(f"Ошибка: {str(e)}")

    def show_modal(self, modal_type):
        if modal_type == "author":
            self.modal = {
                "title": "Об авторе",
                "text": [
                    "ФИО: Кожемяко Дмитрий Андреевич",
                    "Группа: 10701323",
                    "Курсовой проект по дисциплине",
                    "'Конструирование программного обеспечения'",
                    "2025 год",
                    "",
                    "Контакты:",
                    "Instagram: https://www.instagram.com/dazziikk/?hl=ru"
                ],
                "image": "3.jpg"
            }
        elif modal_type == "about":
            self.modal = {
                "title": "О приложении",
                "text": [
                    "Pong v1.0",
                    "Классическая аркадная игра",
                    "Разработана на Python, Pygame",
                    "Особенности:",
                    "• Локальная игра на двоих",
                    "• Игра против ИИ",
                    "• Сетевая игра",
                    "• Загрузка фото",
                    "• Смена темы",
                    "• Сохранение в Excel",
                    "Исходный код: https://github.com/ivanov/pong-project"
                ],
                "image": "2.jpg"
            }

    def save_result_to_excel(self):
        if not self.last_result:
            self.show_message("Игра не сыграна!")
            return

        try:
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            ws.title = "Результат Pong"
            ws.append(["Параметр", "Значение"])
            ws.append(["Режим игры", self.last_result['mode']])
            ws.append(["Счёт левого", self.last_result['left_score']])
            ws.append(["Счёт правого", self.last_result['right_score']])
            ws.append(["Победитель", self.last_result['winner']])

            filename = f"pong_result_{int(pygame.time.get_ticks())}.xlsx"
            wb.save(filename)
            self.show_message(f"Сохранено: {filename}")
        except Exception as e:
            self.show_message(f"Ошибка: {str(e)}")

    def handle_event(self, event):
        if self.modal:
            if event.type == pygame.KEYDOWN:
                self.modal = None
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for rect, url in self.link_rects:
                    if rect.collidepoint(pos):
                        webbrowser.open(url)
                        return
                self.modal = None
                return

            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                hovered = any(rect.collidepoint(pos) for rect, _ in self.link_rects)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hovered else pygame.SYSTEM_CURSOR_ARROW)
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            # Кнопки главного меню
            for btn in self.buttons:
                if btn["rect"].collidepoint(pos):
                    btn["action"]()
                    return

            # Верхнее меню — клик по заголовку
            clicked_item = None
            for item in self.menu_items:
                if item["x"] <= pos[0] <= item["x"] + item["width"] and 0 <= pos[1] <= self.menu_bar_height:
                    clicked_item = item
                    break

            if clicked_item:
                if self.active_submenu == clicked_item:
                    self.active_submenu = None
                else:
                    self.active_submenu = clicked_item
                return  # Важно: return, чтобы не обрабатывать подменю дальше

            # Клик по подменю
            if self.active_submenu:
                y = self.menu_bar_height
                for sub in self.active_submenu["submenu"]:
                    if sub["text"] == "—":
                        y += 20
                        continue
                    sub_rect = pygame.Rect(self.active_submenu["x"], y, 220, 35)
                    if sub_rect.collidepoint(pos):
                        if sub["action"]:
                            sub["action"]()
                        self.active_submenu = None
                        return
                    y += 35

            # Клик вне — закрываем подменю
            self.active_submenu = None

        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self.hovered_button = next((b for b in self.buttons if b["rect"].collidepoint(pos)), None)

    def draw_modal(self):
        if not self.modal:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        modal_w, modal_h = 600, 500
        modal_x = WIDTH // 2 - modal_w // 2
        modal_y = HEIGHT // 2 - modal_h // 2

        pygame.draw.rect(self.screen, self.modal_bg, (modal_x, modal_y, modal_w, modal_h), border_radius=15)
        pygame.draw.rect(self.screen, self.modal_border, (modal_x, modal_y, modal_w, modal_h), 5, border_radius=15)

        title = self.font_info.render(self.modal["title"], True, self.text_color)
        self.screen.blit(title, (modal_x + 30, modal_y + 20))

        # Фото
        img_path = self.modal["image"]
        if os.path.exists(img_path):
            try:
                img = pygame.image.load(img_path)
                img = pygame.transform.scale(img, (180, 180))
                self.screen.blit(img, (modal_x + modal_w - 210, modal_y + 20))
            except:
                pass

        # Текст и ссылки
        y = modal_y + 80
        self.link_rects = []
        for line in self.modal["text"]:
            is_link = (
                line.startswith("http://") or
                line.startswith("https://") or
                "www." in line or
                "instagram.com" in line or
                "github.com" in line or
                "t.me" in line or
                "@" in line
            )
            if is_link:
                url = line.split(":", 1)[-1].strip() if ":" in line else line.strip()
                if not url.startswith("http"):
                    url = "https://" + url

                text = self.font_link.render(line, True, self.link_color)
                text_rect = text.get_rect(topleft=(modal_x + 30, y))
                self.screen.blit(text, text_rect)
                pygame.draw.line(self.screen, self.link_color, (text_rect.left, text_rect.bottom + 3),
                                 (text_rect.right, text_rect.bottom + 3), 2)
                self.link_rects.append((text_rect, url))
            else:
                text = self.font_small.render(line, True, self.text_color)
                self.screen.blit(text, (modal_x + 30, y))
            y += 30

        close_hint = self.font_small.render("Кликните или нажмите клавишу для закрытия", True, self.text_color)
        self.screen.blit(close_hint, (modal_x + 30, modal_y + modal_h - 50))

    def draw(self):
        self.screen.fill(self.bg_color)

        title = self.font_title.render("PONG", True, self.text_color)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for btn in self.buttons:
            color = self.button_hover if btn == self.hovered_button else self.button_color
            pygame.draw.rect(self.screen, color, btn["rect"], border_radius=12)
            text = self.font_button.render(btn["text"], True, self.text_color)
            text_rect = text.get_rect(center=btn["rect"].center)
            self.screen.blit(text, text_rect)

        diff_text = self.font_button.render(f"Сложность: {self.difficulty}", True, self.selected_color)
        self.screen.blit(diff_text, (WIDTH // 2 - diff_text.get_width() // 2, HEIGHT - 50))

        # Верхняя панель меню
        pygame.draw.rect(self.screen, self.menu_bar_color, (0, 0, WIDTH, self.menu_bar_height))
        for item in self.menu_items:
            color = (255, 255, 100) if self.active_submenu == item else self.text_color
            text = self.font_menu.render(item["text"], True, color)
            self.screen.blit(text, (item["x"] + 10, 8))

        # Подменю
        if self.active_submenu:
            x = self.active_submenu["x"]
            y = self.menu_bar_height
            height = sum(35 if s["text"] != "—" else 20 for s in self.active_submenu["submenu"]) + 10
            pygame.draw.rect(self.screen, self.submenu_color, (x, y, 220, height))
            pygame.draw.rect(self.screen, (100, 100, 100), (x, y, 220, height), 2)

            for sub in self.active_submenu["submenu"]:
                if sub["text"] == "—":
                    y += 20
                    pygame.draw.line(self.screen, (100, 100, 100), (x + 10, y - 10), (x + 210, y - 10))
                    continue
                color = self.selected_color if ("Сложность: " + self.difficulty in sub["text"] or "Тема: " + self.theme in sub["text"]) else (0, 0, 0)
                text = self.font_menu.render(sub["text"], True, color)
                self.screen.blit(text, (x + 15, y + 8))
                y += 35

        # Уведомление
        if self.message and pygame.time.get_ticks() < self.message_timer:
            msg_surf = self.font_info.render(self.message, True, self.message_color)
            msg_rect = msg_surf.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            pygame.draw.rect(self.screen, self.bg_color, msg_rect.inflate(20, 10))
            pygame.draw.rect(self.screen, self.message_color, msg_rect.inflate(20, 10), 3)
            self.screen.blit(msg_surf, msg_rect)

        self.draw_modal()

        pygame.display.flip()

    def start_game(self, mode):
        ai_speed = self.get_ai_speed() if mode == "ai" else 10
        game = PongGame(
            mode=mode,
            screen=self.screen,
            ai_speed=ai_speed,
            theme=self.theme,
            custom_image=self.custom_image
        )
        game.run()
        self.last_result = game.get_last_result()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_event(event)

            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    menu = Menu()
    menu.run()
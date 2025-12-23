# title_window.py
# Титульное окно курсового проекта с переходом в игру Pong

import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

# Импортируем класс Menu из твоего menu.py
from menu import Menu  # Убедись, что menu.py в той же папке

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class FirstWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Курсовой проект")
        self.root.geometry("850x680+300+80")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.timeout_id = None
        self.TIMEOUT_SECONDS = 60

        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)

        self.create_widgets()
        self.start_inactivity_timer()

        # Сбрасываем таймер при действиях пользователя
        self.root.bind("<KeyPress>", self.reset_timer)
        self.root.bind("<Button-1>", self.reset_timer)
        self.root.bind("<Button-2>", self.reset_timer)
        self.root.bind("<Button-3>", self.reset_timer)

    def start_inactivity_timer(self):
        self.reset_timer()

    def reset_timer(self, event=None):
        if self.timeout_id:
            self.root.after_cancel(self.timeout_id)
        self.timeout_id = self.root.after(self.TIMEOUT_SECONDS * 1000, self.close_due_to_inactivity)

    def close_due_to_inactivity(self):
        notification = ctk.CTkToplevel(self.root)
        notification.title("")
        notification.geometry("460x120")
        notification.resizable(False, False)
        notification.configure(fg_color="#1e293b")
        notification.overrideredirect(True)
        notification.attributes("-topmost", True)

        notification.update_idletasks()
        x = (notification.winfo_screenwidth() // 2) - 230
        y = (notification.winfo_screenheight() // 2) - 60
        notification.geometry(f"+{x}+{y}")

        ctk.CTkLabel(notification,
                     text="Приложение будет закрыто\nиз-за бездействия (60 сек)...",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="white").pack(expand=True)

        notification.attributes("-alpha", 0.0)
        self.fade_in(notification, 0.0)

        self.root.after(1500, lambda: self.final_close(notification))

    def fade_in(self, window, alpha):
        alpha += 0.08
        if alpha < 1.0:
            window.attributes("-alpha", alpha)
            self.root.after(40, lambda: self.fade_in(window, alpha))
        else:
            window.attributes("-alpha", 1.0)

    def final_close(self, notification):
        notification.destroy()
        self.root.destroy()

    def confirm_exit(self):
        if tk.messagebox.askyesno("Выход", "Вы уверены, что хотите выйти из приложения?"):
            if self.timeout_id:
                self.root.after_cancel(self.timeout_id)
            self.root.destroy()

    def create_widgets(self):
        ctk.CTkLabel(self.root,
                     text="БЕЛОРУССКИЙ НАЦИОНАЛЬНЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ",
                     font=ctk.CTkFont(size=17, weight="bold"),
                     text_color="#1e3a8a").pack(pady=20)

        ctk.CTkLabel(self.root,
                     text="Факультет информационных технологий и робототехрики\n"
                          "Кафедра ПО информационных систем и технологий",
                     font=ctk.CTkFont(size=13),
                     text_color="gray20").pack(pady=10)

        ctk.CTkLabel(self.root,
                     text="КУРСОВОЙ ПРОЕКТ",
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color="#1e40af").pack(pady=25)

        ctk.CTkLabel(self.root,
                     text="по дисциплине «Конструирование программного обеспечения»",
                     font=ctk.CTkFont(size=15)).pack(pady=5)

        ctk.CTkLabel(self.root,
                     text="Классическая игра Pong с расширенными возможностями",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#1e3a8a").pack(pady=35)

        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.pack(pady=20)

        try:
            img_path = resource_path("1.jpg")
            img = Image.open(img_path)
            img = img.resize((260, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=photo, bg=self.root.cget("bg"))
            img_label.image = photo
            img_label.pack(side="left", padx=30)
        except Exception as e:
            print("Фото не загрузилось:", e)
            ctk.CTkLabel(frame, text="[Фото не найдено]", font=ctk.CTkFont(size=14)).pack(side="left", padx=30)

        info_text = """Выполнил:
студент группы 10701323
Кожемяко Дмитрий Андреевич

Преподаватель:
к.ф.-м.н., доцент
Станкевич Сергей Николаевич

Минск, 2025"""
        ctk.CTkLabel(frame, text=info_text, font=ctk.CTkFont(size=14), justify="left").pack(side="right", padx=40)

        btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(pady=40)

        ctk.CTkButton(btn_frame,
                      text="ПРОДОЛЖИТЬ",
                      width=220,
                      height=50,
                      font=ctk.CTkFont(size=18, weight="bold"),
                      fg_color="#1e40af",
                      hover_color="#1e3a8a",
                      command=self.open_pong_game).pack(side="left", padx=20)

        ctk.CTkButton(btn_frame,
                      text="ВЫХОД",
                      width=150,
                      height=50,
                      fg_color="#dc2626",
                      hover_color="#b91c1c",
                      command=self.confirm_exit).pack(side="right", padx=20)

        ctk.CTkLabel(self.root,
                     text="Автозакрытие через 60 секунд бездействия\n(движение мыши не считается)",
                     font=ctk.CTkFont(size=11, slant="italic"),
                     text_color="gray50").pack(side="bottom", pady=12)

    def open_pong_game(self):
        """Открываем главное меню Pong"""
        if self.timeout_id:
            self.root.after_cancel(self.timeout_id)

        self.root.withdraw()  # Скрываем титульное окно

        # Запускаем главное меню Pong
        pong_menu = Menu()
        pong_menu.run()

        # После закрытия Pong — возвращаемся на титульник (если не было выхода)
        self.root.deiconify()
        self.start_inactivity_timer()


if __name__ == "__main__":
    app = FirstWindow()
    app.root.mainloop()
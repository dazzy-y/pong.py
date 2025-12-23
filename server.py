# server.py
# Сервер для сетевой игры Pong
# Запуск: python server.py
# Подключайтесь клиентами к localhost:12345 (или IP сервера)
# Поддерживает ровно 2 игроков: Левый (Player 1), Правый (Player 2)
# Сервер симулирует мяч, коллизии, счёт

import socket
import threading
import json
import time
import random
import sys

# Константы (как в pong.py) фывфвфыв
WIDTH = 800
HEIGHT = 600
PAD_WIDTH = 15
PAD_HEIGHT = 100
BALL_RADIUS = 15
BALL_SPEED = 6
PADDLE_SPEED = 10
WIN_SCORE = 10

class PongServer: # Описание архитектуры приложения и шаблонов проектирования
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        print(f"Сервер запущен на {host}:{port}")
        print("Ожидание подключений игроков...")

        # Игроки
        self.players = [None, None]  # sockets: 0 - левый, 1 - правый
        self.player_connected = [False, False]

        # Состояние игры (thread-safe)
        self.lock = threading.Lock()
        self.game_running = False
        self.left_y = HEIGHT / 2 - PAD_HEIGHT / 2
        self.right_y = HEIGHT / 2 - PAD_HEIGHT / 2
        self.left_vel = 0
        self.right_vel = 0
        self.ball_x = WIDTH / 2
        self.ball_y = HEIGHT / 2
        self.ball_vx = BALL_SPEED * random.choice([-1, 1])
        self.ball_vy = BALL_SPEED * random.uniform(-0.8, 0.8)
        self.left_score = 0
        self.right_score = 0
        self.winner = None

    def start(self):
        # Ждём подключения 2 игроков
        while sum(self.player_connected) < 2:
            conn, addr = self.server_socket.accept()
            print(f"Подключён {addr}")
            # Присваиваём слот первому/второму
            player_id = 0 if not self.player_connected[0] else 1
            self.players[player_id] = conn
            self.player_connected[player_id] = True
            threading.Thread(target=self.handle_client, args=(conn, player_id, addr), daemon=True).start()

        print("Оба игрока подключены! Запуск игры...")
        self.game_running = True
        self.game_loop()

    def handle_client(self, conn, player_id, addr):
        try:
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                msg = json.loads(data)
                if msg['type'] == 'move':
                    with self.lock:
                        if player_id == 0:
                            self.left_vel = {'up': -PADDLE_SPEED, 'down': PADDLE_SPEED, 'stop': 0}[msg['direction']]
                        else:
                            self.right_vel = {'up': -PADDLE_SPEED, 'down': PADDLE_SPEED, 'stop': 0}[msg['direction']]
        except:
            pass
        finally:
            print(f"Игрок {player_id+1} ({addr}) отключился")
            with self.lock:
                self.player_connected[player_id] = False
                self.game_running = False
            conn.close()

    def update_game(self):
        with self.lock:
            # Движение ракеток
            self.left_y += self.left_vel
            self.left_y = max(PAD_HEIGHT / 2, min(HEIGHT - PAD_HEIGHT / 2, self.left_y))
            self.right_y += self.right_vel
            self.right_y = max(PAD_HEIGHT / 2, min(HEIGHT - PAD_HEIGHT / 2, self.right_y))

            # Движение мяча
            self.ball_x += self.ball_vx
            self.ball_y += self.ball_vy

            # Отскок от верха/низа
            if self.ball_y <= BALL_RADIUS or self.ball_y >= HEIGHT - BALL_RADIUS:
                self.ball_vy *= -1

            # Коллизия с левой ракеткой
            if (self.ball_x <= PAD_WIDTH + BALL_RADIUS and
                self.left_y - PAD_HEIGHT / 2 <= self.ball_y <= self.left_y + PAD_HEIGHT / 2):
                self.ball_vx *= -1.1
                self.ball_vy += random.uniform(-2, 2)

            # Коллизия с правой ракеткой
            if (self.ball_x >= WIDTH - PAD_WIDTH - BALL_RADIUS and
                self.right_y - PAD_HEIGHT / 2 <= self.ball_y <= self.right_y + PAD_HEIGHT / 2):
                self.ball_vx *= -1.1
                self.ball_vy += random.uniform(-2, 2)

            # Гол слева (правый игрок забил)
            if self.ball_x < 0:
                self.right_score += 1
                self.reset_ball()

            # Гол справа (левый игрок забил)
            if self.ball_x > WIDTH:
                self.left_score += 1
                self.reset_ball()

            # Проверка победы
            if self.left_score >= WIN_SCORE:
                self.winner = "Левый игрок"
                self.game_running = False
            elif self.right_score >= WIN_SCORE:
                self.winner = "Правый игрок"
                self.game_running = False

    def reset_ball(self):
        self.ball_x = WIDTH / 2
        self.ball_y = HEIGHT / 2
        self.ball_vx = BALL_SPEED * random.choice([-1, 1])
        self.ball_vy = BALL_SPEED * random.uniform(-0.8, 0.8)

    def send_state(self):
        with self.lock:
            state = {
                'type': 'state',
                'left_y': self.left_y,
                'right_y': self.right_y,
                'ball_x': self.ball_x,
                'ball_y': self.ball_y,
                'ball_vx': self.ball_vx,
                'ball_vy': self.ball_vy,
                'left_score': self.left_score,
                'right_score': self.right_score,
                'winner': self.winner
            }
            state_json = json.dumps(state)
            for player in self.players:
                if player:
                    try:
                        player.send(state_json.encode('utf-8'))
                    except:
                        pass

    def game_loop(self):
        while self.game_running:
            self.update_game()
            self.send_state()
            time.sleep(1/60)  # 60 FPS

        # Игра окончена - отправляем финальное состояние
        self.send_state()
        print(f"Игра окончена! Победитель: {self.winner}")

    def stop(self):
        self.server_socket.close()

if __name__ == "__main__":
    server = PongServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    finally:
        server.stop()
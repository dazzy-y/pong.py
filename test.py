# test_server.py
# Unit-тесты для серверной части Pong (server.py)

import unittest
from server import PongServer

class TestPongServer(unittest.TestCase):
    def setUp(self):
        # port=0 — система выберет свободный порт автоматически
        self.server = PongServer(host='localhost', port=0)
        self.server.game_running = True  # имитируем запущенную игру

    def test_ball_reset(self):
        # Устанавливаем мяч за пределами поля (гол справа — левый игрок забил)
        self.server.ball_x = self.server.WIDTH + 10  # за правой границей
        self.server.ball_y = 300
        self.server.update_game()

        # Проверяем, что мяч вернулся в центр
        self.assertAlmostEqual(self.server.ball_x, self.server.WIDTH / 2, delta=5)
        self.assertAlmostEqual(self.server.ball_y, self.server.HEIGHT / 2, delta=5)
        # И счёт левого игрока увеличился
        self.assertEqual(self.server.left_score, 1)

    def test_paddle_collision_acceleration(self):
        # Мяч летит в левую ракетку
        self.server.ball_x = 60
        self.server.ball_y = self.server.HEIGHT // 2
        self.server.ball_vx = -5  # летит влево
        self.server.left_y = self.server.HEIGHT // 2  # ракетка на месте мяча

        initial_speed = abs(self.server.ball_vx)
        self.server.update_game()

        # После отскока скорость должна увеличиться на 10%
        new_speed = abs(self.server.ball_vx)
        self.assertAlmostEqual(new_speed, initial_speed * 1.1, delta=0.5)
        self.assertGreater(self.server.ball_vx, 0)  # направление изменилось (отскок вправо)

    def test_win_condition(self):
        # Даём левому игроку 9 очков
        self.server.left_score = 9
        # Гол левому (мяч за правой границей)
        self.server.ball_x = self.server.WIDTH + 10
        self.server.update_game()

        self.assertEqual(self.server.left_score, 10)
        self.assertIn("Левый игрок", self.server.winner or "")  # текст может варьироваться
        self.assertFalse(self.server.game_running)

if __name__ == '__main__':
    unittest.main()
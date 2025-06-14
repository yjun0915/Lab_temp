from manim import *
import numpy as np


class RandomMinPoint(ThreeDScene):
    def func(self, x, y):
        return np.sin(-x) * np.cos(y / 2)

    def construct(self):
        # 좌표계 설정
        ax = ThreeDAxes(
            x_range=[-np.pi, np.pi],
            y_range=[-np.pi, np.pi],
            z_range=[-1, 1],
            axis_config={
                "color": BLACK,
                "include_numbers": False
            }
        ).add_coordinates()
        self.set_camera_orientation(phi=60 * DEGREES, theta=-60 * DEGREES, zoom=0.7)
        self.camera.background_color = WHITE

        labels = ax.get_axis_labels(x_label=Text("x", color=BLACK), y_label=Text("y", color=BLACK), z_label=Text("z", color=BLACK))
        self.add(ax, labels)

        res = 10
        for idx in range(-res, res+1):
            _x = np.pi * idx/res
            _y = _x

            line_x = ParametricFunction(
                lambda u: ax.c2p(u, _y, self.func(u, _y)),
                color=GRAY, t_range=(-np.pi, np.pi), stroke_width=1
            ).set_shade_in_3d(True)

            line_y = ParametricFunction(
                lambda u: ax.c2p(_x, u, self.func(_x, u)),
                color=GRAY, t_range=(-np.pi, np.pi), stroke_width=1
            ).set_shade_in_3d(True)

            self.add(ax, line_x)
            self.add(ax, line_y)

        # 랜덤 점 생성
        N = 250
        points = []
        min_val = float("inf")
        min_point = None

        for _ in range(N):
            x = np.random.uniform(-np.pi, np.pi)
            y = np.random.uniform(-np.pi, np.pi)
            u = self.func(x, y)
            points.append((x, y, u))
            if u <= min_val:
                min_val = u
                min_point = (x, y)
        print(min_val)
        # 점 찍기
        dots = VGroup()
        for x, y, z in points:
            dot = Dot3D(ax.c2p(x, y, z), radius=0.025, color=DARK_BLUE)
            dots.add(dot)

        min_dot = Dot3D(ax.c2p(min_point[0], min_point[1], min_val), radius=0.08, color=PURE_RED)

        self.play(LaggedStartMap(Create, dots, lag_ratio=0.05), run_time=3)
        self.wait()
        self.play(GrowFromCenter(min_dot))
        self.wait(2)


class VariationalMinimization(ThreeDScene):
    def func(self, x, y):
        return np.sin(-x) * np.cos(y / 2)

    def construct(self):
        ax = ThreeDAxes(
            x_range=[-np.pi, np.pi],
            y_range=[-np.pi, np.pi],
            z_range=[-1, 1],
            axis_config={
                "color": BLACK,
                "include_numbers": False
            }
        ).add_coordinates()

        self.set_camera_orientation(phi=60 * DEGREES, theta=-60 * DEGREES, zoom=0.7)
        self.camera.background_color = WHITE

        labels = ax.get_axis_labels(x_label=Text("x", color=BLACK), y_label=Text("y", color=BLACK), z_label=Text("z", color=BLACK))
        self.add(ax, labels)

        res = 10
        for idx in range(-res, res+1):
            _x = np.pi * idx/res
            _y = _x

            line_x = ParametricFunction(
                lambda u: ax.c2p(u, _y, self.func(u, _y)),
                color=GRAY, t_range=(-np.pi, np.pi), stroke_width=1
            ).set_shade_in_3d(True)

            line_y = ParametricFunction(
                lambda u: ax.c2p(_x, u, self.func(_x, u)),
                color=GRAY, t_range=(-np.pi, np.pi), stroke_width=1
            ).set_shade_in_3d(True)

            self.add(ax, line_x)
            self.add(ax, line_y)

        d = 0.5
        steps = 20
        resolution = 3

        # 초기점
        x, y = -np.pi/4, -np.pi/2
        z = self.func(x, y)
        current_dot = Dot3D(ax.c2p(x, y, z), color="#B8860B")

        self.play(FadeIn(current_dot))
        self.wait()

        for i in range(steps):
            square_dots = VGroup()
            min_val = float("inf")
            new_x, new_y = x, y

            for dx in np.linspace(-d / 2, d / 2, resolution):
                for dy in np.linspace(-d / 2, d / 2, resolution):
                    px = x + dx
                    py = y + dy
                    if -np.pi <= px <= np.pi and -np.pi <= py <= np.pi:
                        val = self.func(px, py)
                        dot = Dot3D(ax.c2p(px, py, val), radius=0.03, color=DARK_BLUE)
                        square_dots.add(dot)

                        if val < min_val:
                            min_val = val
                            new_x, new_y = px, py

            self.play(FadeIn(square_dots), run_time=0.5)
            new_dot = Dot3D(ax.c2p(new_x, new_y, min_val), color="#B8860B")
            self.play(Transform(current_dot, new_dot), run_time=1)
            if new_x == x and new_y == y:
                for dx in np.linspace(-d / 2, d / 2, resolution):
                    for dy in np.linspace(-d / 2, d / 2, resolution):
                        px = x + dx
                        py = y + dy
                        if -np.pi <= px <= np.pi and -np.pi <= py <= np.pi:
                            val = self.func(px, py)
                            dot = Dot3D(ax.c2p(px, py, val), radius=0.03, color=DARK_BLUE)
                            square_dots.add(dot)
                self.play(FadeIn(square_dots), run_time=0.5)
                break
            x, y = new_x, new_y
            self.wait(0.3)

        self.wait(2)

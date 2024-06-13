from manim import *
import numpy as np

class ProjectileMotion(Scene):
    def construct(self):
        # Setup the axes
        axes = Axes(
            x_range=[0, 280, 20], y_range=[0, 80, 10],
            axis_config={"include_numbers": True}
        )#.shift(UP * 1)

        x_label = axes.get_x_axis_label(r"x \, \text{(m)}")
        y_label = axes.get_y_axis_label(r"y \, \text{(m)}")

        # Initial conditions
        v0 = 50  # initial velocity
        angle = PI / 4  # launch angle (45 degrees)
        g = 9.8  # gravity

        # Display initial conditions
        initial_conditions = VGroup(
            Text(f"Initial velocity (v0): {v0} m/s").scale(0.7),
            Text(f"Launch angle: {int(np.degrees(angle))} degrees").scale(0.7),
            Text(f"Gravity (g): {g} m/s²").scale(0.7)
        ).arrange(DOWN, aligned_edge=RIGHT).to_corner(UR)

        # Parametric equations for the projectile motion
        def projectile_pos(t):
            return np.array([
                v0 * np.cos(angle) * t,
                v0 * np.sin(angle) * t - 0.5 * g * t**2,
                0
            ])

        # Velocity vector function
        def velocity(t):
            return np.array([
                v0 * np.cos(angle),
                v0 * np.sin(angle) - g * t,
                0
            ])

        # Acceleration vector (constant)
        acceleration = np.array([0, -g, 0])

        # Trajectory of the projectile
        trajectory = axes.plot_parametric_curve(
            lambda t: projectile_pos(t),
            t_range=[0, (2 * v0 * np.sin(angle)) / g],  # time of flight
            color=BLUE
        )

        # Moving dot for the projectile
        dot = Dot().move_to(axes.coords_to_point(*projectile_pos(0)))

        # Time tracker
        time_tracker = ValueTracker(0)

        # Velocity and acceleration vectors
        velocity_vector = always_redraw(
            lambda: Arrow(
                dot.get_center(),
                dot.get_center() + velocity(time_tracker.get_value()) / 10,
                buff=0,
                color=GREEN
            )
        )

        acceleration_vector = always_redraw(
            lambda: Arrow(
                dot.get_center(),
                dot.get_center() + acceleration / 10,
                buff=0,
                color=RED
            )
        )

        # Velocity and acceleration labels
        velocity_label = always_redraw(
            lambda: MathTex(
                f"\\vec{{v}} = \\begin{{bmatrix}} {velocity(time_tracker.get_value())[0]:.2f} \\\\ {velocity(time_tracker.get_value())[1]:.2f} \\end{{bmatrix}}",
                color=GREEN
            ).next_to(velocity_vector, RIGHT)
        )

        acceleration_label = always_redraw(
            lambda: MathTex(
                f"\\vec{{a}} = \\begin{{bmatrix}} {acceleration[0]} \\\\ {acceleration[1]} \\end{{bmatrix}}",
                color=RED
            ).next_to(acceleration_vector, RIGHT)
        )

        def update_dot(dot):
            t = time_tracker.get_value()
            new_pos = projectile_pos(t)
            dot.move_to(axes.coords_to_point(new_pos[0], new_pos[1]))
            return dot

        dot.add_updater(update_dot)

        # Add elements to the scene
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Write(initial_conditions))
        self.play(Create(trajectory), Create(dot))
        self.add(velocity_vector, acceleration_vector, velocity_label, acceleration_label)

        # Animate the projectile motion
        self.play(time_tracker.animate.set_value((2 * v0 * np.sin(angle)) / g), run_time=10, rate_func=linear)
        self.wait(2)

# To run the scene, use the following command in the terminal:
# manim -pql projectile_motion.py ProjectileMotion

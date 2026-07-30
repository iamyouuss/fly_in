import math
import arcade
from .Simulation import Simulation

SCREEN_WIDTH = 2400
SCREEN_HEIGHT = 1020
SCREEN_TITLE = "Fly-In Simulation"
MARGIN = 150
PALETTE = {
            "red": arcade.color.RED,
            "darkred": arcade.color.DARK_RED,
            "orange": arcade.color.SAE,
            "yellow": arcade.color.AMBER,
            "green": arcade.color.APPLE_GREEN,
            "darkgreen": arcade.color.DARK_GREEN,
            "blue": arcade.color.AZURE,
            "darkblue": arcade.color.DARK_BLUE,
            "purple": arcade.color.BRIGHT_LILAC,
            "violet": arcade.color.VIOLET,
            "pink": arcade.color.CARNATION_PINK,
            "crimson": arcade.color.ALIZARIN_CRIMSON,
            "white": arcade.color.FLORAL_WHITE,
            "black": arcade.color.BLACK,
            "grey": arcade.color.ASH_GREY,
            "brown": arcade.color.DARK_BROWN,
            "cyan": arcade.color.CYAN,
            "rainbow": arcade.color.INDIGO,
            "gold": arcade.color.GOLD,
            "magenta": arcade.color.DARK_MAGENTA,
            "maroon": arcade.color.LIGHT_BROWN,
            "lime": arcade.color.LIME
}


class Visualizer(arcade.Window):
    def __init__(self, simulation: Simulation) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT,
                         SCREEN_TITLE, resizable=True)
        self.sim: Simulation = simulation
        self.auto_play: bool = False
        self.chrono: float = 0.0
        self.speed: int = 1
        self.background_color = arcade.color.BEIGE
        self.turn_output: list[str] = []

        xs = [z.x for z in simulation.map.zones]
        ys = [z.y for z in simulation.map.zones]
        min_x, min_y, max_x, max_y = min(xs), min(ys), max(xs), max(ys)
        logic_w = max_x - min_x or 1
        logic_h = max_y - min_y or 1
        draw_w = SCREEN_WIDTH - 2 * MARGIN
        draw_h = SCREEN_HEIGHT - 2 * MARGIN
        self.scale_x: int = draw_w / logic_w
        self.scale_y: int = draw_h / logic_h
        self.origin_x: float = MARGIN - min_x * self.scale_x
        self.origin_y: float = MARGIN - min_y * self.scale_y

        nb = self.sim.map.nb_of_drones
        self.radius = max(18, min(draw_w / (nb * 2.5), 40))

        self.sim.create_drones()
        self.sim.plan_all_drone_paths()

    def get_pixel_position(self, x: float, y: float) -> tuple[float, float]:
        return (
            self.origin_x + x * self.scale_x,
            self.origin_y + y * self.scale_y
        )

    def step_forward(self) -> None:
        """Joue un tour de simulation et met à jour l'affichage."""
        if not all(drone.is_delivered for drone in self.sim.drones):
            self.sim.play_turn()

            self.turn_output = []
            for drone in self.sim.drones:
                output = drone.format_output()
                if output and "start" not in output:
                    self.turn_output.append(output)

            self.sim.turn_counter += 1

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.SPACE:
            self.auto_play = not self.auto_play
            self.chrono = 0.0
        if key == arcade.key.RIGHT:
            self.auto_play = False
            self.step_forward()

    def on_update(self, delta_time) -> None:
        if self.auto_play:
            self.chrono += delta_time
            if self.chrono >= self.speed:
                """ if not all(
                drone.is_delivered for drone in self.sim.drones):
                    self.sim.play_turn()
                    self.turn_output = []
                    for drone in self.sim.drones:
                        output = drone.format_output()
                        if output and "start" not in output:
                            self.turn_output.append(output)
                    self.sim.turn_counter += 1 """
                self.step_forward()
                self.chrono = 0.0

    def on_draw(self) -> None:
        self.clear()

        for connections in self.sim.map.connection_list.values():
            for connection in connections:
                s_x, s_y = self.get_pixel_position(
                    connection.hub_a.x, connection.hub_a.y)
                e_x, e_y = self.get_pixel_position(
                    connection.hub_b.x, connection.hub_b.y)
                color = arcade.color.GRAY
                arcade.draw_line(s_x, s_y, e_x, e_y, color, 4)

        for zone in self.sim.map.zones:
            x, y = self.get_pixel_position(zone.x, zone.y)
            color = PALETTE.get(zone.color, arcade.color.DARK_GRAY)
            r = self.radius
            arcade.draw_circle_filled(x, y, r, color)
            arcade.draw_text(
                f"{len(zone.current_drones)}/{zone.max_drones}",
                x, y + r + 2,
                arcade.color.BLACK, 10,
                anchor_x='center', anchor_y='bottom'
            )

        for drone in self.sim.drones:
            if drone.current_zone:
                total = len(drone.current_zone.current_drones)
                img = drone.img
                x, y = self.get_pixel_position(drone.current_zone.x,
                                               drone.current_zone.y)
                if total > 1:
                    index = drone.current_zone.current_drones.index(drone)
                    angle = (index / total) * 2 * math.pi
                    shift_x = math.cos(angle) * self.radius
                    shift_y = math.sin(angle) * self.radius
                    x += shift_x
                    y += shift_y

                arcade.draw_texture_rect(
                    drone.img,
                    arcade.XYWH(
                        x, y, img.width, img.height).scale(0.4)
                )
            elif drone.current_connection:
                half_x = (
                    drone.current_connection.hub_b.x
                    + drone.current_connection.hub_a.x) / 2
                half_y = (
                    drone.current_connection.hub_a.y
                    + drone.current_connection.hub_b.y) / 2
                x, y = self.get_pixel_position(half_x, half_y)
                img = drone.img
                arcade.draw_texture_rect(
                    img,
                    arcade.XYWH(
                        x, y, img.width, img.height).scale(0.4)
                )
            arcade.draw_text(
                f"{drone}",
                x, y - 40,
                arcade.color.GRAY, 10
            )
        mode = "Auto-Play" if self.auto_play else "Manual"
        arcade.draw_text(
            f"Turn: {self.sim.turn_counter} "
            f"| {mode} | Press ← or → to navigate | "
            "Press SPACE to switch auto/manual",
            25, SCREEN_HEIGHT - 40, arcade.color.BLACK, 15)
        count = 8
        lines = []

        for i in range(0, len(self.turn_output), count):
            morceau = self.turn_output[i: i + count]
            lines.append("  ".join(morceau))

        start = 25 + (len(lines) * 20)
        current = start
        for ligne in lines:
            arcade.draw_text(ligne, 25, current, arcade.color.BLACK, 13)
            current -= 30

import arcade
from .Simulation import Simulation

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Fly-In Simulation"
MARGIN = 100
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
        # self.maximize()
        self.sim = simulation
        self.chrono = 0.0
        self.speed = 1.0
        self.background_color = arcade.color.BEIGE

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

    def on_update(self, delta_time) -> None:
        self.chrono += delta_time

        if self.chrono >= self.speed:
            if not all(drone.is_delivered for drone in self.sim.drones):
                self.sim.play_turn()
                self.sim.turn_counter += 1
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
            text_size = max(9, r * 0.45)
            arcade.draw_circle_filled(x, y, r, color)

            arcade.draw_text(
                f"{len(zone.current_drones)}/{zone.max_drones}",
                x, y + r + 4,
                arcade.color.BLACK, max(8, text_size * 0.8),
                anchor_x='center', anchor_y='bottom'
            )


"""     def start_simulation(self) -> None:
        self.create_drones()
        self.plan_all_drone_paths()
        while not all(drone.is_delivered for drone in self.drones):
            self.turn_counter += 1
            self.play_turn()
            turn_output = [
            drone.format_output() for drone in self.drones
            if drone.format_output()]
            if turn_output:
                print(f"Turn {self.turn_counter}:")
                for output in turn_output:
                    print(f"  {output}")

        print(f"Simulation done in: {self.turn_counter} turn(s)")
        """

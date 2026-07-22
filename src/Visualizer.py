import arcade
from .Simulation import Simulation

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
SCREEN_TITLE = "Test Arcade 3.0 - Balle, Ligne et Souris"


class Visualizer(arcade.Window):
    def __init__(self, simulation: Simulation):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.sim = simulation
        self.chrono = 0.0
        self.speed = 1.0
        self.margin = 50
        self.dim = self.sim.map.get_map_size()
        self.width = self.dim["max_x"] - self.dim["min_x"]
        self.height = self.dim["max_y"] - self.dim["min_y"]
        self.ratio: int = min(
            ((SCREEN_WIDTH - 2 * self.margin)
             // self.width if self.width > 0 else 1),
            ((SCREEN_HEIGHT - 2 * self.margin)
             // self.height if self.height > 0 else 1))

        self.sim.create_drones()
        for drone in self.sim.drones:
            self.sim.map_zone.start.current_drones.append(drone)
        self.sim.plan_all_drone_paths()

    def on_update(self, delta_time):
        self.chrono += delta_time

        if self.chrono >= self.speed:
            if not all(drone.is_delivered for drone in self.sim.drones):
                self.sim.play_turn()
                self.sim.turn_counter += 1
            self.chrono = 0.0

    def on_draw(self):
        self.clear()

        for zone in (list(self.sim.map.hubs.values())
                     + [self.sim.map.start, self.sim.map.end]):
            arcade.draw_circle_filled(
                center_x=((zone.x - self.dim["min_x"])
                          * self.ratio + self.margin),
                center_y=((zone.y - self.dim["min_y"])
                          * self.ratio + self.margin),
                radius=10,
                color=arcade.color.BLUE
            )

"""     def start_simulation(self) -> None:
        self.create_drones()
        self.plan_all_drone_paths()
        while not all(drone.is_delivered for drone in self.drones):
            self.turn_counter += 1
            self.play_turn()
            turn_output = [drone.format_output() for drone in self.drones if drone.format_output()]
            if turn_output:
                print(f"Turn {self.turn_counter}:")
                for output in turn_output:
                    print(f"  {output}")

        print(f"Simulation done in: {self.turn_counter} turn(s)") """
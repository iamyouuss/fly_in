from Drone import Drone
from Map import Map


class Simulation:
    def __init__(self, map_zone: Map) -> None:
        self.map_zone: Map = map_zone
        self.drones: list[Drone] = []

    def create_drones(self) -> None:
        for i in range(1, self.map_zone.nb_of_drones + 1):
            drone = Drone(i, self.map_zone.start)
            self.drones.append(drone)

    def start_simulation(self) -> None:
        self.create_drones()

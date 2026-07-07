from .Drone import Drone
from .Map import Map, Zone, Zone_Type


class Simulation:
    """Represents the simulation environment for drone navigation."""
    def __init__(self, map_zone: Map) -> None:
        self.map_zone: Map = map_zone
        self.drones: list[Drone] = []
        self.traffic_load: dict[Zone, int] = {}
        self.turns: int = 0


    def create_drones(self) -> None:
        """Creates the drones for the simulation."""
        for i in range(1, self.map_zone.nb_of_drones + 1):
            drone = Drone(i, self.map_zone.start)
            self.drones.append(drone)

    def play_turn(self):
        ...

    def get_final_path(self, path: dict[Zone, Zone]) -> list[Zone]:
        """
        Reconstructs the final path from the start to the end zone.

        Args:
            path (dict[Zone, Zone]): A dictionary mapping each zone to its predecessor in the path.

        Returns:
            list[Zone]: The final path from the start to the end zone.
        """
        final_path: list[Zone] = []
        if self.map_zone.end not in path:
            return final_path
        current = self.map_zone.end
        final_path.append(current)
        while current != self.map_zone.start:
            current = path[current]
            final_path.append(current)
        final_path.reverse()
        return final_path

    def build_path(self) -> list[Zone]:
        """
        Builds the optimal path for a drone to navigate from the start to the end zone.

        Returns:
            list[Zone]: The optimal path from the start to the end zone.
        """
        distances: dict[Zone, float] = {self.map_zone.start: 0,
                                        self.map_zone.end: float('inf')}
        for hub in self.map_zone.hubs.values():
            distances[hub] = float('inf')
        path: dict[Zone, Zone] = {}
        to_visit = [self.map_zone.start, self.map_zone.end] + list(self.map_zone.hubs.values())

        while to_visit:
            current = min(to_visit, key=lambda z: (distances[z], 0 if z.zone_type == Zone_Type.PRIORITY else 1))
            to_visit.remove(current)
            neighbors = self.map_zone.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in to_visit:
                    continue
                if neighbor.zone_type == Zone_Type.BLOCKED:
                    continue
                penality = self.traffic_load.get(neighbor, 0) * 2
                cost = distances[current] + neighbor.movement_cost + penality
                if cost < distances[neighbor]:
                    distances[neighbor] = cost
                    path[neighbor] = current
        return self.get_final_path(path)
    
    def plan_all_drone_paths(self):
        """Plans the paths for all drones in the simulation."""
        for hub in self.map_zone.hubs.values():
            self.traffic_load[hub] = 0

        for drone in self.drones:
            drone.path = self.build_path()
            for zone in drone.path:
                if zone != self.map_zone.start and zone != self.map_zone.end:
                    self.traffic_load[zone] += 1

    def start_simulation(self) -> None:
        """Starts the simulation."""
        self.create_drones()
        self.plan_all_drone_paths()
        while all(not drone.is_delivered for drone in self.drones):
            self.play_turn()
        """ self.map_zone.display_info()
        for drone in self.drones:
            print(drone) """

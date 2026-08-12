from .Map import Map, Zone, Zone_Type, Drone


class Simulation:
    """Represents the simulation environment for drone navigation."""
    def __init__(self, map: Map) -> None:
        self.map: Map = map
        self.drones: list[Drone] = []
        self.traffic_load: dict[Zone, int] = {}
        self.turn_counter: int = 0
        self.max_turns: int = 50
        self.output: str = ""
        self.sim_done: bool = False

    def create_drones(self) -> None:
        """Creates the drones for the simulation."""
        for i in range(1, self.map.nb_of_drones + 1):
            drone = Drone(i, self.map.start)
            self.drones.append(drone)
            self.map.start.current_drones.append(drone)

    def play_turn(self) -> None:
        """Plays a single turn of the simulation."""
        for drone in self.drones:
            if drone.is_delivered:
                continue
            if drone.turns_in_transit > 0:
                drone.turns_in_transit -= 1
                continue

            if drone.current_connection and drone.turns_in_transit == 0:
                destination = drone.path[0]
                drone.current_connection.current_drones.remove(drone)
                drone.current_connection = None
                drone.current_zone = destination
                destination.current_drones.append(drone)
                drone.path.remove(destination)
                if destination == self.map.end:
                    drone.is_delivered = True
                continue

            if not drone.current_connection and drone.path:
                destination = drone.path[0]
                assert drone.current_zone is not None
                connection = self.map.get_connection(
                    drone.current_zone, destination)
                assert connection is not None
                if len(destination.current_drones) < destination.max_drones:
                    if (destination.zone_type == Zone_Type.RESTRICTED
                       and len(connection.current_drones
                               ) < connection.max_link_capacity):
                        drone.current_zone.current_drones.remove(drone)
                        drone.current_zone = None
                        drone.current_connection = connection
                        connection.current_drones.append(drone)
                        drone.turns_in_transit = 1
                    else:
                        drone.current_zone.current_drones.remove(drone)
                        drone.current_zone = destination
                        destination.current_drones.append(drone)
                        drone.path.remove(destination)
                        if destination == self.map.end:
                            drone.is_delivered = True

    def get_final_path(self, path: dict[Zone, Zone]) -> list[Zone]:
        """
        Reconstructs the final path from the start to the end zone.

        Args:
            path (dict[Zone, Zone]):
            A dictionary mapping each zone to its predecessor in the path.

        Returns:
            list[Zone]: The final path from the start to the end zone.
        """
        final_path: list[Zone] = []
        if self.map.end not in path:
            return final_path
        current = self.map.end
        final_path.append(current)
        while current != self.map.start:
            current = path[current]
            final_path.append(current)
        final_path.reverse()
        final_path.remove(self.map.start)
        return final_path

    def build_path(self) -> list[Zone]:
        """
        Builds the optimal path for a drone to navigate
        from the start to the end zone.

        Returns:
            list[Zone]: The optimal path from the start to the end zone.
        """
        distances: dict[Zone, float] = {self.map.start: 0,
                                        self.map.end: float('inf')}
        for hub in self.map.hubs.values():
            distances[hub] = float('inf')
        to_visit = self.map.zones.copy()
        path: dict[Zone, Zone] = {}

        while to_visit:
            current = min(
                to_visit, key=lambda z: (distances[z],
                                         0 if z.zone_type == Zone_Type.PRIORITY
                                         else 1))
            to_visit.remove(current)
            neighbors = self.map.get_neighbors(current)
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

    def plan_all_drone_paths(self) -> None:
        """Plans the paths for all drones in the simulation."""
        for hub in self.map.hubs.values():
            self.traffic_load[hub] = 0

        for drone in self.drones:
            path = self.build_path()
            if not path:
                raise ValueError("Could not find path")
            drone.path = path
            for zone in drone.path:
                if zone != self.map.start and zone != self.map.end:
                    self.traffic_load[zone] += 1

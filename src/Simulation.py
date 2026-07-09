from .Map import Connection, Map, Zone, Zone_Type, Drone

class Simulation:
    """Represents the simulation environment for drone navigation."""
    def __init__(self, map_zone: Map) -> None:
        self.map_zone: Map = map_zone
        self.drones: list[Drone] = []
        self.traffic_load: dict[Zone, int] = {}
        self.turn_counter: int = 0

    def create_drones(self) -> None:
        """Creates the drones for the simulation."""
        for i in range(1, self.map_zone.nb_of_drones + 1):
            drone = Drone(i, self.map_zone.start)
            self.drones.append(drone)
            self.map_zone.start.current_drones.append(drone)

    def play_turn(self) -> None:

        for drone in self.drones:
            if drone.is_delivered:
                continue
            if drone.turns_in_transit > 0:
                drone.turns_in_transit -= 1
            if drone.current_connection and drone.turns_in_transit == 0:
                destination = drone.path[0]

                drone.current_connection.current_drones.remove(drone)
                drone.current_connection = None
                
                drone.current_zone = destination
                # destination.current_drones.append(drone)
                drone.path.remove(destination)
                if destination == self.map_zone.end:
                    drone.is_delivered = True
                continue
            if not drone.current_connection and drone.path:
                destination = drone.path[0]
                connection = self.map_zone.get_connection(drone.current_zone, destination)

                if len(destination.current_drones) < destination.max_drones:

                    if destination.zone_type == Zone_Type.RESTRICTED:
                        # if len(connection.current_drones) < connection.max_link_capacity:
                        drone.current_zone.current_drones.remove(drone)
                        drone.current_zone = None
                        
                        drone.current_connection = connection
                        connection.current_drones.append(drone)                                
                        drone.turns_in_transit = 1

                        destination.current_drones.append(drone)

                    else:
                        # if len(connection.current_drones) < connection.max_link_capacity:
                        drone.current_zone.current_drones.remove(drone)

                        drone.current_zone = destination
                        destination.current_drones.append(drone)

                        drone.path.remove(destination)
                        if destination == self.map_zone.end:
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
        if self.map_zone.end not in path:
            return final_path
        current = self.map_zone.end
        final_path.append(current)
        while current != self.map_zone.start:
            current = path[current]
            final_path.append(current)
        final_path.reverse()
        final_path.remove(self.map_zone.start)
        return final_path

    def build_path(self) -> list[Zone]:
        """
        Builds the optimal path for a drone to navigate
        from the start to the end zone.

        Returns:
            list[Zone]: The optimal path from the start to the end zone.
        """
        distances: dict[Zone, float] = {self.map_zone.start: 0,
                                        self.map_zone.end: float('inf')}
        for hub in self.map_zone.hubs.values():
            distances[hub] = float('inf')
        path: dict[Zone, Zone] = {}
        to_visit = [self.map_zone.start,
                    self.map_zone.end] + list(self.map_zone.hubs.values())

        while to_visit:
            current = min(
                to_visit, key=lambda z: (distances[z],
                                         0 if z.zone_type == Zone_Type.PRIORITY
                                         else 1))
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
        """for drone in self.drones:
            p = [zone.name for zone in drone.path]
            print(p) """
        while not all(drone.is_delivered for drone in self.drones) and self.turn_counter < 100:
            self.turn_counter += 1
            self.play_turn()
            turn_output = [drone.format_output() for drone in self.drones if drone.format_output()]
            if turn_output:
                print(f"Turn {self.turn_counter}:")
                for output in turn_output:
                    print(f"  {output}")
            
        print(f"Simulation done in: {self.turn_counter} turn(s)")


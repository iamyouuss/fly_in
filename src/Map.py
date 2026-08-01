from enum import Enum
import random
import arcade


class Zone_Type(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:
    def __init__(self, name: str, x: int, y: int,
                 max_drones: int = 1, zone_type: str = "normal",
                 color: str = "grey") -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.max_drones: int = max_drones
        self.zone_type: Zone_Type = Zone_Type(zone_type)
        self.color: str = color
        self.movement_cost: int = 2 if zone_type == "restricted" else 1
        self.current_drones: list[Drone] = []


class Drone:
    def __init__(self, drone_id: int, current_zone: Zone) -> None:
        self.drone_id: int = drone_id
        self.path: list[Zone] = []
        self.current_zone: Zone | None = current_zone
        self.current_connection: Connection | None = None
        self.turns_in_transit: int = 0
        self.message: str = ""
        self.is_delivered: bool = False
        characters = [
            "src/img/beige.png",
            "src/img/green.png",
            "src/img/yellow.png",
            "src/img/purple.png",
            "src/img/pink.png"
        ]
        self.img = arcade.load_texture(random.choice(characters))

    def __repr__(self) -> str:
        return f"D{self.drone_id}"

    def format_output(self) -> str:
        msg = ""
        if self.current_connection is not None:
            msg = (f"{self.current_connection.hub_a.name}-{self}-"
                   f"{self.current_connection.hub_b.name}")
        elif self.current_zone is not None:
            msg = f"{self}-{self.current_zone.name}"
        if msg == self.message:
            return ""
        self.message = msg
        return msg


class Connection:
    def __init__(self, hub_a: Zone, hub_b: Zone, max_link_capacity: int = 1
                 ) -> None:
        self.hub_a: Zone = hub_a
        self.hub_b: Zone = hub_b
        self.max_link_capacity: int = max_link_capacity
        self.current_drones: list[Drone] = []


class Map:
    def __init__(self, number_of_drones: int, start: Zone,
                 hubs: dict[str, Zone], end: Zone,
                 connections: list[Connection]) -> None:
        self.nb_of_drones: int = number_of_drones
        self.start: Zone = start
        self.hubs: dict[str, Zone] = hubs
        self.end: Zone = end
        self.zones: list[Zone] = [start, end] + list(hubs.values())
        self.connection_list: dict[
            str, list[Connection]] = self._build_connections(connections)

    def _build_connections(self, connections: list[Connection]
                           ) -> dict[str, list[Connection]]:
        connection_list: dict[str, list[Connection]] = {}
        zone_names = [self.start.name, self.end.name] + list(self.hubs.keys())
        for name in zone_names:
            connection_list[name] = []

        for c in connections:
            connection_list[c.hub_a.name].append(c)
            connection_list[c.hub_b.name].append(c)
        return connection_list

    def get_neighbors(self, zone: Zone) -> list[Zone]:
        """
        Return the list of neighboring zones for the given zone.

        Args:
            zone (Zone): The zone for which to find neighbors.

        Returns:
            list[Zone]: A list of neighboring zones.
        """
        return [c.hub_a if c.hub_a is not zone
                else c.hub_b for c in self.connection_list[zone.name]]

    def get_connection(self, zone_a: Zone, zone_b: Zone) -> Connection | None:
        """
        Return the connection between two zones.

        Args:
            zone_a (Zone): The first zone.
            zone_b (Zone): The second zone.

        Returns:
            Connection | None: The connection between the two zones,
            or None if no such connection exists.
        """
        for c in self.connection_list[zone_a.name]:
            if c.hub_a is zone_b or c.hub_b is zone_b:
                return c
        return None

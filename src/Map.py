from enum import Enum


class Zone_Type(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Zone:
    def __init__(self, name: str, x: int, y: int,
                 max_drones: int = 1, zone_type: str = "normal",
                 color: str | None = None) -> None:
        self.name: str = name
        self.coordinates: tuple[int, int] = (x, y)
        self.max_drones: int = max_drones
        self.zone_type: Zone_Type = Zone_Type(zone_type)
        self.color: str | None = color


class Connection:
    def __init__(self, hub_a: Zone, hub_b: Zone, max_link_capacity: int = 1
                 ) -> None:
        self.hub_a: Zone = hub_a
        self.hub_b: Zone = hub_b
        self.max_link_capacity: int = max_link_capacity

    def __repr__(self) -> str:
        return f"{self.hub_a}-{self.hub_b}"


class Map:
    def __init__(self, number_of_drones: int, start: Zone,
                 hubs: dict[str, Zone], end: Zone,
                 connections: list[Connection]) -> None:
        self.nb_of_drones: int = number_of_drones
        self.start: Zone = start
        self.hubs: dict[str, Zone] = hubs
        self.end: Zone = end
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

    def display_info(self) -> None:
        """Print a summary of the parsed map.

        Shows the number of drones, the start and end zones, every
        regular hub with its metadata, and every connection with its
        capacity.
        """
        print(f"Drones: {self.nb_of_drones}")
        print(f"Start: {self.start.name} {self.start.coordinates}")
        print(f"End: {self.end.name} {self.end.coordinates}")

        print(f"Hubs ({len(self.hubs)}):")
        for hub in self.hubs.values():
            print(f"  - {hub.name} {hub.coordinates} "
                f"type={hub.zone_type.value} "
                f"max_drones={hub.max_drones} "
                f"color={hub.color}")

        print(f"Connections ({len(self.connection_list)}):")
        for connection in self.connection_list:
            print(f"{connection}:")
            for c in self.connection_list[connection]:
                print(f" - {c.hub_a.name} to {c.hub_b.name} "
                    f"max_link_capacity={c.max_link_capacity}")
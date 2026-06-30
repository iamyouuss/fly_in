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

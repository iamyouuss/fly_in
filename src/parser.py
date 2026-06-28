from typing import Any

from .models import Connection, Zone, Map


class Parser:
    def __init__(self) -> None:
        self.start: Zone | None = None
        self.end: Zone | None = None
        self.hubs: dict[str, Zone] = {}
        self.nb_drones: int = 0
        self.connections: list[Connection] = []

    def parse_metadata(self, metadata_str: str) -> dict[str, Any]:
        metadata: dict[str, Any] = {}
        data = metadata_str.replace("]", '').strip().split()
        for line in data:
            key, value = line.split("=")
            if key == "max_drones":
                metadata["max_drones"] = int(value)
            if key == "zone":
                metadata["zone_type"] = value
            if key == "color":
                metadata["color"] = value
        return metadata

    def init_hub(self, prefix: str, content: str) -> None:
        parts = content.split("[")
        data = parts[0].split()
        if len(data) != 3:
            raise ValueError(
                f"Invalid number of arguments for line '{content}'")
        name = data[0]
        x = int(data[1])
        y = int(data[2])

        if len(parts) > 1:
            metadata = self.parse_metadata(parts[1])
            hub = Zone(name, x, y, **metadata)
        else:
            hub = Zone(name, x, y)

        if prefix == "start_hub":
            self.start = hub
        elif prefix == "end_hub":
            self.end = hub
        else:
            self.hubs[hub.name] = hub

    def _get_zone_by_name(self, name: str) -> Zone:
        if self.start and self.start.name == name:
            return self.start
        if self.end and self.end.name == name:
            return self.end
        if name in self.hubs:
            return self.hubs[name]
        raise ValueError(f"[Error] Zone '{name}' not found !")

    def init_connection(self, connection_str: str) -> None:
        parts = connection_str.split("[")
        a, b = [h.strip() for h in parts[0].split("-")]
        hub_a = self._get_zone_by_name(a)
        hub_b = self._get_zone_by_name(b)
        if len(parts) > 1:
            metadata = parts[1]
            metadata = metadata.replace("]", "")
            key, value = metadata.split("=")
            if key == "max_link_capacity":
                max_link_capacity = int(value)
                self.connections.append(
                    Connection(hub_a, hub_b, max_link_capacity))
        else:
            self.connections.append(Connection(hub_a, hub_b))

    def parse(self, file_name: str) -> None:
        with open(file_name, "r") as f:
            for line in f:
                if line.startswith("#") or not line:
                    continue
                cutted_line = line.split(": ")
                if len(cutted_line) < 2:
                    continue
                prefix, content = [c.strip() for c in cutted_line]
                if prefix == "nb_drones":
                    self.nb_drones = int(content)
                elif prefix in ("start_hub", "end_hub", "hub"):
                    self.init_hub(prefix, content)
                elif prefix == "connection":
                    self.init_connection(content)

    def create_map(self) -> Map:
        if self.start is None or self.end is None:
            raise ValueError(
                "[Error] Failed to create Map: no start or end hub")
        if self.nb_drones < 1:
            raise ValueError(
                "[Error] Failed to create map: number of drone invalid")
        if not self.hubs:
            raise ValueError(
                "[Error] Failed to create Map: not enoug hub")
        if not self.connections:
            raise ValueError(
                "[Error] Failed to create Map: no connection between hubs")
        return Map(self.nb_drones, self.start, self.hubs, self.end,
                   self.connections)

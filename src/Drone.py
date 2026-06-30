from Map import Connection, Zone


class Drone:
    def __init__(self, drone_id: int, current_zone: Zone) -> None:
        self.drone_id: int = drone_id
        self.current_zone: Zone | None = current_zone
        self.current_connection: Connection | None = None
        self.turns_in_transit: int = 0
        self.is_delivered: bool = False

    def __repr__(self) -> str:
        return f"D{self.drone_id}"

    def format_output(self) -> str:
        if self.current_connection is not None:
            return f"{self}-{self.current_connection}"
        elif self.current_zone is not None:
            return f"{self}-{self.current_zone.name}"
        return ""

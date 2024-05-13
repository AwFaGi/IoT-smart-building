from .base_device import Valve, eprint


class Conditioner(Valve):
    def __init__(
            self,
            apartment: int,
            host_port: int,
            port: int
    ):
        super().__init__(
            apartment,
            "cond",
            host_port,
            port,
            {"off": self.turn_off, "on": self.turn_on}
        )

    def turn_off(self):
        eprint("Conditioner is disabled")

    def turn_on(self):
        eprint("Conditioner is enabled")

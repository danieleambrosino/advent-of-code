from typing import Protocol


class ClockDrivenDevice(Protocol):
    def update(self, cycle: int):
        ...


class Clock:
    cycle: int = 0
    devices: list[ClockDrivenDevice] = []

    def connect(self, circuit: ClockDrivenDevice):
        self.devices.append(circuit)

    def tick(self):
        self.cycle += 1
        for device in self.devices:
            device.update(self.cycle)


class CPU:
    clock: Clock
    x: int = 1

    def __init__(self, clock: Clock) -> None:
        self.clock = clock

    def exec(self, instruction: list[str]):
        match instruction:
            case "noop", :
                self.clock.tick()
            case "addx", value:
                self.clock.tick()
                self.clock.tick()
                self.x += int(value)
            case _: pass


class SignalStrengthSampler:
    cpu: CPU
    samples: list[int] = []

    def __init__(self, cpu: CPU) -> None:
        self.cpu = cpu

    def update(self, cycle: int):
        self.sample(cycle)

    def sample(self, cycle: int):
        if cycle in (20, 60, 100, 140, 180, 220):
            self.samples.append(cycle * self.cpu.x)


class CRT:
    cpu: CPU
    pixels: list[str] = []

    def __init__(self, cpu: CPU) -> None:
        self.cpu = cpu

    def update(self, cycle: int):
        self.draw(cycle)

    def draw(self, cycle: int):
        pixel = "#" if abs(self.cpu.x - ((cycle - 1) % 40)) <= 1 else "."
        self.pixels.append(pixel)
        if cycle % 40 == 0:
            self.pixels.append("\n")


def part_one(instructions: list[list[str]]) -> int:
    clock = Clock()
    cpu = CPU(clock)
    sampler = SignalStrengthSampler(cpu)
    clock.connect(sampler)
    for instruction in instructions:
        cpu.exec(instruction)
    return sum(sampler.samples)


def part_two(instructions: list[list[str]]) -> str:
    clock = Clock()
    cpu = CPU(clock)
    crt = CRT(cpu)
    clock.connect(crt)
    for instruction in instructions:
        cpu.exec(instruction)
    return "".join(crt.pixels)


def main():
    with open("input.txt", "r") as file:
        instructions = [l.strip().split() for l in file.readlines()]
    print(part_one(instructions))
    print(part_two(instructions))


if __name__ == "__main__":
    main()

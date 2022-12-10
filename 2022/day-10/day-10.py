from typing import Protocol


class ClockDrivenCircuit(Protocol):
    def update(self):
        ...


class Clock:
    cycle: int = 0
    circuits: list[ClockDrivenCircuit] = []

    def connect(self, circuit: ClockDrivenCircuit):
        self.circuits.append(circuit)

    def tick(self):
        self.cycle += 1
        for circuit in self.circuits:
            circuit.update()


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
    clock: Clock
    samples: list[int] = []

    def __init__(self, cpu: CPU, clock: Clock) -> None:
        self.cpu = cpu
        self.clock = clock

    def update(self):
        self.sample()

    def sample(self):
        if self.clock.cycle in (20, 60, 100, 140, 180, 220):
            self.samples.append(self.clock.cycle * self.cpu.x)


class CRT:
    cpu: CPU
    clock: Clock
    pixels: list[str] = []

    def __init__(self, cpu: CPU, clock: Clock) -> None:
        self.cpu = cpu
        self.clock = clock

    def update(self):
        self.draw()

    def draw(self):
        pixel = "#" if abs(
            self.cpu.x - ((self.clock.cycle - 1) % 40)) <= 1 else "."
        self.pixels.append(pixel)
        if not self.clock.cycle % 40:
            self.pixels.append("\n")


def part_one(instructions: list[list[str]]) -> int:
    clock = Clock()
    cpu = CPU(clock)
    sampler = SignalStrengthSampler(cpu, clock)
    clock.connect(sampler)
    for instruction in instructions:
        cpu.exec(instruction)
    return sum(sampler.samples)


def part_two(instructions: list[list[str]]) -> str:
    clock = Clock()
    cpu = CPU(clock)
    crt = CRT(cpu, clock)
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

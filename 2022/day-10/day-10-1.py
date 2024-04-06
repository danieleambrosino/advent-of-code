with open("input.txt", "r") as file:
    instructions = [l.strip().split() for l in file.readlines()]


class CPU:
    cycle: int = 0
    x: int = 1
    signal_strength: int = 0

    def exec(self, instruction: list[str]):
        match instruction:
            case "noop", :
                self.clock()
            case "addx", value:
                self.clock()
                self.clock()
                self.x += int(value)
            case _: pass

    def clock(self):
        self.cycle += 1
        if self.cycle in (20, 60, 100, 140, 180, 220):
            self.signal_strength += self.cycle * self.x


cpu = CPU()
for instruction in instructions:
    cpu.exec(instruction)
print(cpu.signal_strength)

with open("input.txt", "r") as file:
    instructions = [l.strip().split() for l in file.readlines()]


class CPU:
    cycle: int = 0
    x: int = 1

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
        pixel = "#" if abs(self.x - (self.cycle % 40)) <= 1 else "."
        print(pixel, end="" if (self.cycle % 40 != 39) else "\n")
        self.cycle += 1


cpu = CPU()
for instruction in instructions:
    cpu.exec(instruction)

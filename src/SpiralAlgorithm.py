def command(direction):
    match direction:
        case (1, 0):
            return "RIGHT"
        case (-1, 0):
            return "LEFT"
        case (0, 1):
            return "UP"
        case (0, -1):
            return "DOWN"


class SpiralAlgorithm:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.time = 0

    def step(self):
        direction = (1, 0)
        length = 1
        steps = 0
        while True:
            self.x += direction[0]
            self.y += direction[1]
            self.time += 1
            steps += 1
            yield command(direction)
            if steps == length:
                steps = 0
                match direction:
                    case (1, 0):
                        direction = (0, -1)
                    case (-1, 0):
                        direction = (0, 1)
                    case (0, 1):
                        direction = (1, 0)
                        length += 1
                    case (0, -1):
                        direction = (-1, 0)
                        length += 1 

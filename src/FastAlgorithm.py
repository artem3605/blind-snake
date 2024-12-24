def dist(p1, p2, not_visited):
    """
    This method computes the distance between two points.
    :param p1: a tuple (x1, y1)
    :param p2: a tuple (x2, y2)
    :param not_visited: the number of not visited cells
    :return: the distance between p1 and p2
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + not_visited * 2


def find_k(S_max, k_max=100):
    """
    This method finds the optimal value of k for the given S_max.
    :param S_max:
    :param k_max:
    :return:
    """
    l = 0
    r = k_max
    while r - l > 1:
        mid = (l + r) // 2
        alg = FastAlgorithm(S_max, mid)
        steps = list(alg.step())
        if steps[-1] == "ERROR":
            l = mid
        else:
            r = mid
    return r


class FastAlgorithm:
    """
    This class implements the algorithm for the blind snake problem. The method step() is a generator that yields the next move of the snake. 
    """

    def __init__(self, max_s=10 ** 6, k=26):
        self.max_s = max_s  # maximum value of s (s is the area of the field)
        self.k = k  # maximum value of k (k * s is the maximum number of steps)
        self.x = 1  # current horizontal position
        self.y = 1  # current vertical position
        self.time = 0  # current number of steps
        self.finished = False  # True if the snake has visited all possible cells

    def _find_all_divisors(self, cnt):
        """
        This method computes the number of divisors of all numbers from 1 to max_s.
        :return:
        """
        for i in range(1, self.max_s + 1):
            for j in range(i, self.max_s + 1, i):
                cnt[j] += 1

    def _move(self, direction, steps=1):
        """
        This method updates the position of the snake and yields the direction of the move.
        :param direction: the string "RIGHT", "LEFT", "UP" or "DOWN"
        :param steps: the number of steps
        :return: the string "RIGHT", "LEFT", "UP" or "DOWN"
        """
        for _ in range(steps):
            if direction == "RIGHT":
                self.x += 1
            elif direction == "LEFT":
                self.x -= 1
            elif direction == "UP":
                self.y += 1
            elif direction == "DOWN":
                self.y -= 1
            self.time += 1
            yield direction

    def position(self):
        """
        This method returns the current position of the snake.
        :return: a tuple (x, y)
        """
        return self.x, self.y

    def _reachable(self, p1, p2, not_visited, time):
        """
        This method returns True if the point p2 is reachable from the point p1.
        :param p1: a tuple (x1, y1)
        :param p2: a tuple (x2, y2)
        :param not_visited: the number of not visited cells
        :return: True if p2 is reachable from p1 in time
        """
        return dist(p1, p2, not_visited) + time <= p2[0] * p2[1] * self.k

    def step(self):
        """
        This method is a generator that yields the next move of the snake.
        :return: the string "RIGHT", "LEFT", "UP" or "DOWN"
        """
        moves_type = 0
        not_visited = 0
        ret = [1, 2]
        cnt = [0] * (self.max_s + 2)
        self._find_all_divisors(cnt)
        cnt_row = [1] + [0] * (self.max_s + 1)

        while not self.finished:
            if moves_type == 0:
                if not self._reachable((self.x, self.y), (ret[0], ret[1]), not_visited, self.time):
                    yield "ERROR"
                    break
                new_not_visited = not_visited + cnt[self.x + 1] - 1
                if not self._reachable((self.x + 1, self.y), (ret[0], ret[1]), new_not_visited,
                                       self.time + 1) or self.x == self.max_s:
                    moves_type = 1
                    continue
                not_visited = new_not_visited
                yield from self._move("RIGHT")
                cnt_row[self.y] += 1
            elif moves_type == 1:
                curr_s = self.x
                ret = [self.x + 1, 1]
                while self.x != 1 or self.y != curr_s + 1:
                    yield from self._move("UP")
                    to_left = self.x - cnt_row[self.y] - 1
                    to_right = max(0, curr_s // self.y - self.x)
                    cnt_row[self.y] = max(self.x, curr_s // self.y)
                    if to_left < to_right:
                        yield from self._move("LEFT", to_left)
                        yield from self._move("RIGHT", to_left + to_right)
                    else:
                        yield from self._move("RIGHT", to_right)
                        yield from self._move("LEFT", to_left + to_right)
                if curr_s == self.max_s:
                    self.finished = True
                not_visited = 0
                moves_type = 2
            elif moves_type == 2:
                if not self._reachable((self.x, self.y), (ret[0], ret[1]), not_visited, self.time):
                    yield "ERROR"
                    break
                new_not_visited = not_visited + cnt[self.y + 1] - 1
                if not self._reachable((self.x, self.y + 1), (ret[0], ret[1]), new_not_visited,
                                       self.time + 1) or self.y == self.max_s:
                    moves_type = 3
                    continue
                not_visited = new_not_visited
                yield from self._move("UP")
                cnt_row[self.y] += 1
            elif moves_type == 3:
                curr_s = self.y
                yield from self._move("RIGHT")
                cnt_row[self.y] = max(self.x, cnt_row[self.y])
                ret = [1, self.y + 1]
                while self.x != curr_s + 1 or self.y != 1:
                    yield from self._move("DOWN")
                    to_left = max(0, self.x - cnt_row[self.y] - 1)
                    to_right = max(0, curr_s // self.y - self.x)
                    if self.y == 1:
                        to_right += 1
                    cnt_row[self.y] = max(self.x, curr_s // self.y)
                    if to_left < to_right or self.y == 1:
                        yield from self._move("LEFT", to_left)
                        yield from self._move("RIGHT", to_left + to_right)
                    else:
                        yield from self._move("RIGHT", to_right)
                        yield from self._move("LEFT", to_left + to_right)
                not_visited = 0
                if curr_s == self.max_s:
                    self.finished = True
                moves_type = 0

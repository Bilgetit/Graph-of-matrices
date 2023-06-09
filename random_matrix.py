import numpy as np
import time
import random
from collections import deque
from typing import Optional
from tuple2matrix import tuple2matrix
from tuple_graph import get_edges


def random_matrices(
    n: int,
    p: int,
    times: int,
    matrix_list: Optional[np.ndarray] = [],
    matrix_end: Optional[int] = None,
) -> list[np.ndarray]:
    """generates random matrices."""

    # if matrix_end == None:
    #     # stop = 1
    #     stop = np.random.randint(1, 500)
    # else:
    #     stop = matrix_end
    # if matrix_list == []:
    matrix_list = []
    matrix_list.append(get_matrix(n, p))
    for i in range(1, times):
        matrix = get_matrix(n, p, starting_matrix=matrix_list[-1])
        matrix_list.append(matrix)
    return matrix_list


class Get_queue:
    """Class for using a breadth first search in order to retrieve queue. Modified from Search class."""

    def __init__(
        self,
        n: int = 3,
        p: int = 5,
        printing: bool = False,
        stop: Optional[int] = None,
        starting_matrix: Optional[np.ndarray] = None,
    ):
        self.n = n
        self.p = p
        self.s = set()
        self.printing = printing
        self.starting_matrix = starting_matrix
        self.edges = get_edges(n, p)
        self.count = 0
        self.quit = False
        self.stop = stop

    def worker(self) -> None:
        x = self.queue.popleft()

        Xes = np.matmul(x, self.edges)
        Xes %= self.p

        for Xe in Xes:
            Xe_tup = tuple(np.ravel(Xe))

            if Xe_tup not in self.s:
                self.s.add(Xe_tup)
                self.queue.append(Xe)
                self.count += 1

                if self.count % 100_000 == 0 and self.printing:
                    print(f"on number {self.count=}")

                if self.count >= self.stop:
                    self.quit = True
                    break

    def do_work(self) -> None:
        while self.queue:
            self.worker()

            if self.quit:
                break

    def main(self):
        if self.starting_matrix is not None:
            self.queue = deque([self.starting_matrix])
            x_tup = tuple(np.ravel(self.starting_matrix))
            self.s.add(x_tup)
            self.count += 1
            if self.count >= self.stop:
                self.quit = True
                return self.queue
        else:
            self.queue = deque(self.edges)

        self.do_work()

        return self.queue


def time_mat_bfs():
    t0 = time.time()
    my_matrix = get_matrix(n=2, p=101, stop=97, printing=False)
    t1 = time.time()
    print("\n")
    print(f" t_1 - t_0 = {t1-t0}")
    print(f"my_matrix = {my_matrix}")
    print("\n")


def get_matrix(
    n: int,
    p: int,
    stop: Optional[int] = None,
    starting_matrix: Optional[np.ndarray] = None,
    printing: bool = False,
):
    """Get pretty random matrix."""
    if stop == None:
        stop = np.random.randint(1, 300)

    instance = Get_queue(
        n=n, p=p, stop=stop, printing=printing, starting_matrix=starting_matrix
    )
    my_queue = instance.main()
    # m1_tup = my_queue.pop()
    m1_tup = random.choice(my_queue)
    m2_tup = random.choice(my_queue)

    # len_my_queue = len(my_queue)
    # if len_my_queue > 1:
    #     for _ in range(np.random.randint(1, len_my_queue)):
    #         m2_tup = my_queue.pop()
    # else:
    #     m2_tup = m1_tup

    m1 = tuple2matrix(m1_tup, n)
    m2 = tuple2matrix(m2_tup, n)
    m = np.matmul(m1, m2)
    m %= p
    return m


if __name__ == "__main__":
    time_mat_bfs()

"""This module describe detection count of craters on the surface."""
from typing import List


# Read from text file to list
def read_txtfile_to_list(filename: str) -> list:
    """
    (str) -> list.

    Read from text file to list of list of string
    """
    valid = True
    surface = list()
    with open(filename, 'r') as f:
        while True:
            line = f.readline().strip()
            if not line:
                break

            for i in line:
                if i not in ('0', '1'):
                    valid = False
                    break
            if not valid:
                break

            surface.append(line)
    return surface


# Recursive function of detect of crater
def scan_point(crater: list, x: int, y: int) -> None:
    """
    (list, int, int) -> None.

    Recursive function of detect of crater by point of surface
    """
    # if exists the same point in current crater => exit
    if (x, y) in crater:
        return

    # detection point: 1 or 0
    value = surface[y][x]
    if value == '0':
        return
    else:
        crater.append((x, y))

    # check left side
    if x > 0:
        scan_point(crater, x-1, y)

    # check right side
    if x < len(surface[y])-1:
        scan_point(crater, x+1, y)

    # check top side
    if y > 0:
        scan_point(crater, x, y-1)

    # check bottom side
    if y < len(surface)-1:
        scan_point(crater, x, y+1)


# Is exists the such point in craters which found in previous steps
def exists_point_in_craters(craters: list, x: int, y: int) -> bool:
    """
    (list, int, int) -> bool.

    Is exists the such point in craters which found in previous steps
    """
    result = False
    for crater_i in craters:
        if (x, y) in crater_i:
            result = True
            break
    return result


# Detect count of craters on the surface by matrix of surface
def calculate(matrix: list) -> int:
    """
    (list) -> int.

    Detect count of craters on the surface by matrix of surface
    """
    craters = list()  # type: List[tuple]
    for y, line in enumerate(matrix):
        for x, value in enumerate(line):
            if value == '1':
                # if exists the same point in another craters which found in previous steps
                if not exists_point_in_craters(craters, x, y):
                    # then we found a new crater
                    crater = list()  # type: List[tuple]
                    scan_point(crater, x, y)
                    craters.append(tuple(crater))
    # print(craters)
    return len(craters)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    surface = read_txtfile_to_list("input.txt")
    if len(surface) <= 0:
        print("Некорректные входые данные. Должны быть только нули и единицы.")
        exit(1)

    # print(surface)

    count_craters = calculate(surface)
    print(f"Количество кратеров равно {count_craters}.")

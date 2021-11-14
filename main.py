"""This module describe detection count of craters on the surface."""
from typing import List, Any, Callable
from functools import wraps
from datetime import datetime


class TypeValidationError(TypeError):
    """Calls when the coming object don't has the particular type."""

    def __str__(self) -> str:
        """
        (object) -> str.

        Override the print method of class TypeError.
        """
        return f"Ошибка: {type(self)}. {self.args[0]}"


class ValueValidationError(ValueError):
    """Calls when the value of object don't passed check on constraints by value."""

    message: str = ''
    line_error_number: int = 0

    def __init__(self, message: str, line_error_n: int = 0):
        """
        (object, str, int) -> object.

        Override the constructor method of class ValueError.
        """
        self.line_error_number = line_error_n
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        (object) -> str.

        Override the print method of class ValueError.
        """
        if self.line_error_number:
            str_number = f"Ошибка в строке {self.line_error_number}"
        else:
            str_number = "Ошибка"
        return f"{str_number}: {type(self)}. {self.args[0]} Не должно быть пробелов."


class ValueSizeValidationError(ValueValidationError):
    """Calls when the value of object don't passed check on constraints by size."""

    pass


class ValueEmptyError(ValueValidationError):
    """Calls when the value of object is empty."""

    pass


# Read from text file to list
def read_file_to_list(filename: str) -> list:
    """
    (str) -> list.

    Read from text file to list of list of string.
    """
    surface_data = list()
    with open(filename, 'r') as f:
        lines = list(f.readlines())
        for line in lines:
            surface_data .append(list(line.rstrip().replace('\n', '')))
    return surface_data


# Recursive function of detect of crater
def scan_point(crater: list, x: int, y: int) -> None:
    """
    (list, int, int) -> None.

    Recursive function of detect of crater by point of surface.
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

    Is exists the such point in craters which found in previous steps.
    """
    result = False
    for crater_i in craters:
        if (x, y) in crater_i:
            result = True
            break
    return result


def write_error_data(matrix: Any, message: str, line_error_number: int = 0) -> int:
    """
    (list) -> int.

    Write error data to text file.
    """
    date_postfix = datetime.now().strftime("%d%m%Y_%H_%M_%S")
    filename = f"file{date_postfix}.err"
    list_valid = isinstance(matrix, list)
    if list_valid:
        if len(matrix) <= 0:
            return -1
    try:
        with open(filename, 'w') as f:
            if list_valid:
                for n, line in enumerate(matrix, start=1):
                    f.write(''.join(line))
                    if n == line_error_number:
                        s = ''.join(' ' for _ in range(len(matrix)))
                        f.write(f"{s}<<<<< здесь ошибка: {message}")
                    f.write('\n')
            else:
                f.write(message)

    except OSError as ex:
        msg = f"Тип ошибки: {type(ex)}. Невозможно открыть файл {filename}."
        print(msg)
        log(msg)
        return -1
    else:
        return 0


def log(text: str) -> int:
    """
    (str) -> int.

    Logging text to logfile.
    """
    filename = "logfile.txt"
    result = -1
    try:
        with open(filename, 'a') as flog:
            flog.write(text+'\n')
    except FileExistsError as ex:
        msg = f"Тип ошибки: {type(ex)}. Файл {filename} не существует."
        print(msg)
        log(msg)
    except OSError as ex:
        msg = f"Тип ошибки: {type(ex)}. Невозможно открыть файл {filename}."
        print(msg)
        log(msg)
    else:
        result = 0
    return result


def decorator_check(func: Callable) -> Callable:
    """
    (callable) -> callable.

    Decorator of functions of detect count of craters for check input data of surface of craters.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            matrix: List[list]
            msg = "Параметр должен быть типа список списков."
            if not isinstance(args[0], list):
                # Параметр должен быть типа список.
                raise TypeValidationError(msg)

            matrix = list(args[0])
            # print(matrix)
            matrix_length = len(matrix)

            if matrix_length <= 0:
                raise ValueEmptyError("Присланный список пуст.", 0)

            for ns, line in enumerate(matrix, start=1):
                if not isinstance(line, list):
                    # Элементы списка также являются списком.
                    raise TypeValidationError(msg)

                if len(line) <= 0:
                    raise ValueEmptyError("Присланный список содержит пустые строки.", ns)

                for n, ii in enumerate(line):
                    if n >= matrix_length:
                        raise ValueValidationError("Присланный двумерный список - не прямоугольный.", ns)
                    if ii not in ('0', '1'):
                        raise ValueValidationError("В присланном двумерном списке присутствуют элементы которые не "
                                                   "являются нулем либо единицей.", ns)
        except TypeValidationError as ex:
            msg = ex.__str__()
            print(msg)
            log(msg)
            write_error_data(args[0], msg)
            result = -1

        except (ValueSizeValidationError, ValueValidationError, ValueEmptyError) as ex:
            msg = ex.__str__()
            print(msg)
            log(msg)
            write_error_data(list(args[0]), ex.message, ex.line_error_number)
            result = -1
        else:
            result = func(*args, **kwargs)
        return result
    return wrapper


@decorator_check
def calculate(matrix: list) -> int:
    """
    (list) -> int.

    Detect count of craters on the surface by matrix of surface.
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


# Point to start
if __name__ == '__main__':
    surface = read_file_to_list("input.txt")

    # print(surface)
    count_craters = calculate(surface)
    if count_craters > 0:
        print(f"Количество кратеров равно {count_craters}.")
    else:
        print("Не удалось посчитать количество кратеров :( ...")

import math

def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    if len(numbers) == 0:
        return 0
    return total/len(numbers)

def add(a: int, b: int) -> int:
    """
    Add two numbers.

    Args:
        a (int): The first number to add.
        b (int): The second number to add.

    Returns:
        int: The sum of a and b.
    """
    return a + b

class Processor:
    def process(self,data):
        """
        Process data

        Args:
            self (TYPE): the instance of the class
            data (TYPE): the data to be processed

        Returns:
            TYPE: the processed data
        """
        for item in data:
            if item is None:
                continue
            print(item)

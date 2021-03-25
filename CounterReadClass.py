class CounterRead:
    def __init__(self, file):
        temp_file = open(file, 'r')
        self.file = temp_file.read().split('\n')
        self.index = 0
        temp_file.close()

    def __iter__(self):
        return CounterReadIter(self.file)

    def __repr__(self):
        return self.file


class CounterReadIter:
    def __init__(self, c_read):
        """

        :type c_read: list
        """
        self.iterable = c_read

        self.index = 0

    def __next__(self):
        if self.hasnext():
            next_item = self.iterable[self.index]
            self.index += 1
            return next_item
        raise StopIteration

    def hasnext(self):
        return self.index < len(self.iterable)


if __name__ == '__main__':
    read = CounterRead
    for index, line in enumerate(read('counters.txt')):
        print(f'counter{index + 1}, {line}')

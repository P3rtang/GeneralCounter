from .Counter import Counter


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

    def get_list(self):
        # list to store counter objects in
        counter_list = []
        # making counter object from the read line and storing in counter_list
        for line in self.file:
            # individual characteristics of counter object are separated by spaces in the txt file
            item = line.split(' ')
            # check whether the read line has actual text in it
            # because the last line of the txt file is an empty string at all times
            if item[0]:
                # counter needs 7 arguments and they are stored in multiple objects
                counter_list.append(Counter(*item))

        return counter_list


class CounterReadIter:
    def __init__(self, c_read):
        """

        :type c_read: list
        """
        self.iterable = c_read

        self.index = 0

    def __next__(self):
        if self.has_next():
            next_item = self.iterable[self.index]
            self.index += 1
            return next_item
        raise StopIteration

    def has_next(self):
        return self.index < len(self.iterable)


if __name__ == '__main__':
    read = CounterRead('./saves/counters.txt')
    for index, l in enumerate(read):
        print(f'counter{index + 1}, {l}')

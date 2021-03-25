from CounterReadClass import CounterRead


class Counter:
    def __init__(self, id, name, value, jump=1):
        self.id = int(id)
        self.value = int(value)
        self.name = name.replace('_', ' ')
        self.jump = int(jump)

    def __add__(self, other):
        self.value += other

    def __sub__(self, other):
        self.value -= other

    def __set__(self, instance, value):
        self.value = value

    def __repr__(self):
        return self.id, self.name, self.value


if __name__ == '__main__':
    counters = CounterRead('counters.txt')
    counterList = []
    for line in counters:
        item = line.split(' ')
        counterList.append(Counter(*item))
    print(counterList[0].value)

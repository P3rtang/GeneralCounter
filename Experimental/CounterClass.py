from CounterReadClass import CounterRead


class Counter:
    def __init__(self, c_id, name, value, jump=1, method_id=0, odds=8192, active_time=0):
        self.id = int(c_id)
        self.value = int(value)
        self.name = name.replace('_', ' ')
        self.jump = int(jump)
        self.method_id = int(method_id)
        if self.method_id == 0:
            self.odds = float(odds)
            self.cur_step = float(self.value)
        elif self.method_id == 1:
            self.odds = float(odds)
        elif self.method_id == 2:
            self.odds = 1
        elif self.method_id == 3:
            self.odds = 1
        self.active_time = float(active_time)

    def __add__(self, other):
        self.value += other

    def __sub__(self, other):
        self.value -= other

    def __set__(self, instance, value):
        self.value = value

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.value}, {self.jump}, {self.method_id}, {self.odds}'


if __name__ == '__main__':
    counters = CounterRead('./saves/counters.txt')
    counterList = []
    for line in counters:
        item = line.split(' ')
        counterList.append(Counter(*item))
    print(counterList[0].value)

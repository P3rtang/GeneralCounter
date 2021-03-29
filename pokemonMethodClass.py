class Method:
    def __init__(self, counter_id, name, count, _step_size, method_id, odds=8192):
        methods = {
            '0': 'Encounters',
            '1': 'DexNav',
            '2': 'SOS'
        }
        self.counter_id = counter_id
        self.counter_name = name.replace('_', ' ')
        self.method_name = methods[method_id]
        self.count = count
        self.method_id = int(method_id)
        if self.method_id == 0:
            self.odds = float(odds)
            self.cur_step = float(count)
        elif self.method_id == 1:
            self.odds = float(odds)
        elif self.method_id == 2:
            self.odds = float(odds)
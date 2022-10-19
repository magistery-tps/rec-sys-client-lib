class identity:
    def __init__(self, desc=''): self._desc = desc

    @property
    def desc(self): return self._desc

    def closure(self): return lambda it: it


class gte:
    def __init__(self, value): self._value = value

    @property
    def desc(self): return f' (R>={self._value})'

    def closure(self): return lambda it: 1 if it >= self._value else 0


class between:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    @property
    def desc(self): return f'({self.begin},{self.end})'

    def closure(self): return lambda it: 1 if self.begin <= it <= self.end else 0 


class mapping:
    def __init__(self, map): self.map  = map

    @property
    def desc(self): return f'{self.map}'

    def closure(self): return lambda it: self.map[it]


class sequence:
    def __init__(self, values): 
        self.map  = {v: i for i, v in enumerate(values)}

    @property
    def desc(self): return f'{self.map}'

    def closure(self): return lambda it: self.map[it]


class round_sequence:
    def __init__(self, values):
        self.seq = sequence(values).closure()
        self.min_value = values[0]
        self.max_value = values[-1]

    @property
    def desc(self): return f'round-seq'


    def perform(self, it):
        value = round(it)

        if value < self.min_value:
            return self.min_value
        elif value > self.max_value:
            return self.max_value
        else:
            return value

    def closure(self):
        return lambda it: self.seq(self.perform(it))

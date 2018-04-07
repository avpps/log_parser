class LogParser(object):

    _raw = None
    _valid = None
    _parse_details = None
    _parsed = None

    def __init__(self, raw):
        self._raw = raw
        self.parse()

    @property
    def raw(self):
        return self._raw

    @property
    def valid(self):
        return self._valid

    @property
    def parse_details(self):
        return self._parse_details

    @property
    def parsed(self):
        return self._parsed

    def parse(self):

        parsing = Parsing()
        stack = []

        dict_value = []
        other_value = ''

        OBJ_START = ('{', '[', '(')
        OBJ_END = ('}', ']', ')')
        OTHER_START = ('"', "'", '<')
        OTHER_END = ('"', "'", '>')

        inside = False

        def start_end_eq(i):
            """if first and last mark are correct pair"""
            start_index = OTHER_START.index(other_value[0])
            end_index = OTHER_END.index(i)
            return start_index == end_index

        def next_is_obj(n, i):
            """if next """
            return any((
                self._raw[n+3] in OBJ_START,
                self._raw[n+1] in OBJ_END
            ))

        for n, i in enumerate(self._raw):
            if i in OBJ_START and not inside:
                # Start list or dict:
                stack.append(parsing.start_iter(i))
            elif i in OBJ_END and not inside:
                # End list or dict:
                parsing.end_last(i)
                stack.pop()
            elif i in OTHER_START or i.isdigit():
                # Start collect other value.
                # Others are: strings, tags and numbers
                # TODO: float numbers!!
                other_value.join(i)
                inside = True
            elif any((
                 i in OTHER_END and start_end_eq(i),
                 i.isdigit() and next_is_obj(n, i)
            )):
                # End collecting other value
                # and save it to list or dict.
                # TODO: what if is in dict?! Have to collect 'key: value' pair
                parsing.update_last(other_value)
                other_value = ''
            else:
                # Extend other value if not match any of above criteria
                other_value += i

        import pdb
        pdb.set_trace()

        self._valid = False
        self._parse_details = 'Not implemented yet'
        self._parsed = self._raw


class Tag(str):

    def __init__(self):
        super().__init__()



class Parsing(object):

    final = []
    stack = []

    def __init__(self):
        self.stack.append(self.final)

    @ property
    def final(self):
        return self.final

    @property
    def current_type(self):
        return type(self.stack[-1])

    def _start_dict(self):
        n_dict = dict()
        self.stack[-1].append(n_dict)
        self.stack.append(n_dict)
        return dict

    def _start_list(self):
        n_list = list()
        self.stack[-1].append(n_list)
        self.stack.append(n_list)
        return list

    def start_iter(self, value):
        if value == '{':
            self._start_dict()
        elif value in ('[', '('):
            self._start_list()

    def update_last(self, value):
        if isinstance(self.stack[-1], list):
            self.stack[-1].append(value)
        elif isinstance(self.stack[-1], dict):
            self.stack[-1].update(value)

    def end_last(self, value):
        if value == ')':
            self.stack[-1] = tuple(self.stack[-1])
        self.stack.pop()


if __name__ == '__main__':
    PATHS = [
        '/home/piotr/Documents/temp/raw_flat.txt',
        '/home/piotr/Documents/temp/raw_str.txt',
    ]
    for path in PATHS:
        with open(path) as file:
            raw = ''.join(line for line in file)
            parsed = LogParser(raw)
            print(parsed.parsed)

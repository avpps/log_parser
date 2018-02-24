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
        self._valid = False
        self._parse_details = 'Not implemented yet'
        self._parsed = self._raw

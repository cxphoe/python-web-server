class Cookies:
    def __init__(self):
        self.dict = {}

    def __str__(self):
        return ''.join([
            'Set-Cookie: {}={}\r\n'.format(k, v) for k, v in self.dict.items()
        ])

    def set(self, k, v):
        self.dict[k] = v

    def get(self, k):
        return self.dict.get(k, None)

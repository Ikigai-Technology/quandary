class Scope(dict):
    def __init__(self, default={}, functions={}):
        super().__init__(default)
        self.functions = functions

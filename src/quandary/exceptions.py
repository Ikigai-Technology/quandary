class ExecutionError(Exception):
    def __init__(self, node):
        self.node = node

class AutoGPTError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class QueryExecutionError(AutoGPTError):
    def __init__(self, message: str):
        super().__init__(message)

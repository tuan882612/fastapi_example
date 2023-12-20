
class ConflictError(Exception):
    def __init__(self, msg: str, data: any = None) -> None:
        self.msg = msg
        self.data = data

class InternalError(Exception):
    def __init__(self, msg: str, data: any = None) -> None:
        self.msg = msg
        self.data = data
        
class NotFoundError(Exception):
    def __init__(self, msg: str, data: any = None) -> None:
        self.msg = msg
        self.data = data
from typing import Optional


class ApiError(Exception):

    def __init__(self,status: int, msg: str, error_list: list) -> None:
        self.status = status
        self.msg = msg
        self.error_list = error_list
    
    @classmethod
    def internal(cls, msg: str, error_list: Optional[list] = []):
        return cls(500, msg, error_list)
    
    @classmethod
    def forbidden(cls, msg: str, error_list: Optional[list] = []):
        return cls(403, msg, error_list)
    
    @classmethod
    def unauthorized(cls, msg: str, error_list: Optional[list] = []):
        return cls(401, msg, error_list)

    @classmethod
    def bad_request(cls, msg: str, error_list: Optional[list] = []):
        return cls(400, msg, error_list)
    
    


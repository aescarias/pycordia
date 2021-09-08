class QueryError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"{message} (error code {code})")

class GatewayError(QueryError):    
    pass

class ComponentError(Exception):
    pass
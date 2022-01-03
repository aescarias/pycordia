def determine_error(status: int, rs: dict):
    status_map = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: NotFound,
        405: MethodNotAllowed,
        429: TooManyRequests,
        502: GatewayUnavailable
    }

    if status in status_map:
        return status_map[status](rs)
    elif str(status).startswith("5"):
        return ServerError(rs)
    else:
        return HTTPError(rs)

class HTTPError(Exception):
    """General error raised by the HTTP client"""
    def __init__(self, data: dict):
        self.data = data 
        
        self.code = self.data["code"]
        self.errors = self.data.get("errors", {})
        self.message = self.data["message"]

        self.error_message = f"{self.message} (code {self.code})\n\n"

        for key, value in self._flatten_errors(self.errors).items():
            self.error_message += f"In '{key}':\n"

            for error in value:
                self.error_message += f"\t{error['message']} (code {error['code']})\n"

        super().__init__(self.error_message.strip())

    def _flatten_errors(self, errors, input_key: str = "") -> dict:
        items = []

        for key, value in errors.items():
            item_key = f"{input_key}{'.' * bool(input_key)}{key}"

            if isinstance(value, dict):
                try:
                    items.append(( item_key, value["_errors"] ))
                except KeyError:
                    items.extend(self._flatten_errors(value, item_key).items())
            else:
                items.append(( item_key, value ))

        return dict(items)


class BadRequest(HTTPError):
    """Raised when the client cannot understand a request (400)"""
    pass

class Unauthorized(HTTPError):
    """Raised when the client sends an invalid or empty token (401)"""
    pass

class Forbidden(HTTPError):
    """Raised when the client is not allowed access to a resource (403)"""
    pass

class NotFound(HTTPError):
    """Raised when the client requests a resource that is not found (404)"""
    pass

class MethodNotAllowed(HTTPError):
    """Raised when the client performs a request with an invalid method (405)"""
    pass

class TooManyRequests(HTTPError):
    """Raised when the client is ratelimited (429)"""
    pass

class GatewayUnavailable(HTTPError):
    """Raised when no gateway could process the client's request (502)"""
    pass

class ServerError(HTTPError):
    """Raised when the server encountered an error processing the client's request (5xx)"""
    pass 
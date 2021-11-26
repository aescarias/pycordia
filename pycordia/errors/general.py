class GatewayError(Exception):
    """General error raised by the gateway"""
    def __init__(self, code, message) -> None:
        extra = None

        # 4001 = Unknown opcode
        # 4002 = Decode error
        # 4007 = Invalid sequence
        # 4012 = Invalid API version
        if code in (4001, 4002, 4007, 4012):
            extra = "This is an internal error."
        # Not authenticated
        elif code == 4003:
            extra = "Please authenticate and try again."
        # Authentication error
        elif code == 4004:
            extra = "Make sure the token you provided is valid and has not expired."
        # Rate limited
        elif code == 4008:
            extra = "Please wait a few seconds, then try again."
        # Invalid intents
        elif code == 4013:
            extra = "Make sure you have provided a valid intent value."
        # Disallowed intents
        elif code == 4014:
            extra = "Make sure you have approved/enabled the use of the provided intents."
        
        super().__init__(f"{message} {extra} (error code {code})")


class MutuallyExclusiveError(Exception):
    """Raised when multiple mutually exclusive values are provided to a function"""
    def __init__(self, args: tuple, mutual_count: int) -> None:
        super().__init__(
            f"Only one of this group {args} "
            f"can be provided at a time, found {mutual_count}."    
        )

class ClientSetupError(Exception):
    """Raised when an initialized client is not found or is setup improperly"""
    def __init__(self, message=None):
        super().__init__(message or "No initialized client found")

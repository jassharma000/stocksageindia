from typing import Any, Optional

class StockSageException(Exception):

    def __init__(
        self,
        message: str,
        status_code : int =500,
        context: Optional[dict[str,Any]] = None,
    ):

        self.message = message
        self.status_code = status_code
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.message} | context={self.context}"


class DataFetchError(StockSageException):

    def __init__(self, message:str, symbol: str="", source:str=""):
        super().__init__(
            message= message,
            status_code=502,
            context={"symbol":symbol, "source":source},
        )

class SymbolNotFoundError(StockSageException):

    def __init__(self, symbol:str):
        super().__init__(
            message=f"Symbol '{symbol}' not found. Check if it is listed on NSE/BSE.",
            status_code=404,
            context={"symbol": symbol},
        )
    
class CacheError(StockSageException):

    def __init__(self, message:str, operation: str=""):
        super().__init__(
            message=message,
            status_code=500,
            context={"operation": operation},
        )

class NewsAPIError(StockSageException):

    def __init__(self, message:str, source:str=""):
        super().__init__(
            message=message,
            status_code=502,
            context={"source":source},
        )
    
class ModelInferenceError(StockSageException):

    def __init__(self, message: str, model_name: str = ""):
        super().__init__(
            message=message,
            status_code=500,
            context={"model_name": model_name},
        )


class InvalidIntervalError(StockSageException):

    def __init__(self, interval: str):
        super().__init__(
            message=f"Invalid interval '{interval}'. Allowed: 1m 5m 15m 1h 1d 1wk 1mo",
            status_code=422,
            context={"interval": interval},
        )
from typing import Sequence, Any


class LogMe:
    def __init__(self, expr: str) -> None:
        self.expr = expr

    def __enter__(self) -> None:
        print(f'INFO:  {self.expr}')

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            print(f'ERROR: {self.expr} - failed')
        else:
            print(f'INFO:  {self.expr} - done')


class AsyncIterator:
    def __init__(self, seq: Sequence) -> None:
        self.seq = seq

    def __aiter__(self) -> 'AsyncIterator':
        return self

    async def __anext__(self) -> Any:
        if self.seq:
            return self.seq.pop(0)
        raise StopAsyncIteration()

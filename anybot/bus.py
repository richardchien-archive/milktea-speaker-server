from collections import defaultdict
from typing import Callable, List, Any

from .utils import run_async_funcs


class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(set)

    def subscribe(self, event: str, func: Callable) -> None:
        self._subscribers[event].add(func)

    def unsubscribe(self, event: str, func: Callable) -> None:
        if func in self._subscribers[event]:
            self._subscribers[event].remove(func)

    def on(self, event: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.subscribe(event, func)
            return func

        return decorator

    async def emit(self, event: str, *args, **kwargs) -> List[Any]:
        results = []
        while True:
            results += await run_async_funcs(self._subscribers[event],
                                             *args, **kwargs)
            event, *sub_event = event.rsplit('.', maxsplit=1)
            if not sub_event:
                # the current event is the root event
                break
        return results

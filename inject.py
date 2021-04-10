from typing import Any, Callable, Dict, List, Tuple
import importlib

class InvocationRecord:
    'Record when the injected method was invoked.'
    def __init__(self, name: str, *args: Any, **kwargs: Any):
        'Initializes with name and arguments.'
        self._name = name
        self._arguments = args
        self._keywordArguments = kwargs
    @property
    def name(self) -> str:
        'The name of the method.'
        return self._name
    @property
    def arguments(self) -> Tuple[Any]:
        'The positional arguments.'
        return self._arguments
    @property
    def keywordArguments(self) -> Dict[str, Any]:
        'The keyword arguments.'
        return self._keywordArguments

class Recorder:
    'Represents a invocation recorder.'
    def __init__(self):
        'Initializes with empty records.'
        self._records = []
        self._stopped = False
    def record(self, record: InvocationRecord) -> None:
        'Adds a record to the collection.'
        if not self._stopped:
            self._records.append(record)
    def stop(self) -> None:
        'Stops this recorder from recording.'
        self._stopped = True
    def start(self) -> None:
        'Starts this recorder.'
        self._stopped = False
    @property
    def records(self) -> List[InvocationRecord]:
        'The records of this instance.'
        return self._records

class InjectedFunction:
    'Represents an injected function.'
    def __init__(self, function: Callable[..., Any], recorder: Recorder):
        'Initializes a new instance with function to inject and a recorder.'
        self._function = function
        self._recorder = recorder
    @property
    def function(self) -> Callable[..., Any]:
        'The original function.'
        return self._function
    def __call__(self, *args: Any, **kwargs: Any) -> None:
        'Called when this function was invoked.'
        self._recorder.record(InvocationRecord(
            self._function.__module__ + '.' + self._function.__qualname__, 
            *args, **kwargs))

def inject_functions(func_list: List[Tuple[str, str]], recorder: Recorder):
    'Inject the specific functions.'
    for module, funcname in func_list:
        try:
            mod = importlib.import_module(module)
        except ModuleNotFoundError:
            continue
        func = getattr(mod, funcname, None)
        if callable(func) and not isinstance(func, InjectedFunction):
            setattr(mod, funcname, InjectedFunction(func, recorder))

def uninject_functions(func_list: List[Tuple[str, str]], recorder: Recorder):
    'Uninject the specific functions.'
    recorder.stop()
    for module, funcname in func_list:
        try:
            mod = importlib.import_module(module)
        except ModuleNotFoundError:
            continue
        func = getattr(mod, funcname, None)
        if isinstance(func, InjectedFunction):
            setattr(mod, funcname, func.function)

hazardous_functions = [
    ("os", "system"),
    ("os", "execv"),
    ("os", "execl"),
    ("os", "execvp"),
    ("os", "execlp"),
    ("os", "execve"),
    ("os", "execle"),
    ("os", "execvpe"),
    ("os", "execlpe"),
    ("os", "spawnv"),
    ("os", "spawnl"),
    ("os", "spawnve"),
    ("os", "spawnle"),
    ("os", "remove"),
    ("os", "unlink"),
    ("os", "rmdir"),
    ("os", "chdir"),
    ("os", "mkdir"),
    ("os", "popen"),
    ("os", "startfile"),
    ("os", "_exit"),
    ("builtins", "open"),
    ("io", "open")
]
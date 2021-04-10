from io import BytesIO
from image import *
from inject import *
from result import InspectionResult, ResultLoadError
from typing import List, Optional, Tuple
from PIL import Image
import turtle, os

def get_inspection_name(file_name: str) -> str:
    'Gets the inspection name from the file name.'
    return os.path.splitext(file_name)[0]

class InspectionProperties:
    'Represents a inspection properties.'
    def __init__(self, directory: str, files: List[str]):
        'Initializes with a directory and a sequence of included files (with suffix).'
        self._inspectionFiles = files
        self._directory = directory
    @property
    def inspectionFiles(self) -> List[str]:
        'The inspection files.'
        return self._inspectionFiles
    @property
    def directory(self) -> str:
        'The inspection directory.'
        return self._directory

class InspectionItem:
    def __init__(self, directory: str, file_name: str):
        self._directory = directory
        self._fileName = file_name
        self._fullPath = os.path.join(directory, file_name)
    @property
    def fullPath(self) -> str:
        return self._fullPath
    @property
    def name(self) -> str:
        return get_inspection_name(self._fileName)
    def getTurtleScript(self) -> str:
        return open(self._fullPath).read()

class InspectionSuite:
    'Represents a inspection suite.'
    def __init__(self, properties: InspectionProperties):
        'Initializes a new instance with inspection properties.'
        self._properties = properties
        self._results = []
    def scanForMatchingItems(self) -> List[Optional[InspectionItem]]:
        'Scans for inspection items.'
        item_list = []
        entries = os.listdir(self._properties.directory)
        for entry in self._properties.inspectionFiles:
            if entry in entries and Inspector.isTurtleScript(os.path.join(self._properties.directory, entry)):
                item_list.append(InspectionItem(self._properties.directory, entry))
            else:
                item_list.append(None)
        return item_list
    def tryLoadInspectionResults(self) -> List[Tuple[Optional[InspectionResult], Optional[ResultLoadError]]]:
        'Tries to load results stored in local disk.'
        results = []
        load_results = []
        for entry in self._properties.inspectionFiles:
            try:
                r = InspectionResult.load(self._properties.directory, get_inspection_name(entry))
                results.append(r)
                load_results.append((r, None))
            except ResultLoadError as e:
                results.append(None)
                load_results.append((None, e))
        self._results = results
        return load_results
    @property
    def properties(self) -> InspectionProperties:
        'The properties of this suite.'
        return self._properties
    @property
    def results(self) -> List[Optional[InspectionResult]]:
        'The inspection results.'
        return self._results
    @results.setter
    def results(self, value: List[Optional[InspectionResult]]) -> None:
        'The inspection results.'
        self._results = value
    @property
    def totalPercent(self) -> float:
        'Calculates the percentage of the total score.'
        t = 0
        for r in self._results:
            if r is not None: t += r.totalScore * 100
        return t
    @property
    def averagePercent(self) -> float:
        'Calculates the average percentage of the total score.'
        if not self._results: return 0
        return self.totalPercent / len(self._results)

class Inspector:
    'Represents a inspector that runs turtle scripts.'
    @staticmethod
    def isTurtleScript(file_name: str) -> bool:
        'Distinct turtle script by import statements.'
        for line in open(file_name):
            line = line.strip()
            if (line.startswith('import') and 'turtle' in line) or line.startswith('from turtle import'):
                return True
        return False
    @staticmethod
    def runTurtleScript(code: str, finalize: bool=False) -> Tuple[str, Optional[Exception]]:
        'Runs the turtle script in an encapsulated scope.'
        try:
            turtle.speed(0)
        except turtle.Terminator:
            turtle.speed(0)
        scope = { 'turtle': turtle }
        try:
            exec(code, scope)
            turtle.hideturtle()
            return turtle.getcanvas().postscript(colormode='color'), None
        except Exception as e:
            return '', e
        except SystemExit:
            pass
        finally:
            turtle.reset()
            if finalize:
                Inspector.finalizeTurtle()
    @staticmethod
    def finalizeTurtle() -> None:
        'Finalizes the turtle module.'
        try:
            turtle.bye()
        except turtle.Terminator:
            turtle.bye()
    @staticmethod
    def scanForInspectionSuites(directory: str, files: List[str]) -> List[InspectionSuite]:
        'Scans for inspection suites in a directory.'
        results = []
        for entry in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, entry)):
                p = InspectionProperties(os.path.join(directory, entry), files)
                results.append(InspectionSuite(p))
        return results
    def __init__(self, samples: List['SampleSource']):
        'Initializes the inspector with a list of sample sources.'
        self._samples = []
        for source in samples:
            self._samples.append(source.getSample())
    def runInspectionSuite(self, suite: InspectionSuite, callback: Optional[Callable[[int, int], None]]=None, protected: bool=False) -> Optional[Recorder]:
        'Runs specific inspection suite with a callback.'
        items = suite.scanForMatchingItems()
        results = []
        if protected:
            recorder = Recorder()
        def call_callback(index: int, total: int) -> None:
            if callback: callback(index, total)
        for index, item in enumerate(items):
            call_callback(index+1, len(items))
            if item is None:
                name = get_inspection_name(suite.properties.inspectionFiles[index])
                results.append(InspectionResult.skip(name))
                continue
            script = item.getTurtleScript()
            if protected:
                recorder.start()
                inject_functions(hazardous_functions, recorder)
            postscript, error = self.runTurtleScript(script)
            if protected:
                uninject_functions(hazardous_functions, recorder)
            if error:
                results.append(InspectionResult.error(item.name, error))
                continue
            image = Image.open(BytesIO(postscript.encode()))
            image = remove_border(image)
            sample = self._samples[index]
            image = adjust_image_size(image, sample)
            shape_score = calculate_shape_score(image, sample)
            color_score = calculate_color_score(image, sample)
            total_score = calculate_total_score(image, sample)
            results.append(InspectionResult(item.name, shape_score, color_score, total_score, postscript, ''))
        for result in results:
            result.save(suite.properties.directory)
        suite.results = results
        if protected:
            return recorder

from sample import SampleSource
from typing import List
from image import remove_border
from io import BytesIO
from PIL import Image
import json

class SampleProvisionError(Exception):
    'General base class for error during sample provision.'

class ErrorRaisedInCode(SampleProvisionError):
    'There is an error in the code provided.'
    def getInnerError(self) -> Exception:
        'Gets inner error from this exception.'
        return self.__cause__

class SampleSource:
    'Represents a sample source.'
    def getSample(self) -> Image.Image:
        'Gets the sample from the source.'
        raise NotImplementedError
    def serialize(self) -> dict:
        'Serializes this sample to a dictionary.'
        raise NotImplementedError
    @staticmethod
    def deserialize(data: dict) -> 'SampleSource':
        'Deserializes the sample from the data.'
        raise NotImplementedError
    @staticmethod
    def serializeSampleList(samples: List['SampleSource']) -> List[dict]:
        'Serializes a list of samples.'
        slist = []
        for s in samples:
            data = s.serialize()
            data['name'] = s.__class__.__name__
            slist.append(data)
        return slist
    @staticmethod
    def deserializeSampleList(data: List[dict]) -> List['SampleSource']:
        'Deserializes a list of samples.'
        result = []
        for s in data:
            cname = s.pop("name")
            for klass in SampleSource.__subclasses__():
                if klass.__name__ == cname:
                    result.append(klass.deserialize(s))
        return result

from script import Inspector

class CodeSampleSource(SampleSource):
    'Represents a source code sample source.'
    def __init__(self, code: str):
        'Initializes the source with a python code.'
        self._code = code
    @property
    def code(self) -> str:
        'The code to execute.'
        return self._code
    def getSample(self) -> Image.Image:
        'Runs the script and gets the sample.'
        postscript, error = Inspector.runTurtleScript(self._code, True)
        if error:
            raise ErrorRaisedInCode from error
        return remove_border(
            Image.open(BytesIO(postscript.encode()))
        )
    def serialize(self) -> dict:
        'Serializes this sample.'
        return {
            "code": self._code
        }
    @staticmethod
    def deserialize(data: dict) -> 'CodeSampleSource':
        'Deserializes the sample from a dictionary.'
        return CodeSampleSource(data['code'])
    @staticmethod
    def load(file_name: str) -> 'CodeSampleSource':
        'Loads a code file from the local disk.'
        return CodeSampleSource(open(file_name).read())

class JpegSampleSource(SampleSource):
    'Represents a sample from local image.'
    def __init__(self, file_name: str):
        'Initializes the source with a file name.'
        self._fileName = file_name
    @property
    def fileName(self) -> str:
        'The file name of the image.'
        return self._fileName
    def getSample(self) -> Image.Image:
        'Loads the image from the local disk.'
        return remove_border(
            Image.open(self._fileName)
        )
    def serialize(self) -> dict:
        'Serializes this instance.'
        return {
            'file': self._fileName
        }
    @staticmethod
    def deserialize(data: dict) -> 'JpegSampleSource':
        'Deserializes the sample from a dictionary.'
        return JpegSampleSource(data['file'])
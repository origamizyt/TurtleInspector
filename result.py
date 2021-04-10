import os, json
from data import *
from image import remove_border
from io import BytesIO
from PIL import Image
from typing import Optional

class ResultLoadError(Exception):
    'General base class for result loading errors.'

class InvalidPostscriptSignature(ResultLoadError):
    'The digital signature provided is invalid.'
    def __init__(self, nowIs: bytes, shouldBe: bytes, fingerprint: str):
        'Initializes with three parameters.'
        super().__init__("Signature invalid.")
        self._nowIs = nowIs
        self._shouldBe = shouldBe
        self._fingerprint = fingerprint
    @property
    def nowIs(self) -> bytes:
        'What the signature now is.'
        return self._nowIs
    @property
    def shouldBe(self) -> bytes:
        'What the signature should be.'
        return self._shouldBe
    @property
    def fingerprint(self) -> str:
        'The fingerprint of the secret key.'
        return self._fingerprint

class InvalidInspectionDirectory(ResultLoadError):
    'The directory provided does not contain the files needed.'
    def __init__(self, missing_file: str):
        'Initializes with a missing file name.'
        super().__init__("missing {}".format(missing_file))
        self._missingFile = missing_file
    @property
    def missingFile(self) -> str:
        'The missing file in the directory.'
        return self._missingFile

class InspectionResult:
    'Represents an inspection result.'
    def __init__(self, name: str, shape_score: float, color_score: float, total_score: float, postscript: str, exception: str, skipped: bool=False, key: Optional[Key]=None):
        'Initializes a new instance with three scores and the drawing result.'
        self._inspection = name
        self._skipped = skipped
        self._shapeScore = shape_score
        self._colorScore = color_score
        self._totalScore = total_score
        self._postscript = postscript
        self._exception = exception
        self._key = key or Key.generate()
    def save(self, directory: str) -> None:
        'Saves this result to a directory.'
        json_file = os.path.join(directory, "{}.inspect.json".format(self._inspection))
        json.dump({
            'shapeScore': self._shapeScore,
            'colorScore': self._colorScore,
            'totalScore': self._totalScore,
            'signature': encode_base64(
                self._key.sign(self._postscript.encode())
            ),
            'skipped': self._skipped,
            'token': self._key.token,
            'exception': self._exception
        }, open(json_file, 'w'), indent=4)
        ps_file = os.path.join(directory, "{}.inspect.eps".format(self._inspection))
        open(ps_file, 'w').write(self._postscript)
    @staticmethod
    def load(directory: str, name: str) -> 'InspectionResult':
        'Loads a result from a directory.'
        json_file = os.path.join(directory, "{}.inspect.json".format(name))
        if not os.path.isfile(json_file):
            raise InvalidInspectionDirectory("{}.inspect.json".format(name))
        members = json.load(open(json_file))
        shape_score = members['shapeScore']
        color_score = members['colorScore']
        total_score = members['totalScore']
        exception = members['exception']
        skipped = members['skipped']
        signature = decode_base64(members['signature'])
        key = Key.fromToken(members['token'])
        ps_file = os.path.join(directory, "{}.inspect.eps".format(name))
        if not os.path.isfile(ps_file):
            raise InvalidInspectionDirectory("{}.inspect.eps".format(name))
        postscript = open(ps_file, 'r').read()
        if not key.verify(postscript.encode(), signature):
            raise InvalidPostscriptSignature(signature, key.sign(postscript.encode()), key.fingerprint)
        return InspectionResult(name, shape_score, color_score, total_score, postscript, exception, skipped, key)
    @property
    def inspection(self) -> str:
        'The inspection name of this result.'
        return self._inspection
    @property
    def shapeScore(self) -> float:
        'The score of how the shape matches.'
        return self._shapeScore
    @property
    def colorScore(self) -> float:
        'The score of how the color matches.'
        return self._colorScore
    @property
    def totalScore(self) -> float:
        'The score of how the image matches. This score has nothing to do with the other scores.'
        return self._totalScore
    @property
    def skipped(self) -> bool:
        'Whether the file was skipped or tested.'
        return self._skipped
    @property
    def exception(self) -> str:
        'The exception message of an error occurred.'
        return self._exception
    def asImage(self) -> Image.Image:
        'Returns the rendered postscript.'
        return remove_border(
            Image.open(
                BytesIO(self._postscript.encode())
            )
        )
    @staticmethod
    def skip(name: str) -> 'InspectionResult':
        'Skips the current file.'
        return InspectionResult(name, 0.0, 0.0, 0.0, '', '', True)
    @staticmethod
    def error(name: str, error: Exception) -> 'InspectionResult':
        'An error occurred in the script.'
        return InspectionResult(name, 0.0, 0.0, 0.0, '', "{}: {!s}".format(error.__class__.__name__, error))
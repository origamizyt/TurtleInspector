from result import InspectionResult
from script import InspectionSuite
from xml.dom import minidom as dom
import os, time, csv

class ExportProvider:
    'An object that provides internalized api for exporting results.'
    def feed(self, suite: InspectionSuite, data: InspectionResult) -> None:
        'Feeds the data to the provider.'
        raise NotImplementedError
    def save(self, file_name: str) -> None:
        'Saves the file.'
        raise NotImplementedError

class XmlExportProvider(ExportProvider):
    'Provider for xml documents.'
    def __init__(self):
        'Initializes with empty data.'
        self._data = {}
    def feed(self, suite: InspectionSuite, data: InspectionResult) -> None:
        'Feeds the data to the provider.'
        self._data.setdefault(suite, []).append(data)
    def save(self, file_name: str) -> None:
        'Saves the file.'
        impl = dom.getDOMImplementation()
        d = impl.createDocument(None, 'export', dom.DocumentType('export'))
        for key, rlist in self._data.items():
            suite = d.createElement("suite")
            suite.setAttribute("directory", os.path.split(key.properties.directory)[1])
            total = d.createElement("total")
            total.appendChild(d.createTextNode(str(key.totalPercent)))
            suite.appendChild(total)
            average = d.createElement("average")
            average.appendChild(d.createTextNode(str(key.averagePercent)))
            suite.appendChild(average)
            for result in rlist:
                relem = d.createElement("result")
                relem.setAttribute("inspection", result.inspection)
                shape = d.createElement("shape")
                shape.appendChild(d.createTextNode(str(result.shapeScore)))
                relem.appendChild(shape)
                color = d.createElement("color")
                color.appendChild(d.createTextNode(str(result.colorScore)))
                relem.appendChild(color)
                total = d.createElement("total")
                total.appendChild(d.createTextNode(str(result.totalScore)))
                relem.appendChild(total)
                suite.appendChild(relem)
            d.documentElement.appendChild(suite)
        d.documentElement.setAttribute("timestamp", str(int(time.time() * 1000)))
        open(file_name, 'w').write(d.toprettyxml('  '))

class CsvExportProvider(ExportProvider):
    'Provider for CSV documents.'
    def __init__(self):
        'Initializes with empty data.'
        self._data = {}
    def feed(self, suite: InspectionSuite, data: InspectionResult) -> None:
        'Feeds the data to the provider.'
        self._data.setdefault(suite, []).append(data)
    def save(self, file_name: str) -> None:
        fp = open(file_name, 'w')
        writer = csv.writer(fp)
        writer.writerow(['suite', 'name', 'shape', 'color', 'total'])
        for key, value in self._data.items():
            for result in value:
                writer.writerow([
                    os.path.split(key.properties.directory)[1],
                    result.inspection, result.shapeScore, result.colorScore, result.totalScore
                ])
        fp.close()
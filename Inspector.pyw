import json, os
from export import *
from result import InvalidInspectionDirectory, InvalidPostscriptSignature
from PyQt5 import QtCore, QtGui, QtWidgets
from script import InspectionSuite, Inspector, get_inspection_name
from sample import *
from data import encode_base64
from PIL.Image import Image

ABOUT_MSG = \
'''关于此软件：

Turtle Inspector 1.0 by G201142

Copyright© 2021 G201142™.
All rights reserved.'''

class Ui_MainWindow(object):
    font1 = None
    font2 = None
    def __init__(self):
        self.samples = []
        self.CODE_ICON = QtGui.QIcon('assets\\tinspect-code.png')
        self.JPEG_ICON = QtGui.QIcon("assets\\tinspect-jpeg.png")
        self.currentSampleIndex = -1
        self.sampleChanged = False
        self.inspector = None
        self.suites = []
        self.directorySelected = None
        self.inspecting = False
        self.sortIndex = -1
        self.ascend = True
        self.lastSelectionPath = "."
        fid1 = QtGui.QFontDatabase.addApplicationFont("assets\\tfont1.ttf")
        Ui_MainWindow.font1 = QtGui.QFont(QtGui.QFontDatabase.applicationFontFamilies(fid1)[0])
        fid2 = QtGui.QFontDatabase.addApplicationFont("assets\\tfont2.ttf")
        Ui_MainWindow.font2 = QtGui.QFont(QtGui.QFontDatabase.applicationFontFamilies(fid2)[0])
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        self.mainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 640)
        MainWindow.setFont(self.font1)
        MainWindow.setWindowIcon(QtGui.QIcon("assets\\tinspect.png"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 941, 621))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.buttonAddSample = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonAddSample.setObjectName("buttonAddSample")
        self.horizontalLayout_2.addWidget(self.buttonAddSample)
        self.buttonRemoveSample = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonRemoveSample.setObjectName("buttonRemoveSample")
        self.horizontalLayout_2.addWidget(self.buttonRemoveSample)
        self.buttonClearSample = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonClearSample.setObjectName("buttonClearSample")
        self.horizontalLayout_2.addWidget(self.buttonClearSample)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableSamples = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableSamples.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableSamples.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableSamples.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableSamples.setColumnCount(2)
        self.tableSamples.setObjectName("tableSamples")
        self.tableSamples.setRowCount(0)
        self.tableSamples.setHorizontalHeaderLabels(["文件名", "源类型"])
        self.tableSamples.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableSamples.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableSamples)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.buttonSelectDirectory = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonSelectDirectory.setObjectName("buttonSelectDirectory")
        self.horizontalLayout_3.addWidget(self.buttonSelectDirectory)
        self.buttonInspectThis = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonInspectThis.setObjectName("buttonInspectThis")
        self.horizontalLayout_3.addWidget(self.buttonInspectThis)
        self.buttonInspectUninspected = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonInspectUninspected.setObjectName("buttonInspectUninspected")
        self.horizontalLayout_3.addWidget(self.buttonInspectUninspected)
        self.buttonInspectAll = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonInspectAll.setObjectName("buttonInspectAll")
        self.horizontalLayout_3.addWidget(self.buttonInspectAll)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tableSuites = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableSuites.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableSuites.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableSuites.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableSuites.setColumnCount(3)
        self.tableSuites.setObjectName("tableSuites")
        self.tableSuites.setRowCount(0)
        self.tableSuites.setHorizontalHeaderLabels(["目录名", "分数", "平均分"])
        self.tableSuites.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableSuites.horizontalHeader().setSortIndicatorShown(True)
        self.verticalLayout_2.addWidget(self.tableSuites)
        self.checkDetectCode = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.checkDetectCode.setObjectName("checkDetectCode")
        self.checkDetectCode.setText("是否检测危险代码")
        self.checkDetectCode.setChecked(True)
        self.verticalLayout_2.addWidget(self.checkDetectCode)
        self.itemProgress = QtWidgets.QProgressBar(self.horizontalLayoutWidget)
        self.itemProgress.setMaximum(1000)
        self.itemProgress.setProperty("value", 0)
        self.itemProgress.setTextVisible(False)
        self.itemProgress.setObjectName("itemProgress")
        self.verticalLayout_2.addWidget(self.itemProgress)
        self.inspectProgress = QtWidgets.QProgressBar(self.horizontalLayoutWidget)
        self.inspectProgress.setMaximum(1000)
        self.inspectProgress.setProperty("value", 0)
        self.inspectProgress.setTextVisible(False)
        self.inspectProgress.setObjectName("inspectProgress")
        self.verticalLayout_2.addWidget(self.inspectProgress)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.buttonAddSample.clicked.connect(self.addSample)
        self.tableSamples.itemSelectionChanged.connect(self.sampleSelectionChanged)
        self.buttonRemoveSample.clicked.connect(self.removeSample)
        self.buttonClearSample.clicked.connect(self.clearSample)
        self.tableSuites.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableSamples.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.deleteSuiteAction = QtWidgets.QAction("删除套件", self.tableSuites)
        self.tableSuites.addAction(self.deleteSuiteAction)
        self.deleteSuiteAction.triggered.connect(self.deleteSuite)
        self.deleteSuiteAction.setEnabled(False)
        self.refreshSuiteAction = QtWidgets.QAction("刷新", self.tableSuites)
        self.tableSuites.addAction(self.refreshSuiteAction)
        self.refreshSuiteAction.setEnabled(False)
        self.refreshSuiteAction.triggered.connect(self.refreshSuites)
        self.exportResultAction = QtWidgets.QAction("导出为...", self.tableSuites)
        self.exportResultAction.setEnabled(False)
        self.exportResultAction.triggered.connect(self.exportResults)
        self.tableSuites.addAction(self.exportResultAction)
        self.tableSuites.itemSelectionChanged.connect(self.suiteSelectionChanged)
        self.buttonSelectDirectory.clicked.connect(self.selectDirectory)
        self.saveSamplesAction = QtWidgets.QAction("保存样例列表...")
        self.saveSamplesAction.triggered.connect(self.saveSamplesList)
        self.tableSamples.addAction(self.saveSamplesAction)
        self.loadSamplesAction = QtWidgets.QAction("加载样例列表...")
        self.loadSamplesAction.triggered.connect(self.loadSamplesList)
        self.tableSamples.addAction(self.loadSamplesAction)
        self.buttonInspectThis.clicked.connect(self.doInspectThis)
        self.buttonInspectUninspected.clicked.connect(self.doInspectUninspected)
        self.buttonInspectAll.clicked.connect(self.doInspectAll)
        self.buttonInspectThis.setEnabled(False)
        self.buttonInspectUninspected.setEnabled(False)
        self.buttonInspectAll.setEnabled(False)
        self.buttonClearSample.setEnabled(False)
        self.buttonRemoveSample.setEnabled(False)
        self.tableSuites.itemDoubleClicked.connect(self.viewResults)
        self.aboutAction = QtWidgets.QAction("关于...", self.mainWindow)
        self.aboutAction.triggered.connect(self.showAbout)
        self.mainWindow.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.mainWindow.addAction(self.aboutAction)
        self.tableSuites.horizontalHeader().sectionClicked.connect(self.sortSuites)
    def sortSuites(self, index):
        if self.sortIndex != index:
            self.sortIndex = index
            self.ascend = True
        else:
            self.ascend = not self.ascend
        self.tableSuites.sortItems(index, QtCore.Qt.AscendingOrder if self.ascend else QtCore.Qt.DescendingOrder)
    def showAbout(self):
        QtWidgets.QMessageBox.information(self.mainWindow, "关于", ABOUT_MSG)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Turtle Inspector"))
        self.buttonAddSample.setText(_translate("MainWindow", "添加样例..."))
        self.buttonRemoveSample.setText(_translate("MainWindow", "删除样例"))
        self.buttonClearSample.setText(_translate("MainWindow", "清除样例"))
        self.buttonInspectThis.setText(_translate("MainWindow", "测试选中"))
        self.buttonInspectUninspected.setText(_translate("MainWindow", "测试未测试"))
        self.buttonInspectAll.setText(_translate("MainWindow", "测试全部"))
        self.buttonSelectDirectory.setText(_translate("MainWindow", "选择文件夹"))
    def viewResults(self, item: QtWidgets.QTableWidgetItem):
        index = item.row()
        dialog = ViewResultDialog(self.suites[index], self.mainWindow)
        dialog.show()
    def suiteSelectionChanged(self):
        indexes = self.tableSuites.selectedIndexes()
        self.deleteSuiteAction.setEnabled(bool(indexes))
        self.buttonInspectThis.setEnabled(bool(indexes))
    def deleteSuite(self):
        indexes = self.tableSuites.selectedIndexes()
        for index in indexes:
            index = index.row()
            self.suites[index] = None
        while None in self.suites:
            self.suites.remove(None)
        self.updateSuiteList()
    def rebuildInspector(self):
        if self.sampleChanged:
            ret = QtWidgets.QMessageBox.warning(self.mainWindow, "重构测试器", "样本已变更，要重构测试器吗?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if ret != QtWidgets.QMessageBox.Yes: return False
            self.inspector = Inspector(list(map(lambda i: i[1], self.samples)))
            self.sampleChanged = False
            return True
        else:
            return True
    def refreshSuites(self):
        if not self.rebuildInspector(): return
        self.suites = self.inspector.scanForInspectionSuites(self.directorySelected, list(map(lambda i: i[0], self.samples)))
        self.updateSuiteList()
    def selectDirectory(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory(self.mainWindow, "选择文件夹", self.lastSelectionPath)
        if dirname:
            self.lastSelectionPath = os.path.split(dirname)[0]
            if not self.rebuildInspector(): return
            self.suites = self.inspector.scanForInspectionSuites(dirname, list(map(lambda i: i[0], self.samples)))
            self.updateSuiteList()
            self.directorySelected = dirname
            self.refreshSuiteAction.setEnabled(True)
            self.buttonInspectUninspected.setEnabled(True)
            self.buttonInspectAll.setEnabled(True)
            self.exportResultAction.setEnabled(True)
    def exportResults(self):
        name, filt = QtWidgets.QFileDialog.getSaveFileName(self.mainWindow, "导出结果", self.lastSelectionPath,
            "XML 文档 (*.xml);;CSV 文档 (*.csv)")
        if not name: return
        if 'XML' in filt:
            provider = XmlExportProvider()
        elif 'CSV' in filt:
            provider = CsvExportProvider()
        else: return
        for suite in self.suites:
            for result in suite.results:
                if result: provider.feed(suite, result)
        provider.save(name)
    def updateSuiteList(self):
        self.tableSuites.clearContents()
        self.tableSuites.setRowCount(len(self.suites))
        for index, suite in enumerate(self.suites):
            suite.tryLoadInspectionResults()
            self.tableSuites.setItem(index, 0, QtWidgets.QTableWidgetItem(os.path.split(suite.properties.directory)[1]))
            self.tableSuites.setItem(index, 1, QtWidgets.QTableWidgetItem("{:.2f}".format(suite.totalPercent)))
            self.tableSuites.setItem(index, 2, QtWidgets.QTableWidgetItem("{:.2f}".format(suite.averagePercent)))
    def sampleSelectionChanged(self):
        indexes = self.tableSamples.selectedIndexes()
        if indexes:
            self.currentSampleIndex = indexes[0].row()
        else:
            self.currentSampleIndex = -1
        self.buttonRemoveSample.setEnabled(bool(indexes))
    def addSample(self):
        self.addSampleDialog = AddSampleDialog(self.mainWindow)
        self.addSampleDialog.accepted.connect(self.addSampleComplete)
        self.addSampleDialog.show()
    def removeSample(self):
        if self.currentSampleIndex != -1:
            self.samples.pop(self.currentSampleIndex)
            self.updateSampleList()
            self.sampleChanged = True
    def clearSample(self):
        self.samples.clear()
        self.updateSampleList()
        self.sampleChanged = True
    def addSampleComplete(self):
        source = self.addSampleDialog.ui.sourceObject
        name = self.addSampleDialog.ui.fileName
        self.samples.append((name, source))
        self.updateSampleList()
        self.sampleChanged = True
    def updateSampleList(self):
        self.tableSamples.clearContents()
        self.tableSamples.setRowCount(len(self.samples))
        for index, (name, source) in enumerate(self.samples):
            self.tableSamples.setItem(index, 0, QtWidgets.QTableWidgetItem(name))
            if isinstance(source, CodeSampleSource):
                self.tableSamples.setItem(index, 1, QtWidgets.QTableWidgetItem(self.CODE_ICON, '代码源'))
            elif isinstance(source, JpegSampleSource):
                self.tableSamples.setItem(index, 1, QtWidgets.QTableWidgetItem(self.JPEG_ICON, '图像源'))
        self.currentSampleIndex = -1
        self.buttonRemoveSample.setEnabled(False)
        self.buttonClearSample.setEnabled(bool(self.samples))
    def saveSamplesList(self):
        name, _ = QtWidgets.QFileDialog.getSaveFileName(self.mainWindow, "保存样例列表", self.lastSelectionPath, "JSON 文件 (*.json)")
        if not name: return
        self.lastSelectionPath = os.path.dirname(name)
        data, samples, names = {}, [], []
        data['names'] = names
        for sname, sample in self.samples:
            names.append(sname)
            samples.append(sample)
        data['samples'] = SampleSource.serializeSampleList(samples)
        json.dump(data, open(name, 'w'), indent=4)
        QtWidgets.QMessageBox.information(self.mainWindow, "保存样例列表", "列表已保存至 {}。".format(name))
    def loadSamplesList(self):
        name, _ = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow, "加载样例列表", self.lastSelectionPath, "JSON 文件 (*.json)")
        if not name: return
        self.lastSelectionPath = os.path.dirname(name)
        data = json.load(open(name))
        names, samples = data['names'], data['samples']
        samples = SampleSource.deserializeSampleList(samples)
        self.samples = list(zip(names, samples))
        self.updateSampleList()
        self.sampleChanged = True
    def prepareInspection(self):
        if self.sampleChanged:
            self.sampleChanged = False
            self.inspector = Inspector(self.samples)
    def doInspect(self, indexes):
        self.centralwidget.setEnabled(False)
        self.inspectProgress.setValue(0)
        self.itemProgress.setValue(0)
        for i, index in enumerate(indexes):
            r = self.inspector.runInspectionSuite(self.suites[index], self.updateItemProgress, self.checkDetectCode.isChecked())
            if r and r.records:
                info = ""
                for record in r.records:
                    info += "函数名：{}\n位置参数：{!s}\n关键字参数：{!s}\n\n".format(
                        record.name, record.arguments or "无",
                        record.keywordArguments or "无"
                    )
                info = info.rstrip("\n")
                QtWidgets.QMessageBox.warning(self.mainWindow, "危险代码",
                "在 {} 中检测到危险代码。\n该代码尝试用标准库执行系统操作。\n\n调用信息:\n{}".format(
                    os.path.split(self.suites[index].properties.directory)[1], info
                ))
            self.inspectProgress.setValue(int((i+1) * 1000 / len(indexes)))
        self.inspector.finalizeTurtle()
        self.itemProgress.setValue(0)
        self.inspectProgress.setValue(0)
        self.centralwidget.setEnabled(True)
        self.updateSuiteList()
    def updateItemProgress(self, count, total):
        self.itemProgress.setValue(int(count/total*1000))
    def doInspectThis(self):
        indexes = self.tableSuites.selectedIndexes()
        if not indexes: return
        indexes = set(index.row() for index in indexes)
        self.doInspect(indexes)
    def doInspectUninspected(self):
        indexes = []
        for index, suite in enumerate(self.suites):
            inspected = False
            for _, error in suite.tryLoadInspectionResults():
                if not isinstance(error, InvalidInspectionDirectory):
                    inspected = True
                    break
            if not inspected:
                indexes.append(index)
        if indexes:
            self.doInspect(indexes)
    def doInspectAll(self):
        ret = QtWidgets.QMessageBox.warning(self.mainWindow, "测试全部", "确定要测试全部吗？\n之前的测试成绩会全部丢失。", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if ret != QtWidgets.QMessageBox.Yes: return
        indexes = list(range(len(self.suites)))
        self.doInspect(indexes)

class Ui_AddSampleDialog(object):
    def __init__(self):
        self.selection = ""
        self.source = ""
        self.fileName = ""
        self.sourceObject = None
    def setupUi(self, AddSampleDialog: QtWidgets.QDialog):
        self.addSampleDialog = AddSampleDialog
        AddSampleDialog.setObjectName("AddSampleDialog")
        AddSampleDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AddSampleDialog.resize(700, 300)
        AddSampleDialog.setFont(Ui_MainWindow.font1)
        AddSampleDialog.setModal(True)
        AddSampleDialog.setFixedSize(AddSampleDialog.size())
        self.buttonBox = QtWidgets.QDialogButtonBox(AddSampleDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 241, 331, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(AddSampleDialog)
        self.label.setGeometry(QtCore.QRect(20, 28, 72, 21))
        self.label.setObjectName("label")
        self.radioCode = QtWidgets.QRadioButton(AddSampleDialog)
        self.radioCode.setGeometry(QtCore.QRect(90, 30, 115, 19))
        self.radioCode.setObjectName("radioCode")
        self.radioJpeg = QtWidgets.QRadioButton(AddSampleDialog)
        self.radioJpeg.setGeometry(QtCore.QRect(210, 30, 115, 19))
        self.radioJpeg.setObjectName("radioJpeg")
        self.textSource = QtWidgets.QLineEdit(AddSampleDialog)
        self.textSource.setGeometry(QtCore.QRect(20, 90, 351, 31))
        self.textSource.setObjectName("textSource")
        self.label_2 = QtWidgets.QLabel(AddSampleDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 361, 21))
        self.label_2.setObjectName("label_2")
        self.buttonSelect = QtWidgets.QPushButton(AddSampleDialog)
        self.buttonSelect.setGeometry(QtCore.QRect(20, 130, 93, 31))
        self.buttonSelect.setObjectName("buttonSelect")
        self.label_3 = QtWidgets.QLabel(AddSampleDialog)
        self.label_3.setGeometry(QtCore.QRect(20, 170, 361, 21))
        self.label_3.setObjectName("label_3")
        self.textFileName = QtWidgets.QLineEdit(AddSampleDialog)
        self.textFileName.setGeometry(QtCore.QRect(20, 200, 351, 31))
        self.textFileName.setObjectName("textFileName")
        self.viewSampleImage = QtWidgets.QGraphicsView(AddSampleDialog)
        self.viewSampleImage.setGeometry(QtCore.QRect(390, 10, 301, 281))
        self.viewSampleImage.setObjectName("viewSampleImage")
        self.retranslateUi(AddSampleDialog)
        self.buttonBox.accepted.connect(AddSampleDialog.accept)
        self.buttonBox.rejected.connect(AddSampleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddSampleDialog)
        self.textSource.setEnabled(False)
        self.textFileName.setEnabled(False)
        self.buttonSelect.setEnabled(False)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.radioCode.clicked.connect(self.toggleSelection)
        self.radioJpeg.clicked.connect(self.toggleSelection)
        self.textSource.setReadOnly(True)
        self.textFileName.textChanged.connect(self.fileNameChanged)
        self.buttonSelect.clicked.connect(self.selectSource)
        self.viewSampleImage.verticalScrollBar().setVisible(False)
        self.viewSampleImage.horizontalScrollBar().setVisible(False)
    def retranslateUi(self, AddSampleDialog):
        _translate = QtCore.QCoreApplication.translate
        AddSampleDialog.setWindowTitle(_translate("AddSampleDialog", "添加样例"))
        self.label.setText(_translate("AddSampleDialog", "源类型:"))
        self.radioCode.setText(_translate("AddSampleDialog", "从示例代码"))
        self.radioJpeg.setText(_translate("AddSampleDialog", "从图片文件"))
        self.label_2.setText(_translate("AddSampleDialog", "文件名:"))
        self.buttonSelect.setText(_translate("AddSampleDialog", "选择..."))
        self.label_3.setText(_translate("AddSampleDialog", "应提交的文件名 (含扩展名):"))
    def selectSource(self):
        if self.selection == 'code':
            name, _ = QtWidgets.QFileDialog.getOpenFileName(self.addSampleDialog, "选择文件", ".", "Python 文件 (*.py)")
            if name:
                if not Inspector.isTurtleScript(name):
                    QtWidgets.QMessageBox.critical(self.addSampleDialog, "无效代码", "由于代码中未导入 turtle，\n该文件不是 turtle 脚本。")
                    return
                self.sourceObject = CodeSampleSource.load(name)
                try:
                    image = self.sourceObject.getSample()
                except ErrorRaisedInCode as e:
                    self.sourceObject = None
                    err = e.__cause__
                    QtWidgets.QMessageBox.critical(self.addSampleDialog, "无效代码", "在代码中出现了错误:\n\n%s: %s" % (err.__class__.__name__, str(err)))
                    return
                pixmap = image.toqpixmap().scaled(self.viewSampleImage.size().width()-10, self.viewSampleImage.size().height()-10)
                scene = QtWidgets.QGraphicsScene()
                scene.addPixmap(pixmap)
                self.viewSampleImage.setScene(scene)
                self.source = name
                self.textSource.setText(os.path.split(name)[1])
                self.checkAccept()
        elif self.selection == 'jpeg':
            name, _ = QtWidgets.QFileDialog.getOpenFileName(self.addSampleDialog, "选择文件", ".", "JPEG 文件 (*.jpg; *.jpeg)")
            if name:
                self.sourceObject = JpegSampleSource(name)
                self.textSource.setText(os.path.split(name)[1])
                self.source = name
                image = self.sourceObject.getSample()
                pixmap = image.toqpixmap().scaled(self.viewSampleImage.size().width()-10, self.viewSampleImage.size().height()-10)
                scene = QtWidgets.QGraphicsScene()
                scene.addPixmap(pixmap)
                self.viewSampleImage.setScene(scene)
                self.checkAccept()
    def toggleSelection(self):
        oldSelection = self.selection
        self.textSource.setEnabled(True)
        self.textFileName.setEnabled(True)
        self.buttonSelect.setEnabled(True)
        if self.radioCode.isChecked():
            self.selection = "code"
        elif self.radioJpeg.isChecked():
            self.selection = "jpeg"
        if self.selection != oldSelection:
            self.source = ""
            self.textSource.setText("")
            self.sourceObject = None
            self.viewSampleImage.setScene(QtWidgets.QGraphicsScene())
    def fileNameChanged(self, text: str):
        self.fileName = text
        self.checkAccept()
    def checkAccept(self):
        canaccept = bool(self.source.strip() and self.fileName.strip())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(canaccept)

class Ui_ViewResultDialog(object):
    def __init__(self, suite: InspectionSuite):
        self.suite = suite
        self.results = suite.tryLoadInspectionResults()
        self.currentSelectedIndex = -1
    def setupUi(self, ViewResultDialog: QtWidgets.QDialog):
        self.viewResultDialog = ViewResultDialog
        ViewResultDialog.setObjectName("ViewResultDialog")
        ViewResultDialog.resize(500, 600)
        ViewResultDialog.setFixedSize(ViewResultDialog.size())
        ViewResultDialog.setFont(Ui_MainWindow.font1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ViewResultDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 560, 441, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.labelDirName = QtWidgets.QLabel(ViewResultDialog)
        self.labelDirName.setGeometry(QtCore.QRect(20, 20, 461, 31))
        self.labelDirName.setObjectName("labelDirName")
        self.labelTotal = QtWidgets.QLabel(ViewResultDialog)
        self.labelTotal.setGeometry(QtCore.QRect(20, 60, 461, 31))
        self.labelTotal.setObjectName("labelTotal")
        self.tableScores = QtWidgets.QTableWidget(ViewResultDialog)
        self.tableScores.setGeometry(QtCore.QRect(20, 100, 461, 451))
        self.tableScores.setColumnCount(4)
        self.tableScores.setObjectName("tableScores")
        self.tableScores.setRowCount(0)
        self.tableScores.verticalHeader().setVisible(False)
        self.tableScores.setHorizontalHeaderLabels(['名称', '形状分', '颜色分', '总分'])
        self.retranslateUi(ViewResultDialog)
        self.buttonBox.accepted.connect(ViewResultDialog.accept)
        self.buttonBox.rejected.connect(ViewResultDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ViewResultDialog)
        self.tableScores.setRowCount(len(self.results))
        self.tableScores.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for index, (result, _) in enumerate(self.results):
            if result:
                self.tableScores.setItem(index, 0, QtWidgets.QTableWidgetItem(result.inspection))
                self.tableScores.setItem(index, 1, QtWidgets.QTableWidgetItem('{:.2f}'.format(result.shapeScore*100)))
                self.tableScores.setItem(index, 2, QtWidgets.QTableWidgetItem('{:.2f}'.format(result.colorScore*100)))
                self.tableScores.setItem(index, 3, QtWidgets.QTableWidgetItem('{:.2f}'.format(result.totalScore*100)))
            else:
                self.tableScores.setItem(index, 0, QtWidgets.QTableWidgetItem(get_inspection_name(self.suite.properties.inspectionFiles[index])))
                self.tableScores.setItem(index, 1, QtWidgets.QTableWidgetItem('0.00'))
                self.tableScores.setItem(index, 2, QtWidgets.QTableWidgetItem('0.00'))
                self.tableScores.setItem(index, 3, QtWidgets.QTableWidgetItem('0.00'))
        self.tableScores.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableScores.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableScores.setSelectionMode(QtWidgets.QHeaderView.SingleSelection)
        self.tableScores.itemDoubleClicked.connect(self.viewItemDetails)
        self.tableScores.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.viewSourceAction = QtWidgets.QAction("查看源", self.tableScores)
        self.viewSourceAction.triggered.connect(self.viewSource)
        self.tableScores.addAction(self.viewSourceAction)
        self.tableScores.itemSelectionChanged.connect(self.resultSelectionChanged)
    def resultSelectionChanged(self):
        indexes = self.tableScores.selectedIndexes()
        if indexes:
            self.currentSelectedIndex = indexes[0].row()
            result, _ = self.results[self.currentSelectedIndex]
            if result and not result.skipped:
                self.viewSourceAction.setEnabled(True)
            else:
                self.viewSourceAction.setEnabled(False)
        else:
            self.currentSelectedIndex = -1
            self.viewSourceAction.setEnabled(False)
    def viewSource(self):
        if self.currentSelectedIndex < 0: return
        fullpath = os.path.join(self.suite.properties.directory, self.suite.properties.inspectionFiles[self.currentSelectedIndex])
        dialog = ViewSourceDialog(fullpath, self.viewResultDialog)
        dialog.show()
    def retranslateUi(self, ViewResultDialog):
        _translate = QtCore.QCoreApplication.translate
        ViewResultDialog.setWindowTitle(_translate("ViewResultDialog", "查看结果"))
        self.labelDirName.setText(_translate("ViewResultDialog", "文件夹名称：{}".format(
            os.path.split(self.suite.properties.directory)[1]
        )))
        self.labelTotal.setText(_translate("ViewResultDialog", "总分：{:.2f}".format(self.suite.totalPercent)))
    def viewItemDetails(self, item: QtWidgets.QTableWidgetItem):
        result, error = self.results[item.row()]
        if result:
            if result.skipped:
                QtWidgets.QMessageBox.information(self.viewResultDialog, "测试错误", "未找到测试文件。")
            elif result.exception:
                QtWidgets.QMessageBox.information(self.viewResultDialog, "测试错误", "代码运行时错误:\n{}".format(result.exception))
            else:
                dialog = ViewImageDialog(result.asImage(), self.viewResultDialog)
                dialog.show()
        else:
            if isinstance(error, InvalidInspectionDirectory):
                QtWidgets.QMessageBox.information(self.viewResultDialog, "测试错误", "未找到测试结果。\n缺失文件: {}".format(error.missingFile))
            elif isinstance(error, InvalidPostscriptSignature):
                QtWidgets.QMessageBox.information(self.viewResultDialog, "测试错误", "测试结果数字签名错误。\n\n应为: {}\n文件中却是: {}\n\n密钥指纹: {}".format(
                    encode_base64(error.shouldBe), encode_base64(error.nowIs), error.fingerprint
                ))

class Ui_ViewSourceDialog(object):
    def __init__(self, name: str):
        self.name = name
    def setupUi(self, ViewSourceDialog: QtWidgets.QDialog):
        ViewSourceDialog.setObjectName("ViewSourceDialog")
        ViewSourceDialog.resize(400, 500)
        ViewSourceDialog.setFixedSize(ViewSourceDialog.size())
        ViewSourceDialog.setFont(Ui_MainWindow.font1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ViewSourceDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 460, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.sourceViewer = QtWidgets.QTextBrowser(ViewSourceDialog)
        self.sourceViewer.setGeometry(QtCore.QRect(10, 50, 381, 401))
        self.sourceViewer.setObjectName("sourceViewer")
        monoFont = Ui_MainWindow.font2
        monoFont.setPointSize(10)
        self.sourceViewer.setFont(monoFont)
        self.labelFile = QtWidgets.QLabel(ViewSourceDialog)
        self.labelFile.setGeometry(QtCore.QRect(10, 10, 381, 31))
        self.labelFile.setObjectName("labelFile")

        self.retranslateUi(ViewSourceDialog)
        self.buttonBox.accepted.connect(ViewSourceDialog.accept)
        self.buttonBox.rejected.connect(ViewSourceDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ViewSourceDialog)

        try:
            self.sourceViewer.setText(open(self.name).read())
        except FileNotFoundError:
            self.sourceViewer.setText("File not found.")
    def retranslateUi(self, ViewSourceDialog):
        _translate = QtCore.QCoreApplication.translate
        ViewSourceDialog.setWindowTitle(_translate("ViewSourceDialog", "预览源"))
        self.labelFile.setText(_translate("ViewSourceDialog", "文件名：{}".format(os.path.split(self.name)[1])))

class Ui_ViewImageDialog(object):
    def __init__(self, image: Image):
        self.image = image
    def setupUi(self, ViewImageDialog: QtWidgets.QDialog):
        ViewImageDialog.setObjectName("ViewImageDialog")
        ViewImageDialog.resize(500, 400)
        ViewImageDialog.setFont(Ui_MainWindow.font1)
        self.verticalLayoutWidget = QtWidgets.QWidget(ViewImageDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 501, 401))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(5, 5, 5, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.verticalLayoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(ViewImageDialog.accept)

        self.retranslateUi(ViewImageDialog)
        QtCore.QMetaObject.connectSlotsByName(ViewImageDialog)

        w, h = self.image.size
        w = max(w+30, 300)
        h = max(h+60, 300)
        ViewImageDialog.resize(w, h)
        self.verticalLayoutWidget.resize(w, h)
        ViewImageDialog.setFixedSize(ViewImageDialog.size())
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(self.image.toqpixmap())
        self.graphicsView.setScene(scene)
    def retranslateUi(self, ViewImageDialog):
        _translate = QtCore.QCoreApplication.translate
        ViewImageDialog.setWindowTitle(_translate("ViewImageDialog", "查看图片"))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.ui.horizontalLayoutWidget.resize(a0.size().width()-20, a0.size().height()-20)

class AddSampleDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AddSampleDialog()
        self.ui.setupUi(self)

class ViewResultDialog(QtWidgets.QDialog):
    def __init__(self, suite, parent=None):
        super().__init__(parent)
        self.ui = Ui_ViewResultDialog(suite)
        self.ui.setupUi(self)

class ViewSourceDialog(QtWidgets.QDialog):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.ui = Ui_ViewSourceDialog(name)
        self.ui.setupUi(self)

class ViewImageDialog(QtWidgets.QDialog):
    def __init__(self, image: Image, parent=None):
        super().__init__(parent)
        self.ui = Ui_ViewImageDialog(image)
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
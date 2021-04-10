# Python 小海龟画图测试器 1.0

Github 代码库：https://github.com/origamizyt/TurtleInspector

## 0. 前言

### 0.1 介绍

此程序的功能非常简单，即实现对 Python 小海龟作图的结果与标准进行比对并给出几项分数。程序的设计初衷是为了在信息技术课上给老师提供一些便利，而不是让老师手动运行并检查代码。

### 0.2 实现

此程序的原型是非常易懂的——使用 Python 函数运行文件中的代码，并将小乌龟画图窗口 Canvas 中的结果保存为 PostScript，并使用 PIL 进行分析与评分。然而实现却非常复杂，在此不做细说。

## 1. 安装

在 Github 上，可以找到此程序的发行版本并下载。或者您也可以下载源代码，并使用 Python 运行它。
```
git clone http://github.com/origamizyt/TurtleInspector.git
```

此程序需要以下依赖：
- Pillow 7.2.0
- Ghostscript 9.53.3 (安装在本地即可)
- PyQt5 5.15.1

在下载源代码后，运行 `Inspector.pyw` 即可运行程序。

您也可以在 http://ztools.cf/project 上找到该项目。

## 2. 使用

### 2.1 概念

在开始使用程序之前，有一些概念是有必要说明的。
- **样例**：样例是一个标准答案，内置的样例有两种类型：代码源和图像源。代码源是一段 Python 小海龟代码，被执行后可以画出应使用的示例图片。图像源是储存在本机上的一个 JPEG 图像。值得注意的是，样例是可扩展的，具体请参见 *4. 扩展* 一节。
- **测试器**：测试器是一个对象，负责对图像进行测试与评分。值得注意的是，一个测试器只有一个样例列表。如果样例列表改变了，那么就需要重新构造测试器。
- **套件**：一个套件指一个测试目录，其中包含了要测试的文件与测试结果。无法判断一个目录是否是一个套件。当测试时，测试器会测试这个套件里所有符合要求的文件并给出分数。测试完成后，在该目录下会生成两个文件，分别表示测试结果与图像数据。

### 2.2 使用 GUI 版本

**2.2.1 启动**

在发行版本中，目录下的 `Inspector.exe` 即是 GUI 版本的程序。双击运行该程序会打开一个 GUI 窗口。

![Gui_Startup](assets/doc/gui01.png)

可以看到，两个表格控件将整个窗体分为了两部分。左半部分为样例控制，右半部分为测试控制。整体布局是固定的，但是控件排列是响应式的，控件大小随窗体大小改变而改变。您可以自由地拉伸窗口。

**2.2.2 样例**

这时的测试器还没有任何样例，您可以通过"添加样例"按钮添加一个新的样例。单击"添加样例"按钮，将弹出"添加样例"对话框。

![Gui_AddSample_1](assets/doc/gui02.png)

> 注：强烈建议您选择示例代码而不是图片文件，因为 JPEG 文件有可能是经压缩的，导致其颜色与图案发生改变。

若要以示例代码作为样例，单击示例代码单选按钮。本教程中使用的示例代码如下：
```py
import turtle

turtle.pencolor('green')
turtle.pensize(5)
turtle.fillcolor('red')

turtle.begin_fill()
for _ in range(4):
    turtle.forward(100)
    turtle.left(90)
turtle.end_fill()
```

该代码绘制了一个绿色边框红色填充的正方形。

单击"选择..."按钮，在弹出的对话框中选择示例代码文件。程序会自动帮您运行该文件并获取结果。此时您应该会看到小海龟作图的窗口一闪而过，而图像出现在右侧的图片框中。

![Gui_AddSample_2](assets/doc/gui03.png)

在下方"应提交的文件名"文本框中输入测试者应提交的文件名，如`T1.py`。此时下方的"OK"按钮会被启用，单击"OK"按钮完成添加样例。应该能看到添加的样例出现在样例列表中。

![Gui_AddSample_3](assets/doc/gui04.png)

单击选中一个样例并单击"删除样例"按钮可以删除该样例。单击"清除样例"按钮可以删除所有添加的样例。此时可以继续通过"添加样例"按钮添加样例。本教程中使用的样例还有另一个示例代码：
```py
import turtle

turtle.pencolor('green')
turtle.pensize(5)
turtle.fillcolor('red')

turtle.begin_fill()
turtle.circle(100)
turtle.end_fill()
```

> 注：读者可能会注意到，所有代码中均未出现 `turtle.done` 或 `turtle.bye` 等语句。这是因为这些语句会挂起或退出画图窗口，使得代码无法正常测评。请读者一定小心这一点。

以上代码绘制了一个绿色边框红色填充的圆。我们将其添加为 `T2.py`。

为了让重复的添加样例的操作省去，可以将样例列表保存起来。在样例列表中右键，在出现的菜单中选择"保存样例列表..."，在弹出的对话框中保存即可。加载时，只需右键点击"加载样例列表..."，选择之前保存的文件即可。

> 注：在加载样例列表之前，请确保 JPEG 图像源的图像仍然保存在相同的位置。

至此，样例操作就完成了。

**2.2.3 测试**

在详细讲解之前，请读者先了解测试的目录结构。在测试根目录下，有许多文件夹，这些文件夹即为被测试者提交的代码。在文件夹中，有测试者提交的代码文件，程序也会将测试结果存放在这里。

我们先来建立一些测试数据。新建一个测试根目录，任何名称都是可接受的，我将其命名为 `suites`。在 `suites` 目录中新建名为 `Suite1` 的目录，这代表第一位测试者。将刚刚的示例文件复制到 `Suite1` 中并重命名为 `T1.py` 与 `T2.py`。这样第一位测试者的分数应该为满分。

回到程序中，单击"选择文件夹"按钮并选择 `suites` 文件夹。此时程序会提示您重构测试器，单击"Yes"按钮并等待测试器重构。应该可以看到 `Suite1` 出现在右侧的列表中。

![Gui_Inspection_1](assets\doc\gui05.png)

选中 `Suite1` 并单击"测试选中按钮"来测试 `Suite1`。应该会看到小海龟画图的窗口出现并绘制出代码中的图案。当窗口关闭时，可以看到 `Suite1` 的总分与平均分。

![Gui_Inspection_2](assets\doc\gui06.png)

双击 `Suite1` 会弹出结果窗口，在其中双击一项可以查看测试结果，右键点击"查看源"可以查看源代码。

<div style='display: flex; justify-content: space-between'>
    <img src="assets\doc\gui07.png"
    style='max-width: 30%;' alt='Gui_Result_1'/>
    <img src="assets\doc\gui08.png" 
    style='max-width: 30%;' alt='Gui_Result_2'/>
    <img src="assets\doc\gui09.png" 
    style='max-width: 30%;' alt='Gui_Result_3'/>
</div><br/>

切换至 `Suite1` 目录，可以发现多出了4个文件：`T1.inspect.json`, `T1.inspect.eps`, `T2.inspect.json`, `T2.inspect.eps`。这四个文件代表了两个题目的测试结果和图像。删除 `T1.inspect.json` 并在套件列表中右键点击刷新，应该可以看到 `Suite1` 的总分变为了 100 分。双击 `Suite1` 并双击 `T1` 题目可以看到缺失结果的提示。

![Gui_Error_1](assets/doc/gui10.png)

接下来构造一个错误的代码。在 `suites` 文件夹下创建 `Suite2` 文件夹，将第一个示例代码复制两次，分别命名为 `T1.py` 与 `T2.py`。第一个代码是完全正确的，而第二个则绘制了错误的图形。回到窗口中，在套件列表中右键点击刷新，`Suite2` 应该会出现在列表中。

![Gui_Inspection_3](assets/doc/gui11.png)

单击"测试未测试"按钮以测试 `Suite2`。应该会看到 `Suite2` 的总分并不是 200 分，而是介于 170~180 之间。双击 `Suite2` 能看到第一题是满分，而第二题不是。

接下来测试另一种异常现象。在 `suites` 文件夹中创建 `Suite3` 文件夹并将第一个示例复制并重命名为 `T1.py`。这种情况代表了测试者未提交全部题目而是只提交了一部分。

再次刷新套件列表并测试未测试的套件。可以看到 `Suite3` 的总分只有 100 分。双击 `Suite3` 并双击 `T2` 题目，将会弹出消息框告知您缺少题目文件。

![Gui_Error_2](assets/doc/gui12.png)

回到 `Suite3` 目录中，创建 `T2.py` 文件并输入以下代码：
```py
import turtle
raise Exception("exception in code")
```

> 注：之所以要添加导入语句的原因是，测试器在运行代码之前，会检测代码是不是 turtle 脚本，而这种操作是用检测导入语句而实现的。如果没有该语句，测试器会直接跳过该文件。

选中 `Suite3` 并测试，双击 `Suite3` 并双击 `T2` 题目，将会弹出消息框告知您代码运行时错误。

![Gui_Error_3](assets/doc/gui13.png)

至此，测试部分就完成了。

### 2.3 使用命令行版本

在发行版中，`Inspectx.exe` 为命令行版本。在当前目录打开 `cmd.exe` 并输入以下命令：
```
inspectx
```

应该得到以下结果：
```
Usage: inspectx <sample_file> <inspection_file>
Error: invalid argument count.
```

以上一节的数据为例，演示命令行版本的用法：
```
$ inspectx Sample1.py suites\Suite1\T1.py
OK
1.0000
1.0000
1.0000

$ inspectx Sample2.py suites\Suite2\T2.py
OK
0.7782
1.0000
0.7883

$ inspectx Sample2.py suites\Suite3\T2.py
ERROR: exception in code

$ inspectx no_such_sample.jpg blah
ERROR: [Errno 2] No such file or directory: 'no_such_sample.jpg'
```

## 3. 一些额外功能

在 GUI 版本中，增加了一些额外的功能。命令行版本则没有这些功能。

### 3.1 危险代码

在运行 GUI 版本时，读者可能会注意到右侧面板下方的"检测危险代码"复选框。当开启这个功能时，将检测代码文件中的危险代码并汇报给测试者，以防止不必要的麻烦。该功能默认是开启的，要显式关闭该功能，请取消勾选该复选框。

我们强烈建议您开启该功能。但是尽管这个功能可以检测到一些危险代码，仍然无法避免一些极端的情况，比如调用 ctypes 库执行 Windows API 代码以及调用手动编译的 Python 扩展。这是作弊的行为，应该给予其 0 分的处罚。

下面来写一段代码测试该功能，打开 `suites` 目录，新建 `Suite4` 文件夹并将以下内容键入至 `T1.py`：
```py
import turtle, os
os._exit(0)
```

> 注：这里使用 `os._exit` 的原因是 `sys.exit` 是被允许的，因为它经常被用来结束程序。程序可以捕捉 `sys.exit` 引发的 `SystemExit` 异常。但 `os._exit` 调用了 C 的标准函数，因此被认为是危险代码。

打开 GUI 窗口并刷新套件列表，点击"测试未测试"以测试 `Suite4`。在测试的过程中，会弹出消息框提示您危险代码的存在。

![Gui_Error_4](assets/doc/gui14.png)

### 3.2 测试结果数字签名

为防止测试结果被他人篡改，在测试结果文件中加入了密钥与签名。在 `Suite1` 目录下，打开 `T1.inspect.json` 文件，将会看到如下信息（不完全一致）：
```json
{
    "shapeScore": 1.0,
    "colorScore": 1.0,
    "totalScore": 1.0,
    "signature": "pxxJrPulk3aXjqAvhR/dHaNCMGEycPREPNL4KWAQtGEw/3syWbqj6kObGTEwUDfC",
    "skipped": false,
    "token": "0ec22e2149625f79cdde7ea7b14a01f3ea487be22488b99ef1fce95db98db481",
    "exception": ""
}
```

现在将 `token` 项最后两位改为 `00`，回到窗口并刷新套件列表，会发现 `Suite1` 的测试结果变为 100 分。双击 `Suite1` 并双击 `T1` 题目，将弹出消息框提示您签名有误。

![Gui_Error_5](assets/doc/gui15.png)

可以看出密钥一旦更改一点，产生的签名就大不相同。

## 4. 扩展

这一节将教您如何扩展本程序。扩展的先决条件是下载了本程序的源代码。

### 4.1 编写您自己的 Turtle Inspector

要编写个性化的功能，首先需要了解本程序的实现原理。本程序分为以下几个模块：
- `data.py`：负责数据的签名与验签工作。
- `export.py`：负责结果的导出，可扩展。
- `image.py`：处理图像，包括调整大小、去边框与评分。
- `inject.py`：负责对危险代码的注入、记录与屏蔽。
- `result.py`：含有对结果的封装，包括加载与保存结果。
- `sample.py`：含有对样例的支持，可扩展。
- `script.py`：核心模块，负责寻找套件与套件中的测试项，运行小海龟画图脚本，可扩展。

检测器类位于 `script.py` 中，构造函数接受一个样例列表作为唯一的参数。样例位于 `sample.py` 中，以 `CodeSampleSource` 为例，其接受一段代码作为唯一的参数，也可以调用 `load` 静态方法从文件加载：
```py
from sample import CodeSampleSource
from script import Inspector

sample_list = [
    CodeSampleSource.load("Sample1.py"),
    CodeSampleSource.load("Sample2.py")
]

i = Inspector(sample_list)
```

运行这段代码，您将会获得一个带有指定样例的测试器。测试器示例的 `scanForInspectionSuites` 方法可以为指定的测试根目录创建一系列的套件并返回。其接受根目录与测试文件列表作为参数：
```py
suites = i.scanForInspectionSuites(
    "suites", ["T1.py", "T2.py"]
)
```

此时 `suites` 变量包含套件列表。使用 `runInspectionSuite` 方法运行套件。该方法接受套件为唯一的必选参数，接受一个可选的回调函数及可选的布尔值，表示是否检测危险代码。当检测危险代码为 `True` 时，该函数返回一个 `inject.Recorder` 实例，否则返回 `None`。回调接受两个整型参数，表示当前测试的索引（从1开始）和全部测试文件的数量。
```py
def callback(count, total):
    print('{}/{}'.format(count, total))
suite = suites[0]
i.runInspectionSuite(suite, callback)
```

运行代码后，测试数据应被存储在套件中，使用 `results` 属性来访问它：
```py
print(suite.results[0].totalScore) # T1.py
```

当重新运行 Python 解释器时，使用套件的 `tryLoadInspectionResults` 方法加载上次的结果。该方法返回一个元组列表，每一项都是结果/错误的元组，且必有其一为 `None`。若加载成功则错误为 `None`，加载失败则结果为 `None`。错误为 `result.ResultLoadError` 的实例。
```py
from result import *
results = suite.tryLoadInspectionResults()
result, error = results[0]
if error:
    print('ERROR:', error)
else:
    print(result.totalScore)
```

### 4.2 扩展样例源

扩展样例只需要继承自 `sample.SampleSource` 并实现 `getSample` 与方法即可。内置的样例还有 `JpegSampleSource`，其使用一个文件名作为参数。以下代码创建了 `NetworkSampleSource`，使其从互联网上下载图片：
```py
from sample import SampleSource
from PIL import Image
import requests as req

class NetworkSampleSource(SampleSource):
    def __init__(self, url: str):
        self._url = url
    def getSample(self) -> Image.Image:
        resp = req.get(self._url, stream=True)
        return Image.open(resp.raw)
```

要实现保存样例的功能，请实现 `serialize` 与 `deserialize` 方法：
```py
class NetworkSampleSource(SampleSource):
    def __init__(self, url: str):
        self._url = url
    def getSample(self) -> Image.Image:
        resp = req.get(self._url, stream=True)
        return Image.open(resp.raw)
    def serialize(self) -> dict:
        return { 'url': self._url }
    @staticmethod
    def deserialize(data: dict) -> SampleSource:
        return NetworkSampleSource(data['url'])
```

现在您可以在测试器中使用它。

4.3 扩展导出格式

要扩展导出格式，只需继承自 `export.ExportProvider` 并实现 `feed` 与 `save` 方法。`feed` 方法接受两个参数，分别为套件实例与结果对象。`save` 方法接受文件名作为唯一的参数。

目前还没有任何内置功能使用 `ExportProvider`。也许会在之后的版本中添加。
from io import BytesIO
from sample import CodeSampleSource, JpegSampleSource
from script import Inspector
from image import *
from PIL import Image
import sys

if len(sys.argv) != 3:
    print('Usage: inspectx <sample_file> <inspection_file>')
    print('Error: invalid argument count.')
    sys.exit()

sample_file = sys.argv[1]
code_file = sys.argv[2]

if sample_file.endswith('.py'):
    sample = CodeSampleSource.load(sample_file)
else:
    sample = JpegSampleSource(sample_file)

try:
    sample_image = sample.getSample()
except Exception as e:
    print('ERROR: {!s}'.format(e))
    sys.exit()
postscript, error = Inspector.runTurtleScript(open(code_file).read(), True)
if error:
    print('ERROR: {!s}'.format(error))
    sys.exit()
image = Image.open(BytesIO(postscript.encode()))
image = adjust_image_size(remove_border(image), sample_image)
shape_score = calculate_shape_score(image, sample_image)
color_score = calculate_color_score(image, sample_image)
total_score = calculate_total_score(image, sample_image)
print('OK\n{:.4f}\n{:.4f}\n{:.4f}'.format(
    shape_score, color_score, total_score
))
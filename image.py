from PIL import Image, ImageChops

WHITE = (255, 255, 255)

def remove_border(image: Image.Image) -> Image.Image:
    'Removes the border of the image.'
    bg = Image.new(image.mode, image.size, (255, 255, 255))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 0.2, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    else: 
        return image

def adjust_image_size(image: Image.Image, master: Image.Image) -> Image.Image:
    'Adjusts the image size.'
    return image.resize(master.size)

def calculate_shape_score(image: Image.Image, master: Image.Image) -> float:
    'Calculates the shape score. Assume the two image have the same size.'
    total = image.size[0] * image.size[1]
    count = 0
    for d1 in range(image.size[0]):
        for d2 in range(image.size[1]):
            imageiswhite = image.getpixel((d1, d2)) == WHITE
            masteriswhite = master.getpixel((d1, d2)) == WHITE
            if imageiswhite == masteriswhite: count += 1
    return count / total

def calculate_color_score(image: Image.Image, master: Image.Image) -> float:
    'Calculates the color score.'
    maxcount = 256*256*256
    mastercolors = set(map(lambda i: i[1], master.getcolors(maxcount)))
    imagecolors = set(map(lambda i: i[1], image.getcolors(maxcount)))
    total = len(mastercolors)
    count = 0
    for pixel in mastercolors:
        if pixel in imagecolors:
            count += 1
    return count / total

def calculate_total_score(image: Image.Image, master: Image.Image) -> float:
    'Calculates the total score.'
    diff = ImageChops.difference(image, master)
    total = 0
    invcount = 0
    for d1 in range(image.size[0]):
        for d2 in range(image.size[1]):
            masterpixel = master.getpixel((d1, d2))
            total += sum(map(lambda i: max(i, 255-i), masterpixel))
            invcount += sum(diff.getpixel((d1, d2)))
    return 1-invcount / total
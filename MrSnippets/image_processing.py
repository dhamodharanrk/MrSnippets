from PIL import Image
from PIL import ImageEnhance

def adjust_brightness(input_image, output_image, factor):
    image = Image.open(input_image)
    enhancer_object = ImageEnhance.Brightness(image)
    out = enhancer_object.enhance(factor)
    out.save(output_image)

def adjust_contrast(input_image, output_image, factor):
    image = Image.open(input_image)
    enhancer_object = ImageEnhance.Contrast(image)
    out = enhancer_object.enhance(factor)
    out.save(output_image)

def adjust_sharpness(input_image, output_image, factor):
    image = Image.open(input_image)
    enhancer_object = ImageEnhance.Sharpness(image)
    out = enhancer_object.enhance(factor)
    out.save(output_image)

def resize_image(input_image_path,output_image_path,size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)

def scale_image(input_image_path,output_image_path,width=None,height=None):
    original_image = Image.open(input_image_path)
    w, h = original_image.size
    if width and height: max_size = (width, height)
    elif width: max_size = (width, h)
    elif height: max_size = (w, height)
    else: raise RuntimeError('Width or height required!')
    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path)

def black_and_white(input_image_path,output_image_path):
   color_image = Image.open(input_image_path)
   bw = color_image.convert('L')
   bw.save(output_image_path)

def rotateImage(image_path, degrees_to_rotate, saved_location):
    image_obj = Image.open(image_path)
    rotated_image = image_obj.rotate(degrees_to_rotate)
    rotated_image.save(saved_location)

def flipImage(image_path, saved_location,direction):
    image_obj = Image.open(image_path)
    if direction=="FLIP_LEFT_RIGHT":
        rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
        rotated_image.save(saved_location)
    elif direction=="FLIP_TOP_BOTTOM":
        rotated_image = image_obj.transpose(Image.FLIP_TOP_BOTTOM)
        rotated_image.save(saved_location)
    elif direction=="TRANSPOSE":
        rotated_image = image_obj.transpose(Image.TRANSPOSE)
        rotated_image.save(saved_location)

def cropImage(image_path, coords, saved_location):
    '''crop('image.jpg', (161, 166, 706, 1050), 'cropped.jpg')'''
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)

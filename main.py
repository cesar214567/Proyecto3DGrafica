from PIL import Image
from glob import glob
import os

def binarize(image_to_transform, threshold):
    #output_image=image_to_transform.convert("L")
    output_image=image_to_transform

    for x in range(output_image.width):
        white_pixel = False
        for y in range(output_image.height):
            print(output_image.getpixel((x,y)))
            if output_image.getpixel((x,y))< threshold: #note that the first parameter is actually a tuple object
                output_image.putpixel( (x,y), 0 )
            else:
                output_image.putpixel( (x,y), 255 )
    return output_image



BASE_IMG_PATH=os.path.join('.','')
all_images_list = glob(os.path.join(BASE_IMG_PATH,'imagenes','*.jpg'))
all_images_list.sort(key=lambda x:int(x.split("/")[-1].split(".")[0]))
print(all_images_list)
image = Image.open(all_images_list[0])
image = image.convert('RGB')
image = binarize(image,15)

image.show()

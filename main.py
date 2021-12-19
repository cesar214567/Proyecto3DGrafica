from PIL import Image
from glob import glob
import os

def binarize(image_to_transform, threshold,iteration):
    output_image=image_to_transform
    modified_image=image_to_transform.convert("L")
    all_points = []
    first_white_pixel =False
    for y in range(0,output_image.height,3):
        points = []
        white_pixel = False
        for x in range(output_image.width):
            if modified_image.getpixel((x,y))> threshold: #note that the first parameter is actually a tuple object
                output_image.putpixel( (x,y), (255,0,0) )
                first_white_pixel = white_pixel = True
                points.append([x,y,iteration])
                break
        for x in reversed(range(output_image.width)):
            if modified_image.getpixel((x,y))> threshold: #note that the first parameter is actually a tuple object
                output_image.putpixel( (x,y), (255,0,0) )
                first_white_pixel = white_pixel = True
                points.append([x,y,iteration])
                break
        if white_pixel == False and first_white_pixel == True :
            break
        if white_pixel:
            all_points.append(points)
    return all_points,output_image

def process_squares(all_images_points,edges,counter_indexes1,counter_indexes2,iteration):
    vertex_array1 = all_images_points[iteration]
    vertex_array2 = all_images_points[iteration+1]
    inferior_limit = min(vertex_array1.size-1, vertex_array2.size-1)
    superior_limit = max(vertex_array1.size-1, vertex_array2.size-1)
    for j in range(inferior_limit):
        edges.append([counter_indexes1+2*j,counter_indexes1+2*(j+1), counter_indexes2+2*(j)])
        edges.append([counter_indexes1+2*(j+1), counter_indexes2+2*(j),counter_indexes2+2*(j+1)])
    if(inferior_limit == vertex_array1.size-1):
        for j in range (inferior_limit,superior_limit):
            edges.append([counter_indexes1+2*(inferior_limit-2),counter_indexes1+2*(inferior_limit-1), counter_indexes2+2*(j)])
            edges.append([counter_indexes1+2*(inferior_limit-1), counter_indexes2+2*(j),counter_indexes2+2*(j+1)])
    else:
        for j in range (inferior_limit,superior_limit):
            edges.append([counter_indexes1+2*j,counter_indexes1+2*(j+1), counter_indexes2+2*(inferior_limit-2)])
            edges.append([counter_indexes1+2*(j+1), counter_indexes2+2*(inferior_limit-2),counter_indexes2+2*(inferior_limit-1)])

def generate_edges(all_images_points):
    counter_indexes1 = 0
    counter_indexes2 = len(all_images_points[0])*2
    edges = []
    for i in range(0,all_images_points.size-1):
        #pixeles izquierdos
        process_squares(all_images_points,edges,counter_indexes1,counter_indexes2,i)
        #pixeles derechos
        process_squares(all_images_points,edges,counter_indexes1+1,counter_indexes2+1,i)
    return edges


BASE_IMG_PATH=os.path.join('.','')
all_images_list = glob(os.path.join(BASE_IMG_PATH,'imagenes','*.jpg'))
all_images_list.sort(key=lambda x:int(x.split("/")[-1].split(".")[0]))
all_images_points = []
for index,image_path in enumerate(all_images_list):
    image = Image.open(all_images_list[0])
    image = image.convert('RGB')
    image.show()
    all_points,image = binarize(image,40,index)
    all_images_points.append(all_points)

local = all_images_points
while isinstance(local,list):
    print(len(local))
    local = local[0]
    print(type(local))

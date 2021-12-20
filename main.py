from PIL import Image
from glob import glob
import os
import numpy as np
import csv
from math import ceil, floor

def binarize(image_to_transform, threshold,iteration):
    output_image=image_to_transform
    modified_image=image_to_transform.convert("L")
    all_points = []
    first_white_pixel =False
    for y in range(0,output_image.height,3):
        points = []
        white_pixel = False
        x1 = 0
        x2= 640
        for x in range(floor(output_image.width/8.0),floor(output_image.width*7/8.0)):
            if modified_image.getpixel((x,y))> threshold and modified_image.getpixel((x,y))< 40: #note that the first parameter is actually a tuple object
                #print(modified_image.getpixel((x,y)))
                output_image.putpixel( (x,y), (255,0,0) )
                first_white_pixel = white_pixel = True
                points.append([x,y,iteration])
                x1 = x
                break
        for x in reversed(range(floor(output_image.width/8.0),floor(output_image.width*7/8.0))):
            if modified_image.getpixel((x,y))> threshold and modified_image.getpixel((x,y))< 40: #note that the first parameter is actually a tuple object
                #print(modified_image.getpixel((x,y)))
                output_image.putpixel( (x,y), (255,0,0) )
                first_white_pixel = white_pixel = True
                points.append([x,y,iteration])
                x2 = x
                break
        if x2-x1 > 550 and first_white_pixel:
            break
        if white_pixel == False and first_white_pixel == True :
            break
        if white_pixel:
            all_points.append(points)
    return all_points,output_image

def process_squares(all_images_points,edges,counter_indexes1,counter_indexes2,iteration):
    vertex_array1 = all_images_points[iteration]
    vertex_array2 = all_images_points[iteration+1]
    inferior_limit = min(len(vertex_array1)-1, len(vertex_array2)-1)
    superior_limit = max(len(vertex_array1)-1, len(vertex_array2)-1)
    for j in range(inferior_limit):
        edges.append([counter_indexes1+2*j,counter_indexes1+2*(j+1), counter_indexes2+2*(j)])
        edges.append([counter_indexes1+2*(j+1), counter_indexes2+2*(j),counter_indexes2+2*(j+1)])
    if(inferior_limit == len(vertex_array1)-1):
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
    for i in range(len(all_images_points)-1):
        #pixeles izquierdos
        process_squares(all_images_points,edges,counter_indexes1,counter_indexes2,i)
        #pixeles derechos
        process_squares(all_images_points,edges,counter_indexes1+1,counter_indexes2+1,i)
        counter_indexes1 = counter_indexes2
        counter_indexes2 += len(all_images_points[i+1])*2
        print("####")
        print(counter_indexes2)
        print("####")
    return edges


BASE_IMG_PATH=os.path.join('.','')
all_images_list = glob(os.path.join(BASE_IMG_PATH,'imagenes','*.jpg'))
all_images_list.sort(key=lambda x:int(x.split("/")[-1].split(".")[0]))
all_images_points = []
#all_images_list = all_images_list[13:15]
for index,image_path in enumerate(all_images_list):
    image = Image.open(image_path)
    image = image.convert('RGB')
    all_points,image = binarize(image,10,index)
    image.show()
    all_images_points.append(all_points)

'''
local = all_images_points
while isinstance(local,list):
    print(len(local))
    local = local[0]
    print(type(local))
'''

edges = generate_edges(all_images_points)
print(all_images_points)
print(edges)
print(len(edges))

sum = 0

for index,array in enumerate(all_images_points):
    print(index, len(array))
    sum+= 2*len(array)
print(sum)
#############################
file_object = open("vertex.txt", "w")
writer = csv.writer(file_object, delimiter = " ")
#writer.writerow([sum])
for image_points in all_images_points:
    for row in image_points:
        for point in row:
            writer.writerow(point)
file_object.close()

file_object2 = open("edges.txt", "w")
writer = csv.writer(file_object2, delimiter = " ")
#writer.writerow([len(edges)])
for triangle in edges:
    writer.writerow(triangle)
file_object2.close()

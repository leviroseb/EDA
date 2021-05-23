import random
import math
from PIL import Image
import numpy as np
import glob

k = 12288
class Node:
    def __init__(self,point,axis,clase):
        self.point = point
        self.left = None
        self.right = None
        self.axis = axis
        self.clase = clase

def getHeight(node):
	if(node==None):
		return 0
	else:
		return max(getHeight(node.left),getHeight(node.right)) + 1

def build_kdtree(points,depth=0):
	n = len(points)
	axis = depth % k
	if(n<=0):
		return None
	if(n==1):
		return Node(points[0],axis,points[0][12288])
	
	points.sort(key=lambda point: point[axis])
	median = len(points)//2

	node = Node(points[median],axis,points[median][12288])
	node.left = build_kdtree(points[:median],depth + 1)
	node.right = build_kdtree(points[median+1:], depth + 1)
	return node

def distanceSquared(point1,point2):
    distance = 0
    for i in range(k):
        distance+=math.pow(point1[i]-point2[i],2)
    return math.sqrt(distance)

def order(queue):
    for i in range (len(queue)):
        j = i+1
        for j in range (len(queue)):
            if (queue[i][0]>queue[j][0]) :
                temp=queue[i]
                queue[i]=queue[j]
                queue[j]=temp

def priority_queue(queue,point,count):
    if (len(queue)<count):
        queue.append(point)
        sorted(queue,key=lambda point: point[0])
    else:
        for i in range (len(queue)):
            if (queue[i][0]>point[0]):
                temp=queue[i]
                queue[i]=point
                point=temp

def Knearest(node,point,k):
	quever=[]
	k_nearest_point(node,point,quever,k);
	indices=[]
	for i in range (len(quever)):
		indices.append(quever[i][1])
	clases= []
	tipo=""
	for nodo in indices:
		clase = nodo[12288]
		if clase == 1:
			tipo="Bug"
		if clase == 2:
			tipo="Water"
		if clase == 3:
			tipo="Fire"
		if clase == 4:
			tipo="Grass"
		if clase == 5:
			tipo="Rock"
		if clase == 6:
			tipo="Electric"
		if clase == 7:
			tipo="Ghost"
		clases.append(tipo)
	return clases

def k_nearest_point( node , point , queue, k):
	if ( node == None ):
		return
	axis = node.axis
	dist=distanceSquared(point,node.point)
	priority_queue(queue,[dist,node.point],k)
	next_branch = None
	opposite_branch = None
	if (point[axis]<node.point[axis]):
		next_branch=node.left
		opposite_branch=node.right
	else:
		next_branch=node.right
		opposite_branch=node.left
	k_nearest_point(next_branch,point,queue,k)
	if(len(queue)<k or queue[0][0]>abs(point[axis]-node.point[axis])):
		k_nearest_point(opposite_branch,point,queue,k)

image_list = []

def most_frequent(List): 
    return max(set(List), key = List.count)

def cargar(carpeta,tipo):
	for filename in glob.glob(carpeta+'*.png'):
		imge = Image.open(filename).convert('RGB')
		arr1 = np.array(imge)
		flat_arr = arr1.ravel()
		arr2=np.append(flat_arr,tipo)
		image_list.append(arr2)


cargar('train/Bug/',1)
cargar('train/Water/',2)
cargar('train/Fire/',3)
cargar('train/Grass/',4)
cargar('train/Rock/',5)
cargar('train/Electric/',6)
cargar('train/Ghost/',7)


kdtree=build_kdtree(image_list)

while True:
	n = input("Ingresa imagen:")
	if n == "salir":
	    break
	img = Image.open('train/'+n).convert('RGB')
	arr = np.array(img)
	arr1= arr.ravel()

	queue=Knearest(kdtree,arr1,10)

	print(most_frequent(queue))
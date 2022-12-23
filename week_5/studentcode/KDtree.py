import matplotlib.pyplot as mp
import scipy.spatial as spatial 
import random

x=[]
y=[]
for i in range(500): 
    x.append(random.uniform(0,1))
    y.append(random.uniform(0,1))

points=zip(x,y) #converts two lists in to a tuple
print(type(points))

pointsList=list(points)
print(pointsList)

for x, y in pointsList:
    print ("x={}, y={}".format(x, y))
    mp.scatter(x,y,color="black")

myTree=spatial.KDTree(pointsList)

pointsToCheck = (0.5, 0.1)

# query for one nearest neighbour
res = myTree.query(pointsToCheck)
print ("Nearest point is index {}, distance {}, coordinate {}".format(res[1], res[0], pointsList[res[1]]))

# query for multiple nearest neighbour
dist, ind = myTree.query(pointsToCheck, 25)

for i in range(len(dist)):
    nearPoint = pointsList[ind[i]]
    print ("{} Nearest point is index {}, distance {}, coordinate {}".format(i, ind[i], dist[i], nearPoint))
    xs=[pointsToCheck[0], nearPoint[0]]
    ys=[pointsToCheck[1], nearPoint[1]]
    mp.plot(xs,ys,color='blue')


mp.scatter(pointsToCheck[0], pointsToCheck[1],color="red")
#

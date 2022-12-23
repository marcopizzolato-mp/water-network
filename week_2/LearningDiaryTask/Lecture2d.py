from PointPlotter import PointPlotter
from ChainHandler import ChainLoader


xlo=0.0
xhi=1000.0
ylo=0.0
yhi=1000.0


# Create pp as an Object of the class "PointPlotter"
pp=PointPlotter()
# On pp calls the method set_axis
pp.set_axis(xlo, xhi, ylo, yhi)

# Loops that goes over all the Wiggles
for i in range(1,10):
    print ('\nThis is the Widget{}'.format(i))
    # call the function chain from ChainHandler and load the Wiggle as a Polyline object
    chain=ChainLoader("Wiggle"+str(i)+".txt")
    #on pp call "Plotpoints" method. As argument chain[0]._allPoints
    pp.plotPoint(chain[0]._allPoints, 'black')
    
    #call the method plotPolylines on the 
    pp.plotPolylines(chain[0].generalise(20.0), 'red')
    pp.show()

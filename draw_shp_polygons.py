from osgeo import ogr
import matplotlib.pyplot as plt
import sys

def plot_rings(geom):                  # plot
    ptsx = []
    ptsy = []
    for ring in geom:                  # loop all rings
        points = ring.GetPoints()      # get points in ring
        ptsx += [p[0] for p in points]
        ptsy += [p[1] for p in points]
    plt.plot(ptsx, ptsy, color='grey')

drvName = "ESRI Shapefile"
driver = ogr.GetDriverByName(drvName)  # a shapefile driver

driver = ogr.GetDriverByName("ESRI Shapefile")
if len(sys.argv) == 2:
    fname = sys.argv[1]                # file name input
else:
    print "Usage:", sys.argv[0], "FILE.shp"
    sys.exit()

vector = driver.Open(fname, 0)         # open input file
layer = vector.GetLayer(0)             # shapefiles use 0
for f in layer:
    geom = f.GetGeometryRef()          # geometry of feature
    geomtype = geom.GetGeometryName()
    if geomtype == "MULTIPOLYGON":
        for geom1 in geom:
            plot_rings(geom1)
    elif geomtype == "POLYGON":
        plot_rings(geom)
    else:
        pass                           # none polygon types
    f.Destroy()                        # remove input feature

vector.Destroy()                       # close the shapefile
plt.axis('scaled')
plt.savefig('us48prj.eps', bbox_inches='tight', pad_inches=0)
plt.show()

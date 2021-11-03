import sys
from osgeo import ogr                  # import OGR
                                       #
drvName = "ESRI Shapefile"             # driver format
driver = ogr.GetDriverByName(drvName)  # create a shapefile driver

if len(sys.argv)!=2:
    exit()

fname = sys.argv[1]
vector = driver.Open(fname, 0)         # open input file (0 for read only)
layer = vector.GetLayer(0)             # index is 0, as always for shapefiles
                                       #
def trans_rings(geom):                 # return a polygon 
    polygon = ogr.Geometry(
        ogr.wkbPolygon)                # create an ampty polygon
    nump = 0
    for ring in geom:                  # loop through all rings
        nump += len(ring.GetPoints())
    return nump

k = 0
num_points = 0
for f in layer:                        # loop all features in layer
    geom = f.GetGeometryRef()          # get the geometry of feature
    geomtype = geom.GetGeometryName()
    if geomtype == "MULTIPOLYGON":
        for geom1 in geom:
            num_points += trans_rings(geom1)
    elif geomtype == "POLYGON":
        num_points += trans_rings(geom)
    else:
        pass                           # other none polygon types

vector.Destroy()                       # close the input shapefile
print num_points

# version 2
#
# This version contains functions only for calling externally

from osgeo import ogr
import matplotlib.pyplot as plt
import matplotlib
import sys

def plot_lines(geom, edgecolor='grey', linewidth=0.5):
    points = geom.GetPoints()
    line = [[p[0], p[1]] for p in points]
    l = plt.Polygon(line, closed=False, fill=False, edgecolor=edgecolor, lw=linewidth)
    plt.gca().add_line(l)

def plot_rings(geom, facecolor='lightgrey', edgecolor='grey', linewidth=0.5,
               fill=True, alpha=None, axis=None):
    poly = []
    if edgecolor == 'same':
        edgecolor = facecolor
    if alpha is None:
        alpha = 1
    for ring in geom:                  # loop all rings
        points = ring.GetPoints()      # get points in ring
        poly += [[p[0], p[1]] for p in points]
    l = plt.Polygon(poly, closed=True, fill=fill,
                    facecolor=facecolor, lw=linewidth, edgecolor=edgecolor, alpha=alpha)
    if axis is None:
        plt.gca().add_line(l)
    else:
        axis.add_line(l)

def plot_geom(geom, facecolor='lightgrey', edgecolor='grey', linewidth=0.5,
              fill=True, alpha=None, axis=None):
    geomtype = geom.GetGeometryName()
    if geomtype == "MULTIPOLYGON":
        for geom1 in geom:
            print('MULTI!')
            plot_rings(geom1, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth,
                       alpha=alpha, axis=axis)
    elif geomtype == "POLYGON":
        plot_rings(geom, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth,
                   alpha=alpha, axis=axis)
    elif geomtype == "LINESTRING":       # none polygon types
        print('LINESTRING!')
        plot_linesx(geom, edgecolor='blue', linewidth=linewidth)
        pass

# layer: an OGR layer
# classes: integer class assignment for each feature
# colors: a list of colors for each class
def draw_layer(layer, classes=None, colors=None, edgecolor='grey', alpha=None, axis=None, linewidth=0.5):
    for f in layer:
        geom = f.GetGeometryRef()          # geometry of feature
        geomtype = geom.GetGeometryName()
        facecolor = 'lightgrey'
        if classes is not None and colors is not None:
            id = f.GetFID()
            facecolor = colors[classes[id]]
        if geomtype == "MULTIPOLYGON":
            for geom1 in geom:
                plot_rings(geom1, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha, axis=axis, linewidth=linewidth)
        elif geomtype == "POLYGON":
            plot_rings(geom, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha, axis=axis, linewidth=linewidth)
        elif geomtype == "LINESTRING":       # none polygon types
            plot_linesx(geom, edgecolor=edgecolor, linewidth=linewidth)
            pass


def rect_legend(x, y, w, h, xgap, axis, colors, ygap=0.1, edgecolor=None, intervals=None, order='descending', use_integers=True):
    k = len(colors)
    for i in range(k):
        if order=='descending':
            ii = i
        else:
            ii = k-i-1
        c = colors[ii]
        rect1 = matplotlib.patches.Rectangle((x, y+h*i), w, h, facecolor=c, edgecolor=edgecolor)
        axis.add_patch(rect1)
        label = ''
        if intervals is not None:
            if use_integers:
                label = '{0:.0f} - {1:.0f}'.format(intervals.intervals[ii].min, intervals.intervals[ii].max)
            else:
                label = '{0:.1f} - {1:.1f}'.format(intervals.intervals[ii].min, intervals.intervals[ii].max)
        axis.text(x+w+xgap, y+h*i+ygap, label)


def make_label(objs, digit):
    label = '['
    for i in range(len(objs)):
        label += '{0:.{l}f} '.format(objs[i], l=digit)
    label += ']'
    return label

def mark_make_label(x, y, ax, objs, digit=4):
    ax.text(x, y, make_label(objs, digit))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        fname = sys.argv[1]                # file name input
        drvName = "ESRI Shapefile"
        driver = ogr.GetDriverByName(drvName)  # a shapefile driver
        driver = ogr.GetDriverByName("ESRI Shapefile")
        vector = driver.Open(fname, 0)         # open input file
        layer = vector.GetLayer(0)             # shapefiles use 0
        draw_layer(layer)
        plt.axis('scaled')
        plt.show()
    else:
        print("Usage:", sys.argv[0], "FILE.shp")

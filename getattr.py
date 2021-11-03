from osgeo import ogr
def get_shp_attribute_by_name(shpfname, attrname):
    """
    Get attribute values by column name from a shapefile
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")
    vector = driver.Open(shpfname, 0)
    layer = vector.GetLayer(0)
    f = layer.GetFeature(0)
    val = []
    for i in range(layer.GetFeatureCount()):
        f = layer.GetFeature(i)
        val.append(f.GetField(attrname))
    return val

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "FILE.shp", 'column_name')
        sys.exit()

    fname = sys.argv[1]                # file name input
    varname = sys.argv[2]
    vals = get_shp_attribute_by_name(fname, varname)
    for v in vals:
        print(v)

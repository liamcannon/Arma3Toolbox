# Class structure, read-write methods and conversion functions for handling
# the ASCII Esri GRID raster format. Format specifications:
# https://en.wikipedia.org/wiki/Esri_grid


class ASC_Error(Exception):
    pass


class ASC_File():
    POS_CORNER = 0
    POS_CENTER = 1

    def __init__(self):
        self.pos = (self.POS_CORNER, 0, 0) # type, x, y
        self.cellsize = 1
        self.nodata = None
        self.data = []
    
    def assign_props(self, props):
        nrows = props.get("nrows")
        ncols = props.get("ncols")
        xllcorner = props.get("xllcorner")
        xllcenter = props.get("xllcenter")
        yllcorner = props.get("yllcorner")
        yllcenter = props.get("yllcenter")
        cellsize = props.get("cellsize")
        nodata = props.get("nodata_value")

        if ncols is None:
            raise ASC_Error("Missing ncols property")
        if nrows is None:
            raise ASC_Error("Missing nrows property")
        if cellsize is None:
            raise ASC_Error("Missing cellsize property")
        elif cellsize <= 0:
            raise ASC_Error("Invalid cellsize property")
        
        self.cellsize = cellsize

        if xllcorner is not None and yllcorner is not None:
            self.pos = (self.POS_CORNER, xllcorner, yllcorner)
        elif xllcenter is not None and yllcenter is not None:
            self.pos = (self.POS_CENTER, xllcenter, yllcenter)
        else:
            raise ASC_Error("Missing valid georeference")
        
        if nodata is not None:
            self.nodata = nodata

        return int(nrows), int(ncols)

    def assign_data(self, nrows, ncols, data):
        if len(data) != (nrows * ncols):
            raise ASC_Error("Data length not matching raster dimensions")

        row = []
        for item in data:
            row.append(item)
            
            if len(row) == ncols:
                self.data.append(row)
                row = []

    @classmethod
    def read(cls, file):
        output = cls()

        lines = file.readlines()

        props = {}
        data = []
        for line in lines:
            values = line.split()
            if len(values) == 2 and values[0][0].isalpha():
                props[values[0].lower()] = float(values[1])
            else:
                data.extend([float(item) for item in values])
        
        if not len(data) > 0:
            raise ASC_Error("Cannot import raster without data")
        
        nrows, ncols = output.assign_props(props)
        output.assign_data(nrows, ncols, data)
        
        return output
    
    @classmethod
    def read_file(cls, filepath):
        output = None
        with open(filepath, "r") as file:
            output = cls.read(file)
        
        return output
    
    def write(self, file):
        file.write("nrows %d\n" % len(self.data))
        file.write("ncols %d\n" % len(self.data[0]))
        pos_type, x, y = self.pos
        if pos_type == self.POS_CENTER:
            file.write("xllcenter %s\n" % str(x))
            file.write("yllcenter %s\n" % str(y))
        elif pos_type == self.POS_CORNER:
            file.write("xllcorner %s\n" % str(x))
            file.write("yllcorner %s\n" % str(y))
        file.write("cellsize %s\n" % str(self.cellsize))

        if self.nodata is not None:
            file.write("nodata_value %s\n" % str(self.nodata))

        for row in self.data:
            row_string = ["%.4f" % item for item in row]
            file.write(" ".join(row_string) + "\n")
    
    def write_file(self, filepath):
        with open(filepath, "wt") as file:
            self.write(file)

    def get_dimensions(self):
        nrows = len(self.data)
        if nrows == 0:
            return 0, 0
        
        ncols = len(self.data[0])

        return nrows, ncols
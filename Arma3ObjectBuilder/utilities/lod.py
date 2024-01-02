# Backend functions mainly used by the P3D I/O, and the LOD
# validation tool.


import re

import bmesh

from . import generic as utils
from . import data
from . import errors
from .logger import ProcessLogger


def has_ngons(mesh):
    for face in mesh.polygons:
        if len(face.vertices) > 4:
            return True
    
    return False


def is_contiguous_mesh(bm):
        for edge in bm.edges:
            if not edge.is_contiguous:
                return False
                
        return True


def get_lod_id(value):
    fraction, exponent = utils.normalize_float(value)

    if exponent < 3: # Escape at resolutions
        return 0, round(value)

    base_value = utils.floor(fraction)

    if exponent in [3, 16]: # LODs in these ranges have identifier values in the X.X positions not just X.0
        base_value = utils.floor(fraction, 1)

    index = data.lod_type_index.get((base_value, exponent), 30)
    resolution_position = data.lod_resolution_position.get(index, None)
    
    resolution = 0
    if resolution_position is not None:
        resolution = int(round((fraction - base_value) * 10**resolution_position, resolution_position))

    return index, resolution


def get_lod_signature(index, resolution):    
    if index == 0:
        return resolution
    
    index = list(data.lod_type_index.values()).index(index, 0)
    fraction, exponent = list(data.lod_type_index.keys())[index]
    
    resolution_position = data.lod_resolution_position.get(index, None)
    resolution_signature = 0
    if resolution_position is not None:
        resolution_signature = resolution * 10**(exponent - resolution_position)
    
    return fraction * 10**exponent + resolution_signature


def get_lod_name(index):
    return data.lod_type_names.get(index,data.lod_type_names[30])[0]


def format_lod_name(index, resolution):
    if data.lod_resolution_position.get(index, None) is not None:
        return "%s %d" % (get_lod_name(index), resolution)
        
    return get_lod_name(index)
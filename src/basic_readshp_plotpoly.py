"""
basic_readshp_plotpoly.py

reads a shapefile using the shapefile library, loops over imported shapes 
and plots polygons for each shape

Plotting is configured for use with state boundary shapefile from census.gov: 
  https://www.census.gov/geo/maps-data/data/cbf/cbf_state.html

Copyright (C) 2016  Chris Havlin, <https://chrishavlin.wordpress.com>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import shapefile
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

"""
 IMPORT THE SHAPEFILE 
"""
shp_file_base='cb_2015_us_state_20m'
dat_dir='../shapefiles/'+shp_file_base +'/'
sf = shapefile.Reader(dat_dir+shp_file_base)

print 'number of shapes imported:',len(sf.shapes())
print ' '
print 'geometry attributes in each shape:'
for name in dir(sf.shape()):
    if not name.startswith('__'):
       print name

"""
       PLOTTING
"""

""" PLOTS A SINGLE SHAPE """
plt.figure()
ax = plt.axes()
ax.set_aspect('equal')

shape_ex = sf.shape(5) # could break if selected shape has multiple polygons. 

# build the polygon from exterior points
polygon = Polygon(shape_ex.points)
patch = PolygonPatch(polygon, facecolor=[0,0,0.5], edgecolor=[0,0,0], alpha=0.7, zorder=2)
ax.add_patch(patch)

# use bbox (bounding box) to set plot limits
plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
plt.ylim(shape_ex.bbox[1],shape_ex.bbox[3])

""" PLOTS ALL SHAPES AND PARTS """
plt.figure()
ax = plt.axes() # add the axes
ax.set_aspect('equal')

icolor = 1
for shape in list(sf.iterShapes()):

    # define polygon fill color (facecolor) RGB values:
    R = (float(icolor)-1.0)/52.0
    G = 0 
    B = 0 

    # check number of parts (could use MultiPolygon class of shapely?)
    nparts = len(shape.parts) # total parts
    if nparts == 1:
        polygon = Polygon(shape.points)
        patch = PolygonPatch(polygon, facecolor=[R,G,B], alpha=1.0, zorder=2)
        ax.add_patch(patch)

    else: # loop over parts of each shape, plot separately
        for ip in range(nparts): # loop over parts, plot separately
            i0=shape.parts[ip]
            if ip < nparts-1:
               i1 = shape.parts[ip+1]-1
            else:
               i1 = len(shape.points)
            
            polygon = Polygon(shape.points[i0:i1+1])
            patch = PolygonPatch(polygon, facecolor=[R,G,B], alpha=1.0, zorder=2)
            ax.add_patch(patch)

    icolor = icolor + 1

plt.xlim(-130,-60)
plt.ylim(23,50)
plt.show()


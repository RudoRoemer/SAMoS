# * *************************************************************
# *  
# *   Soft Active Mater on Surfaces (SAMoS)
# *   
# *   Author: Rastko Sknepnek
# *  
# *   Division of Physics
# *   School of Engineering, Physics and Mathematics
# *   University of Dundee
# *   
# *   (c) 2013, 2014
# * 
# *   School of Science and Engineering
# *   School of Life Sciences 
# *   University of Dundee
# * 
# *   (c) 2015
# * 
# *   Author: Silke Henkes
# * 
# *   Department of Physics 
# *   Institute for Complex Systems and Mathematical Biology
# *   University of Aberdeen  
# * 
# *   (c) 2014, 2015
# *  
# *   This program cannot be used, copied, or modified without
# *   explicit written permission of the authors.
# * 
# * ***************************************************************


#
#  Cell class
#
#  Cell list class
#
#

from copy import deepcopy
from Geometry import *

# Single cell of the CellList object
# it has its own index (label), position r (==(rx,ry,rz)) and extension L (==(Lx,Ly,Lz))
class Cell:
  
  def __init__(self, idx, r, L):
    self.idx = idx
    self.r = r
    self.L = L
    self.indices = []
    # Labels (indices) of the neighbouring cells
    self.neighbors = []
    
  def add_particle(self, idx):
    self.indices.append(idx)
    
  def printMe(self):
    print "I am cell " + str(self.idx)
    print "My position is: " + str(self.r)
    print "My particles are: " + str(self.indices)
    print "My neighbour cells are: " + str(self.neighbors)
    
  
class CellList:
  # Create my boxes
  def __init__(self,geom, r_cut):
    self.geom=geom
    self.r_cut = r_cut
    #self.box = box
    self.cell_indices = {}
    # The size of the box collection is always set by the system box size
    # Which is what is used in the C++ code as well
    #Lx, Ly, Lz = self.box
    #self.Lx, self.Ly, self.Lz = Lx, Ly, Lz 
    # Number and linear extensions of the boxes in all three dimensions
    self.nx = int(self.geom.Lx/r_cut)
    self.ny = int(self.geom.Ly/r_cut)
    self.nz = int(self.geom.Lz/r_cut)
    self.dx = self.geom.Lx/float(self.nx)
    self.dy = self.geom.Ly/float(self.ny)
    self.dz = self.geom.Lz/float(self.nz)
    # total number of cells
    n_cell = self.nx*self.ny*self.nz
    print "Created CellList with " + str(n_cell) + " boxes."
    # Cell list is a python list
    self.cell_list = [None for i in range(n_cell)]
    for i in range(self.nx):
      x = -0.5*self.geom.Lx + float(i)*self.dx
      for j in range(self.ny):
        y = -0.5*self.geom.Ly + float(j)*self.dy
        for k in range(self.nz):
          z = -0.5*self.geom.Lz + float(k)*self.dz
          # Cell labeling scheme: for each x, do all y, and for all y, do all z
          idx = self.ny*self.nz*i + self.nz*j + k
          # Create new cell with index, position and size
          self.cell_list[idx] = Cell(idx,(x,y,z),(self.dx,self.dy,self.dz))
          # Find neighbours: up to one above and below in all directions, moduly PBC
          # Note that a cell is its own neigbhbour ...
          self.PeriodicNeighbours(idx,i,j,k)
         
  # Function appropriate to periodically wrap cell list boxes
  # or not entering the cell if it doesn't exist
  def PeriodicNeighbours(self,idx,i,j,k):
     for ix in range(-1,2):
	for iy in range(-1,2):
	    for iz in range(-1,2):
	      dobox=True
	      iix, iiy, iiz = i + ix, j + iy, k + iz
	      if (iix == self.nx): 
		if self.geom.periodic:
		  iix = 0
		else:# do not wrap - there should not be a box here!
		  dobox=False
	      if (iiy == self.ny): 
		if self.geom.periodic:
		  iiy = 0
		else:# do not wrap - there should not be a box here!
		  dobox=False
	      if (iiz == self.nz): 
		if self.geom.periodic:
		  iiz = 0
		else:# do not wrap - there should not be a box here!
		  dobox=False
	      if (iix < 0):  
		if self.geom.periodic:
		  iix = self.nx - 1
		else:# do not wrap - there should not be a box here!
		  dobox=False
	      if (iiy < 0):  
		if self.geom.periodic:
		  iiy = self.ny - 1   
		else:
		  dobox=False
	      if (iiz < 0):  
		if self.geom.periodic:
		  iiz = self.nz - 1  
		else:
		  dobox=False
	      # A neighbour is just a label of the neighbouring cell
	      if dobox:
		self.cell_list[idx].neighbors.append(self.ny*self.nz*iix + self.nz*iiy + iiz)
			
  # Get the cell label for a given position vector v
  def get_cell_idx(self, rval):
    rval=self.geom.ApplyPeriodic1d(rval)
    xmin, ymin, zmin = -0.5*self.geom.Lx, -0.5*self.geom.Ly, -0.5*self.geom.Lz
    i, j, k = int((rval[0]-xmin)/self.dx), int((rval[1]-ymin)/self.dy), int((rval[2]-zmin)/self.dz) 
    cell_idx = self.ny*self.nz*i + self.nz*j + k
    return cell_idx
  
  # Add a particle to a cell: This means compute its cell index (if not given already)
  # Then add it with add_vertex of cell
  # Give the index to the list of cell indices: this particle is in this cell
  def add_particle(self, rval, idx, cell_idx = None):
    if cell_idx == None:
      cell_idx = self.get_cell_idx(rval)
    else:
      cell_idx = cell_index    
    self.cell_list[cell_idx].add_particle(idx)
    self.cell_indices[idx] = cell_idx
    #print "Added particle " + str(idx) + " to cell " + str(cell_idx)
    
  # Nuke the contents of the whole cell list
  def wipe(self):
    for cell in self.cell_list:
      cell.vertices = []
      
  # Get the neighbours of particle at position rval
  # This means looking at the neighbour boxes (including oneself), and copying their list of neighbours into one
  # single neighbour list
  def get_neighbours(self,rval):
      cell_index = self.get_cell_idx(rval)
      #print "My cell is: " + str(cell_index)
      neighbors = []
      for idx in self.cell_list[cell_index].neighbors:
	  #print "Cell " + str(idx) + " contributes neighbours " + str(self.cell_list[idx].indices)
          neighbors.extend(deepcopy(self.cell_list[idx].indices))
      return neighbors
    
    
  def printMe(self):
      for cell in self.cell_list:
	cell.printMe()
      
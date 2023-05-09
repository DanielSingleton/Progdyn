import numpy as np
import sys
from math import cos, pi, sin
np.set_printoptions(precision=2)

arglist = []
for arg in sys.argv[1:]:
   arglist.append(arg)
assert len(arglist) > 0,"You need to specify an input file"
atSym = []; lengthlist = []; anglelist = []; dihedrallist = []; atcon_l = []; atcon_a = []; atcon_d = []

with open(arglist[0], 'r') as f:
   for line in f:
      if len(line) > 5:
         words = line.split()
         assert len(words[6]) > 0
         atSym.append(words[0])
         lengthlist.append(float(words[1]))
         anglelist.append(float(words[2]))
         dihedrallist.append(float(words[3]))
         atcon_l.append(int(words[4])-1)
         atcon_a.append(int(words[5])-1)
         atcon_d.append(int(words[6])-1)

anglelist = [pi * (180 - x) / 180 for x in anglelist]
dihedrallist = [pi * x / 180 for x in dihedrallist]
numAtoms = int(len(atSym))
geoArr = np.zeros([numAtoms,3])

for i in range(1,numAtoms):
   if i == 1:
      geoArr[1,0] = lengthlist[i] 
   if i == 2:
      geoArr[i,0] = geoArr[atcon_l[i],0] + lengthlist[i]*cos(anglelist[i])
      geoArr[i,2] = geoArr[atcon_l[i],2] + lengthlist[i]*sin(anglelist[i])
   if i > 2:
      ab = geoArr[atcon_a[i],:] - geoArr[atcon_d[i],:] 
      bc = geoArr[atcon_l[i],:] - geoArr[atcon_a[i],:]
      bc /= np.linalg.norm(bc)
      ucaret = np.cross(ab, bc)
      ucaret = ucaret / np.linalg.norm(ucaret)
      cd0 = bc * lengthlist[i]
      cd1 = cos(anglelist[i])*cd0 + np.cross(ucaret,sin(anglelist[i])*cd0) + np.dot(cd0,ucaret)*ucaret*(1-cos(anglelist[i]))
      cd2 = cos(dihedrallist[i])*cd1 + np.cross(bc,sin(dihedrallist[i])*cd1) + np.dot(cd1,bc)*bc*(1-cos(dihedrallist[i]))
      geoArr[i,:] = geoArr[atcon_l[i],:] + cd2

for i in range(0,numAtoms):
   print(atSym[i],"% 12.9f" % geoArr[i,0], "% 12.9f" % geoArr[i,1], "% 12.9f" % geoArr[i,2])


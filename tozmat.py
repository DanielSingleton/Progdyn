import numpy as np
import sys
from math import cos, pi, sin, sqrt

def distance(Atom1,Atom2):
  if Atom1 < 0 or Atom2 < 0:
      return 0.
  return sqrt((geoArr[Atom1,0]-geoArr[Atom2,0])**2 + (geoArr[Atom1,1]-geoArr[Atom2,1])**2 + (geoArr[Atom1,2]-geoArr[Atom2,2])**2)

def angle(Atom1,Atom2,Atom3):
   ba = geoArr[Atom1,:] - geoArr[Atom2,:]
   bc = geoArr[Atom3,:] - geoArr[Atom2,:]
   cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
   angle = np.arccos(cosine_angle)
   return np.degrees(angle)
   
def dihedral(Atom1,Atom2,Atom3,Atom4):
    p0 = geoArr[Atom1,:]
    p1 = geoArr[Atom2,:]
    p2 = geoArr[Atom3,:]
    p3 = geoArr[Atom4,:]
    b0 = -1.0*(p1 - p0)
    b1 = p2 - p1
    b2 = p3 - p2
    b1 /= np.linalg.norm(b1)
    v = b0 - np.dot(b0, b1)*b1
    w = b2 - np.dot(b2, b1)*b1
    x = np.dot(v, w)
    y = np.dot(np.cross(b1, v), w)
    return np.degrees(np.arctan2(y, x))

arglist = []
for arg in sys.argv[1:]:
   arglist.append(arg)
assert len(arglist) > 0,"You need to specify an input file"
atSym = []; lengthlist = []; anglelist = []; dihedrallist = []; atcon_l = []; atcon_a = []; atcon_d = []

lengthlist = [0.]
anglelist = [0., 0.]
dihedrallist = [0., 0., 0.]
atcon_l = [-1]
atcon_a = [-1, -1]
atcon_d = [-1, -1, -1]
atom_x = []
atom_y = []
atom_z = []
distance_adjustment = {'H': 0.5, 'O': 0.3}


with open(arglist[0], 'r') as f:
   for line in f:
      if len(line) > 5:
         words = line.split()
         assert len(words[3]) > 0,"Problem with input file format. It should be ElementSymbol number number number"
         atSym.append(words[0])
         atom_x.append(float(words[1]))
         atom_y.append(float(words[2]))
         atom_z.append(float(words[3]))

numAtoms = int(len(atSym))
geoArr = np.array(list(zip(atom_x,atom_y,atom_z)))

#internally leaving the numbering starting at zero, but will add one for all output
# the atcons and length for the first atom are assigned in the initialization
for i in range(1,numAtoms): 
   shortest_distance = 100
   closest_atom = 0
   for j in range(0,i):
      if (distance(i,j) + distance_adjustment.get(atSym[j], 0.0)) < shortest_distance:
         shortest_distance = distance(i,j)
         closest_atom = j
   lengthlist.append(shortest_distance)
   atcon_l.append(closest_atom)

for i in range(2,numAtoms):
   shortest_distance = 100
   closest_atom = 0
   for j in range(0,i):
      consistency_pref = 0
      if j != atcon_l[i]:
         if j == atcon_l[atcon_l[i]]:
            consistency_pref = 1
         if (distance(j,atcon_l[i]) + distance_adjustment.get(atSym[j], 0.0) - consistency_pref) < shortest_distance:
            shortest_distance = distance(j,atcon_l[i]) + distance_adjustment.get(atSym[j], 0.0) - consistency_pref
            closest_atom = j
   if atcon_l[atcon_l[i]] > 1:
      if atcon_l[atcon_l[i]] != i:
         closest_atom = atcon_l[atcon_l[i]]
#        print("default angle atom",i+1,atcon_l[i]+1,closest_atom+1)
   atcon_a.append(closest_atom)
   anglelist.append(angle(i,atcon_l[i],atcon_a[i]))

for i in range(3,numAtoms):
   shortest_distance = 100
   closest_atom = 0
   for j in range(0,i):
      consistency_pref = 0
      if j != atcon_l[i] and j != atcon_a[i]:
         if j == atcon_l[atcon_a[i]]:
            consistency_pref = 1
         if (distance(j,atcon_a[i]) + distance_adjustment.get(atSym[j], 0.0) - consistency_pref) < shortest_distance:
            shortest_distance = distance(j,atcon_a[i]) + distance_adjustment.get(atSym[j], 0.0) - consistency_pref
            closest_atom = j
   if atcon_l[atcon_a[i]] > 0:
      if atcon_l[atcon_a[i]] != i:
         if atcon_l[atcon_a[i]] != atcon_l[i]:
            closest_atom = atcon_l[atcon_a[i]]
#           print("default dihedral atom",i+1,atcon_l[i]+1,atcon_a[i]+1,closest_atom+1)
   atcon_d.append(closest_atom)
   dihedrallist.append(dihedral(i,atcon_l[i],atcon_a[i],atcon_d[i]))

for i in range(0,numAtoms):
   print(atSym[i],"% 12.9f" % lengthlist[i], "% 10.7f" % anglelist[i], "% 10.7f" % dihedrallist[i], "% 4s" % str(atcon_l[i] + 1), "% 4s" % str(atcon_a[i] + 1), "% 4s" % str(atcon_d[i] + 1))



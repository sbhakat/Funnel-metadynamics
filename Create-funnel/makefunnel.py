#!/usr/bin/python
from math import *
import sys

#Usage: makefunnel.py Zcc Rcyl alpha kappa Zmin Zmax Rmax nbinZ nbinR outputfile

#Funnel parameters according to PNAS paper:
#   Zcc,Rcyl in Angstrom
#   alpha in degress

#Force constant of harmonic wall of the funnel:
#   kappa in kJ/(mol*nm^2)

#Grid parameters:
#   Zmin,Zmax,Rmax in nm (grid goes from Zmin to Zmax and from 0 to Rmax)
#   nbinZ,nbinR  grid size in each dimension  (400, 200 should be completely safe)



Zcc=float(sys.argv[1])
Rcyl=float(sys.argv[2])
alpha=float(sys.argv[3])
kappa=float(sys.argv[4])
Zmin=float(sys.argv[5])
Zmax=float(sys.argv[6])
Rmax=float(sys.argv[7])
nbinZ=int(sys.argv[8])
nbinR=int(sys.argv[9])
of=open(sys.argv[10], 'w')

def potential(z,r):   #  z>=0, r>=0
    #First compute radius of funnel for given value of z
    if z>Zcc:
        Rfun=Rcyl
    else:
        Rfun=Rcyl+(Zcc-z)*tan(alpha/180*pi)
    #Then define a harmonic upper wall on r starting at the funnel radius
    if r>Rfun:
        return kappa/2*(r-Rfun)**2
    else:
        return 0


of.write('#! FORCE 0\n#! NVAR 2\n#! TYPE 1 1\n#! BIN %d %d\n#! MIN %f 0.0\n#! MAX %f %f\n#! PBC 0 0\n' % (nbinZ,nbinR,-Zmax,Zmax,Rmax))

for i in range(nbinZ+1):
    z=Zmin+i*((Zmax-Zmin)/nbinZ)
    for j in range(nbinR+1):
        r=j*(Rmax/nbinR)
        of.write("%.5f %.5f %.5f\n" % (z, r, potential(abs(z),r) ))
    of.write("\n")   #uncomment to get a file that can be plotted by gnuplot: set pm3d map; sp 'funnel.dat'


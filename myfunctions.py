def read_xyz(fname):
   ##################################################
   # read_xyz:	Reads xyz file 'fname'
   # Inputs:	fname, the file name of the xyz file to read
   # Outputs: 	AtomList (string list), (list of atomic labels); 
   # 		Coords (float list), coordinates as column vector with the format X1,Y1,Z1,X2,Y2,Z2,...
   ##################################################
   with open(fname,'r') as f:			# open file   
      AtomList=[]; Coords=[]
      c=0
      for i in range(0,2):
         f.next()				# Skip first 2 lines
      for line in f:				
         AtomList.append(line.split()[0]) 	# List of atomic labels
         for i in range(1,4):
            Coords.append(float(line.split()[i]))
   ##################################################dd
   return AtomList,Coords


def read_displacements(Nat,imode):
   ##################################################
   # read_displacements: Reads displacement coordinates for mode 'imode' from 'normalmodes.txt'
   # Inputs: 	Nat (int), total number of atoms
   #		imode (int), the displacements are taken from mode number 'imode'
   # Outputs:	Displacements (float list), single column of displacement coordinates (length 3*Nat)
   ##################################################
   # Definitions
   N = 3*Nat  # Number of coordinates
   # Error checks
   if Nat==2:
      Nmode=2
   elif Nat>2:
      Nmode=N-6
   else:
      print "ERROR: Something wrong with number of atoms"
      print "Are there <2 atoms?"
      return
   
   if imode>=1 and imode<=Nmode:
      print "Reading displacements for mode " + str(imode)
   else:
      print 'ERROR: imode out of range (1,Nmode).'
      return
   # Known pattern of g09 frequencies output file...
   row = int((imode-1)/5)
   a = (row+1)*7 + row*N
   b = (row+1)*(7 + N)
   d = row*5
   # Append displacements from file to column vector 'Displacements'
   c=0
   Displacements=[]
   with open('normalmodes.txt','r') as f:
      for line in f:
         c=c+1
         if c>a and c<=b:
            Displacements.append(float(line.split()[imode+2-d]))
   ##################################################
   return Displacements


def displace_coords(xyzfile,imode,Factor):
   ##################################################
   # displace_coords: Displace coords from xyz file 'xyzfile' along mode 'imode' (0<int<=Nmode) by 'Factor' (float)
   # Inputs:	xyzfile (str), the xyz file to displace the coordinates from (e.g. the equilibrium geometry)
   #		imode (int), the coordinates are displaced along mode number 'imode'
   # 		Factor (float), the coordinates are displaced along mode number 'imode' by 'Factor' atomic units  
   # Outputs:	'displaced_coords.xyz' (file), xyz file containing the displaced coordinates in units of Angstroms
   ##################################################
   au2ang = 0.529177249			# Bohr to Angstrom conversion factor
   AtomList,R0=read_xyz(xyzfile)	# Read AtomList (vector of length Nat) and R0 (vector of length 3*Nat)
   Nat=len(AtomList)			# Number of atoms 
   Displc=read_displacements(Nat,imode)	# Read normal mode displacements (vector of length 3*Nat)
   
   with open('displaced_coords.xyz','w') as f:
      f.write(str(Nat)+'\n')				# The first line of an xyz file contains only the number of atoms
      f.write('Displaced Coordinates\n')		# The second line is blank or contains a title string (convention)
      for i in range(0,3*Nat):				# Loop over vectors of lentgh 3*Nat
         if i%3==0:					# Indices 0,3,6,...
            Atom=AtomList[i/3]				# Read atom labels (at indices 0,1,2,... every i=0,3,6,...)
            x = R0[i] + (Factor*Displc[i])*au2ang 	# Displaced x coordinate
         elif (i-1)%3==0:				# Indices 1,4,7,...
            y = R0[i] + (Factor*Displc[i])*au2ang	# Displaced y coordinate
         elif (i-2)%3==0:				# Indices 2,5,8,...
            z = R0[i] + (Factor*Displc[i])*au2ang	# Displaced z coordinate
            f.write( Atom + '  ' + str(x) + '  ' + str(y) + '  ' + str(z) + '\n')	# Write out Lines containing atom labels and x,y,z coordinates
   ################################################## 
   return


def read_gwpcentres(Nstate,istate):
   ##################################################
   # Read displacement factors from file 'gwpcentres' for state 'istate'.
   # Inputs: 	Nstate (int), the total number of states
   #		istate (int), the state to read
   # Outputs:	Time (float list), list of time in atomic units 
   # 		v1,v2,v3,v4 (float lists), Lists of displacement factors for modes 1-4
   # At the moment hard-coded 4 modes, so can only be used when there are exactly 4 modes!
   ##################################################
   f=open('gwpcentres','r')
   lines=f.readlines()
   Time=[]; v1=[]; v2=[]; v3=[]; v4=[];
   c=0
   with open('gwpcentres','r') as f:
      for line in f:
         c=c+1
         if c>1:
            if (c-2)%(2*Nstate+1)==0:
               Time.append(float(line.split()[1]))         # List of time in atomic units
            elif (c+3-2*istate)%(2*Nstate+1)==0:	   # This fits the formatting of the gwpcentres file
               v1.append(float(line.split()[0]))
               v2.append(float(line.split()[1]))
               v3.append(float(line.split()[2]))
               v4.append(float(line.split()[3]))
   ##################################################
   return Time,v1,v2,v3,v4 



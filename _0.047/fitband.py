import numpy as np
import matplotlib.pyplot as plt
import os 


import sys
dftb_path="/home/leandro/Documents/dftb+/dftb+"


def molecule(molecula,dftbin):
    for archivos in ["band.out","detailed.out"]:
        try:
            os.remove(archivos)
        except OSError:
            pass

    os.system("xyz2gen "+molecula+".xyz")
    g=open("dftb_in.hsd","w")
    g.write("Geometry = GenFormat {\n<<< "+molecula+".gen"+"\n}\n")
    f=open(dftbin,"r")
    for line in f:
        g.write(line)
    
    g.close()
    f.close()
    
    os.system(dftb_path+" > tmp.log")
    f=open("band.out","r")
    
    E=[]
    line=f.readline()
    line=f.readline()
    s=line.split()
    ocup=float(s[1])
    
    while (ocup>0.01):
        E.append(float(s[0]))
        line=f.readline()
        s=line.split()
        ocup=float(s[1])
        
   
    f.close()
    return np.array(E)

def dft_orbital_a(archivo):
   f=open(archivo,"r")
   line=f.readline()
   while("SPIN UP ORBITALS" not in line):
       line=f.readline()
   line=f.readline()
   string=f.readline()
   s=string.split()
   fxyz=np.array(float(s[3]))
   string=f.readline()
   s=string.split()
   ocup=float(s[1])
   while (ocup >0.01):
       fxyz=np.hstack((fxyz,float(s[3])))
       string=f.readline()
       s=string.split()
       ocup=float(s[1])
       
       
   f.close()
   return  fxyz

def molec(xyz,dftbin,log):
    a=molecule(xyz,dftbin)
    dft=dft_orbital_a(log)
    i=len(a)
    a=(a-a[-1])
    dft=(dft[-i:]-dft[-1])
    return sum(abs(a-dft))/a.size

def band(qeband,dftb_in,qe_minband,qe_maxband,dftb_minband,dftb_maxband):
    for archivos in ["salida_tot.dat","band.out","detailed.out"]:
        try:
            os.remove(archivos)
        except OSError:
            pass
           
    
    b=np.loadtxt(qeband)
    b=np.sort(b)
    b=b[:,qe_minband:qe_maxband]
    a=100*np.ones(np.shape(b))
    os.system("cp "+dftb_in+" dftb_in.hsd")
    os.system(dftb_path+" > tmp.log")     
    os.system("dp_bands band.out salida 2> /dev/null" )
    
    Efermi=0.
    try:
        if(os.stat("detailed.out").st_size != 0):
            f=open("detailed.out","r")
            line=f.readline()
            while("Fermi energy:" not in line):
                line=f.readline()
            e=line.split()
            Efermi=e[4]
            f.close()  
        
    except OSError:
        pass
        
    try:
        a=np.loadtxt("salida_tot.dat")
        a=a[:,dftb_minband:dftb_maxband]
    except IOError:
        pass
            
    
    
    fermi=float(Efermi)*np.ones(np.shape(a))
    a=a-fermi
    
    x=np.sum(np.absolute(a-b))/a.size
    return x



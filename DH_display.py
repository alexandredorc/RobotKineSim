import numpy as np 
from math import cos, sin, pi

# fonction qui calcule la matrice DH pour chaque transformation avec a, alpha, d, theta.
def Trans_mat(a,alpha,d, theta):
    res=np.array([[cos(theta),-sin(theta),0,a]
              ,[sin(theta)*cos(alpha), cos(theta)*cos(alpha),-sin(alpha),-sin(alpha)*d]
              ,[sin(theta)*sin(alpha),cos(theta)*sin(alpha),cos(alpha),cos(alpha)*d]
              ,[0,0,0,1]])

    return res

def deg2rad(deg):
    res=[]
    for d in deg: 
        res.append(180*d/pi)
    return res

def display_trans(DH_mat,theta):
    P=[0,0,0,1]

    #matrice identité
    Id=np.eye(4)
    count=0
    #multiplication des matrice DH successive tel que T01*T12*....Tn-1n
    for dh in DH_mat:
        Id=np.dot(Id,Trans_mat(dh[0],dh[1],dh[2],dh[3]))
        print("matrice T"+str(count)+str(count+1),Trans_mat(dh[0],dh[1],dh[2],dh[3]))
        count+=1
    T06=Id
    print("matrice de transfert global",T06)

    #position de l'effecteur par apport à la base
    Pf=np.dot(T06,P)
    print("point final",Pf)

# angles de chaque joint
#thetas=deg2rad([19.48,-30.410, -12.38, 0, -47.21, 19.48])
thetas= [0,0,0,0,0,0]
print(thetas)
# description des paramètre pour chaque tranformation
DH_mat=np.array([[ 0 ,   0  ,  0   ,thetas[0]]
                ,[ 0 ,pi/2, 169.5 ,thetas[1]]
                ,[ 221.325, 0  , 0 ,thetas[2]]
                ,[ 35.406  ,-pi/2,235 ,thetas[3]]
                ,[ 0  , pi/2, 0 ,thetas[4]]
                ,[ 9.25  ,pi/2, 41.2,thetas[5]]])
print("hello world")
#point initial
P=[0,0,0,1]

#matrice identité
Id=np.eye(4)

#multiplication des matrice DH successive tel que T01*T12*....Tn-1n
for dh in DH_mat:
    Id=np.dot(Id,Trans_mat(dh[0],dh[1],dh[2],dh[3]))
    #print(Trans_mat(dh[0],dh[1],dh[2],dh[3]))
T06=Id
print(T06)

#position de l'effecteur par apport à la base
Pf=np.dot(T06,P)
print(Pf)
print((Pf*10000).astype(int)/10000.0)




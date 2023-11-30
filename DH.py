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

def generateDH(DH_mat):
    # description des paramètre pour chaque tranformation
    """DH_mat=np.array([[ 0     ,   0 , 0   ,thetas[0]]
                    ,[ 0.050 ,-pi/2, 0   ,thetas[1]]
                    ,[ 0.425 , 0   ,0.050,thetas[2]]
                    ,[ 0     ,-pi/2,0.425,thetas[3]]
                    ,[ 0     , pi/2, 0   ,thetas[4]]
                    ,[ 0     , -pi/2, 0.1 ,thetas[5]]])"""
   
    res=[]

    #matrice identité
    Id=np.eye(4)
    res.append(Id)
    #multiplication des matrice DH successive tel que T01*T12*....Tn-1n
    for dh in DH_mat:
        Id=np.dot(Id,Trans_mat(dh[0],dh[1],dh[2],dh[3]))
        res.append(Id)
        
    return res
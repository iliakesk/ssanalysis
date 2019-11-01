# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 11:12:38 2019

@author: Ilias
"""

import numpy as np
import pandas as pd
import ireact3d as ir3


class Member():
    
    def __init__(self, name, start, stop, theta, section, group = "beam", release=None):# "beam" or "column"
        
        self.start_node = start
        self.stop_node = stop
        self.name = name
        self.L = self.length(start, stop)
        self.theta = theta
        self.release=release
        if release!=None:
            self.r_released = self.releaseEdge(release) #r_released to prwhn Rr
#        rigid node den exw valei?->na dw pws ylopoieitai
        self.rigid_node = None
        self.axes = self.localAxes(start, stop, self.theta)
        self.rotv, self.rotation_matrix = self.rotationMatrix(self.axes)
        self.section = section # section is an object of class Section
        self.group = group
#        self.b
#        self.h

    def get_K_local(self, L, A, E, G, Ix, Iy, Iz):        
        '''Returns the local stiffness matrix of the member'''
        if self.release != None:
            return self.get_K_released(self, self.release)
        else:
            return self.get_K(self)
            
    def get_K(self, L, A, E, G, Ix, Iy, Iz):
        "Returns the basic stiffness matrix of the member, without releases etc"
        K =np.zeros(shape=(12,12))
        K[0][0]=K[6][6] = E*A/L
        K[1][1]=K[7][7] = 12*E*Iz/(L**3)
        K[2][2]=K[8][8] = 12*E*Iy/(L**3)
        K[3][3]=K[9][9] = G*Ix/L
        K[4][4]=K[10][10] = 4*E*Iy/L
        K[5][5]=K[11][11] = 4*E*Iz/L
        K[1][5]=K[5][1]=K[1][11]=K[11][1] = 6*E*Iz/(L**2)
        K[7][11]=K[11][7]=K[5][7]=K[7][5] = -6*E*Iz/(L**2)
        K[4][8]=K[8][4]=K[8][10]=K[10][8] = 6*E*Iy/(L**2)
        K[2][4]=K[4][2]=K[2][10]=K[10][2] = -6*E*Iy/(L**2)
        K[0][6]=K[6][0]=-K[0][0]
        K[1][7]=K[7][1]=-K[1][1]
        K[2][8]=K[8][2]=-K[2][2]
        K[3][9]=K[9][3]=-K[3][3]
        K[4][10]=K[10][4]=K[4][4]/2
        K[5][11]=K[11][5]=K[5][5]/2
        return K

    def get_K_released(self, release):
        """Returns the stiffness matrix of the member if the member has any kind of edge release
        Inserts two new attributes, rels which is the number of rels and the tM, which is the
        transformation matrix"""
        R = self.rotation_matrix
        RT = np.linalg.inv(R)
        K = self.get_K()
        RrT = np.linalg.inv(R)
        K_released = np.dot(RrT,np.dot(K,R))
        Krglob = np.dot(RT,np.dot(K_released,R))
# xreiazontai kia allou ta self.rels , self.tM kai self.Kt ?????????????????????
        self.rels, self.tM = self.transformReleases(release)
        tMT = np.linalg.inv(self.tM)
        Kt = np.dot(self.tM,np.dot(Krglob,tMT))
        self.Kt = Kt
        tKt11 = np.linalg.pinv(Kt[:self.rels,:self.rels])
        Kt12 = Kt[:self.rels,self.rels:]
        Kt21 = Kt[self.rels:,:self.rels]
        Kt22 = Kt[self.rels:,self.rels:]
        K_released = Kt22 - np.dot(Kt21,np.dot(tKt11,Kt12))
        indexes = []
        for i, r in enumerate(release):
            if r==1:
                indexes.append(i)
        for i in indexes:
            K_released = np.insert(K_released, i, 0, axis=1)
        for i in indexes:
            K_released = np.insert(K_released, i, np.zeros(12), axis=0)
        return K_released
        
    def releaseEdge(self, release):
        """If a member has a released edge the function returns the rotation matrix
        of the edge"""
        release_angles = release[2]#[0,pi/3,0,0,0,0]
        return self.edgeRotationMatrix(release_angles)

    def get_K_global(self): #R = ELEMENTS[member].rotMatrix
        """Returns the global stiffness matrix of the member"""
        R = self.rotation_matrix
        if self.rigid_node == None:
            local_K = self.get_K_local()
        else:
            local_K = self.get_K_rigid()
        RT = np.linalg.inv(R)
        return np.dot(RT,np.dot(local_K, R))

    def get_K_rigid(self):
        K = self.get_K_local()
        rn = self.rigid_node#edw thelei kati allo giati pleon to
#        RigidNode den yfistatai alla einai attribute apo kapoio class
        rnstart = rn[0]
        rnend = rn[1]
        ei = np.identity(12)
        ei[1][5] = rnstart[0]
        ei[2][4] = (-1)*rnstart[0]
        ei[0][5] = (-1)*rnstart[1]
        ei[2][3] = rnstart[1]
        ei[0][4] = rnstart[2]
        ei[1][3] = (-1)*rnstart[2]
        ei[7][11] = rnend[0]
        ei[8][10] = (-1)*rnend[0]
        ei[6][11] = (-1)*rnend[1]
        ei[8][9] = rnend[1]
        ei[6][10] = rnend[2]
        ei[7][9] = (-1)*rnend[2]
        eiT = np.linalg.inv(ei)
        K_rig = np.dot(eiT,np.dot(K,ei))
        return K_rig


    def length(self, start, stop):
        '''Takes input the names of the nodes eg n1, n2 and returns the length of the member'''
        length = np.sqrt([(stop[0]-start[0])**2 + (stop[1]-start[1])**2 + (stop[2]-start[2])**2])
        return length[0]

        
    def localAxes(self, start, stop, theta):
        '''Returns the unit vectors of the local axes of the member'''
        u = np.array([stop[i]-start[i] for i in range(3)])
        x_local = u/np.linalg.norm(u)
        reflect = np.array([[-1,0,0],[0,-1,0],[0,0,1]])
        uz = np.dot(u,reflect)
        if u[2]>0:
            if u[0]==0 and u[1]==0:
                z_local = np.array([-1,0,0])
                y_local = np.cross(z_local,u)/np.linalg.norm(np.cross(u,z_local))
            else:
                y_local = np.cross(uz,u)/np.linalg.norm(np.cross(u,uz))
                z_local = np.cross(u,y_local)/np.linalg.norm(np.cross(y_local,u))
        elif u[2]<0:
            if u[0]==0 and u[1]==0:
                z_local = np.array([1,0,0])
                y_local = np.cross(z_local,u)/np.linalg.norm(np.cross(u,z_local))
            else:
                y_local = np.cross(u,uz)/np.linalg.norm(np.cross(uz,u))
                z_local = np.cross(u,y_local)/np.linalg.norm(np.cross(y_local,u))
        elif u[2]==0:
            z_local = np.array([0,0,1])
            y_local = np.cross(z_local,u)/np.linalg.norm(np.cross(u,z_local))
        if theta!=0:#oxi mono 0 alla paragwgo tou 2*pi
            rot_x = self.rot_theta(x_local, theta)
            y_local = np.dot(y_local, rot_x)
            z_local = np.dot(z_local, rot_x)
        return x_local, y_local, z_local
        
        
    def rot_theta(self, axis, theta):
        '''Returns the rot matrix if there is angle in x'''
        axis = axis/np.sqrt(np.dot(axis, axis))
        a = np.cos(theta/2)
        b, c, d = -axis*np.sin(theta/2)
        return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                      [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                      [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])       
    
    def rotationMatrix(self, axes):
        '''Returns the rotation matrix of the element with axes being a tuple
        --> axes = (x_local, y_local, z_local)'''
        rotv = np.zeros(shape=(3,3))
        rotv[0],rotv[1],rotv[2]=axes[0],axes[1],axes[2]
        for l,line in enumerate(rotv):
            for v,value in enumerate(line):
                if abs(value)<1e-8:
                    rotv[l][v]=0
        rotationMatrix = np.zeros(shape=(12,12))
        for count in [0,3,6,9]:
            for i in range(3):
                for j in range(3):
                    rotationMatrix[i+count][j+count] = rotv[i][j]
        return rotv, rotationMatrix    
    
    
    def transformReleases(self, releases):#releases =[0,0,0,0,0,0  ,  0,0,0,0,1,0]
        T = np.zeros(shape=(12,12))
        count = 0
        num_of_rel = 0
        for i, r in enumerate(releases):
            if r==1:
                T[count][i]=1
                count+=1
                num_of_rel+=1
        for i, r in enumerate(releases):
            if r==0:
                T[count][i]=1
                count+=1
        return num_of_rel, T    
    

    def edgeRotationMatrix(self, angles = (0,0,0)):
        phix = angles[0]                  
        phiy = angles[1]
        phiz = angles[2]
        rx = np.array([[1,0,0], [0, np.cos(phix), np.sin(phix)], [0, -np.sin(phix), np.cos(phix)]])
        ry = np.array([[np.cos(phiy), 0, np.sin(phiy)], [0,1,0], [-np.sin(phiy), 0, np.cos(phiy)]])
        rz = np.array([[np.cos(phiz), np.sin(phiz),0], [-np.sin(phiz), np.cos(phiz),0], [0,0,1]])
        rotv = np.dot(rx,np.dot(ry,rz))
        for l,line in enumerate(rotv):
            for v,value in enumerate(line):
                if abs(value)<1e-8:
                    rotv[l][v]=0
        rotationMatrix = np.zeros(shape=(12,12))
        for count in [0,3,6,9]:
            for i in range(3):
                for j in range(3):
                    rotationMatrix[i+count][j+count] = rotv[i][j]
        return rotationMatrix


    
    
  
    
class Node():
    
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords
        self.supports = None # (1,1,1,1,1,1) for paktwsi?
        self.disp = None

    def elasticMatrix(self, stiff):#nfr=(0,0,0,0,0,0) opou oi times einai oi dyskamcies p.x. (5,0,3.6,0,0,0)
        """Returns a matrix"""
        elastMat = np.zeros(shape=(6,6))####EXEI DIORTHWTHEI GIA 3D???
        for i in range(6):
            elastMat[i][i] = stiff[i]
    #    Beam.ElasticNode[node] = elastMat
        for i,s in enumerate(stiff):
            if s!=0:
                self.supports[i] = 2#create the elastic support with index 2
        return elastMat

    def rotateSupport(self, angles = (0,0,0)):
        """Returns the rotation matrix of the support"""
        phix = angles[0]              
        phiy = angles[1]
        phiz = angles[2]
        rx = np.array([[1,0,0], [0, np.cos(phix), np.sin(phix)], [0, -np.sin(phix), np.cos(phix)]])
        ry = np.array([[np.cos(phiy), 0, np.sin(phiy)], [0,1,0], [-np.sin(phiy), 0, np.cos(phiy)]])
        rz = np.array([[np.cos(phiz), np.sin(phiz),0], [-np.sin(phiz), np.cos(phiz),0], [0,0,1]])
        rotv = np.dot(rx,np.dot(ry,rz))
        RotV = np.zeros(shape=(6,6))
        for count in [0,3]:
            for i in range(3):
                for j in range(3):
                    RotV[i+count][j+count] = rotv[i][j]
        return RotV



def getComponents(axx, axy, axz, q, m=False):
    pass























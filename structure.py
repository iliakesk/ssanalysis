# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 11:12:38 2019

@author: Ilias
"""
import numpy as np
import frame3d as frame


class Structure():
    
    def __init__(self, name, structure="frame3d"):
        
        self.name = name #the name of the project
        self.structure = structure #truss or frame 2d or 3d
#        if structure=="frame3d":
#            import frame3d as frame
        self.nodes = {}
        self.members = {}
        

    def addElement(self, start, stop, theta, section):
        name = self.memberNextName()
        new_member = frame.Member(name, start, stop, theta, section)
        self.members[name] = new_member
    
    
    def addNode(self, coords):
        name = self.nodeNextName
        new_node = frame.Node(name, coords)
        self.nodes[name] = new_node
      
    def deleteElement(self, name):
        del self.members[name]
        
    def deleteNode(self, name):
        del self.nodes[name]
        #PROSOXI an yparxoun beams ston idio komvo        

    def getRearrangedNodes(self):
        nodes = list(self.nodes.keys())
        # PROSOXI DEN KANEI AKOMA REARRANGE NA DW TON KWDIKA APO KAPOIO ALLO MODULE
        return sorted(nodes)


    def memberNextName(self):
        '''Returns the name of the new element based on the existing names'''
        names = self.members.keys()
        try:
            members=[int(k[2:]) for k in names]
            members.sort()
            name='el' + str(members[-1]+1)
            return name
        except:
            return 'el1'


    def nodeNextName(self):
        '''Adds to the NODES dictionary the new node as object with its name as key'''
        '''Returns the name of the new node based on the existing names'''
        names =self.nodes.keys()
        try:
            nodes=[int(k[1:]) for k in names]
            nodes.sort()
            nextnode = 'n' + str(nodes[-1] + 1)
            return nextnode
        except: 
            return 'n1'



def analysis(yg, yq, sl):
    disps, reacts = dispsReacts(yg, yq, sl)
    edgeforces = calculateEdgeForces(disps, reacts, sl)
    int_forces = getInternalForces(yg, yq, sl, edgeforces)
    return edgeforces, int_forces, disps, reacts


def getInternalForces(yg, yq, sl, edgeforces):
    loads = frame.Beam.Loads if sl else frame.Beam.Loads[frame.Beam.Loads.self_load!='YES'].reset_index(drop=True)
    step = 0.01
    int_forces = {}
    for element, values in edgeforces.items():
        load = loads.loc[loads.member==element]
        L = round(frame.Beam.Beams[element].L,2)
        axx, axy, axz = frame.Beam.Beams[element].axes
        forces = edgeforces[element]
        steps = int(L/step)
        N = np.zeros(shape=(1,steps))
        Qy = np.zeros(shape=(1,steps))
        Qz = np.zeros(shape=(1,steps))
        Mx = np.zeros(shape=(1,steps))
        My = np.zeros(shape=(1,steps))
        Mz = np.zeros(shape=(1,steps))
        for i in range(steps):
            N[0][i]-=forces[0]
            Qy[0][i]+=forces[1]
            Qz[0][i]+=forces[2]
            Mx[0][i]+=forces[3]
            My[0][i]+=forces[4] + forces[2]*(0.01*i)
            Mz[0][i]+=forces[5] - forces[1]*(0.01*i)

        for i in range(len(load)):
            function = load.function.iloc[i]
            if function=='Po' or function=='M':
                a = round(load.a.iloc[i],2)
                firstpart = int(a/step)
                secondpart = int((L)/step)
                vector = load.vector.iloc[i]
                if function=='M':
                    comps = frame.getComponents(axx, axy, axz, vector, m=True)
                else:
                    comps = frame.getComponents(axx, axy, axz, vector)
                for i in range(firstpart):
                    N[0][i]+=0
                    Qy[0][i]+=0
                    Qz[0][i]+=0
                    Mx[0][i]+=0
                    My[0][i]+=0
                    Mz[0][i]+=0
                for i in range(firstpart,secondpart):
                    j=i-firstpart
                    N[0][i]-=comps[0]
                    Qy[0][i]+=comps[1]
                    Qz[0][i]+=comps[2]
                    Mx[0][i]+=comps[3]
                    My[0][i]+=comps[2]*(0.01*j) + comps[4]
                    Mz[0][i]+=comps[1]*(0.01*j) + comps[5]
            elif function=='FE':
                a = round(load.a.iloc[i],2)
                b = round(load.b.iloc[i],2)
                firstpart = int(a/step)
                secondpart = int((L-b)/step)
                thirdpart = int(b/step)
                vector = load.vector.iloc[i]
                comps = frame.getComponents(axx, axy, axz, vector)
                for i in range(firstpart):
                    N[0][i]+=0
                    Qy[0][i]+=0
                    Qz[0][i]+=0
                    Mx[0][i]+=0
                    My[0][i]+=0
                    Mz[0][i]+=0
                for i in range(firstpart,secondpart):
                    j=i-firstpart
                    N[0][i]-=comps[0]*(0.01*j)
                    Qy[0][i]+=comps[1]*(0.01*j)
                    Qz[0][i]+=comps[2]*(0.01*j)
                    Mx[0][i]+=0
                    My[0][i]+=0.5*comps[2]*((0.01*j)**2)
                    Mz[0][i]+=0.5*comps[1]*((0.01*j)**2)
                for i in range(secondpart,thirdpart):
                    j=i-secondpart
                    N[0][i]+=0
                    Qy[0][i]+=0
                    Qz[0][i]+=0
                    Mx[0][i]+=0
                    My[0][i]+=comps[2]*(L-a-b)*(L-a-b+0.02*j)*0.5
                    Mz[0][i]+=comps[1]*(L-a-b)*(L-a-b+0.02*j)*0.5
            elif function=='FR':
                a = round(load.a.iloc[i],2)
                b = round(load.b.iloc[i],2)
                firstpart = int(a/step)
                secondpart = int(L-b/step)
                thirdpart = int(L/step)
                vector = load.vector.iloc[i]
                comps = frame.getComponents(axx, axy, axz, vector)
                if vector[0]==0:
                    for i in range(firstpart):
                        N[0][i]+=0
                        Qy[0][i]+=0
                        Qz[0][i]+=0
                        Mx[0][i]+=0
                        My[0][i]+=0
                        Mz[0][i]+=0
                    for i in range(firstpart,firstpart+secondpart):
                        j=i-firstpart
                        N[0][i]-=0.5*comps[3]*(0.01*j)
                        Qy[0][i]+=0.5*comps[4]*(0.01*j)
                        Qz[0][i]+=0.5*comps[5]*(0.01*j)
                        Mx[0][i]+=0
                        My[0][i]+=(0.5*comps[5]*((0.01*j)**2))/3
                        Mz[0][i]+=(0.5*comps[4]*((0.01*j)**2))/3
                    for i in range(firstpart,firstpart+secondpart):
                        j=i-secondpart
                        N[0][i]+=0.5*comps[3]*(L-a-b)
                        Qy[0][i]+=0.5*comps[4]*(L-a-b)
                        Qz[0][i]+=0.5*comps[5]*(L-a-b)
                        Mx[0][i]+=0
                        My[0][i]+=0.5*comps[5]*(L-a-b)*(L-a-b+0.03*j)/3
                        Mz[0][i]+=0.5*comps[4]*(L-a-b)*(L-a-b+0.03*j)/3
                else:
                    for i in range(firstpart):
                        N[0][i]+=0
                        Qy[0][i]+=0
                        Qz[0][i]+=0
                        Mx[0][i]+=0
                        My[0][i]+=0
                        Mz[0][i]+=0
                    for i in range(firstpart,firstpart+secondpart):
                        j=i-firstpart
                        N[0][i]-=comps[3]*0.05*j + (comps[3]-comps[3]*0.01*j)*0.01*j
                        Qy[0][i]+=comps[4]*0.05*j + (comps[4]-comps[4]*0.01*j)*0.01*j
                        Qz[0][i]+=comps[5]*0.05*j + (comps[5]-comps[5]*0.01*j)*0.01*j
                        Mx[0][i]+=0
                        My[0][i]+=(comps[5]*0.001*j**2)/3 + 0.5*(comps[5]-comps[5]*0.01*j)*(0.01*j)**2
                        Mz[0][i]+=(comps[4]*0.001*j**2)/3 + 0.5*(comps[4]-comps[4]*0.01*j)*(0.01*j)**2
                    for i in range(firstpart,firstpart+secondpart):
                        j=i-secondpart
                        N[0][i]-=0.5*comps[3]*(L-a-b)
                        Qy[0][i]+=0.5*comps[4]*(L-a-b)
                        Qz[0][i]+=0.5*comps[5]*(L-a-b)
                        Mx[0][i]+=0
                        My[0][i]+=comps[5]*(L-a-b)*(L-a-b+0.03*j)/3
                        Mz[0][i]+=comps[4]*(L-a-b)*(L-a-b+0.03*j)/3
            elif function=='FT':
                pass
        
        int_forces[element]=N[0].tolist(),Qy[0].tolist(),Qz[0].tolist(),Mx[0].tolist(),My[0].tolist(),Mz[0].tolist()
        
        for el, values in int_forces.items():
            v = []
            for value in values:
                value = [round(i,2) for i in value]
                v.append(value)
            int_forces[el] = v
    return int_forces
    

def dispsReacts(yg, yq, sl):
    if nodeContinuation() is False: renameAllNodes()
    beams = st.Beam.Beams
    for beam in beams.values():
        beam.initValues(beam.theta)
    nodes = st.Beam.Nodes
    nodal_supps = st.Beam.NodalSupports
    s=0 # size 'supported' for the analysis of the matrices
    for value in nodal_supps.values():
        for sup in value:
            if sup==1:
                s+=1
    f = len(nodes)*6 - s
    K = K_global(beams)
    tM = transformMatrix()
    F1 = forceMatrix('G', sl)
    F2 = forceMatrix('Q', sl)
    Fall = yg*F1 + yq*F2
    Dmatrix = displacementMatrix()
    Kt = np.dot(tM,np.dot(K,np.linalg.inv(tM)))
    Fall_t = np.dot(tM,Fall)
    Dt = np.dot(tM,Dmatrix)
    Kff, Kfs, Ksf, Kss = Kt[:f,:f], Kt[:f,f:], Kt[f:,:f], Kt[f:,f:]
    Ff  = Fall_t[:f,]
    Fs1 = Fall_t[f:,]
    Ds = Dt[f:]
    try:
        Kffinv = np.linalg.inv(Kff)
    except:
        Kffinv = np.linalg.pinv(Kff)
        print('! ! ! ! ! In forcematrix of analysis3dframe 251 the pinv was used instead of inv')
    Df = np.dot(Kffinv,Ff-np.dot(Kfs,Ds))
    Fs = np.dot(Ksf,Df) + np.dot(Kss,Ds)

    Fs = Fs - Fs1
    DISPS = returnDisplacements(Df)
    REACTS = returnReactions(Fs)
    if thereΙsElasticNode():
        DISPS,REACTS = calculateElasticNode(DISPS, REACTS)
    return DISPS,REACTS



def thereΙsElasticNode():
    if len(st.Beam.ElasticNode)>0:
        return True
    else: return False


def returnDisplacements(Df):
    '''Returns a full list of ALL displacements, zeros and non-zeros'''
    supports = st.Beam.NodalSupports
    dispvals = Df.flatten().tolist()
    dispvalues = [round(i,6) for i in dispvals]
    disps = []
    nodes = sorted(supports.keys(), key = lambda x: int(x[1:]))
    supindex = 0
    for node in nodes:
        for sup in supports[node]:
            if sup!=1:
                disps.append(dispvalues[supindex])
                supindex += 1
            else:
                disps.append(0)
    return disps

def returnReactions(Fs):
    '''Returns a dictionary with the reaction values with keys the number of 
    the freedom eg {'R1':30,'R5':20}'''
    supports = st.Beam.NodalSupports
    react = []
    for node in sorted(supports.keys(), key = lambda x: int(x[1:])):
        numnode = int(node[1:])-1
        for i,re in enumerate(supports[node]):
            if re==1:
                rname = 'R'+str(i+1 + 6*numnode)
                react.append(rname)
    reactvals = Fs.flatten().tolist()
    reactvalues = [round(i,3) for i in reactvals]
    reacts = dict(zip(react,reactvalues))  
    return reacts
   
def calculateElasticNode(disps, reacts):
    '''Returns the reactions on the elastic number of freedoms'''
    elastnode = st.Beam.ElasticNode #'n1':[0,kel,0] dyskamcia
    for node, stiffnesses in elastnode.items():
        numnode = int(node[1:])-1
        stiffMatrix = st.elasticNode(node,stiffnesses)
        for i in range(6):
            if stiffMatrix[i][i]!=0:
                indexofdisp = i + 6*numnode
                nameofreact = 'R'+str(i+1 + 6*numnode)
                valueofdisp = disps[indexofdisp]
                reacts[nameofreact] = -stiffMatrix[i][i]*valueofdisp
    return disps, reacts

def calculateEdgeForces(disps, reacts, sl):
    '''Returns a dictionary with the internal forces for each member from start to end'''
    beamForces = {}
    loads = st.Beam.Loads if sl else st.Beam.Loads[st.Beam.Loads.self_load!='YES'].reset_index(drop=True)
    for name, beam in st.Beam.Beams.items():
        K = beam.Klocal
        R = beam.rotMatrix
        lstop = np.zeros(6)
        lstart = np.zeros(6)
        loadstart = loads.loc[loads.member==name, 'loadsstart']
        loadstop = loads.loc[loads.member==name, 'loadsstop']
        for load in loadstart:
            lstart += load
        for load in loadstop:
            lstop += load
        A = np.concatenate([lstart,lstop])
        A = np.dot(R,A)
        startnode = beam.start_node
        indexstart = 6*(int(startnode[1:])-1)
        stopnode = beam.stop_node
        indexstop = 6*(int(stopnode[1:])-1)
        if beam.release==None:
            alldisps = disps[indexstart:indexstart+6] + disps[indexstop:indexstop+6]
            forces = A + np.around(np.dot(K,np.dot(R,alldisps)),2)
        else:
            alldisps = disps[indexstart:indexstart+6] + disps[indexstop:indexstop+6]
            alldispsT = np.dot(beam.tM,alldisps)
            Dc = np.transpose(alldispsT[beam.rels:])
            
            De = np.dot(beam.Keeinv,-1*beam.Pe-np.dot(beam.Kec,Dc))
            alldisps = np.concatenate((De,Dc))
            alldisps = np.dot(np.linalg.inv(beam.tM),alldisps)
            
            a = loads.loc[loads.member==name, 'loadsstart_release']
            if a.empty:
                forces = np.around(np.dot(K,np.dot(R,alldisps)),2)
            else:
                a = a.tolist()
                a=a[0]
                A = np.array(a)
                A = np.dot(R,A)
                forces = A + np.around(np.dot(K,np.dot(R,alldisps)),2)
        roundforces = []
        for i in forces:
            if abs(i)<1:
                roundforces.append(0)
            else:
                roundforces.append(i)
        forces = np.array(roundforces)
        beamForces[name]=forces
    return beamForces


def K_global(beams):
    '''Returns the stiffness matrix of the structure'''
    nodes = st.Beam.Nodes
    rotatedsupports = st.Beam.RotatedSupports
    elasticnode = st.Beam.ElasticNode
    n = len(nodes)*6
    Kall = np.zeros(shape=(n,n))
    els = sorted(beams.keys(), key = lambda x: int(x[2:]))
    el=[]
    for e in els:
        el.append(beams[e])
    for e in el:
        start = int(e.start_node[1:])-1
        stop = int(e.stop_node[1:])-1
        Kel = e.K
        for i in range(6):
            for j in range(6):
                Kall[i+start*6][j+start*6] += Kel[i][j]
                Kall[i+start*6][j+stop*6] += Kel[i][j+6]
                Kall[i+stop*6][j+start*6] += Kel[i+6][j]
                Kall[i+stop*6][j+stop*6] += Kel[i+6][j+6]
    if len(rotatedsupports)>0:
        for node, angles in rotatedsupports.items():
            rotv = supportRotationMatrix(node,angles)
            Kall = np.dot(np.linalg.inv(rotv),np.dot(Kall,rotv))
    if len(elasticnode)>0:
        allnodes = sorted(nodes.keys(), key = lambda x: int(x[1:]))
        for node in allnodes:
            index = 6*(int(node[1:])-1)
            if node in elasticnode.keys():
                transfmatrix = st.elasticNode(node,elasticnode[node])
                for l in range(6):
                    Kall[index+l][index+l] += transfmatrix[l][l]
    return Kall


def forceMatrix(group, sl):
    '''Return the force matrix for each group of loads. Needs to be called for
    each group specifically (the load combinations will be formed after this)'''
    n = len(st.Beam.Nodes)*6
    loads = st.Beam.Loads if sl else st.Beam.Loads[st.Beam.Loads.self_load!='YES'].reset_index(drop=True)
    Pmatrix = np.zeros(shape=(n,1))
    P = {}
    beams = st.Beam.Beams
    for name,member in beams.items():
        if member.release!=None:
            Kt = member.Kt
            releases = member.release[1]
            rels, tM = st.transformReleases(releases)
            for i in range(len(loads)):
                if loads.member[i]==name:
                    loadsstart = loads.loadsstart[i]
                    loadsstop = loads.loadsstop[i]
                    tkKt11 = np.linalg.inv(Kt[:rels,:rels])
                    Rr = member.Rr
                    loadsstart_release = np.concatenate((loadsstart,loadsstop))
                    Lr = np.dot(Rr,loadsstart_release)
                    LrT = np.dot(tM,Lr)
                    LrT = LrT[rels:] - np.dot(Kt[rels:,:rels],np.dot(tkKt11,LrT[:rels]))
                    indexes = []
                    for j, r in enumerate(releases):
                        if r==1:
                            indexes.append(j)
                    for k in indexes:
                        LrT = np.insert(LrT, k, 0)
                    loadsstart = LrT[:6]
                    loadsstop = LrT[6:]
                    loads.at[i,'loadsstart']=loadsstart
                    loads.at[i,'loadsstop']=loadsstop
                    loads.at[i,'loadsstart_release']=loadsstart_release.tolist()
                    st.Beam.Loads = loads if sl else pd.concat([loads,st.Beam.Loads[st.Beam.Loads.self_load=='YES']], axis=0, join='outer', ignore_index=True)
                    member.Pe = LrT[:rels]
                    try:
                        member.Keeinv = np.linalg.inv(Kt[:rels,:rels])
                    except:
                        member.Keeinv = np.linalg.pinv(Kt[:rels,:rels])
                        print(' ! ! ! ! In forcematrix of analysis3dframe 475 the pinv was used instead of inv')
                    member.Kec = Kt[:rels,rels:]
                else:
                    member.Pe = np.zeros(shape=(12,))[:rels]
                    member.Keeinv = np.linalg.pinv(Kt[:rels,:rels])
                    member.Kec = Kt[:rels,rels:]

    for node in st.Beam.Nodes.keys():
        P[node] = np.array([0,0,0,0,0,0],dtype=np.float)
        loadstart = loads.loc[(loads.nodestart==node) & (loads.group==group), 'loadsstart']
        loadstop = loads.loc[(loads.nodestop==node) & (loads.group==group), 'loadsstop']
        nodalload =  loads.loc[(loads.node==node) & (loads.group==group), 'loadsstart']
        
        for load in loadstart:
            P[node]-=load
        for load in loadstop:
            P[node]-=load
        for load in nodalload:
            P[node]+=load

    i=0
    for node in sorted(P.keys(), key=lambda x: int(x[1:])):
        Pmatrix[i] = P[node][0]
        Pmatrix[i+1] = P[node][1]
        Pmatrix[i+2] = P[node][2]
        Pmatrix[i+3] = P[node][3]
        Pmatrix[i+4] = P[node][4]
        Pmatrix[i+5] = P[node][5]
        i+=6
    return Pmatrix


def supportRotationMatrix(node,angles):
    nodes = st.Beam.Nodes
    n = len(nodes)*6
    sRM = np.identity(n)
    rotv = st.rotateSupport(node,angles)
    index = 6*(int(node[1:])-1)
    for i in range(6):
        for j in range(6):
            sRM[index+i][index+j] = rotv[i][j]
    return sRM


def displacementMatrix():
    nodes = st.Beam.Nodes
    displacements = st.Beam.Displacements
    n = len(nodes)*6
    Dmatrix = np.zeros(shape=(n,1))
    for node in sorted(nodes.keys(), key = lambda x: int(x[1:])):
        if node in displacements.keys():
            index = 6*(int(node[1:])-1)
            for i in range(6): 
                Dmatrix[index+i] = displacements[node][i]
    return Dmatrix


def transformMatrix():
    '''Returns the transformation matrix given the number of freedoms per node in general'''
    supports = st.Beam.NodalSupports
    n = len(st.Beam.Nodes)*6
    T = np.identity(n)
    transfMatrix = np.zeros(shape=(n,n))
    keynodes = sorted(supports.keys(), key = lambda x: int(x[1:]))
    numfreedom = []
    for i, node in enumerate(keynodes):
        for position, support in enumerate(supports[node]):
            if support==1:
                numfreedom.append(position+6*i+1)
    count = 0            
    firstpos = n - len(numfreedom)
    for f in range(n):
        if f+1 not in numfreedom:
            transfMatrix[f-count]=T[f]
        else:
            transfMatrix[firstpos+count] = T[f]
            count+=1
    return transfMatrix


def nodeContinuation():
    '''Check the continuation of the nodes'''
    nodes = st.Beam.Nodes
    notarranged = sorted(nodes.keys(), key = lambda x: int(x[1:]))
    numcheck=[]
    for name in notarranged:
        numcheck.append(int(name[1:]))
    for i, value in enumerate(numcheck):
        if numcheck[i]==i+1:
            return True
        else: return False


def arrangedNodes():
    '''Returns the rearranged name of the node'''
    nodes = st.Beam.Nodes
    notarranged = sorted(nodes.keys(), key = lambda x: int(x[1:]))
    arrangednodes = {}   #create dict with oldnames as keys and arranged names as values
    for i, oldname in enumerate(notarranged):
        newname = 'n'+str(i+1)
        arrangednodes[oldname] = newname
    return arrangednodes


def renameNode(node):
    '''Takes the old name of the node and returns the new'''
    if type(node) is str:
        arrangednodes = arrangedNodes()
        return arrangednodes[node]


def renameAllNodes():
    '''Rename all nodes in all data structures'''
    nodes = st.Beam.Nodes
    ArNod={}#arrange Beam.Nodes
    for oldname, coords in nodes.items():
        new = renameNode(oldname)
        ArNod[new] = coords
    st.Beam.Nodes = ArNod
    for beam in st.Beam.Beams.values():#change start and stop nodes with new ones
        beam.start_node = renameNode(beam.start_node)
        beam.stop_node = renameNode(beam.stop_node)
        
    for item in [st.Beam.NodalSupports, st.Beam.RotatedSupports, st.Beam.Displacements, st.Beam.ElasticNode]:
        newitem={}
        for oldname, value in item.items():
            new = renameNode(oldname)
            newitem[new] = value
        item = newitem   
    for item in ['nodestart','nodestop']:
        column = st.Beam.Loads[item].apply(renameNode)
        st.Beam.Loads[item] = column


































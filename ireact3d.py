# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 11:39:00 2018

@author: Ilias
"""
import sys


def comInLoads(function, el, q, a=0, b=0):

    if function[0]=='c':
        m1,m2,q1,q2 = getattr(sys.modules[__name__], function)(el,q, a, b)
        return m1,m2,q1,q2
    elif function[0]=='a':
        n1, n2 = getattr(sys.modules[__name__], function)(el,q, a, b)
        return n1, n2

def cFE(el, q,  a, b):
    l = el.L
    Q1 = Q2 = q*l/2
    M1 = M2 = q*l*l/12
    return M1, -M2, -Q1, -Q2

def cPE(el, q,  a, b):
    l = el.L
    Q1 = q*(l**4-(b**3)*(2*l-b)-a*(2*l**3-2*l*a**2+a**3))/(2*l**3)
    Q2 = q*(l**4-(a**3)*(2*l-a)-b*(2*l**3-2*l*b**2+b**3))/(2*l**3)
    M1 = q*(l**4-(b**3)*(4*l-3*b)-(a**2)*(6*l**2-8*a*l+3*a**2))/12*l**2
    M2 = q*(l**4-(a**3)*(4*l-3*a)-(b**2)*(6*l**2-8*b*l+3*b**2))/12*l**2
    return M1, -M2, -Q1, -Q2 


def cFT(el, q,  a, b):
    #gia ayjanomeno trigwniko. gia fortio pou meiwnetai anapoda ta Q1,Q2,M1,M2
    q1, q2 = q
    l = el.L
    Q1 = 3*q2*l/20
    Q2 = 7*q2*l/20
    M1 = q2*l*l/30
    M2 = q2*l*l/20

    if q1 == 0:
        return M1, -M2, -Q1, -Q2

    else:
        Q1, Q2 = Q2, Q1
        M1, M2 = M2, M1
        return M1, -M2, -Q1, -Q2



def cPT(el, q,  a, b):
    #gia ayjanomeno trigwniko. gia fortio pou meiwnetai anapoda ta Q1,Q2,M1,M2
    L = el.L
    b=L-b
    q1, q2 = q
    Q1 = -a**2*q2/(2*L) + b**2*q2/(2*L) + 3*a**4*q2/(4*L**3) - 3*b**4*q2/(4*L**3) - 2*a**5*q2/(5*L**4) + 2*b**5*q2/(5*L**4)
    Q2 = -3*a**4*q2/(4*L**3) + 3*b**4*q2/(4*L**3) + 2*a**5*q2/(5*L**4) - 2*b**5*q2/(5*L**4)
    M1 = -a**3*q2/(3*L) + b**3*q2/(3*L) + a**4*q2/(2*L**2) - b**4*q2/(2*L**2) - a**5*q2/(5*L**3) + b**5*q2/(5*L**3)
    M2 = -a**4*q2/(4*L**2) + b**4*q2/(4*L**2) + a**5*q2/(5*L**3) - b**5*q2/(5*L**3)
    if q1 == 0:
        return M1, -M2, -Q1, -Q2 
    else: 
        Q1, Q2 = Q2, Q1
        M1, M2 = M2, M1
        return M1, -M2, -Q1, -Q2 



def cPo(el, q,  a, b):
    l = el.L
    Q1 = (q*(b**2)/(l**2))*(3-2*b/l)
    Q2 = (q*(a**2)/(l**2))*(3-2*a/l)
    M1 = q*a*(b**2)/(l**2)
    M2 = q*b*(a**2)/(l**2)
    return M1, -M2, -Q1, -Q2




def cM(el, q,  a, b):
    l = el.L
    Q1 = 6*q*a*b/(l**3)
    Q2 = -6*q*a*b/(l**3)
    M1 = q*b*(2-3*b/l)/l
    M2 = q*a*(2-3*a/l)/l
    return M1, M2, -Q1, Q2



def aFE(el, q,  a, b):
    l = el.L
    N1 = q*(l-a-b)*(l-a+b)/(2*l)
    N2 = q*(l-a-b)*(l+a-b)/(2*l)
    return -N1, -N2



def aPE(el, q,  a, b):
    l = el.L
    N1 = q*(l-a-b)*(l-a+b)/(2*l)
    N2 = q*(l-a-b)*(l+a-b)/(2*l)
    return -N1, -N2




def aFT(el, q,  a, b):
    if q[0]==0:q=q[1]
    else:q=q[0]
    l = el.L
    N1 = q*(l-a-b)*(l-a+b)/(2*l)
    N2 = q*(l-a-b)*(l+a-b)/(2*l)
    return -N1/2, -N2/2




def aPT(el, q,  a, b):
    if q[0]==0:q=q[1]
    else:q=q[0]
    l = el.L
    N1 = q*(l-a-b)*(l-a+b)/(2*l)
    N2 = q*(l-a-b)*(l+a-b)/(2*l)
    return -N1/2, -N2/2



def aPo(el, q,  a, b):
    l = el.L
    N1 = q*b/l
    N2 = q*a/l
    return -N1, -N2




def aM(el, q,  a, b): 
    l = el.L
    M1 = q*b/l
    M2 = q*a/l
    return -M1, -M2


# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:16:27 2014

@author: Tadesse 
"""

import numpy as np
import random
import math 

#multi dimensional array
def valueIterationx(mdp,h):
    v=np.matrix(np.zeros([mdp[0],h]))   #initialize v[0][k]=0
    pol=np.matrix(np.zeros([mdp[0],h],dtype=np.character))  #Initial policy set 0
    v[:,0]=mdp[1] #assign the R(s) to V[0]
    for k in range(1,h):
      v[:,k]=Bellman(v[:,k-1],mdp)   #call bellman backup with v argument
      pol[:,k]=GetPol(v,mdp)                   
    return v,pol
     
def Bellman(v,mdp):
     v1= mdp[1] + np.amax([mdp[3][act]*v for act in mdp[2]],axis=0)
     return v1
def GetPol(v,mdp):  #returns action for argmax
     n=mdp[0] #no of states
     allValue=dict((act,mdp[3][act]*v) for act in mdp[2])
     mxValue = np.amax([mdp[3][act]*v for act in mdp[2]],axis=0)
     pol=[]
     for el in mxValue[:,0]:
         for key in allValue:
             if el in allValue[key]:
                 pol.append(key)
                 break
     return np.matrix(pol).reshape([n,1])
def run():
    '''Uncomment one experiment at a time.'''
    '''#####################################################'''
    H=5 #horizon 
    #conf file and transition file for first experiment.
    #'''
    filename1="Exp1\\conf.txt"  #file to define state,reward and actions.
    tranFiles1=["Exp1\\tran1.csv","Exp1\\tran2.csv","Exp1\\tran3.csv"] #'''
    
    #conf file and transition file for second experiment uncomment to run it.
    '''
    filename1="Exp2\\conf.txt"
    tranFiles1=["Exp2\\tran1.csv","Exp2\\tran2.csv","Exp2\\tran3.csv"]
    #'''
    mdp=getInput(filename1,tranFiles1)
    value,policy=valueIterationx(mdp,H)
    
    print value  #value matrix
    print policy  #policy matrix
    
       
def getInput(filename,tranFiles): #parse input file
    lines=[line.strip() for line in open(filename)]
    state=int(lines[0]) #states
    r=np.matrix(lines[1]).T #rewards,
    a=[ b for b in lines[2] if b!=',']  #actions
    #transtion, transpose to make it column matrix
    t=[np.matrix(lines[i]).reshape([state,state]).T for i in range(3,len(lines)) if len(lines[i])>0]
    t=[np.matrix(np.genfromtxt(fname,delimiter=','))for fname in tranFiles]
    #action associated with transition
    TranstionAction={}
    for i in range(0,len(a)):
        TranstionAction[a[i]]=t[i]
    return state,r,a,TranstionAction
       
if __name__=="__main__":
    run()




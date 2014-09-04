# -*- coding: utf-8 -*-
"""
Created on Mon May 26 11:38:20 2014

@author: Tadesse Zemicheal
Experimenting with K-mean algorithm for clustering.
Requires matplotlib and numpy external libraries

"""
import numpy as np
import random
import matplotlib.pylab as plt
#main Kmean algorithm takes k and data 
#return centroids and clusters
def kmean(k,data):
    #initialize the centroids
    centroids=random.sample(data,k)
    clust={m:[] for m in range(k)}
    #assign each elements to the centroid
    notConverged=True
    
    while(notConverged):
        oldcentroids=centroids;
        clust={m:[] for m in range(k)}
        for dt in data:
        #calcualte nearest neighbor
            currentcent=np.argmin([(dt[0]-centr[0])**2 +(dt[1]-centr[1])**2 for centr in centroids])
            clust[currentcent].append(dt)
        #evaluate the cluster mean
        centroids=[np.mean(value,axis=0) for key,value in sorted(clust.items())]
        #print (centroids)
        #check convergence if there is any change in assignment
        notConverged=checkConvergence(oldcentroids,centroids,k)
    return centroids,clust
#check convergence
def checkConvergence(oldcent,newcentr,k):
      return (set([tuple(n) for n in oldcent])-set([tuple(m) for m in newcentr]))
#run 200 times for k=5
def kmeanofTwoH():
    data=np.loadtxt('data1.csv',delimiter=',')
    k=5;
    centers=[]
    SSD=[]
    
    for i in range(200):
        summary_cluster={m:[] for m in range(k)}
        centroid,cluster=kmean(k,data)
        centers.append(centroid)
        summary_cluster=getSquaredClusterDistance(centroid,cluster,summary_cluster)
        print('Finished running iteration',i)
        SSD.append(np.sum(summary_cluster.values()))
    #summary(summary_cluster)
    print('min,max,mean,sd \n'+str(min(SSD))+','+str(max(SSD))+','+str(np.mean(SSD))+','+str(np.std(SSD)))
    #priting the clusters
    for center in centers:
        center_mat=np.matrix(center)
        plt.plot(center_mat[:,0],center_mat[:,1],'bo')
    data_mat=np.matrix(data)
    plt.plot(data_mat[:,0],data_mat[:,1],'r+')
    plt.ylabel('Y index')
    plt.xlabel('X index')
    plt.title('Kmean clustering with 200 runs')
    plt.show()
#identifying optimal k value
def findingK():
    data=np.loadtxt('data2.csv',delimiter=',')
    ks=range(2,16)
    optimalK={}
    for k in ks:
       summary_clusterOp={m:[] for m in range(k)}
       for n in range(10):
           centroid1,cluster1=kmean(k,data)
           summary_clusterOp=getSquaredClusterDistance(centroid1,cluster1,summary_clusterOp)
       
       optimalK.update({k:sum([min(value) for key,value in summary_clusterOp.items()])})
       print("Finished running", k)
    plt.plot(optimalK.keys(),optimalK.values(),'r-')
    plt.ylabel('Sum of squared Distance')
    plt.xlabel('K value')
    plt.title('Selecting optimal K value')
    plt.show()
   #plot k with their value

def normalizeKmean():
    k=2
    n=200
    
    #centers={m:[] for m in range(n)}
   
    def scatter_plot(sdata,title):
        plt.figure()
        #plt.subplot(2,1,i)
        centers=[]
        for itern in range(n):
            centroids,cluster=kmean(k,sdata)
            centers.append(centroids)
            center_mat=np.matrix(centroids)
            plt.plot(center_mat[:,0],center_mat[:,1],'ro')
            print("-----Finished iteration ---", itern)
        data_mat=np.matrix(sdata)
        plt.plot(data_mat[:,0],data_mat[:,1],'y+')
        plt.title(title)
        plt.show()

    data=np.loadtxt('data3.csv',delimiter=',')
    Z_data=(data-np.mean(data,axis=0))/np.std(data,axis=0)    
    scatter_plot(data,'Graph of unormalized data')
    scatter_plot(Z_data,'Graph of Normalized data')
    
def getSquaredClusterDistance(centroid,cluster,summary_cluster):
    for key,values in sorted(cluster.items()):
            squared_dist=sum([(centroid[key][0]-value[0])**2+(centroid[key][1]-value[1])**2 for value in values])
            summary_cluster[key].append(squared_dist)
    return summary_cluster

if __name__=="__main__":
    print("\nType \n1. For kmean 200 runs \n2. For finding optimal K value \n3. For Normalized kmean")
    opt=raw_input("Enter your choice\n" )
    if opt=='1':
       kmeanofTwoH() 
    elif opt=='2':
        findingK()
    elif opt=='3':
     normalizeKmean()
    else:
        print "Quit"

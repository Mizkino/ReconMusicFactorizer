# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 08:10:15 2016

@author: god
"""
#from math import sqrt
import numpy as np


def calc_U(U,G,O,K,t2,tau,envs):
    for ks in range(K):
        for ts in range(t2):
            if ts - tau < 0: continue
            U[ks,ts] = np.sum(np.sum(G[:,0:tau+1].T*O[ks,slice(ts,ts-tau-1,-1),:]))
    return U

def calc_G(H,X,G,O,K,t2,tau,envs,pg,rg):
    Gt = G
    for j in range(envs):
        for taus in range(tau):
            if t2 - taus < 0: break
            Gt[j,ts] = G[j,ts]*np.sum(np.sum(O[:,j,slice(t2-taus,t2)]))* sum(sum(H.T.dot(Y)))\
             / ( np.sum(np.sum(O[:,j,slice(t2-taus,t2+1)]))*sum(sum(H.T.dot(X))) + pg*rg *np.power(abs(G[j,ts]),pg))
    return Gt

def calc_O(H,X,G,O,K,t2,tau,envs,pg,rg):
    for t in range(t2-tau):
        for i in range(K):
            for j in range(envs):
                for taus in range(tau):
                    if t - taus < 0: break
                    # O[i,j,taus] = Ot[i,j,taus] * sum(G[j,max(0:
                    np.sum(G[j,slice(t-taus,t+1)]) * sum(sum(H.T.dot(Y)))\
                    / ( np.sum(G[j,slice(t-taus,t+1)])*sum(sum(H.T.dot(X))) + pg*rg *np.power(abs(O[i,j,t+taus]),pg))


def nmf_euc(Y,K,iter):

    H = np.random.rand(Y.shape[0],K)
    U = np.random.rand(K,Y.shape[1])*1000
    # U = U / U.max()
    for ks in range(K):
        H[:,ks] = H[:,ks] / np.sum(H[:,ks])
        U[ks,:] = U[ks,:] * np.sum(H[:,ks])
    eps = np.finfo(float).eps
#    onemat = np.ones(Y.shape)

    for i in range(0,iter):
        H = H * Y.dot(U.T) / (H.dot(U.dot(U.T)) + eps)
        U = U * H.T.dot(Y) / (H.T.dot(H.dot(U)) + eps)
        # U = U / U.max()
        for ks in range(K):
            H[:,ks] = H[:,ks]/np.sum(H[:,ks])
            U[ks,:] = U[ks,:] * np.sum(H[:,ks])
    return H,U


def m_fact_euc(Y,K,envs,iter,H,U):
    tau = 40
    # U=(k,y2) G = (j,tau) O =(k,y2,j)
    G = np.zeros((envs,tau))
    O = np.zeros((U.shape[0],U.shape[1],envs))
    X = np.zeros(Y.shape)
    eps = np.finfo(float).eps
    tau = 20
    envs = 4
    pg = 1
    rg = 1
    po = 1
    ro = 1
    t2 = Y.shape[1]

    for js in range(envs):
        ranjtau = [-1*np.random.rand() for i in range(G.shape[1])]
        G[js,:] = np.exp(ranjtau)
        G[js,:] = G[js,:]/np.sum(G[js,:])
        O[:,:,js] = U

    U = calc_U(U,G,O,K,U.shape[1],tau,envs)
    X = H.dot(U)
    for ks in range(K):
        H[:,ks] = H[:,ks]/np.sum(H[:,ks])
        U[ks,:] = U[ks,:] * np.sum(H[:,ks])

    for it in range(iter):
        H = H * Y.dot(U.T) / (H.dot(U.dot(U.T)) + eps)
        # for ks in range(K):
        #     H[:,ks] = H[:,ks]/np.sum(H[:,ks])
        U = calc_U(U,G,O,K,U.t2,tau,envs)
        X = H.dot(U)
        G = calc_G(H,X,G,O,K,t2,tau,envs,pg,rg)
        O = calc_O(H,X,G,O,K,t2,tau,envs,pg,rg)
        for ks in range(K):
            H[:,ks] = H[:,ks]/np.sum(H[:,ks])
            U[ks,:] = U[ks,:] * np.sum(H[:,ks])

    return H,U,G,O

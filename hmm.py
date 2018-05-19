"""Automatic chord recogniton with HMM, as suggested by Juan P. Bello in
'A mid level representation for harmonic content in music signals'
@author ORCHISAMA"""

from __future__ import division
from chromagram import compute_chroma
import os
from scipy.io.wavfile import read
import numpy as np
import json



"""calculates multivariate gaussian matrix from mean and covariance matrices"""
def multivariate_gaussian(x, meu, cov):

    det = np.linalg.det(cov)
    val = np.exp(-0.5 * np.dot(np.dot((x-meu).T, np.linalg.inv(cov)), (x-meu)))
    try:
        val /= np.sqrt(((2*np.pi)**12)*det)
    except:
        print('Matrix is not positive, semi-definite')
    if np.isnan(val):
        val = np.finfo(float).eps
    return val


"""initialize the emission, transition and initialisation matrices for HMM in chord recognition
PI - initialisation matrix, #A - transition matrix, #B - observation matrix"""
def initialize(chroma, templates, nested_cof):

    """initialising PI with equal probabilities"""
    PI = np.ones(24)/24

    """initialising A based on nested circle of fifths"""
    eps = 0.01
    A = np.empty((24,24))
    for chord in chords:
        ind = nested_cof.index(chord)
        t = ind
        for i in range(24):
            if t >= 24:
                t = t%24
            A[ind][t] = (abs(12-i)+eps)/(144 + 24*eps)
            t += 1

    """initialising based on tonic triads - Mean matrix; Tonic with dominant - 0.8,
    tonic with mediant 0.6 and mediant-dominant 0.8, non-triad diagonal	elements 
    with 0.2 - covariance matrix"""


    offset = 0
    cov_mat = np.zeros((24,12,12))
    for i in range(24):
        if i == 12:
            offset = 0
        tonic = offset
        if i<12:
            mediant = (tonic + 4)%12
        else:
            mediant = (tonic + 3)%12
        dominant = (tonic+7)%12

        #weighted diagonal
        cov_mat[i,tonic,tonic] = 0.8
        cov_mat[i,mediant,mediant] = 0.6
        cov_mat[i,dominant,dominant] = 0.8

        #off-diagonal - matrix not positive semidefinite, hence determinant is negative
        # for n in [tonic,mediant,dominant]:
        # 	for m in [tonic, mediant, dominant]:
        # 		if (n is tonic and m is mediant) or (n is mediant and m is tonic):
        # 			cov_mat[i,n,m] = 0.6
        # 		else:
        # 			cov_mat[i,n,m] = 0.8

        #filling non zero diagonals
        for j in range(12):
            if cov_mat[i,j,j] == 0:
                cov_mat[i,j,j] = 0.2
        offset += 1


    """observation matrix B is a multivariate Gaussian calculated from mean vector and 
    covariance matrix"""

    B = np.zeros(24)
    meu_mat = np.array(templates)
    for n in range(24):
        B[n] = multivariate_gaussian(chroma, meu_mat[n,:],cov_mat[n,:,:])

    return (PI,A,B)



"""Viterbi algorithm to find Path with highest probability - dynamic programming"""

def viterbi(PI,A,B):
    nrow = len(B)
    states = np.zeros(len(B))
    path = PI * B

    for j in range(nrow):
        s = [(path[k] * A[k,j] * B[j], k) for k in range(nrow)]
        (prob,state) = max(s)
        path[j] = prob
        states[j] = state

    return (path,states)


"""read from JSON file to get chord templates"""

with open('chord_templates.json', 'r') as fp:
    templates_json = json.load(fp)

chords = ['G','G#','A','A#','B','C','C#','D','D#','E','F','F#','Gm','G#m','Am','A#m','Bm','Cm','C#m','Dm','D#m','Em','Fm','F#m']
nested_cof = ['G','Bm','D','F#m','A','C#m','E','G#m','B','D#m','F#','A#m','C#',"Fm","G#",'Cm','D#','Gm','A#','Dm','F','Am','C','Em']
templates = []

for chord in chords:
    templates.append(templates_json[chord])

def compute_chord_for_frame(frame, frame_rate):
    frame = frame[::4]
    frame_rate = int(frame_rate / 4)

    chroma = compute_chroma(frame, frame_rate)
    if np.all(chroma == 0):
        chroma = np.finfo(float).eps
    else:
        chroma /= np.max(np.absolute(chroma))

    #get max probability path from Viterbi algorithm
    (PI,A,B) = initialize(chroma, templates, nested_cof)
    (path, states) = viterbi(PI,A,B)

    #normalize path
    # for i in range(nFrames):
    path /= sum(path)

    #choose most likely chord - with max value in 'path'
    indicator = np.argmax(path,axis=0)


    #find no chord zone
    set_zero = np.where(np.max(path,axis=0) < 0.3*np.max(path))
    if np.size(set_zero) is not 0:
        return 'NC'

    #identify chords
    final_state = states[indicator]
    final_chord = chords[int(final_state)]
    return final_chord







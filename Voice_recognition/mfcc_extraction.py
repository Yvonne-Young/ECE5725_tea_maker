#==============================================================================#
# file: mfcc_extraction.py
# author: Yifan Yang
# updated: 11/24/2019
#==============================================================================#

import librosa
import numpy as np
import matplotlib.pyplot as plt

def mfcc_extraction(file_name):
    y,sr = librosa.load(file_name)
    hop_length = 512
    mfcc = librosa.feature.mfcc(y=y,sr=sr,hop_length=hop_length,n_mfcc=13)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta_delta = librosa.feature.delta(mfcc_delta)
    feature = np.vstack([mfcc,mfcc_delta,mfcc_delta_delta])
    return feature
  
if __name__ == '__main__':
    feature = mfcc_extraction("F:\EE\graduation project\dataset\BiCASLer\HouJingchao\SA1.wav")
    feature = feature.T
    fig = plt.plot(figsize=(6,10))
    plt.imshow(feature,extent=[0,13,500,0],aspect='auto')
    plt.colorbar()
    #plt.savefig("C:\Users\win\Desktop\SA1_hou.png")

#===============================================================================#
# file: training.py
# author: Yifan Yang
# updated: 11/24/2019
# ==============================================================================#

from mfcc_extraction import *
from speaker import *
import numpy as np
import wave
import string 
import time 
import joblib


#get all GMM models of speakers in dataset
#model parameters are saved as xxx.model
def training():
    dataset = os.listdir("/home/pi/project/ECE5725_tea_maker/voice_set/")
    speaker_list = []
    speaker_dic = {}
    
    for name in dataset:
        sub_dir = "/home/pi/project/ECE5725_tea_maker/voice_set/%s"%name
        speaker_i = Speaker(name,sub_dir)
        print (name)
        gmm = speaker_i.get_GMM()
        joblib.dump(gmm,'%s.model'%name)
        print ("done")
        speaker_list.append(speaker_i)
        speaker_dic[name] = speaker_i
    return speaker_dic

if __name__ == '__main__':
    training()

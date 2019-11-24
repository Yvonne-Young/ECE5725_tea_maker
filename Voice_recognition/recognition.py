#==============================================================================#
# file: recognition.py
# author: Yifan Yang
# updated: 11/24/2019
#==============================================================================#

from mfcc_extraction import *
from speaker import *
import numpy as np
import wave
import string 
import time 
from sklearn.externals import joblib    

#test all speakers in the TEST dataset
#calculate the recognition correctness rate
if __name__ == '__main__':
    start = time.clock()
    scores = {}
    count = 0
    dataset = os.listdir("/Users/yvonneyoung/Desktop/ECE5725_tea_maker/voice_set/")
    
    for name in dataset:
        utter_feature = []
        print "The tested speaker is: "+name
        fp1 = "F:\EE\graduation project\dataset\TEST\%s\SX307.wav"%name
        fp2 = "F:\EE\graduation project\dataset\TEST\%s\SX397.wav"%name
        utter_mfcc = mfcc_extraction(fp1)
        utter_feature.extend(utter_mfcc.T)
        utter_mfcc = mfcc_extraction(fp2)
        utter_feature.extend(utter_mfcc.T)
        utter_feature = Normalizer().fit_transform(utter_feature)
        for k in dataset:
            estimator = joblib.load("%s.model"%k)
            score = estimator.score(utter_feature)
            scores[k] = score
        predicted_speaker = max(scores,key=scores.get)
        print "The predicted speaker is: "+predicted_speaker
        if name == predicted_speaker:
            print "Identification passed!"
            count += 1

    end = time.clock()       
    print "The correctness rate of identification is "+str(count)+"/30"
    print "Run time: %s seconds"%(end-start)

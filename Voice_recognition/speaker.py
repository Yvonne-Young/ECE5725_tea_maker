#==============================================================================#
# file: speaker.py
# author: Yifan Yang
# updated: 12.24/2019
#==============================================================================#

from sklearn.preprocessing import Normalizer
from sklearn.mixture import GaussianMixture
from mfcc_extraction import *
import os
import wave

class Speaker(object):
    def __init__(self,speaker_id,wave_file,feature=None,model=None):
        self.speaker_id = speaker_id
        self.wave_file = wave_file
        self.feature = feature
        self.model = model

    def get_mfcc(self):
        mfcc = []
        files = os.listdir(self.wave_file)
        print files
        waves = []
        for i in files:
            if os.path.splitext(i)[1] == ".wav":
                waves.append(i)
        for file in files:
            fp = "/Users/yvonneyoung/Desktop/ECE5725_tea_maker/voice_set/%s/%s"%(self.speaker_id,file)
            mfcc_file = mfcc_extraction(fp)
            mfcc.extend(mfcc_file.T)
            self.feature = mfcc
        print np.shape(mfcc)
        return mfcc

    def get_GMM(self):
        mfcc = self.get_mfcc()
        K = 4
        mfcc = Normalizer().fit_transform(mfcc)
        estimator = GaussianMixture(n_components=K,covariance_type="full",max_iter=200,random_state=0,tol=1e-5)
        print "building GMM model..."
        estimator.fit(mfcc)
        self.model = estimator
        return estimator


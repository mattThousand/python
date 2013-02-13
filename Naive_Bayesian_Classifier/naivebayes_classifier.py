#===================================================================================
# Title: Naive Bayesian Classifier
# Author: Matt Buckley
# Description: Takes as input a comma delimited list in the form 'variable,feature',
# and outputs predicted values, test values, and RMSE as a measure of model preformance
# Liscense: MIT license: http://www.opensource.org/licenses/mit-license.php 
#===================================================================================

import sys
import collections
import numpy
import math

class bayesian_classifier:
    def __init__(self):
        self.lines=sys.stdin.readlines()
        self.featureCounts=collections.Counter()
        self.test_indices=numpy.random.randint(0,len(self.lines), round(len(self.lines)/4))
        self.train_indices=list(set(i for i in xrange(len(self.lines)))-set(self.test_indices))
        self.data_test=[self.lines[i].strip().split(',') for i in self.test_indices]
        self.data_train=[self.lines[i].strip().split(',') for i in self.train_indices]
        
    def get_trainingDataCounts(self):
        conditionals=collections.Counter()
        priors=collections.defaultdict(int)
        for line in self.data_train:
            feature1, feature2=line
            conditionals.update(((feature1,feature2),))
            priors[feature1]+=1
            priors[feature2]+=1
        for i in conditionals:
            conditionals[i]=(float(conditionals[i])/float(len(self.data_train)))
        for i in priors:
            priors[i]=(float(priors[i])/float(len(self.data_train)))
        return priors, conditionals
    
    def test_classifier(self, conditionals, priors):
        print 'PREDICTED VALUES:'
        pred_conditionals=[]
        pred=[]
        for i in conditionals:
            print '%s: %i'% (i, round(len(self.data_test)*conditionals[i]))
            pred_conditionals.append(round(len(self.data_test)*conditionals[i]))
        for i in priors:
            #print '%s: %i'% (i, round(len(self.data_test)*priors[i]))
            pred.append(round(len(self.data_test)*priors[i]))
        print 'TEST DATA:'
        conditionals_test=collections.Counter()
        priors_test=collections.defaultdict(int)
        for line in self.data_test:
            feature1, feature2=line
            conditionals_test.update(((feature1,feature2),))
            priors_test[feature1]+=1
            priors_test[feature2]+=1
        index=0
        for i in conditionals_test:
            pred_conditionals[index]=(pred_conditionals[index]-conditionals_test[i])**2
            print '%s: %i'% (i,conditionals_test[i])
            index+=1
        #for i in priors_test:
            #print '%s: %i'% (i,priors_test[i])
        print '%s: %f' % ('RMSE',math.sqrt(sum(pred_conditionals)/len(pred_conditionals))) 
    

if __name__ == '__main__':
    classifier=bayesian_classifier()
    priors, conditionals=classifier.get_trainingDataCounts()
    #print priors, conditionals
    classifier.test_classifier(conditionals,priors)
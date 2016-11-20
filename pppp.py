import numpy as np
from sklearn.decomposition import PCA

import pandas as pd
import numpy as np
import csv as csv

from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
train_raw=pd.read_csv('train.csv',header=0)
test_raw=pd.read_csv('test.csv',header=0)

knn = KNeighborsClassifier()

train = train_raw.values
test = test_raw.values
print ('Start PCA to 100')

train_x=train[0::,1::]
pca = PCA(n_components=100, whiten=True).fit(train_x)
train_x_pca=pca.transform(train_x)
test_x_pca=pca.transform(test)
print ('Start training')

knn.fit(train_x_pca,train[0::,0])
print ('Start predicting')
out=knn.predict(test_x_pca)
print ('Start writing!')
n,m=test_x_pca.shape
ids = range(1,n+1)
predictions_file = open("out_pca_100.csv","wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["ImageId","Label"])
open_file_object.writerows(zip(ids,out))
predictions_file.close()
print ('All is done')


#sndandasd


#new dev test bwbwbbw
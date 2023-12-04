# -*- coding: utf-8 -*-
"""Ann_churn_modelling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L3f_eGF3M5GNPaouLiSeihyoiJ1lBOLH
"""

import tensorflow as tf
print(tf.__version__)

##import some basic libararies##
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset=pd.read_csv('Churn_Modelling.csv')
dataset.head

# convert the data set into independent and dependent features#
x=dataset.iloc[:,3:13]
y=dataset.iloc[:,13]
x.head()

y

#feature engineering converting geography and gender into one hot endoded#
geography=pd.get_dummies(x['Geography'],drop_first=True)
gender=pd.get_dummies(x['Gender'],drop_first=True)

#concatenate the VARIABLES WITH DATAFRAME##
x=x.drop(['Geography','Gender'],axis=1)
x.head()

x=pd.concat([x,geography,gender],axis=1)

#splitting the dataset into traning set and test set#
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)

##feature scaling ( required only for distancebased algorithms,ex.-Kmeans Knn)
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
x_train=sc.fit_transform(x_train)
x_test=sc.transform(x_test)

x_train

x_test

x_train.shape

#part 2 To create the ANN##
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LeakyReLU, PReLU, ELU, ReLU     # Activations
from tensorflow.keras.layers import Dropout     # used in cutting off the neuron if deactivated, basically reduce the overfittinng and work in an efficient way #

# lets intialize ANN
classifier=Sequential()

# adding the input layer
classifier.add(Dense(units=11, activation='relu'))

#adding the first hidden layer
classifier.add(Dense(units=7, activation='relu'))

#adding the second hidden layer
classifier.add(Dense(units=6,activation='relu'))

## Adding the output layer
classifier.add(Dense(1,activation='sigmoid'))  #output layer and is have the binary classification therefore the acivations function is sigmoid #

import tensorflow
opt=tensorflow.keras.optimizers.Adam(learning_rate=0.01)  #additionaly if to update the adam ##  # to specify the learning rate, replace the adam to opt in the  code

classifier.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])   # Adam (Adaptive Moment Estimation) works with momentums of first and second order#

# Early stopping ## Stop training when a monitored metric has stopped improving
import tensorflow as tf
early_stopping=tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    min_delta=0.0001,
    patience=20,
    verbose=1,
    mode="auto",
    baseline=None,
    restore_best_weights=False,
)

model=classifier.fit(x_train,y_train,validation_split=0.33,batch_size=10,epochs=1000,callbacks=early_stopping)

model.history.keys()

plt.plot(model.history['accuracy'], label='Training Accuracy')
plt.plot(model.history['val_accuracy'], label='Validation Accuracy')

# Set labels and title
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Model Accuracy')

# Add a legend
plt.legend()

# Show the plot
plt.show()

plt.plot(model.history['loss'], label='Training Loss')
plt.plot(model.history['val_loss'], label='Validation Loss')

# Set labels and title
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Model Loss')

# Add a legend
plt.legend(loc='upper right')

# Show the plot
plt.show()

#predicting the test set result
y_predict= classifier.predict(x_test)
y_predict=(y_predict>0.5)
y_predict

#make the confusion metrics
import seaborn as sns
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_predict)
sns.heatmap(cm, annot=True, fmt="d", cmap="Reds", xticklabels=['Not Churned', 'Churned'], yticklabels=['Not Churned', 'Churned'])

# Add labels, title, and show the plot
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

#claculate the accuracy
from sklearn.metrics import accuracy_score
score=accuracy_score(y_test,y_predict)
score

#to get the weights of neurons
classifier.get_weights()

classifier.save('ANN_churn_modelling.h5')
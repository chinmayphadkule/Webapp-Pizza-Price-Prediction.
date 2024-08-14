
import pandas as pd
import numpy as np

import pickle

# df  = pd.read_csv('final_pizza.csv',index_col= 0)
# df = df.drop(['time','date'], axis=1)

# li = [1,'Classic', 'Sliced Ham, Pineapple, Mozzarella Cheese', 'M', 'Thursday']
# sample = np.array(li)
# print(len(sample))
class Pizza_Sales_Model():
    @staticmethod
    def give_prediction(sample):

        li = []
        
        li.append(int(sample[0]))

        
        f1 = open('pickle_files/category.pkl','rb')
        l_enc1 = pickle.load(f1)
        li.append(l_enc1.transform([sample[1]])[0])
        
        f2 = open('pickle_files/ingredients.pkl','rb')
        l_enc2 = pickle.load(f2)
        li.append((l_enc2.transform([sample[2]]))[0])
        
        f3 = open('pickle_files/size.pkl','rb')
        l_enc3 = pickle.load(f3)
        li.append(l_enc3.transform([sample[3]])[0])
        
        f4 = open('pickle_files/weekday.pkl','rb')
        l_enc4 = pickle.load(f4)
        li.append(l_enc4.transform([sample[4]])[0])
        
        encoded_sample = np.array([li])
        encoded_sample
        
        model = pickle.load(open('pickle_files/modelRFR.pkl','rb'))
        pred = model.predict(encoded_sample)
        return pred


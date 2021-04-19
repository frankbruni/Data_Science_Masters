import pandas as pd
import os
import numpy as np

# Create Full Dataset from NYT Articles
full_data = pd.DataFrame()
for date in os.listdir('headlines'):
    path = os.path.join('headlines', date)
    month_data = pd.read_csv(path)
    full_data = pd.concat([full_data, month_data])
full_data.to_csv('dataset/full_nyt_dataset.csv', index=False)

full_data

# split the data into train, validation, and test set (60%, 20% , 20%)
train, val, test = np.split(full_data.sample(frac=1, random_state=42), [
                            int(.6*len(full_data)), int(.8*len(full_data))])
# training set has 119299 rows
train.to_csv('dataset/train_dataset.csv', index=False)
# testing set has 39767 rows
val.to_csv('dataset/val_dataset.csv', index=False)
# validation set has 39767 rows
test.to_csv('dataset/test_dataset.csv', index=False)

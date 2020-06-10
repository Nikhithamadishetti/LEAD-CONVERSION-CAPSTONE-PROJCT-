import pandas as pd
from pandas_profiling import ProfileReport
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
data = pd.read_excel("modified-leadconversion.xlsx")

data.isnull().sum()

data.dtypes

cat_columns = data.select_dtypes(['object']).columns
data[cat_columns] = data[cat_columns].apply(lambda x: x.astype('category'))
cat_to_code = {col: dict(zip(data[col], data[col].cat.codes)) for col in cat_columns}
code_to_cat = {k: {v2: k2 for k2, v2 in v.items()} for k, v in cat_to_code.items()}
data[cat_columns] = data[cat_columns].apply(lambda x: x.cat.codes)

data.info()
x = data.loc[:, data.columns != 'Converted']
x.head()
y = data['Converted']
y.head()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
logreg = LogisticRegression()
logreg.fit(x_train,y_train)
y_pred=logreg.predict(x_test)
logreg.coef_
t = logreg.predict_proba(x_test)
t
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

################# Random Forest ##################################
x = data.loc[:, data.columns != 'Converted']
y = data['Converted']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20,random_state=0)

from sklearn.ensemble import RandomForestClassifier
rf=RandomForestClassifier(n_estimators=1000,random_state=14)
rf.fit(x_train,y_train)

accuracy=rf.score(x_test,y_test)*100
print("Random Forest Accuracy Score :" ,accuracy)


# save the model to disk
import pickle
filename = 'model/model.pkl'
pickle.dump(rf, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(x_test, y_test)
print(result)

#testing
prediction = rf.predict([[0,8,1,5,87,0,0,186,0,0,26,2791]])
prediction
int(prediction[0])
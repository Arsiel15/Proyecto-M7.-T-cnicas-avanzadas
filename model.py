from funtion import encode
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv('Your_Career_Aspirations_of_GenZ.csv')
df.head()

"""# Plots"""

plt.figure(figsize=(12, 6))
sns.countplot(y=df['What is the most preferred working environment for you.'], order = df['What is the most preferred working environment for you.'].value_counts().index)
plt.title('Distribución de Preferencias de Entorno de Trabajo')
plt.xlabel('Número de Respuestas')
plt.ylabel('Tipo de Entorno de Trabajo')
plt.show()

plt.figure(figsize=(12, 6))
sns.countplot(x='Your Gender', hue='What is the most preferred working environment for you.', data=df)
plt.title('Preferencias de Entorno de Trabajo por Género')
plt.xlabel('Género')
plt.ylabel('Número de Respuestas')
plt.legend(title='Entorno de Trabajo', loc='upper right')
plt.show()

data = encode(df)

"""## Correlation matrix"""

correlations = data.corr()
correlations[correlations > 0.1]

# Find the correlation above 0.1
high_corr_columns = correlations.index[abs(correlations['misalign_actions']) > 0.1]

with open("columns.txt", "w") as f:
    f.write(",".join(high_corr_columns))
# Select Columns with high correlation
high_corr_data = data[high_corr_columns]

# Display columns
print(high_corr_columns)

"""## Change column type to str"""

le = LabelEncoder()
for col in high_corr_data.columns:
    if high_corr_data[col].dtype == 'object':
        high_corr_data[col] = le.fit_transform(high_corr_data[col].astype(str))

high_corr_data.head()

"""## Build RFC model to confirm importance of columns"""

rf = RandomForestClassifier()
rf.fit(high_corr_data.drop('misalign_actions', axis=1), high_corr_data['misalign_actions'])

"""## Show feature importance"""

feature_importance = pd.DataFrame({'feature': high_corr_data.drop('misalign_actions', axis=1).columns,
                                   'importance': rf.feature_importances_}).sort_values('importance', ascending=False)

print(feature_importance)

"""## Split data misalign_actions will be or target column"""

X = high_corr_data.drop('misalign_actions', axis=1)
y = high_corr_data['misalign_actions']

# Split data for test and train - 80/20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict test data
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

joblib.dump(clf,'./Model.joblib')
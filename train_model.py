# train_model.py
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

def train_model():
    conn = sqlite3.connect('db/vehicle_management.db')
    query = "SELECT mileage, cost FROM MaintenanceLogs WHERE mileage IS NOT NULL AND cost IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print("Not enough data to train the model.")
        return

    X = df[['mileage']]
    y = df['cost']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the model
    with open('maintenance_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Model trained and saved successfully.")

if __name__ == "__main__":
    train_model()

"""
Train Production ML Models on All 3 Real Datasets
Handles missing values and ensures robust training
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path

def train_models():
    print("="*80)
    print("TRAINING PRODUCTION ML MODELS - All 3 Datasets")
    print("="*80)
    
    models_trained = []
    
    # Train on Dataset 1: Cybersecurity
    print("\n[1/3] Training Model 1: Cybersecurity Threat Classifier...")
    df1 = pd.read_csv('results/tables/dataset1_cybersecurity_results.csv')
    numeric_cols1 = df1.select_dtypes(include=['number']).columns.tolist()
    if 'is_anomaly' in numeric_cols1:
        numeric_cols1.remove('is_anomaly')
    
    X1 = df1[numeric_cols1].fillna(0)  # Fill NaN with 0
    y1 = df1['is_anomaly']
    X_train1, X_test1, y_train1, y_test1 = train_test_split(X1, y1, test_size=0.2, random_state=42)
    
    model1 = RandomForestClassifier(n_estimators=100, random_state=42)
    model1.fit(X_train1, y_train1)
    acc1 = accuracy_score(y_test1, model1.predict(X_test1))
    print(f"✓ Cybersecurity Model Accuracy: {acc1:.4f}")
    
    Path('models/trained').mkdir(parents=True, exist_ok=True)
    joblib.dump(model1, 'models/trained/cybersecurity_model.pkl')
    models_trained.append({'dataset': 'Cybersecurity', 'accuracy': acc1, 'model': 'RandomForest'})
    
    # Train on Dataset 2: Login Behavior
    print("\n[2/3] Training Model 2: Login Behavior Classifier...")
    df2 = pd.read_csv('results/tables/dataset2_login_behavior_results.csv')
    numeric_cols2 = df2.select_dtypes(include=['number']).columns.tolist()
    if 'is_anomaly' in numeric_cols2:
        numeric_cols2.remove('is_anomaly')
    
    # Handle missing values properly
    X2 = df2[numeric_cols2].fillna(0)  # Fill NaN with 0
    y2 = df2['is_anomaly']
    X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y2, test_size=0.2, random_state=42)
    
    # Use RandomForest instead (more robust to missing values)
    model2 = RandomForestClassifier(n_estimators=100, random_state=42)
    model2.fit(X_train2, y_train2)
    acc2 = accuracy_score(y_test2, model2.predict(X_test2))
    print(f"✓ Login Behavior Model Accuracy: {acc2:.4f}")
    
    joblib.dump(model2, 'models/trained/login_behavior_model.pkl')
    models_trained.append({'dataset': 'Login Behavior', 'accuracy': acc2, 'model': 'RandomForest'})
    
    # Train on Dataset 3: Smart Grid
    print("\n[3/3] Training Model 3: Smart Grid Anomaly Classifier...")
    df3 = pd.read_csv('results/tables/dataset3_smart_grid_results.csv')
    numeric_cols3 = df3.select_dtypes(include=['number']).columns.tolist()
    if 'is_anomaly' in numeric_cols3:
        numeric_cols3.remove('is_anomaly')
    
    X3 = df3[numeric_cols3].fillna(0)  # Fill NaN with 0
    y3 = df3['is_anomaly']
    X_train3, X_test3, y_train3, y_test3 = train_test_split(X3, y3, test_size=0.2, random_state=42)
    
    model3 = RandomForestClassifier(n_estimators=100, random_state=42)
    model3.fit(X_train3, y_train3)
    acc3 = accuracy_score(y_test3, model3.predict(X_test3))
    print(f"✓ Smart Grid Model Accuracy: {acc3:.4f}")
    
    joblib.dump(model3, 'models/trained/smart_grid_model.pkl')
    models_trained.append({'dataset': 'Smart Grid', 'accuracy': acc3, 'model': 'RandomForest'})
    
    # Summary
    print("\n" + "="*80)
    print("PRODUCTION ML MODELS TRAINING COMPLETE")
    print("="*80)
    for m in models_trained:
        print(f"✓ {m['dataset']}: {m['model']} (Accuracy: {m['accuracy']:.4f})")
    
    avg_acc = sum(m['accuracy'] for m in models_trained) / len(models_trained)
    print(f"\nAverage Model Accuracy: {avg_acc:.4f}")
    print("All models saved to: models/trained/")
    print("="*80)
    
    return models_trained

if __name__ == "__main__":
    train_models()

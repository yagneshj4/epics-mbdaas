"""
Training Pipeline - Real ML Model Training on Anonymized Data
Trains models on privacy-preserved data for production use
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from pathlib import Path

class TrainingPipeline:
    def __init__(self):
        self.models = {}
        print("Training Pipeline Initialized")
    
    def train_anomaly_model(self, data_path='data/anonymized/sample_anonymized.csv'):
        """Train production ML model on anonymized data"""
        print("="*80)
        print("TRAINING PRODUCTION ML MODEL")
        print("="*80)
        
        # Load anonymized data
        print("\n[1/5] Loading anonymized training data...")
        df = pd.read_csv(data_path)
        
        # Prepare features
        print("[2/5] Preparing features...")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'is_anomaly' in numeric_cols:
            numeric_cols.remove('is_anomaly')
        
        X = df[numeric_cols]
        # If we have labels from detection
        if 'is_anomaly' in df.columns:
            y = df['is_anomaly']
        else:
            # Unsupervised learning
            from sklearn.ensemble import IsolationForest
            iso = IsolationForest(contamination=0.1, random_state=42)
            y = iso.fit_predict(X)
            y = (y == -1).astype(int)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train multiple models
        print("[3/5] Training models...")
        models_to_train = {
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
            'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
        }
        
        best_score = 0
        best_model_name = None
        
        for name, model in models_to_train.items():
            print(f"   Training {name}...")
            model.fit(X_train, y_train)
            score = model.score(X_test, y_test)
            print(f"   {name} Accuracy: {score:.4f}")
            
            self.models[name] = {
                'model': model,
                'score': score,
                'features': numeric_cols
            }
            
            if score > best_score:
                best_score = score
                best_model_name = name
        
        # Evaluate best model
        print(f"\n[4/5] Evaluating best model: {best_model_name}")
        best_model = self.models[best_model_name]['model']
        y_pred = best_model.predict(X_test)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save model
        print("[5/5] Saving production model...")
        model_path = Path('models/trained/')
        model_path.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(best_model, model_path / 'production_model.pkl')
        joblib.dump(numeric_cols, model_path / 'feature_names.pkl')
        
        # Save metadata
        metadata = {
            'model_name': best_model_name,
            'accuracy': best_score,
            'features': numeric_cols,
            'training_date': pd.Timestamp.now().isoformat()
        }
        pd.DataFrame([metadata]).to_csv(model_path / 'model_metadata.csv', index=False)
        
        print(f"\n{'='*80}")
        print(f"TRAINING COMPLETE!")
        print(f"Best Model: {best_model_name}")
        print(f"Accuracy: {best_score:.4f}")
        print(f"Model saved to: {model_path / 'production_model.pkl'}")
        print(f"{'='*80}")
        
        return best_model

if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.train_anomaly_model()
# Training Pipeline 

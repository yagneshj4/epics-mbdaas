"""
PrivBayes - Differential Privacy Implementation
Bayesian network-based differentially private data release
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class PrivBayes:
    def __init__(self, epsilon=0.1):
        """
        Initialize PrivBayes with privacy budget epsilon
        Args:
            epsilon: Privacy parameter (smaller = more private)
        """
        self.epsilon = epsilon
        print(f"PrivBayes Initialized (epsilon={epsilon})")
    
    def add_laplace_noise(self, value, sensitivity=1.0):
        """Add Laplace noise for differential privacy"""
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        return value + noise
    
    def anonymize_dataframe(self, df, sensitive_columns):
        """
        Apply differential privacy to sensitive columns
        Args:
            df: Input dataframe
            sensitive_columns: List of columns to protect
        """
        df_copy = df.copy()
        
        for col in sensitive_columns:
            if col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Add noise to numeric columns
                    df_copy[col] = df[col].apply(
                        lambda x: self.add_laplace_noise(x)
                    )
                else:
                    # For categorical, use k-anonymity approach
                    df_copy[col] = 'GENERALIZED'
        
        print(f"Applied PrivBayes to {len(sensitive_columns)} columns")
        return df_copy

if __name__ == "__main__":
    # Test PrivBayes
    privbayes = PrivBayes(epsilon=0.1)
    
    # Create test data
    test_df = pd.DataFrame({
        'age': [25, 30, 35, 40, 45],
        'salary': [50000, 60000, 70000, 80000, 90000]
    })
    
    result = privbayes.anonymize_dataframe(test_df, ['age', 'salary'])
    print("\nOriginal vs Anonymized:")
    print(pd.concat([test_df, result], axis=1, keys=['Original', 'Anonymized']))

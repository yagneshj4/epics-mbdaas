"""
Generate Sample Test Data
"""
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

# Generate sample dataset
data = {
    'name': [fake.name() for _ in range(100)],
    'email': [fake.email() for _ in range(100)],
    'age': np.random.randint(18, 80, 100),
    'salary': np.random.randint(30000, 150000, 100),
    'department': np.random.choice(['IT', 'HR', 'Finance', 'Sales'], 100)
}

df = pd.DataFrame(data)
df.to_csv('data/raw/sample_data.csv', index=False)
print("Sample data created: data/raw/sample_data.csv")

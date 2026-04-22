"""
Fake News Detection Model Training Script
Trains a LogisticRegression model on fake and real news datasets.
"""

import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def load_and_prepare_data(fake_path, true_path):
    """Load fake and real news datasets and combine them."""
    # Load datasets with optimized parameters
    try:
        print(f"Loading {fake_path}...")
        fake_df = pd.read_csv(
            fake_path,
            encoding='utf-8',
            on_bad_lines='skip',
            engine='python'
        )
        print(f"  Loaded {len(fake_df)} rows")
    except Exception as e:
        print(f"Error loading {fake_path}: {e}")
        raise
    
    try:
        print(f"Loading {true_path}...")
        true_df = pd.read_csv(
            true_path,
            encoding='utf-8',
            on_bad_lines='skip',
            engine='python'
        )
        print(f"  Loaded {len(true_df)} rows")
    except Exception as e:
        print(f"Error loading {true_path}: {e}")
        raise
    
    # Add label column (0 for fake, 1 for real)
    fake_df['label'] = 0
    true_df['label'] = 1
    
    # Combine datasets
    df = pd.concat([fake_df, true_df], ignore_index=True)
    
    # Verify text column exists
    if 'text' not in df.columns:
        print(f"Available columns: {df.columns.tolist()}")
        raise ValueError("'text' column not found in datasets")
    
    # Remove rows with missing text
    df = df.dropna(subset=['text'])
    print(f"  After removing null values: {len(df)} rows")
    
    return df


def train_model(df):
    """Train the fake news detection model."""
    # Extract text column and convert to string
    X = df['text'].astype(str)
    y = df['label']
    
    print(f"Dataset size: {len(X)}")
    print(f"Fake news samples: {(y == 0).sum()}")
    print(f"Real news samples: {(y == 1).sum()}")
    
    # Split into train/test (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Vectorize text using TfidfVectorizer
    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_df=0.7,
        min_df=2,
        max_features=5000
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"Vocabulary size: {len(vectorizer.get_feature_names_out())}")
    
    # Train LogisticRegression model
    print("Training LogisticRegression model...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )
    model.fit(X_train_tfidf, y_train)
    
    # Evaluate model
    print("Evaluating model...")
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, vectorizer, accuracy


def save_models(model, vectorizer, model_path='model.pkl', vectorizer_path='vectorizer.pkl'):
    """Save trained model and vectorizer to pickle files."""
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)


def main():
    """Main training pipeline."""
    try:
        print("Loading datasets...")
        df = load_and_prepare_data('Fake.csv', 'True.csv')
        print(f"Total samples: {len(df)}\n")
        
        print("Training model...")
        model, vectorizer, accuracy = train_model(df)
        
        print("\nSaving models...")
        save_models(model, vectorizer)
        
        print(f"\n{'='*50}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Model saved as model.pkl")
        print(f"Vectorizer saved as vectorizer.pkl")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"\nError during training: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    main()

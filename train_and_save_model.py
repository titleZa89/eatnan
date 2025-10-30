# train_and_save_model.py
import os
import joblib            # pip install joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def main(output_path="model.pkl"):
    # Load example data (replace with your own data pipeline)
    X, y = load_iris(return_X_y=True)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a model (simple, replace with your pipeline)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate (quick smoke test)
    acc = model.score(X_test, y_test)
    print(f"Test accuracy: {acc:.4f}")

    # Save with joblib (recommended for scikit-learn)
    joblib.dump(model, output_path)
    print(f"Saved model to {output_path}")

if __name__ == "__main__":
    main()
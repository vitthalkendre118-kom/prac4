from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
DATA = HERE / "data" / "raw.csv"
OUT = HERE / "data" / "processed.csv"

def main():
    HERE.joinpath("data").mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        pd.DataFrame({
            "hours": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "attendance": [55, 60, 65, 70, 75, 80, 85, 90, 95, 98],
            "target": [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        }).to_csv(DATA, index=False)
        print("Created demonstration input data.")
    df = pd.read_csv(DATA)
    if df.empty or "target" not in df.columns:
        raise ValueError("Input must be non-empty and contain target")
    X, y = df.drop(columns="target"), df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    X_train_p = scaler.fit_transform(imputer.fit_transform(X_train))
    X_test_p = scaler.transform(imputer.transform(X_test))
    output = pd.DataFrame(X_test_p, columns=X.columns)
    output["target"] = y_test.reset_index(drop=True)
    output.to_csv(OUT, index=False)
    print(f"Input rows: {len(df)}")
    print(f"Training rows: {len(X_train)}")
    print(f"Test rows: {len(X_test)}")
    print(f"Processed feature count: {X_train_p.shape[1]}")
    print(f"Saved test partition: {OUT.relative_to(HERE)}")

if __name__ == "__main__":
    main()

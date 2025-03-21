import os
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

data_path = "data_scraping"
file_path = os.path.join(data_path, "data_v2", "nba_2k_cleaned_final.csv")
df = pd.read_csv(file_path)
df = df[df["year"] <= 2024]
df = df.drop_duplicates(subset=["name", "year"], keep="first")
df = df.sort_values(by=["name", "year"])

df["previous_rating"] = df.groupby("name")["rating"].shift(1)
df["has_previous_rating"] = df["previous_rating"].notna().astype(int)
df["previous_rating"] = df["previous_rating"].fillna(0)

X = df[
    [
        "age",
        "games",
        "minutes_played_per_game",
        "field_goal_percentage",
        "three_point_field_goal_attempts_per_game",
        "three_point_field_goal_percentage",
        "total_rebounds_per_game",
        "assists_per_game",
        "steals_per_game",
        "blocks_per_game",
        "turnovers_per_game",
        "points_per_game",
        "previous_rating",
        "has_previous_rating",
    ]
]
y = df["rating"]

X = X.fillna(0)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

model = GridSearchCV(
    estimator=KNeighborsRegressor(),
    param_grid={"n_neighbors": range(1, 50)},
    scoring="neg_mean_squared_error",
)

model.fit(X_train, y_train)

best_n_neighbors = model.best_params_
print("Best n_neighbors:", best_n_neighbors)

y_hat_train = model.predict(X_train)
y_hat_test = model.predict(X_test)

train_mse = mean_squared_error(y_train, y_hat_train)
train_mae = mean_absolute_error(y_train, y_hat_train)
train_r2 = r2_score(y_train, y_hat_train)

test_mse = mean_squared_error(y_test, y_hat_test)
test_mae = mean_absolute_error(y_test, y_hat_test)
test_r2 = r2_score(y_test, y_hat_test)

print("Train Metrics:")
print(f"Training MSE: {train_mse}")
print(f"Training MAE: {train_mae}")
print(f"Training R²: {train_r2}")
print("Test Metrics:")
print(f"Testing MSE: {test_mse}")
print(f"Testing MAE: {test_mae}")
print(f"Testing R²: {test_r2}")

print(f"Total observations: {df.shape[0]}")

import os
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# Only loading data up to 2024.
data_path = "data_scraping"
file_path = os.path.join(data_path, "data_v2", "nba_2k_cleaned_final.csv")
df = pd.read_csv(file_path)
df = df[df["year"] <= 2024]
df = df.drop_duplicates(subset=["name", "year"], keep="first")
df = df.sort_values(by=["name", "year"])

df["agesq"] = df["age"] ** 2

# Create a feature for previous rating / fill missing previous ratings with 0.
df["previous_rating"] = df.groupby("name")["rating"].shift(1)
df["has_previous_rating"] = df["previous_rating"].notna().astype(int)
df["previous_rating"] = df["previous_rating"].fillna(0)

NUM_VARS = ["age","agesq","games","minutes_played_per_game",
            "field_goal_percentage","three_point_field_goal_attempts_per_game",
            "three_point_field_goal_percentage","total_rebounds_per_game","assists_per_game","steals_per_game",
            "blocks_per_game","turnovers_per_game","points_per_game","previous_rating", "has_previous_rating", "AS",
            "MVP","DPOY"]

CAT_VARS = ["position"]

X = df[[
    "age", "agesq","games", "minutes_played_per_game", "field_goal_percentage",
    "three_point_field_goal_attempts_per_game", "three_point_field_goal_percentage",
    "total_rebounds_per_game", "assists_per_game", "steals_per_game",
    "blocks_per_game", "turnovers_per_game", "points_per_game",
    "previous_rating", "has_previous_rating", "position", "AS","MVP","DPOY"
]]
y = df["rating"]

X = X.fillna(0)

X_train, X_test, y_train, y_test= train_test_split(X, y, random_state=42)

base_model = make_pipeline(
    ColumnTransformer(
        [
            ("cat_vars", OneHotEncoder(drop="first"), CAT_VARS),
            ("num_vars", make_pipeline(StandardScaler()), NUM_VARS)
        ],
        remainder="drop"
    ),
    SVR()
)

param_grid = {
    "svr__C": [0.1, 1, 10],
    "svr__epsilon": [0.01, 0.1, 1]
}

grid_search = GridSearchCV(base_model, param_grid, cv=5, scoring="neg_mean_squared_error", n_jobs=-1)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
best_params = grid_search.best_params_
print(f"\nBest Parameters: {best_params}")

y_hat_train = best_model.predict(X_train)
y_hat_test = best_model.predict(X_test)

feature_names = best_model.named_steps["columntransformer"].get_feature_names_out()

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
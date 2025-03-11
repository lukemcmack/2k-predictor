import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv("data_scraping/data_3-11/nba_combined_stats_with_slugs.csv")
df["agesq"] = df["age"] ** 2

df = df[["age","agesq","games","minutes_played_per_game",
            "field_goal_percentage","three_point_field_goal_attempts_per_game",
            "three_point_field_goal_percentage","total_rebounds_per_game","assists_per_game","steals_per_game",
            "blocks_per_game","turnovers_per_game","points_per_game",
            "position","Rating"]]

df = df.dropna()
df = df.drop_duplicates()

NUM_VARS = ["age","agesq","games","minutes_played_per_game",
            "field_goal_percentage","three_point_field_goal_attempts_per_game",
            "three_point_field_goal_percentage","total_rebounds_per_game","assists_per_game","steals_per_game",
            "blocks_per_game","turnovers_per_game","points_per_game"]

CAT_VARS = ["position"]

X = df[["age","agesq","games","minutes_played_per_game",
            "field_goal_percentage","three_point_field_goal_attempts_per_game",
            "three_point_field_goal_percentage","total_rebounds_per_game","assists_per_game","steals_per_game",
            "blocks_per_game","turnovers_per_game","points_per_game","position"]]

y = df[["Rating"]]

X_train, X_test, y_train, y_test= train_test_split(X, y, random_state=42)

model = make_pipeline(
    ColumnTransformer(
        [
            ("cat_vars", OneHotEncoder(drop="first"), CAT_VARS),
            ("num_vars", "passthrough", NUM_VARS)
        ],
        remainder="drop"
    ),
    LinearRegression()
)

model.fit(X_train, y_train)

y_hat_train = model.predict(X_train)
y_hat_test = model.predict(X_test)

train_mse = mean_squared_error(y_train, y_hat_train)
test_mse = mean_squared_error(y_test, y_hat_test)

print(train_mse)
print(test_mse)

train_r2 = r2_score(y_train, y_hat_train)
test_r2 = r2_score(y_test, y_hat_test)

print(train_r2)
print(test_r2)

feature_names = model.named_steps['columntransformer'].get_feature_names_out()
coefs = model.named_steps['linearregression'].coef_.flatten()
for name, coef in zip(feature_names, coefs):
    print(f"{name}: {coef}")

print(df.size)
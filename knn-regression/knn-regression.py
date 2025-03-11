import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# load up to 2024
file_path = r'.\data_scraping/data_3-11/nba_combined_stats_with_slugs.csv'
data = pd.read_csv(file_path)
data = data[data['year'] <= 2024]
data = data.drop_duplicates(subset=['name', 'year'], keep='first')
data = data.sort_values(by=['name', 'year'])

# use previous rating/ fill missing previous
data['previous_rating'] = data.groupby('name')['Rating'].shift(1)
data['has_previous_rating'] = data['previous_rating'].notna().astype(int)
data['previous_rating'] = data['previous_rating'].fillna(0)

# define X and y
features = [
    'age', 'games', 'minutes_played_per_game', 'field_goal_percentage',
    'three_point_field_goal_attempts_per_game', 'three_point_field_goal_percentage',
    'total_rebounds_per_game', 'assists_per_game', 'steals_per_game',
    'blocks_per_game', 'turnovers_per_game', 'points_per_game',
    'previous_rating', 'has_previous_rating'
]
X = data[features]
y = data['Rating']

# drop remaining missing's
X = X[y.notna()]
y = y[y.notna()]
X = X.fillna(0)

# split and fit
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
print("Training set shape:", X_train.shape)
print("Testing set shape:", X_test.shape)

# use gridsearch to find best neighbors
knn = KNeighborsRegressor()
param_grid = {'n_neighbors': range(5, 50)}
grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# get best knn
best_n_neighbors = grid_search.best_params_['n_neighbors']
best_knn = grid_search.best_estimator_
y_train_pred = best_knn.predict(X_train)
y_test_pred = best_knn.predict(X_test)
print("Best n_neighbors:", best_n_neighbors)

# calculate train metrics
train_mse = mean_squared_error(y_train, y_train_pred)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_r2 = r2_score(y_train, y_train_pred)

# calculate testing metrics
test_mse = mean_squared_error(y_test, y_test_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)

# print metrics
print(f"Training MSE: {train_mse}")
print(f"Training MAE: {train_mae}")
print(f"Training R²: {train_r2}")
print("Test Metrics:")
print(f"Testing MSE: {test_mse}")
print(f"Testing MAE: {test_mae}")
print(f"Testing R²: {test_r2}")
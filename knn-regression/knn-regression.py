import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error

# Step 1: Load the dataset
file_path = r'.\data_scraping/data_3-11/nba_combined_stats_with_slugs.csv'  # Use raw string or forward slashes
data = pd.read_csv(file_path)

# Step 2: Filter data up to 2024
data = data[data['year'] <= 2024]

# Step 3: Define X (features) and y (target)
features = [
    'age', 'games', 'minutes_played_per_game', 'field_goal_percentage',
    'three_point_field_goal_attempts_per_game', 'three_point_field_goal_percentage',
    'total_rebounds_per_game', 'assists_per_game', 'steals_per_game',
    'blocks_per_game', 'turnovers_per_game', 'points_per_game'
]

X = data[features]
y = data['Rating']

# Step 4: Handle missing values
# Drop rows where 'Rating' is missing (since it's the target variable)
X = X[y.notna()]
y = y[y.notna()]

# Fill missing values in X with 0 (or another placeholder)
X = X.fillna(0)

# Step 5: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Step 6: Normalize numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Check the result
print("Training set shape:", X_train.shape)
print("Testing set shape:", X_test.shape)

param_grid = {
    'n_neighbors': range(1, 21),  # Test n_neighbors from 1 to 20
    'weights': ['uniform', 'distance']  # Test both weighting schemes
}

knn = KNeighborsRegressor()
grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_mean_squared_error')

# Step 2: Fit the GridSearchCV model to the training data
grid_search.fit(X_train, y_train)

# Step 3: Get the best hyperparameters
best_n_neighbors = grid_search.best_params_['n_neighbors']
best_weights = grid_search.best_params_['weights']
print("Best n_neighbors:", best_n_neighbors)
print("Best weights:", best_weights)

# Step 4: Train the best model
best_knn = grid_search.best_estimator_

# Step 5: Make predictions on the test set
y_pred = best_knn.predict(X_test)

# Step 6: Calculate the Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error (MSE):", mse)
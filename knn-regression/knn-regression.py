import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

# Step 1: Load the dataset
file_path = r'.\data_scraping/data_3-11/nba_combined_stats_with_slugs.csv'  # Use raw string or forward slashes
data = pd.read_csv(file_path)

# Step 2: Filter data up to 2024
data = data[data['year'] <= 2024]

# Step 3: Sort the data by 'name' and 'year'
data = data.sort_values(by=['name', 'year'])

# Step 4: Create a unique ID for each player-season combination
data['ID'] = data['name'] + '_' + data['year'].astype(str)

# Step 5: Add the previous year's rating as a feature
data['Rating_prev'] = data.groupby('name')['Rating'].shift(1)

# Check the result of the shift operation
print(data[['name', 'year', 'Rating', 'Rating_prev']].head(20))

# Fill missing values in 'Rating_prev' with 0
data['Rating_prev'] = data['Rating_prev'].fillna(0)

# Verify that 'Rating_prev' is numeric
print(data['Rating_prev'].dtype)

# Check for missing values in 'Rating_prev'
print(data['Rating_prev'].isnull().sum())

# Step 6: Add a binary column to indicate whether a previous rating exists
data['has_previous_rating'] = data['Rating_prev'].apply(lambda x: 1 if x > 0 else 0)

# Step 7: Add a binary column to indicate whether a player participated in the playoffs
data['made_playoffs'] = data['games_post'].apply(lambda x: 1 if x > 0 else 0)

# Step 8: Fill missing playoff stats with 0 (or another placeholder)
playoff_columns = [col for col in data.columns if col.endswith('_post')]
data[playoff_columns] = data[playoff_columns].fillna(0)

# Step 9: Encode categorical columns (e.g., 'team', 'position')
categorical_columns = ['team', 'position']  # Add any other categorical columns here
data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)

# Step 10: Drop unnecessary columns (but keep 'name' for now)
columns_to_drop = ['year', 'name_slug', 'twok_year', 'Team', 'Height', 'Wingspan']  # Adjust as needed
data = data.drop(columns=columns_to_drop)

# Step 11: Separate features (X) and target (y)
X = data.drop(columns=['Rating', 'name'])  # Drop 'name' here
y = data['Rating']

# Step 12: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Check the result
print("Training set shape:", X_train.shape)
print("Testing set shape:", X_test.shape)

# Step 13: Normalize numerical features
numerical_features = X.select_dtypes(include=['float64', 'int64']).columns
scaler = StandardScaler()
X_train[numerical_features] = scaler.fit_transform(X_train[numerical_features])
X_test[numerical_features] = scaler.transform(X_test[numerical_features])

# Step 14: Set up GridSearchCV
param_grid = {
    'n_neighbors': range(1, 21),  # Test n_neighbors from 1 to 20
    'weights': ['uniform', 'distance']  # Test both weighting schemes
}

knn = KNeighborsRegressor()
grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_mean_squared_error')

# Step 15: Fit the GridSearchCV model
grid_search.fit(X_train, y_train)

# Step 16: Get the best hyperparameters
best_n_neighbors = grid_search.best_params_['n_neighbors']
best_weights = grid_search.best_params_['weights']
print("Best n_neighbors:", best_n_neighbors)
print("Best weights:", best_weights)

# Step 17: Train the best model
best_knn = grid_search.best_estimator_

# Step 18: Make predictions on the test set
y_pred = best_knn.predict(X_test)

# Step 19: Calculate the Mean Squared Error (MSE)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error (MSE):", mse)
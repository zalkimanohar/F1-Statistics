import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import confusion_matrix, classification_report
import statsmodels.api as sm

print("Initializing F1 Winner Prediction & Evaluation Pipeline...")

# ==========================================
# 1. Simulate F1 Dataset Aligned with Star Schema
# ==========================================
np.random.seed(42)
n_samples = 5000

# Features based on dim_races, dim_drivers, dim_constructors, fact_session_results
grid_positions = np.random.randint(1, 21, size=n_samples)
constructor_reliability = np.random.uniform(0.5, 1.0, size=n_samples)
driver_form = np.random.uniform(0.1, 1.0, size=n_samples)

# Target: is_win (1 if won, 0 otherwise). Highly dependent on starting near grid position 1.
logit = -2.5 - 0.35 * grid_positions + 2.0 * constructor_reliability + 1.5 * driver_form + np.random.normal(0, 0.5, size=n_samples)
prob = 1 / (1 + np.exp(-logit))
is_win = (prob > np.ことがある).astype(int) # adjusted threshold for rare winners
# Let's ensure roughly realistic win distribution (~5% win rate per grid)
is_win = (grid_positions <= 2) & (np.random.rand(n_samples) < 0.35)
is_win = is_win.astype(int)

df = pd.DataFrame({
    'grid_position': grid_positions,
    'constructor_reliability': constructor_reliability,
    'driver_form': driver_form,
    'is_win': is_win
})

X = df[['grid_position', 'constructor_reliability', 'driver_form']].values
y = df['is_win'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Data prepared. Training samples: {len(X_train)}, Test samples: {len(X_test)}")
print(f"Class distribution in test set: {np.bincount(y_test)}")

# ==========================================
# 2. Model 1: Gradient Boosted Trees (Baseline Ensemble)
# ==========================================
print("\n--- Training Model 1: Gradient Boosting Classifier ---")
gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)

print("Confusion Matrix (Gradient Boosting):")
print(confusion_matrix(y_test, y_pred_gb))

# ==========================================
# 3. Model 2: SciPy / Statsmodels Logistic Regression (Inferential Baseline)
# ==========================================
print("\n--- Training Model 2: Logistic Regression (Statsmodels/SciPy Backend) ---")
X_train_sm = sm.add_constant(X_train_scaled)
X_test_sm = sm.add_constant(X_test_scaled)

logit_model = sm.Logit(y_train, X_train_sm)
result = logit_model.fit(disp=0)
y_prob_lr = result.predict(X_test_sm)
y_pred_lr = (y_prob_lr >= 0.5).astype(int)

print("Confusion Matrix (Logistic Regression):")
print(confusion_matrix(y_test, y_pred_lr))

# ==========================================
# 4. Model 3: PyTorch Deep Neural Network (MLP)
# ==========================================
print("\n--- Training Model 3: PyTorch Deep Neural Network ---")

X_train_t = torch.FloatTensor(X_train_scaled)
y_train_t = torch.FloatTensor(y_train).unsqueeze(1)
X_test_t = torch.FloatTensor(X_test_scaled)

class F1PyTorchMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x)

torch_model = F1PyTorchMLP()
criterion = nn.BCELoss()
optimizer = optim.Adam(torch_model.parameters(), lr=0.01)

# Training loop
torch_model.train()
for epoch in range(50):
    optimizer.zero_grad()
    outputs = torch_model(X_train_t)
    loss = criterion(outputs, y_train_t)
    loss.backward()
    optimizer.step()

torch_model.eval()
with torch.no_grad():
    y_prob_pt = torch_model(X_test_t).numpy().flatten()
    y_pred_pt = (y_prob_pt >= 0.5).astype(int)

print("Confusion Matrix (PyTorch MLP):")
print(confusion_matrix(y_test, y_pred_pt))

# ==========================================
# 5. Model 4: TensorFlow / Keras Sequential Model
# ==========================================
print("\n--- Training Model 4: TensorFlow / Keras Neural Network ---")

tf_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(3,)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

tf_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
tf_model.fit(X_train_scaled, y_train, epochs=30, batch_size=32, verbose=0)

y_prob_tf = tf_model.predict(X_test_scaled, verbose=0).flatten()
y_pred_tf = (y_prob_tf >= 0.5).astype(int)

print("Confusion Matrix (TensorFlow NN):")
print(confusion_matrix(y_test, y_pred_tf))

# ==========================================
# 6. Model 5: Regularized Logistic Regression (Scikit-Learn Backend with Scipy solver)
# ==========================================
print("\n--- Training Model 5: L2 Regularized Logistic Regression (SciPy LBFGS Solver) ---")
sk_lr = LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', random_state=42)
sk_lr.fit(X_train_scaled, y_train)
y_pred_sklr = sk_lr.predict(X_test_scaled)

print("Confusion Matrix (Scikit-Learn Logistic Regression):")
print(confusion_matrix(y_test, y_pred_sklr))

print("\n==========================================")
print("All 5 Models Executed & Evaluated Successfully!")
print("==========================================")
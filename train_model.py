
import tensorflow as tf
import numpy as np
import random
from ayurveda_bot import get_advanced_questions, calculate_advanced_dosha, get_imbalance

# 1. Define Labels
# We need to map our string outputs to integers for the model
# Using 0-6 classes
LABEL_MAP = {
    "Vata": 0,
    "Pitta": 1,
    "Kapha": 2,
    "Vata-Pitta": 3,
    "Pitta-Vata": 3, # Treat as same class
    "Pitta-Kapha": 4,
    "Kapha-Pitta": 4,
    "Vata-Kapha": 5,
    "Kapha-Vata": 5,
    "Unknown": 6,
    "None": 6
}
REVERSE_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}

# 2. Synthetic Data Generatio
# We simulate random user answers and compute the ground truth label
def generate_data(num_samples=5000):
    questions = get_advanced_questions()
    
    X = [] # Input features
    y = [] # Target labels
    
    for _ in range(num_samples):
        # Generate random answers for 4 questions
        # Q1 has 6 options (indices 0-5)
        # Q2 has 4 options (indices 0-3)
        # Q3 has 5 options (indices 0-4)
        # Q4 has 4 options (indices 0-3)
        
        a1 = random.randint(0, 5)
        a2 = random.randint(0, 3)
        a3 = random.randint(0, 4)
        a4 = random.randint(0, 3)
        
        # Calculate ground truth using our existing logic (python functions)
        user_answers = [(0, a1), (1, a2), (2, a3), (3, a4)]
        scores = calculate_advanced_dosha(user_answers)
        imbalance = get_imbalance(scores)
        
        # Convert string label to integer
        label_idx = LABEL_MAP.get(imbalance, 6) # Default to Unknown class 6
        
        if label_idx == 6 and imbalance not in ["Unknown", "None"]:
             # If get_imbalance returns something unexpected, map it to unknown
             label_idx = 6

        X.append([float(a1), float(a2), float(a3), float(a4)])
        y.append(label_idx)
        
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)

print("Generating synthetic training data...")
X_train, y_train = generate_data()

print(f"Data generated. Shapes: X={X_train.shape}, y={y_train.shape}")


# 3. Build Model
# Simple feedforward network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(4,)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(7) # 7 classes (0-6), logits output
])

# Use sparse categorical crossentropy because labels are integers
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# 4. Train
print("\nTraining model...")
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

# 5. Convert to TFLite
print("\nConverting model to TFLite format...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model
with open('dosha_predictor.tflite', 'wb') as f:
    f.write(tflite_model)

print("\nSuccess! Model saved as 'dosha_predictor.tflite'")

# Save labels for reference
with open('labels.txt', 'w') as f:
    for i in range(7):
        # Find key for value i
        found_key = "Unknown"
        for k, v in LABEL_MAP.items():
            if v == i:
                found_key = k
                break
        f.write(f"{i}: {found_key}\n")
print("Labels saved to 'labels.txt'")

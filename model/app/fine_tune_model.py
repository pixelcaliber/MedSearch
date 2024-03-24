from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
target_layer = model.layers[-2].output
feature_extractor_model = Model(inputs=model.input, outputs=target_layer)


# X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)


# base_model = ResNet50(weights=None, include_top=False, input_shape=(224, 224, 1))
# x = base_model.output
# x = GlobalAveragePooling2D()(x)
# predictions = Dense(1024, activation='relu')(x)  # Example: 1024 units with ReLU activation
# model = Model(inputs=base_model.input, outputs=predictions)
# model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
# model.fit(X_train, X_train, epochs=10, validation_data=(X_val, X_val))  # Adjust epochs as needed

# model.save('grayscale_xray_model.h5')

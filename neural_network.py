import sys
import cv2
import glob
import keras
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


# --- FUNCTIONS ---

def shift_to_top_left(img_bin):
    
    rows = np.any(img_bin, axis=1)
    cols = np.any(img_bin, axis=0)
    
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    cropped = img_bin[rmin:rmax+1, cmin:cmax+1]
    shifted_img = np.zeros_like(img_bin)
    
    shifted_img[0:cropped.shape[0], 0:cropped.shape[1]] = cropped
    
    return shifted_img

def load_data(path :str) -> tuple[np.array,np.array]:
    
    data = []
    label = []
    for filename in glob.glob(path + '/*.jpg'):
        
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        
        img_bin = np.where(img < 220, 1, 0)     
        shifted_img_bin = shift_to_top_left(img_bin)
        
        data.append(shifted_img_bin)
        label.append(filename.split('/')[-1][0])
        
    return (np.array(data), np.array(label, dtype=np.uint8))


# --- MAIN ---

def main():
    
    # - read images -
    
    data, label = load_data("assets/numbers")
    train_data, val_data, train_labels, val_labels = train_test_split(data, label, test_size=0.1)
        
    input_units = 400
    output_units = 10
    hidden_units = [512, 256, 128]
    
    model = keras.Sequential([
        keras.Input(shape=(20, 20)),
        keras.layers.Flatten(),
        keras.layers.Dense(hidden_units[0], input_dim=input_units, activation='relu'),
        keras.layers.Dense(hidden_units[1], activation='relu'),
        keras.layers.Dense(hidden_units[2], activation='relu'),
        keras.layers.Dense(output_units, activation='softmax'),
    ])

    opt = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=opt)
    model.summary()

    encoder = OneHotEncoder(categories='auto')
    train_labels_encoded = encoder.fit_transform(train_labels.reshape(-1, 1)).toarray()
    val_labels_encoded = encoder.transform(val_labels.reshape(-1, 1)).toarray()
        
    history = model.fit(train_data, train_labels_encoded, batch_size=32, epochs=30, validation_data=(val_data, val_labels_encoded))
    
    model.save('models/model.h5')
    
    # Plot training & validation accuracy values
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()

    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()
    
    return 0

# - launcher -

if __name__ == "__main__":
    main()
import tensorflow as tf
import numpy as np
import cv2
from label import get_label_df

model = tf.keras.models.load_model("../model/best_emnist_cnn.keras")
label_df = get_label_df()


def get_predicted_text(chars):
    processed_chars = []

    for c in chars:
        rotated = cv2.rotate(c, cv2.ROTATE_90_CLOCKWISE)
        flipped = cv2.flip(rotated, 1)
        processed_chars.append(flipped)

    X = np.array(processed_chars, dtype=np.float32) / 255.0
    X = X.reshape((-1, 32, 32, 1))

    preds = model.predict(X, verbose=0)
    labels = preds.argmax(axis=1)

    chars_pred = [label_df.loc[l, 'char'] for l in labels]

    result_text = "".join(chars_pred)

    return result_text

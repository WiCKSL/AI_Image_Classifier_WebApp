import os
import uuid
import numpy as np
from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

IMG_SIZE = 128

base_model = MobileNetV2(
    input_shape=(128,128,3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(1, activation="sigmoid")
])

model.load_weights("model.weights.h5")


@app.route("/")
def intro():
    return render_template("intro.html")


@app.route("/detect", methods=["GET","POST"])
def detect():

    if request.method == "POST":

        file = request.files["file"]

        if file:

            filename = str(uuid.uuid4()) + "_" + file.filename
            filepath = os.path.join("static", filename)

            file.save(filepath)

            img = image.load_img(filepath, target_size=(IMG_SIZE,IMG_SIZE))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array/255.0

            result = model.predict(img_array)[0][0]

            if result > 0.5:
                prediction = "REAL IMAGE"
                confidence = round(result*100,2)
            else:
                prediction = "AI GENERATED IMAGE"
                confidence = round((1-result)*100,2)

            return render_template(
                "result.html",
                prediction=prediction,
                confidence=confidence,
                image_path=filepath
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
import os
from typing import List

import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow import keras

IMAGE_DIM = 224   # required/default image dimensionality


def get_model():
    model = globals().get('MODEL', None)
    if not model:
        model = load_model('src/detection/nsfw_model.h5')
        globals()['MODEL'] = model

    return model


def load_images(image_paths, image_size, verbose=True):
    '''
    Function for loading images into numpy arrays for passing to model.predict
    inputs:
        image_paths: list of image paths to load
        image_size: size into which images should be resized
        verbose: show all of the image path and sizes loaded
    outputs:
        loaded_images: loaded images on which keras model can run predictions
        loaded_image_indexes: paths of images which the function is able to process
    '''
    loaded_images = []
    loaded_image_paths = []

    for img_path in image_paths:
        try:
            if verbose:
                print(img_path, "size:", image_size)
            image = keras.preprocessing.image.load_img(
                img_path, target_size=image_size)
            image = keras.preprocessing.image.img_to_array(image)
            image /= 255
            loaded_images.append(image)
            loaded_image_paths.append(img_path)
        except Exception as ex:
            print("Image Load Failure: ", img_path, ex)

    return np.asarray(loaded_images), loaded_image_paths


def load_model(model_path):
    if model_path is None or not os.path.isfile(model_path):
        raise ValueError(
            "saved_model_path must be the valid directory of a saved model to load.")

    model = tf.keras.models.load_model(model_path, custom_objects={
                                       'KerasLayer': hub.KerasLayer})
    return model


def classify(model, input_paths, image_dim=IMAGE_DIM):
    """ Classify given a model, input paths (could be single string),
    and image dimensionality...."""
    images, _ = load_images(input_paths, (image_dim, image_dim))
    probs = classify_nd(model, images)
    return dict(zip(['data'], probs))


def classify_nd(model, nd_images):
    """ Classify given a model, image array (numpy)...."""

    model_preds = model.predict(nd_images)

    categories = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

    probs = []
    for _, single_preds in enumerate(model_preds):
        single_probs = {}
        for j, pred in enumerate(single_preds):
            single_probs[categories[j]] = round(float(pred), 6) * 100
        probs.append(single_probs)
    return probs


def predict(files: List[str]):
    model = get_model()
    image_preds = classify(model, files, IMAGE_DIM)
    return image_preds


def extract_video_frames(video_file_name: str,
                         n_frames: int,
                         destiny_folder: str) -> List[str]:
    """Extract frames from video and saves into destiny folder
    Returns list of files for each frame"""
    video_file_name = os.path.abspath(video_file_name)
    if not os.path.isfile(video_file_name):
        raise FileNotFoundError(video_file_name)
    if not os.path.isdir(destiny_folder):
        raise FileNotFoundError(destiny_folder)

    vidcap = cv2.VideoCapture(video_file_name)
    skip = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)/n_frames)
    frame = 0

    success = True
    files = []
    while success:
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame*skip)
        frame += 1
        success, image = vidcap.read()
        if success:
            frame_file_name = os.path.join(
                destiny_folder, f'frame_{frame:03}.jpg')
            if cv2.imwrite(frame_file_name, image):
                files.append(frame_file_name)
        if frame >= n_frames:
            success = False

    return files

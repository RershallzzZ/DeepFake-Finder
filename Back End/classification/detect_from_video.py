"""
Evaluates a folder of video files or a single file with a xception binary
classification network.

Usage:
python detect_from_video.py
    -i <folder with video files or path to video file>
    -m <path to model file>
    -o <path to output folder, will write one or multiple output videos there>

Author: Andreas Rössler
"""
import os
import argparse
from os.path import join
import cv2
import dlib
import torch
import torch.nn as nn
from PIL import Image as pil_image
from tqdm import tqdm
from classification.keyframe_extraction import get_keyframe
from classification.network.models import model_selection
from classification.dataset.transform import xception_default_data_transforms

# https://discuss.pytorch.org/t/problem-loading-model-trained-on-gpu/17745
# Download this and change in models.py
# https://data.lip6.fr/cadene/pretrainedmodels/

cuda = True


def get_boundingbox(face, width, height, scale=1.3, minsize=None):
    """
    Expects a dlib face to generate a quadratic bounding box.
    :param face: dlib face class
    :param width: frame width
    :param height: frame height
    :param scale: bounding box size multiplier to get a bigger face region
    :param minsize: set minimum bounding box size
    :return: x, y, bounding_box_size in opencv form
    """
    x1 = face.left()
    y1 = face.top()
    x2 = face.right()
    y2 = face.bottom()
    size_bb = int(max(x2 - x1, y2 - y1) * scale)
    if minsize:
        if size_bb < minsize:
            size_bb = minsize
    center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

    # Check for out of bounds, x-y top left corner
    x1 = max(int(center_x - size_bb // 2), 0)
    y1 = max(int(center_y - size_bb // 2), 0)
    # Check for too big bb size for given x, y
    size_bb = min(width - x1, size_bb)
    size_bb = min(height - y1, size_bb)

    return x1, y1, size_bb


def preprocess_image(image, cuda=cuda):
    """
    Preprocesses the image such that it can be fed into our network.
    During this process we envoke PIL to cast it into a PIL image.

    :param image: numpy image in opencv form (i.e., BGR and of shape
    :return: pytorch tensor of shape [1, 3, image_size, image_size], not
    necessarily casted to cuda
    """
    # Revert from BGR
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Preprocess using the preprocessing function used during training and
    # casting it to PIL image
    preprocess = xception_default_data_transforms['test']
    preprocessed_image = preprocess(pil_image.fromarray(image))
    # Add first dimension as the network expects a batch
    preprocessed_image = preprocessed_image.unsqueeze(0)
    if cuda:
        preprocessed_image = preprocessed_image.cuda()
    return preprocessed_image


def predict_with_model(image, model, post_function=nn.Softmax(dim=1),
                       cuda=cuda):
    """
    Predicts the label of an input image. Preprocesses the input image and
    casts it to cuda if required

    :param image: numpy image
    :param model: torch model with linear layer at the end
    :param post_function: e.g., softmax
    :param cuda: enables cuda, must be the same parameter as the model
    :return: prediction (1 = fake, 0 = real)
    """
    # Preprocess
    preprocessed_image = preprocess_image(image, cuda)

    # Model prediction
    output = model(preprocessed_image)
    output = post_function(output)

    # Cast to desired
    _, prediction = torch.max(output, 1)  # argmax
    prediction = float(prediction.cpu().numpy())

    return int(prediction), output


def test_full_image_network(video_path, output_path=None, image_path=None, detect_mode=None, model=None,
                            model_path=None,
                            start_frame=0, end_frame=None, threshold=.1, cuda=cuda):
    """
    Reads a video and evaluates a subset of frames with the a detection network
    that takes in a full frame. Outputs are only given if a face is present
    and the face is highlighted using dlib.
    :param video_path: path to video file
    :param model_path: path to model file (should expect the full sized image)
    :param output_path: path where the output video is stored
    :param start_frame: first frame to evaluate
    :param end_frame: last frame to evaluate
    :param cuda: enable cuda
    :return:
    """
    # Face detector
    face_detector = dlib.get_frontal_face_detector()

    # Load model
    # model, *_ = model_selection(modelname='xception', num_out_classes=2)
    if model is None:
        if model_path is not None:
            model = torch.load(model_path, map_location=lambda storage, loc: storage)
            print('Model found in {}'.format(model_path))
        else:
            print('No model found, initializing random model.')

    if cuda:
        print('CUDA!!!!!!!!!!')
        model = model.cuda()

    # Text variables
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 2
    font_scale = 1
    predictions = []

    print('Starting: {}'.format(video_path))
    reader = cv2.VideoCapture(video_path)
    if detect_mode == 1:
        os.makedirs(image_path, exist_ok=True)

        keyframe_id_set = get_keyframe(video_path, image_path)
        pbar = tqdm(total=len(keyframe_id_set))
        success, image = reader.read()
        idx = 0
        while success:
            if idx in keyframe_id_set:
                pbar.update(1)
                # Image size
                height, width = image.shape[:2]
                # 2. Detect with dlib
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_detector(gray, 1)
                if len(faces):
                    # For now only take biggest face
                    face = faces[0]

                    # --- Prediction ---------------------------------------------------
                    # Face crop with dlib and bounding box scale enlargement
                    x, y, size = get_boundingbox(face, width, height)
                    cropped_face = image[y:y + size, x:x + size]

                    # Actual prediction using our model
                    prediction, output = predict_with_model(cropped_face, model,
                                                            cuda=cuda)
                    predictions.append(prediction)
                    # ------------------------------------------------------------------

                    tqdm.write(f'prediction = {prediction}')

                    # Text and bb
                    x = face.left()
                    y = face.top()
                    w = face.right() - x
                    h = face.bottom() - y
                    label = 'fake' if prediction == 1 else 'real'
                    color = (0, 255, 0) if prediction == 0 else (0, 0, 255)
                    output_list = ['{0:.2f}'.format(float(x)) for x in
                                   output.detach().cpu().numpy()[0]]
                    cv2.putText(image, str(output_list) + '=>' + label, (x, y + h + 30),
                                font_face, font_scale,
                                color, thickness, 2)
                    # draw box over face
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

                name = "keyframe_" + str(idx) + ".png"
                cv2.imwrite(join(image_path, name), image)
                keyframe_id_set.remove(idx)
                if len(keyframe_id_set) == 0:
                    break
            idx = idx + 1
            success, image = reader.read()
        pbar.close()
        reader.release()
        cv2.destroyAllWindows()
    elif detect_mode == 2:
        # Read and write
        # os.makedirs(output_path, exist_ok=True)
        split = '/' if '/' in video_path else '\\'
        print("视频路径", video_path)
        print("输出路径", output_path)
        video_fn = video_path.split(split)[-1].split('.')[0] + '.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        fps = reader.get(cv2.CAP_PROP_FPS)
        num_frames = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))
        writer = None

        # Frame numbers and length of output video
        frame_num = 0
        assert start_frame < num_frames - 1
        end_frame = end_frame if end_frame else num_frames
        pbar = tqdm(total=end_frame - start_frame)

        while reader.isOpened():
            _, image = reader.read()
            if image is None:
                break
            frame_num += 1

            if frame_num < start_frame:
                continue
            pbar.update(1)

            # Image size
            height, width = image.shape[:2]

            # Init output writer
            if writer is None:
                print(video_fn)
                writer = cv2.VideoWriter(output_path, fourcc, fps,
                                         (height, width)[::-1])

            # 2. Detect with dlib
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_detector(gray, 1)
            if len(faces):
                # For now only take biggest face
                face = faces[0]

                # --- Prediction ---------------------------------------------------
                # Face crop with dlib and bounding box scale enlargement
                x, y, size = get_boundingbox(face, width, height)
                cropped_face = image[y:y + size, x:x + size]

                # Actual prediction using our model
                prediction, output = predict_with_model(cropped_face, model,
                                                        cuda=cuda)
                predictions.append(prediction)
                # ------------------------------------------------------------------

                tqdm.write(f'prediction = {prediction}')

                # Text and bb
                x = face.left()
                y = face.top()
                w = face.right() - x
                h = face.bottom() - y
                label = 'fake' if prediction == 1 else 'real'
                color = (0, 255, 0) if prediction == 0 else (0, 0, 255)
                output_list = ['{0:.2f}'.format(float(x)) for x in
                               output.detach().cpu().numpy()[0]]
                cv2.putText(image, str(output_list) + '=>' + label, (x, y + h + 30),
                            font_face, font_scale,
                            color, thickness, 2)
                # draw box over face
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

            if frame_num >= end_frame:
                break

            # Show
            cv2.imshow('Frame', image)
            cv2.waitKey(33)  # About 30 fps
            writer.write(image)
        pbar.close()
        reader.release()
        cv2.destroyAllWindows()
        if writer is not None:
            writer.release()
            print('Finished! Output saved under {}'.format(output_path))
        else:
            print('Input video file was empty')
    import numpy as np
    mean = np.mean(predictions)
    print('result:', mean)
    if mean >= 0.3:
        return 4
    elif 0.2 <= mean < 0.3:
        return 3
    elif 0.1 <= mean < 0.2:
        return 2
    else:
        return 1


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--video_path', '-i', type=str)
    p.add_argument('--model_path', '-m', type=str, default=None)
    p.add_argument('--output_path', '-o', type=str,
                   default='.')
    p.add_argument('--start_frame', type=int, default=0)
    p.add_argument('--end_frame', type=int, default=None)
    p.add_argument('--cuda', action='store_true')
    args = p.parse_args()

    video_path = args.video_path
    if video_path.endswith('.mp4') or video_path.endswith('.avi'):
        test_full_image_network(**vars(args))
    else:
        videos = os.listdir(video_path)
        for video in videos:
            args.video_path = join(video_path, video)
            test_full_image_network(**vars(args))

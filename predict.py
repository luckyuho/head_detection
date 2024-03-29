#! /usr/bin/env python

import argparse
import os
import cv2
import numpy as np
from tqdm import tqdm
from preprocessing import parse_annotation
from utils import draw_boxes
from frontend import YOLO
import json

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def _main_():

    config_path = 'config.json'
    # weights_path = 'full_yolo_backend.h5'
    weights_path = 'model.h5'

    with open(config_path) as config_buffer:
        config = json.load(config_buffer)

    ###############################
    #   Make the model
    ###############################

    yolo = YOLO(backend=config['model']['backend'],
                input_size=config['model']['input_size'],
                labels=config['model']['labels'],
                max_box_per_image=config['model']['max_box_per_image'],
                anchors=config['model']['anchors'])

    ###############################
    #   Load trained weights
    ###############################

    yolo.load_weights(weights_path)

    ###############################
    #   Predict bounding boxes
    ###############################

    for i in range(80):
        num = i + 21
        file_text = '/home/yuho/Face_Detection/data/photo/frame'
        image_path = file_text + str(num) + '.png'

        save_text = '/home/yuho/Face_Detection/data/save_data/frame'
        save_path = save_text + str(num) + '.png'

        # image_path   = '/home/yuho/Face_Detection/data/photo/frame56.png'
        # image_path = 'frame19.png'

        if image_path[-4:] == '.mp4':
            video_out = image_path[:-4] + '_detected' + image_path[-4:]
            video_reader = cv2.VideoCapture(image_path)

            nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))

            video_writer = cv2.VideoWriter(video_out,
                                           cv2.VideoWriter_fourcc(*'MPEG'),
                                           50.0,
                                           (frame_w, frame_h))

            for i in tqdm(range(nb_frames)):
                _, image = video_reader.read()

                boxes = yolo.predict(image)
                image = draw_boxes(image, boxes, config['model']['labels'])

                video_writer.write(np.uint8(image))

            video_reader.release()
            video_writer.release()
        else:
            image = cv2.imread(image_path)
            boxes = yolo.predict(image)

            if boxes == 0:
                pass
            else:
                image = draw_boxes(image, boxes, config['model']['labels'])

            print(len(boxes), 'boxes are found')

            cv2.imwrite(save_path, image)


if __name__ == '__main__':
    _main_()

import tensorflow as tf
import os
from model import model_fn, RestoreMovingAverageHook
from input_pipeline import Pipeline
from PIL import Image
import numpy as np

tf.logging.set_verbosity('INFO')


"""
The purpose of this script is to train a network.
Evaluation will happen periodically.

To use it just run:
python train.py

Parameters below is for training 0.5x version.
"""

# 1281144/128 = 10008.9375
# so 1 epoch ~ 10000 steps

GPU_TO_USE = '0'
PARAMS = {
    'model_dir': 'models/tzb',
    'num_classes': 2,
    'depth_multiplier': '0.5'  # set '1.0' for 1.0x version
}



session_config = tf.ConfigProto(allow_soft_placement=True)
session_config.gpu_options.visible_device_list = GPU_TO_USE
session_config.gpu_options.allow_growth = True
run_config = tf.estimator.RunConfig()
run_config = run_config.replace(model_dir=PARAMS['model_dir'], session_config=session_config)


estimator = tf.estimator.Estimator(model_fn, params=PARAMS, config=run_config)

  
#feature_spec = {'images': tf.image.resize_images(tf.placeholder(dtype=float, shape=[None, None,None,1],name='images'),[224,224])}
feature_spec = {'images': tf.placeholder(dtype=float, shape=[None, None,None,1],name='images'),
    'labels': tf.placeholder(dtype=float, shape=[None,1],name='labels')}
serving_input_fn = tf.estimator.export.build_raw_serving_input_receiver_fn(feature_spec)
estimator.export_savedmodel(PARAMS['model_dir'], serving_input_fn)


# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import time

import numpy as np
import tensorflow as tf


def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=500,
                                input_width=500,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(
        file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  sess = tf.compat.v1.Session()
  result = sess.run(normalized)

  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def find_gender(img,sess,output_operation,input_operation,label_file):
  t0 = time.time()
  t = read_tensor_from_image_file(
    img,
    input_height=299,
    input_width=299,
    input_mean=0,
    input_std=255)

  results = sess.run(output_operation.outputs[0], {
    input_operation.outputs[0]: t
  })

  results = np.squeeze(results)

  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(label_file)
  for i in top_k:
    print(labels[i], results[i])
  print(time.time() - t0)
  return labels[top_k[0]], results[top_k[0]]

if __name__ == "__main__":

  model_file = os.path.dirname(os.path.abspath(__file__)) + '/gender_model.pb'
  input_layer = 'Placeholder'
  output_layer = 'final_result'
  label_file = os.path.dirname(os.path.abspath(__file__)) + '/gender_labels.txt'
  graph = load_graph(model_file)

  input_name = "import/" + input_layer
  output_name = "import/" + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  with tf.compat.v1.Session(graph=graph) as sess:
    count_detect_men=0
    count_detect_women = 0
    count_photo_dataset_men = 0
    count_photo_dataset_women = 0
    path_dataset_men=os.path.dirname(os.path.abspath(__file__))+'/dataset_gender_tests/man'
    path_dataset_women = os.path.dirname(os.path.abspath(__file__)) + '/dataset_gender_tests/woman'

    for list_photos in os.walk(path_dataset_men):
      count_photo_dataset_men=len(list_photos[2])
      for photo in list_photos[2]:
        p,k=find_gender(path_dataset_men+'/'+photo,sess,output_operation,input_operation,label_file)
        if p=='men':
          count_detect_men=count_detect_men+1


    for list_photos in os.walk(path_dataset_women):
      count_photo_dataset_women = len(list_photos[2])
      for photo in list_photos[2]:
        p, k = find_gender(path_dataset_women + '/' + photo, sess, output_operation, input_operation, label_file)
        if p == 'women':
          count_detect_women = count_detect_women + 1

    print('Всего найдено men: ' + str(count_detect_men))
    print('Всего фотографий в наборе: ' + str(count_photo_dataset_men))
    print('Точность распознавания: ' + str(count_detect_men*100/count_photo_dataset_men))
    print('------------------------------------------------------------')
    print('Всего найдено women: ' + str(count_detect_women))
    print('Всего фотографий в наборе: ' + str(count_photo_dataset_women))
    print('Точность распознавания: ' + str(count_detect_women * 100 / count_photo_dataset_women))

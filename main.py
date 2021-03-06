import os
import tensorflow as tf
import tensorflow_hub as hub
import PIL
import numpy as np

def load_img(path_to_img):
  max_dim = 512
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img

def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)

def mian():
  style_image_path = "assets/style.png"
  style_image = load_img(style_image_path)
  hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1')
  stylized_image = hub_module(tf.constant(content_image), tf.constant(style_image))[0]
  tensor_to_image(stylized_image)

  
#for path, subdirs, files in os.walk("."):
#  print(path)

print(tf.__version__)
for root, dirs, files in os.walk("."):
  for file in files:
    if (file.endswith(".jpg") or file.endswith(".png") or file.endswith(".tiff") or file.endswith(".jpeg")):
      print(os.path.join(root, file))

style_img = PIL.Image.open("assets/sn.png")
print(style_img[0])

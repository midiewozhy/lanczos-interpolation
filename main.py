import cv2
import numpy as np
#import scipy as sp


def new_map_ori(row, col, scale_factor):

  row_ori = (row + 0.5) / scale_factor - 0.5
  col_ori = (col + 0.5) / scale_factor - 0.5

  return row_ori, col_ori


def lanczos_kernel(delta, a):
  #define the kernel
  if delta == 0:
    return 1
  elif delta > -a and delta < a:
    return np.sinc(delta) * np.sinc(delta / a)
  else:
    return 0

def new_pixel_value(row, col, a):
  #new value of pixel
  S = 0

  #sum of all the kernels
  w = 0

  row_ori, col_ori = new_map_ori(row, col, sf)
  int_row_ori, int_col_ori = int(np.floor(row_ori)), int(np.floor(col_ori))

  for i in range(int_row_ori - a + 1, int_row_ori + a + 1):
    for j in range(int_col_ori - a + 1, int_col_ori + a + 1):

      i = np.clip(i, 0, ori_height - 1)
      j = np.clip(j, 0, ori_width - 1)

      weight = lanczos_kernel(row_ori - i, a) * lanczos_kernel(col_ori - j, a)
      w += weight
      S += image[i, j] * weight

  return S / w if w != 0 else 0.0


image = cv2.imread('image.jpg')
ori_height, ori_width, _ = image.shape
sf = 2
scaled_height, scaled_width = 2 * ori_height, 2 * ori_width

scaled_image = np.zeros((scaled_height, scaled_width, 3), dtype=np.float32)
for row in range(scaled_height):
  for col in range(scaled_width):
    scaled_image[row, col] = new_pixel_value(row, col, a=3)

scaled_image = np.clip(scaled_image, 0, 255).astype(np.uint8)
cv2.imwrite('scaled_image.jpg', scaled_image)


from tensorflow import keras
import numpy as np
import os
import cv2
import csv
import config

OUTPUT = '/home/harshini/backup_to_drive/workspace/harshini/posebox/output'

smoke_testing = "/home/harshini/backup_to_drive/workspace/harshini/posebox/smoke_testing"

visualize_smoke_test = True

smoke_testing_results = "/home/harshini/backup_to_drive/workspace/harshini/posebox/smoke_testing_visualize"

ckpt_path = OUTPUT + "/ckpt" + "/weights.476-0.0456.hdf5"


data = np.empty((0,512,512,3), dtype=np.int8)
files_store = np.empty((0,1), dtype=np.str)
widths = np.empty((0,1), dtype=np.int)
heights = np.empty((0,1), dtype=np.int)

#normalizing the images bofe sending todel
for root, folders, files in os.walk(smoke_testing):
  for file in files:
    image_path = os.path.join(smoke_testing, file)
    print(image_path)
    image = cv2.imread(image_path)
    width = image.shape[0]
    height = image.shape[1]
    print(image.shape)
    image = image/255
    image = np.expand_dims(image, axis=0)
    if image is not None:
        data = np.vstack((data, image))
        files_store = np.append(files_store, str(file))
        widths = np.append(widths, width)
        heights = np.append(heights, height)

num_samples = data.shape[0]
arr = np.arange(num_samples)
np.random.shuffle(arr)
data = data[arr]

#loading the model
model = keras.models.load_model(ckpt_path)

#predicting
res = model.predict(data)
res = np.multiply(res, 512)
res = res.tolist()

#storing the output from model into csv
rows = zip(files_store, res, widths, heights)
with open(OUTPUT + '/smoke_testing_results.csv', "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

#drawing the coordinates on the image for visualization
if visualize_smoke_test:
    if not os.path.exists(smoke_testing_results):
        os.makedirs(smoke_testing_results)

    with open(OUTPUT + '/smoke_testing_results.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # print(row)
            image_name = row[0]
            image_path = os.path.join(smoke_testing,image_name)
            image = cv2.imread(image_path)
            res = row[1].strip('][').split(', ')
            res = list(res)
            cv2.circle(image, (int(float(res[0])), int(float(res[1]))), 2, [0, 0, 255], -1)
            cv2.circle(image, (int(float(res[2])), int(float(res[3]))), 2, [0, 0, 255], -1)
            cv2.circle(image, (int(float(res[4])), int(float(res[5]))), 2, [0, 0, 255], -1)
            cv2.circle(image, (int(float(res[6])), int(float(res[7]))), 2, [0, 0, 255], -1)

            cv2.imwrite(smoke_testing_results + "/" + str(image_name), image)

import numpy as np
import json
import os
from tqdm import tqdm

# file1 = np.load('/libras/video_features/palavras/i3d/0-a-noite-toda_rgb.npy')
# file2 = np.load('/libras/video_features/palavras/i3d/0-abacaxi_rgb.npy')
# file2 = np.load('/libras/video_features/palavras/i3d/0-abacaxi_rgb.npy')
# file3 = np.load('/libras/video_features/palavras/i3d/0-agua_rgb.npy')

path = '/libras/video_features/palavras/i3d/'
path_to_save = "/libras/video_features/selected_words/v76/i3d/"
rgb_suffix = '_rgb.npy'
flow_suffix = '_flow.npy'

max_stack = 0

def kebab_case(string):
  return "-".join(word.lower() for word in string.split(" "))

with open("./dataset-sentences-features.json", "r", encoding="utf-8") as file:
    dataset = json.load(file)

for item in tqdm(dataset):
    numpy_arr_rgb = []
    numpy_arr_flow = []
    #Open numpy files

    file_rgb_name = str(item.get("interpreter")) + "-" + item.get("video_name") + rgb_suffix
    file_flow_name = str(item.get("interpreter")) + "-" + item.get("video_name") + flow_suffix

    if os.path.exists(os.path.join(path_to_save, file_rgb_name)):
        continue

    for video in item.get('signs_videos'):
        video_name = video.split('.')[0]
        
        numpy_arr_rgb.append(
            np.load(path + video_name + rgb_suffix)
        )
        
        numpy_arr_flow.append(
            np.load(path + video_name + flow_suffix)
        )
    
    new_file_rgb = np.concatenate(tuple(numpy_arr_rgb))
    new_file_flow = np.concatenate(tuple(numpy_arr_flow))    

    np.save(path_to_save + file_rgb_name, new_file_rgb)
    
    np.save(path_to_save + file_flow_name, new_file_flow)
    
    if new_file_flow.shape[0] > max_stack:
        max_stack = new_file_flow.shape[0]
    #print(new_file_flow.shape)
    #print(new_file_rgb.shape)


print("MAIOR STACK", max_stack) #463

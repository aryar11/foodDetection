import os
import shutil
from collections import OrderedDict
import yaml

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Paths for the datasets
dataset2_path = r'C:\Users\Arya Rahmanian\Documents\foodDetection\data\utensils'
dataset1_path = 'C:\\Users\\Arya Rahmanian\\Documents\\foodDetection\\data\\combined'
combined_path = 'C:\\Users\\Arya Rahmanian\\Documents\\foodDetection\\data\\combined-utensils'

# Class lists from both datasets
classes1 = ['avocado', 'beans', 'beet', 'bell pepper', 'broccoli', 'brus capusta', 'cabbage', 'carrot', 'cayliflower', 'celery', 'corn', 'cucumber', 'eggplant', 'fasol', 'garlic', 'hot pepper', 'onion', 'peas', 'potato', 'pumpkin', 'rediska', 'redka', 'salad', 'squash-patisson', 'tomato', 'vegetable marrow', 'bean sprouts', 'beef', 'cheese', 'chicken', 'chili', 'daikon', 'egg', 'egg plant', 'green onion', 'ham', 'kimchi', 'lettuce', 'mushroom', 'paprika', 'pork belly', 'rice', 'sausage', 'spinach', 'sweet potato', 'tofu', 'zucchini']
classes2 = ['Can_opener', 'bottle_opener', 'fork', 'knife', 'pizza_cutter', 'spatula', 'spoon', 'tongs', 'whisk']

# Creating a unified class list
all_classes = list(OrderedDict.fromkeys(classes1 + classes2))
class_map = {cls: idx for idx, cls in enumerate(all_classes)}
print(all_classes)
# Create directories
ensure_dir(os.path.join(combined_path, 'train', 'images'))
ensure_dir(os.path.join(combined_path, 'train', 'labels'))
ensure_dir(os.path.join(combined_path, 'valid', 'images'))
ensure_dir(os.path.join(combined_path, 'valid', 'labels'))
ensure_dir(os.path.join(combined_path, 'test', 'images'))
ensure_dir(os.path.join(combined_path, 'test', 'labels'))

def copy_and_rename_files(src_dir, dest_dir, prefix, is_label=False):
    for item in os.listdir(src_dir):
        src = os.path.join(src_dir, item)
        new_name = f"{prefix}_{item}"
        dst = os.path.join(dest_dir, new_name)
        if is_label:
            # Process label files to update class indices
            with open(src, 'r') as file:
                lines = file.readlines()
            with open(dst, 'w') as file:
                for line in lines:
                    parts = line.strip().split()
                    cls = int(parts[0])
                    original_class = classes1[cls] if prefix.startswith('veg') else classes2[cls]
                    parts[0] = str(class_map[original_class])
                    file.write(' '.join(parts) + '\n')
        else:
            shutil.copy(src, dst)

# Copy and rename files from both datasets
copy_and_rename_files(os.path.join(dataset1_path, 'train', 'images'), os.path.join(combined_path, 'train', 'images'), 'veg')
copy_and_rename_files(os.path.join(dataset1_path, 'train', 'labels'), os.path.join(combined_path, 'train', 'labels'), 'veg', is_label=True)
copy_and_rename_files(os.path.join(dataset2_path, 'train', 'images'), os.path.join(combined_path, 'train', 'images'), 'ing')
copy_and_rename_files(os.path.join(dataset2_path, 'train', 'labels'), os.path.join(combined_path, 'train', 'labels'), 'ing', is_label=True)

copy_and_rename_files(os.path.join(dataset1_path, 'valid', 'images'), os.path.join(combined_path, 'valid', 'images'), 'veg')
copy_and_rename_files(os.path.join(dataset1_path, 'valid', 'labels'), os.path.join(combined_path, 'valid', 'labels'), 'veg', is_label=True)
copy_and_rename_files(os.path.join(dataset2_path, 'valid', 'images'), os.path.join(combined_path, 'valid', 'images'), 'ing')
copy_and_rename_files(os.path.join(dataset2_path, 'valid', 'labels'), os.path.join(combined_path, 'valid', 'labels'), 'ing', is_label=True)

copy_and_rename_files(os.path.join(dataset1_path, 'test', 'images'), os.path.join(combined_path, 'test', 'images'), 'veg')
copy_and_rename_files(os.path.join(dataset1_path, 'test', 'labels'), os.path.join(combined_path, 'test', 'labels'), 'veg', is_label=True)
copy_and_rename_files(os.path.join(dataset2_path, 'test', 'images'), os.path.join(combined_path, 'test', 'images'), 'ing')
copy_and_rename_files(os.path.join(dataset2_path, 'test', 'labels'), os.path.join(combined_path, 'test', 'labels'), 'ing', is_label=True)
# Create a new data.yaml file
data_yaml = {
    'train': os.path.join(combined_path, 'train', 'images'),
    'val': os.path.join(combined_path, 'valid', 'images'),
    'test': os.path.join(combined_path, 'test', 'images'),
    'nc': len(all_classes),
    'names': all_classes
}

with open(os.path.join(combined_path, 'data.yaml'), 'w') as file:
    yaml.dump(data_yaml, file, default_flow_style=False)

print("Dataset combined successfully!")

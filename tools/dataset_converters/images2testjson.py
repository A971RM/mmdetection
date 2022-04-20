# Copyright (c) OpenMMLab. All rights reserved.
import argparse
import json
import os

from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert images to coco format without annotations')
    parser.add_argument('img_path', help='The root path of images')
    parser.add_argument(
        'train_val', type=str, help='The train.json/val.json file name of storage categories list')
    parser.add_argument(
        '--out',
        dest='out',
        type=str,
        default='test.json',
        help='The output annotation json file name, The save dir is in the '
        'same directory as img_path')
    parser.add_argument(
        '-e',
        '--exclude-extensions',
        type=str,
        nargs='+',
        help='The suffix of images to be excluded, such as "png" and "bmp"')
    args = parser.parse_args()
    return args


def scandir_track_iter_progress(path, recursive = True):
    """
    返回所有扫描到的文件
    :param path:
    :param recursive:
    :return:
    """
    normpath = os.path.normpath(path)
    for dirpath, dirnames, filenames in os.walk(path):
        if not recursive and os.path.normpath(dirpath) != normpath:
            break
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def collect_image_infos(path, exclude_extensions=None, basename=True):
    img_infos = []

    for image_path in scandir_track_iter_progress(path, recursive=True):
        if exclude_extensions is None or (
                exclude_extensions is not None
                and not image_path.lower().endswith(exclude_extensions)):
            img_pillow = Image.open(image_path)
            img_info = {
                'filename': os.path.basename(image_path) if basename else image_path,
                'width': img_pillow.width,
                'height': img_pillow.height,
            }
            img_infos.append(img_info)
    return img_infos


def cvt_to_coco_json(img_infos, categories):
    image_id = 0
    coco = dict()
    coco['images'] = []
    coco['type'] = 'instance'
    coco.update(categories)
    coco['annotations'] = []
    image_set = set()

    for img_dict in img_infos:
        file_name = img_dict['filename']
        assert file_name not in image_set
        image_item = dict()
        image_item['id'] = int(image_id)
        image_item['file_name'] = str(file_name)
        image_item['height'] = int(img_dict['height'])
        image_item['width'] = int(img_dict['width'])
        coco['images'].append(image_item)
        image_set.add(file_name)

        image_id += 1
    return coco


def categories_from_file(train_val):
    """
    从train.json或者val.json中得到categories
    :param train:
    :return:
    """
    with open(train_val, 'rt', encoding='u8') as f:
        train_val_json = json.load(f)
    categories = train_val_json.get('categories', [])
    return dict(categories=categories)


def main():
    args = parse_args()
    assert args.out.endswith(
        'json'), 'The output file name must be json suffix'

    # 1 load image list info
    img_infos = collect_image_infos(args.img_path, args.exclude_extensions, basename=True)

    # 2 convert to coco format data
    categories = categories_from_file(args.train_val)
    coco_info = cvt_to_coco_json(img_infos, categories)

    # 3 dump
    save_path = args.out
    with open(save_path, 'wt') as f:
        json.dump(coco_info, f)
    print(f'save json file: {save_path}')


if __name__ == '__main__':
    main()

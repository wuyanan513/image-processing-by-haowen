import SimpleITK as sitk
import numpy as np
import os
from tqdm import trange


def get_listdir(path):  # 获取目录下所有gz格式文件的地址，返回地址list
    tmp_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.gz':
            file_path = os.path.join(path, file)
            tmp_list.append(file_path)
    return tmp_list


def dice_3d(mask_path, pred_path, label):
    # print(mask_path)
    mask_sitk_img = sitk.ReadImage(mask_path)
    mask_img_arr = sitk.GetArrayFromImage(mask_sitk_img)
    pred_sitk_img = sitk.ReadImage(pred_path)
    pred_img_arr = sitk.GetArrayFromImage(pred_sitk_img)
    pred_img_arr = pred_img_arr.astype(np.uint16)
    # 求不同的肺叶dice修改此处
    mask_img_arr[mask_img_arr != label] = 0
    mask_img_arr[mask_img_arr == label] = 1
    pred_img_arr[pred_img_arr != label] = 0
    pred_img_arr[pred_img_arr == label] = 1

    denominator = np.sum(mask_img_arr) + np.sum(pred_img_arr)
    numerator = 2 * np.sum(mask_img_arr * pred_img_arr)
    dice = numerator / denominator
    print(dice)
    return dice


def dice_3d_lung(mask_path, pred_path):
    # print(mask_path)
    mask_sitk_img = sitk.ReadImage(mask_path)
    mask_img_arr = sitk.GetArrayFromImage(mask_sitk_img)
    pred_sitk_img = sitk.ReadImage(pred_path)
    pred_img_arr = sitk.GetArrayFromImage(pred_sitk_img)
    pred_img_arr = pred_img_arr.astype(np.uint16)
    mask_img_arr[mask_img_arr != 0] = 1
    pred_img_arr[pred_img_arr != 0] = 1

    denominator = np.sum(mask_img_arr) + np.sum(pred_img_arr)
    numerator = 2 * np.sum(mask_img_arr * pred_img_arr)
    dice = numerator / denominator
    print(dice)
    return dice


if __name__ == '__main__':
    mask_path = r'H:\CT2CECT\segmentation\ISICDM2021\NCCT_mask_lungbox_extractlung'
    pred_path = r'F:\my_code\pix2pix-3d-cect2ncct\2022-06-09-17-22-11\nnunet_test'
    mask = get_listdir(mask_path)
    mask.sort()
    pred = get_listdir(pred_path)
    pred.sort()
    dice = 0
    for i in trange(len(mask)):
        dice += dice_3d(mask[i], pred[i], 1)
        # dice_3d_lung(mask[i], pred[i])
    print(dice / len(mask))

import SimpleITK as sitk
import os
from tqdm import trange


def get_listdir(path):  # 获取目录下所有gz格式文件的地址，返回地址list
    tmp_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.gz':
            file_path = os.path.join(path, file)
            tmp_list.append(file_path)
    return tmp_list


def add_label(img, mask, save_path):
    img_sitk = sitk.ReadImage(img)
    mask_sitk = sitk.ReadImage(mask)
    img_arr = sitk.GetArrayFromImage(img_sitk)
    mask_arr = sitk.GetArrayFromImage(mask_sitk)
    img_arr[mask_arr == 0] = -1000  # TODO: 修改此处
    # img_arr[mask_arr == 0] = 0  # TODO: 修改此处
    new_mask_img = sitk.GetImageFromArray(img_arr)
    new_mask_img.SetDirection(img_sitk.GetDirection())
    new_mask_img.SetOrigin(img_sitk.GetOrigin())
    new_mask_img.SetSpacing(img_sitk.GetSpacing())
    _, fullflname = os.path.split(img)
    sitk.WriteImage(new_mask_img, os.path.join(save_path, fullflname))


if __name__ == '__main__':
    img_path = r'F:\my_code\pix2pix-3d\baseline_dect\2022-06-27-15-51-01\generator_99'
    mask_path = r'F:\my_code\pix2pix-ct2cect\pix2pix\pred\lungmask_lungbox'
    save_path = r'F:\my_code\pix2pix-3d\baseline_dect\2022-06-27-15-51-01\generator_99\pred'
    img_list = get_listdir(img_path)
    mask_list = get_listdir(mask_path)
    img_list.sort()
    mask_list.sort()
    for i in trange(len(img_list)):
        add_label(img_list[i], mask_list[i], save_path)

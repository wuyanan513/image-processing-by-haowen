import SimpleITK as sitk
import os
import numpy as np
import tqdm
import copy


def get_listdir(path):
    tmp_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.gz':
            file_path = os.path.join(path, file)
            tmp_list.append(file_path)
    return tmp_list


def crop(img_path, mask_path, img_save_path, mask_save_path):
    img_sitk = sitk.ReadImage(img_path)
    img_arr = sitk.GetArrayFromImage(img_sitk)
    mask_sitk = sitk.ReadImage(mask_path)
    mask_arr = sitk.GetArrayFromImage(mask_sitk)
    tem_arr = copy.deepcopy(mask_arr)
    print(img_arr.shape, end=" ")
    for axis in [0, 1, 2]:
        sums = np.sum(np.sum(tem_arr, axis=axis), axis=(axis + 1) % 2)

        # Track all =0 layers from front from that axis
        remove_front_index = 0
        while sums[remove_front_index] == 0:
            remove_front_index += 1

        # Track all =0 layers from back from that axis
        remove_back_index = len(sums) - 1
        while sums[remove_back_index] == 0:
            remove_back_index -= 1

        # Remove those layers
        img_arr = np.delete(
            img_arr, list(range(remove_front_index - 1)) + list(range(remove_back_index + 2, len(sums))),
            axis=(axis + 1) % 3
        )

        mask_arr = np.delete(
            mask_arr, list(range(remove_front_index - 1)) + list(range(remove_back_index + 2, len(sums))),
            axis=(axis + 1) % 3
        )
        print(" -> ", img_arr.shape, end=" ")

    _, fullflname = os.path.split(img_path)

    new_img = sitk.GetImageFromArray(img_arr)
    new_img.SetDirection(img_sitk.GetDirection())
    new_img.SetOrigin(img_sitk.GetOrigin())
    new_img.SetSpacing(img_sitk.GetSpacing())
    sitk.WriteImage(new_img, os.path.join(img_save_path, fullflname))

    new_mask = sitk.GetImageFromArray(mask_arr)
    new_mask.SetDirection(img_sitk.GetDirection())
    new_mask.SetOrigin(img_sitk.GetOrigin())
    new_mask.SetSpacing(img_sitk.GetSpacing())
    sitk.WriteImage(new_mask, os.path.join(mask_save_path, fullflname))


if __name__ == '__main__':
    img_path = r'F:\my_code\pix2pix-ct2cect\pix2pix_cect2ncct\pred\SNCCT'
    mask_path = r'F:\my_code\pix2pix-ct2cect\pix2pix_cect2ncct\pred\lungmask'
    img_save_path = r'F:\my_code\pix2pix-ct2cect\pix2pix_cect2ncct\pred\SNCCT_lungbox'
    mask_save_path = r'F:\my_code\pix2pix-ct2cect\pix2pix_cect2ncct\pred\lungmask_lungbox'

    l_img = get_listdir(img_path)
    l_img.sort()
    l_mask = get_listdir(mask_path)
    l_mask.sort()
    for i in tqdm.trange(len(l_img)):
        crop(l_img[i], l_mask[i], img_save_path, mask_save_path)

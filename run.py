from utils.class_util import process_circles
from utils.general_utils import *
import glob
import pandas as pd
import yaml
from pathlib import Path

with open("./configs/config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)
if config["test_image_path"][-1] == "/":
    config["test_image_path"] = config["test_image_path"][:-1]
if config["image_save_path"][-1] == "/":
    config["image_save_path"] = config["image_save_path"][:-1]
Path(config["image_save_path"]).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    file_paths = glob.glob(f"{config["test_image_path"]}/*/*.jpg") + glob.glob(f"{config["test_image_path"]}/*.jpg")
    circles_data_df = annotate_images(file_paths,config["image_save_path"])



    # image_paths = []
    # files = []
    # fits = []
    # image_paths = glob.glob(f"{config["test_image_path"]}/*/*.jpg") + glob.glob(f"{config["test_image_path"]}/*.jpg")
    # fit_dictionary = {}
    # for image_path in image_paths:
    #     process_obj = process_circles(image_path)

    #     process_obj.plot_circles(plot=False)
    #     identifications_filled = process_obj.plot_circles(
    #         plot=False,
    #         fill=True,
    #         radius_overlay=False,
    #         out_dir="gray_coloured"
    #     )
    #     identified_pixel_count = process_obj.count_colour_pixels(identifications_filled)

    #     dark_pixels_coloured = process_obj.colour_dark_by_threshhold()
    #     dark_pixel_count = process_obj.count_colour_pixels(dark_pixels_coloured)
    #     path_parts = image_path.split("\\")
    #     path_parts[0] = "gray_coloured"
    #     out_path = "\\".join(path_parts)
    #     process_obj.save_image(out_path,dark_pixels_coloured)

    #     files.append("\\".join(image_path.split("\\")[-2:]))
    #     fits.append(identified_pixel_count/dark_pixel_count)

    # fit_df = pd.DataFrame({"files":files,"fit":fits})
    # print(fit_df.query("fit < 0.9"))
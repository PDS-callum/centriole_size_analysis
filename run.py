from utils.class_util import process_circles
import glob
import pandas as pd

image_path = "test_data/20240503_Spheroid (StemFlex and StemScale) of iPSC maintain in diff media/mTeSR plus Stemflex D2-1.jpg"

if __name__ == "__main__":
    image_paths = []
    files = []
    fits = []
    image_paths = glob.glob("./test_data/*/*.jpg")
    # image_paths = ["test_data\\20240503_Spheroid (StemFlex and StemScale) of iPSC maintain in diff media\\mTeSR plus Stemflex D2-1.jpg"]
    fit_dictionary = {}
    for image_path in image_paths:
        process_obj = process_circles(image_path)

        process_obj.plot_circles(plot=False)
        identifications_filled = process_obj.plot_circles(
            plot=False,
            fill=True,
            radius_overlay=False,
            out_dir="gray_coloured"
        )
        identified_pixel_count = process_obj.count_colour_pixels(identifications_filled)

        dark_pixels_coloured = process_obj.colour_dark_by_threshhold()
        dark_pixel_count = process_obj.count_colour_pixels(dark_pixels_coloured)
        path_parts = image_path.split("\\")
        path_parts[0] = "gray_coloured"
        out_path = "\\".join(path_parts)
        process_obj.save_image(out_path,dark_pixels_coloured)

        files.append("\\".join(image_path.split("\\")[-2:]))
        fits.append(identified_pixel_count/dark_pixel_count)

    fit_df = pd.DataFrame({"files":files,"fit":fits})
    print(fit_df.query("fit < 0.9"))
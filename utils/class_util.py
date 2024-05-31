import cv2
import numpy as np
import pandas as pd
from sklearn.metrics import jaccard_score

class process_circles:
    def __init__(self,image_path:str):
        '''
        PARAMETERS
        path (str): The string path to the image file.
        '''
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)
        self.image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def find_circles(
            self,
            image,
            method=cv2.HOUGH_GRADIENT, 
            dp=1.3, 
            minDist=50,
            param1=70, 
            param2=40, 
            minRadius=10, 
            maxRadius=100,
            blur_type:str="standard",
            blur=(9,9)
    ):
        '''
        This function takes in an image by the file path, reads it into an object and then returns those circles.
        PARAMETERS
        path (str): The string path to the image file.
        '''
        if blur_type == "standard":
            self.image_gray_blur = cv2.blur(image,blur, 0)
        elif blur_type == "gaussian":
            self.image_gray_blur = cv2.GaussianBlur(image,blur, 0)
        circles = cv2.HoughCircles(
            image=image, 
            method=method, 
            dp=dp, 
            minDist=minDist,
            param1=param1, 
            param2=param2, 
            minRadius=minRadius, 
            maxRadius=maxRadius
        )
        coordinates = [(x[0],x[1]) for x in np.uint16(np.around(circles))[0, :]]
        radii = [x[2] for x in np.uint16(np.around(circles))[0, :]]
        self.circles_df = pd.DataFrame({"coordinate":coordinates,"radius":radii})
        return self.circles_df
    
    def plot_circles(
            self,
            plot:bool=False,
            fill:bool=False,
            out_dir:str="out_images",
            save:bool=True,
            radius_overlay:bool=True,
            thickness:int=2,
            font_size=0.5
    ):
        annotated_image = self.image.copy()
        if fill:
            thickness = -1
        for i, row in self.circles_df.iterrows():
            cv2.circle(annotated_image, row.coordinate, row.radius, (255, 0, 0), thickness)
            font = cv2.FONT_HERSHEY_SIMPLEX
            if radius_overlay:
                label = f"{int(row.radius)}"
                cv2.putText(annotated_image, label, (row.coordinate[0] - int(row.radius/2), row.coordinate[1] + int(row.radius/2)), font, font_size, (0,0,255), 2)
        if plot:
            cv2.imshow("Circles with Labels", annotated_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        if save:
            path_parts = self.image_path.split("\\")
            path_parts[0] = out_dir
            out_path = "\\".join(path_parts)
            cv2.imwrite(out_path, annotated_image)
        return annotated_image
    
    def count_colour_pixels(
            self,
            annotated_image,
            colour_lower_bound:np.array=np.array([255, 0, 0]),
            colour_upper_bound:np.array=np.array([255, 0, 0])
    ):
        hsv_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, colour_lower_bound, colour_upper_bound)
        pixel_count = cv2.countNonZero(mask)
        return pixel_count

    def colour_dark_by_threshhold(self,threshold:int=120):
        # Create mask for black and gray pixels
        mask = cv2.threshold(self.image_gray, threshold, 255, cv2.THRESH_BINARY)[1]

        # Invert the mask for easier manipulation (black becomes white, white becomes black)
        mask = 255 - mask

        # Convert image to BGR format for color manipulation (might be redundant if loaded as BGR already)
        bgr_image = cv2.cvtColor(self.image_gray, cv2.COLOR_GRAY2BGR)

        # Set blue color
        color = (255, 0, 0)

        # Apply color based on mask
        bgr_image[mask == 255] = color  # Replace black/gray pixels with blue where mask is white (inverted)
        return bgr_image
    
    def show_image(self,image,label:str="image label"):
        cv2.imshow(label,image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_image(self,out_path,image):
        cv2.imwrite(out_path, image)

    def tune_circle_search(
            self,
            opts,
            minRadius, 
            maxRadius, 
            minDist,
            average,
            test=False
    ):
        dp, param1, param2, blur = opts
        param1 = int(param1)
        param2 = int(param2)
        blur = int(blur)
        blur = (blur,blur)

        minRadius = int(minRadius)
        maxRadius = int(maxRadius)
        minDist = int(minDist)
        
        # lab= cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        # edges = cv2.Canny(lab, 100, 200)
        # kernel = np.ones((9, 9), np.uint8)
        # closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)  # Close small holes in edges
        closed_edged = self.image_gray.copy()

        # try:
        #     print("a")
        self.find_circles(
            image=closed_edged,
            method=cv2.HOUGH_GRADIENT, 
            dp=dp, 
            minDist=minDist,
            param1=param1, 
            param2=param2, 
            minRadius=minRadius, 
            maxRadius=maxRadius,
            blur=blur
        )
        #     print("a")
        # except:
        #     return 1000
        identifications_filled = self.plot_circles(
            plot=False,
            fill=True,
            radius_overlay=False,
            save=False
        )
        dark_pixels_coloured = self.colour_dark_by_threshhold()
        identifications_filled_mask = cv2.inRange(identifications_filled, np.array([255, 0, 0]), np.array([255, 0, 0]))
        dark_pixels_coloured_mask = cv2.inRange(dark_pixels_coloured, np.array([255, 0, 0]), np.array([255, 0, 0]))
        
        # Calculate the intersection of the masks using bitwise AND operation
        intersection = cv2.bitwise_and(identifications_filled_mask, dark_pixels_coloured_mask)

        # Calculate the union of the masks using bitwise OR operation
        union = cv2.bitwise_or(identifications_filled_mask, dark_pixels_coloured_mask)

        # Calculate the Jaccard Similarity Coefficient
        js = jaccard_score(intersection, union, average=average)
        if test:
            return identifications_filled, dark_pixels_coloured, identifications_filled_mask, dark_pixels_coloured_mask
        else:
            return abs(js-1)


        identified_pixel_count = np.count_nonzero(np.all(identifications_filled == (255, 0, 0), axis=2))
        intersection = np.bitwise_and(dark_pixels_coloured, identifications_filled)
        print(intersection)
        dark_pixel_count = np.count_nonzero(np.all(dark_pixels_coloured == (255, 0, 0), axis=2))
        return abs((identified_pixel_count/dark_pixel_count)-1)
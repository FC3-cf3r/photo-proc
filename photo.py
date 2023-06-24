import cv2
import rembg
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np

pwd = "/home/cfisher/Documents/git/photo-proc"
out_dir = Path(f"{pwd}""/output")
in_dir = Path(f"{pwd}""/input")

# define the alpha and beta (pre)
alpha = 1 # Contrast control
beta = 0 # Brightness control
# define the contrast and brightness value (post)
contrast = 1. # Contrast control ( 0 to 127)
brightness = 4. # Brightness control (0-100)


def is_image(absolute_path: Path):
    return absolute_path.is_file and str(absolute_path).endswith('.JPG')


input_filenames = [p for p in filter(is_image, Path(in_dir).iterdir())]


def process_image(in_dir):
    try:
        image_pre = cv2.imread(str(in_dir))
        image = cv2.convertScaleAbs(image_pre, alpha=alpha, beta=beta)
        if image is None or not image.data:
            raise cv2.error("read failed")
        output1 = rembg.remove(
                            image,
                            # alpha_matting=True,
                            # alpha_matting_foreground_threshold=240,
                            # alpha_matting_background_threshold=10,
                            # alpha_matting_erode_structure_size=10,
                            # alpha_matting_base_size=1000,
                            )

                            
        #output2 = rembg.remove(
        #                    output1,
        #                    # alpha_matting=True,
        #                    # alpha_matting_foreground_threshold=240,
        #                    # alpha_matting_background_threshold=10,
        #                    # alpha_matting_erode_structure_size=10,
        #                    # alpha_matting_base_size=1000,
        #                    )
        in_dir = out_dir / in_dir.with_suffix(".JPG").name
        adjusted = cv2.addWeighted( output2, contrast, output2, 0, brightness)
        array = np.full((500, 500, 3), 255, dtype = np.uint8)
        adjusted_bg= cv2.imshow(adjusted, array)
        cv2.imwrite(str(in_dir), adjusted_bg)
        
    except Exception as e:
        print(f"{in_dir}: {e}", file=sys.stderr)


executor = ThreadPoolExecutor(max_workers=4)


for result in executor.map(process_image, input_filenames):
    print(f"Processing image: {result}")
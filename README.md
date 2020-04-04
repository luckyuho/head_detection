# Head_Detection

This is used for fun to change head roughly by head detection.

The main funciton cmoes from https://github.com/pranoyr/head-detection-using-yolo

In this project, only replacing the retangle detecting to head picture

Beside, make sure it can work even if there is no deteciton


# If you want to change your own data, you can go modify the following code

 - predict.py: file_text(input_image_path), save_text(output_image_path), for range(number_of_photo)
 - utils.py: head_photo(your_friend's_head_photo_path)

# Result

Before:

![](test_movie.gif)

After:

![](output_movie.gif)

# Image Resizer

## Description
The script allows you to resize and scale images. It is possible to provide height and width or only one of them or scale of wished size – the script will generate new image saving the sides ratio. The fully supported image formats:
* JPG
* PNG
* BMP
* TIFF

**IMPORTANT:** This scpirt works only with Python3.5 or higher!


## How to use
Run the script with specific path to the original image and necessary resize options (you can't specify scale and width or height together). If you want to save new resize image in the current directory just omit optinon ```-destination```. 

New image name will save with original name plus add new size. For instance: ```pic.jpg >>> pic_200x200.jpg``` 

**Options:**

Name | Type | Key | Desription
--- | --- | --- | ---|
**Scale** | float | `-scale`| Scale of resizing (can be < 1)
**Width** | int | `-width`| Width of new image
**Height** | int | `-height`| Height of new image
**Destination** | string | `-destination`| Output path 


### Example
```python3 image_resize.py ~/pic.jpg -scale 1.5 -destination /some/path``` 


### Requirements
Install the packages from requirements.txt using pip:

```pip install -r requirements.txt```



# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

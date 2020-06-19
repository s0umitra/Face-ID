# **Face-ID**

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

A <strong>'python-based'</strong> Face Detector and Recognizer that
works on images, videos and live stream too!

For user convenience, working is distributed over individual programs.
                                            
- ***encoder.py*** encodes the face details extracted from provided images

- Individual Recognizing programs to use as per the requirement;

	- ***rec_img.py*** recognizes the Faces in Images
	
	- ***rec_vid.py*** recognizes the Faces in Videos
	
	- ***rec_live.py*** recognizes the Faces in Live WebCam Feed
	
- ***set_builder.py*** crops the faces from provided images and sort them wrt database

- ***config.cfg*** provides easy to change parameters

### New Features!

  - Now supports Videos and Live Streams
  - Config file is updated to match the usage requirements

### Sample Usage:

***rec_img.py*** <br>

![](https://github.com/s0umitra/Face-ID/blob/master/.readme/rec_img1.jpg)

![](https://github.com/s0umitra/Face-ID/blob/master/.readme/rec_img2.jpg)



### Package Dependencies

* face_recognition
* pickle
* os
* cv2
* random

### Notes

* Based on [face-recognition](https://github.com/ageitgey/face_recognition) api maintained by **Adam Geitgey**

### License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://github.com/s0umitra/Face-ID/blob/master/LICENSE.md)

This software is licenced under [MIT](https://github.com/s0umitra/Face-ID/blob/master/LICENSE.md)

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

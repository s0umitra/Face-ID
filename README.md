<h1>Face-ID</h1>
<h3>This is a <b>'in-progress'</b> Face Detector and Recognizer built in Python.</h3>
<br>

(Based on face-recognition api maintained by <b>Adam Geitgey</b>)<br><br><br>


Files:-<br><br>

1) <b>detector.py</b> :-<br>
 <ul>
  <li>Detects and encodes the faces.<br></li>
  <li>Images are read from database folder.</li>
  <li>Outputs a file named 'data.sys' which contains encodings.</li>
</ul> <br>

2) <b>recognizer.py</b> :-<br>
 <ul>
  <li>Takes image or images as an input.<br></li>
  <li>Reads encodings from 'data.sys'.<br></li>
  <li>Images are read from input folder.</li>
  <li>Generates a image with recognized labels.</li>
  <li>Image is saved to output folder.</li>
</ul> <br>

3) <b>setbuilder.py</b> :-<br>
 <ul>
  <li>Takes image or images as an input.<br></li>
  <li>Generates cropped face images and places them in separated folders.</li>
  <li>Input images are to be places in /data-buider/src folder.</li>
  <li>Output is saved to /data-buider/output folder.</li>
  <li>This can be used to create required database quickly.</li>
</ul> <br>

4) <b>resizer.py</b> :-<br>
 <ul>
  <li>Contains fuctions to resize the images.<br></li>
  <li>Used by other processes.</li>
</ul> <br>

5) <b>arguments.py</b> :-<br>
 <ul>
  <li>Loads the configuration for 'congif.cfg' file.<br></li>
  <li>Sets the new configuration if possible or else pass default values.</li>
</ul> <br>

6) <b>config.cfg</b> :-<br>
 <ul>
  <li>Contains values to be set for Detection and Recognition Process.<br></li>
</ul> <br>


Required libraries:-
<ul>
  <li>face_recognition</li>
  <li>pickle</li>
  <li>os</li>
  <li>cv2</li>
  <li>random</li>
</ul>



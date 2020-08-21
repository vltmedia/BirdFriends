## Desecription
This app currently takes multiple pictures with ESP32-S Cameras, that are then fed to a web server and uploaded. On the webserver, the files are then organized into dated and alphabet based folders. The files can then be transcoded into .mp4 movie files for viewing and editing.


## Quickstart
### Cleanup Folders and Transcode Today
- Run ```\Backend\FileHandling\python\CleanupFolers.py```
- This takes all the images taken that haven't been placed into folders and transcoded from ```birdphotos/camera```.
- This splits them up between
  - Date  
  - Camera Letter
- This Transcodes the date folders being copied to into .mp4 video files.

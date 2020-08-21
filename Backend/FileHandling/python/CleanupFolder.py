import pathlib
import json
import os
import shutil
import subprocess as sp
import ffmpeg


countt = 0

def MoveFile (fileToMove, datename):
    global countt
    filenamee = str(fileToMove.stem)
    transcodedpath = "/var/www/html/birdphotos/transcoded"
    cameraSplit = filenamee.split("-")[4]
    
    newpath = transcodedpath + "/"+ datename + "/"+cameraSplit +"/"+ str(fileToMove.name).replace(":","")
    datepath =  transcodedpath + "/"+ datename + "/"+cameraSplit
    datetemppath =  datepath +"/temp"
    newtemppath = os.path.join(datetemppath, "image_"+str(countt).zfill(4) + ".jpg")
    
    print(datepath)
    print(newpath)
    
    if(os.path.isdir(datepath)):
        print(datepath +"  ||  EXISTS ")
    else:
        print(datepath +"  ||  DOESN NOT EXISTS ")
        gallerypath = "/var/www/html/birdphotos/transcoded/gallery.php"
        gallerynewpath = os.path.join(datepath, "gallery.php")
        os.makedirs(datepath)
        os.makedirs(datetemppath)
        shutil.copyfile(gallerypath, gallerynewpath)
    
    shutil.copyfile(str(fileToMove), newpath)
    shutil.copyfile(str(fileToMove), newtemppath)
    os.remove(str(fileToMove))
    countt += 1
    return [newpath,newtemppath]


def TranscodeToVideo(arrayToTranscode):
    countt = 0
    print(arrayToTranscode)
    DateTodayy = str(pathlib.Path(arrayToTranscode[1][0]).stem).split("_")[0]
    print(str(pathlib.Path(arrayToTranscode[1][0]).stem).split("_")[0])
    filenamee = str(pathlib.Path(arrayToTranscode[1][0]).stem)
    
    dirpath = str(pathlib.Path(arrayToTranscode[1][0]).parent)
    cameraSplit = filenamee.split("-")[4]
    moviepath = str(pathlib.Path(arrayToTranscode[1][0]).parent) + "/"+DateTodayy+"_"+cameraSplit+"_birdfriends_seq.mp4"
    print(dirpath)
    output_options = {
    'crf': 2,
    'preset': 'slower',
    'movflags': 'faststart',
    'pix_fmt': 'yuv420p',
    'vcodec' :'libx264'
}
    if os.path.exists(moviepath):
        os.remove(moviepath)
    (
    ffmpeg
    .input(dirpath+"/*.jpg", pattern_type='glob', framerate=12)
    .output(moviepath, 
        **output_options)
    .run()
    )
    # cmd='ffmpeg -i inputVideo outputFrames_%04d.sgi'
    # sp.call(cmd,shell=True)

def ProcessPhotos():
    
    imagespath = "/var/www/html/birdphotos/cameras"
    jsonn = {}
    flist = []
    camA = []
    camB = []
    for p in pathlib.Path(imagespath).iterdir():
        if p.is_file():
            filenamee = str(p.stem)
            undersplit = filenamee.split("_")
            cameraSplit = filenamee.split("-")[4]
            datee = undersplit[0] + " " +  undersplit[1]
            dateen = undersplit[0].replace("-","")
            # print(p.stem)
            # print(datee)
            if(cameraSplit == "A"):
                camA.append(MoveFile(p, dateen))
                
                
            if(cameraSplit == "B"):
                camB.append(MoveFile(p, dateen))
                
                
            # print(cameraSplit)
            
    jsonn["CameraA"] = camA 
    jsonn["CameraB"] = camB 
    TranscodeToVideo(camA)
    print(json.dumps(jsonn))
    
    
if __name__ == "__main__":
    ProcessPhotos()

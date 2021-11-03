import inspect
import os
import shutil
import json
from typing import Dict, Any
from datetime import datetime

from PIL import ExifTags, Image
from pathlib import Path
from os.path import join

folderdatalake = os.path.dirname(os.path.abspath(__file__)) + "\\datalake"
folderpicture = os.path.dirname(os.path.abspath(__file__)) + "\\picture"

def imageanalyzer():
    listimages = listfilesdirectory()

    try:
        for img in listimages:
            print(img)
            tags = print_tag_image(img)
            data = "{namepicture: %s, pathpicture: %s,'tags': %s}" % (os.path.basename(img), img, tags)

            json_object = json.dumps(data)

            with open(folderdatalake + "\\tags.json", "a") as outfile:
                outfile.write(json_object + ",\n")

    except ValueError:
        print('error')


def print_tag_image(pathimagem):
    # img = '\\Picture\\20191122_132318.jpg'
    img = pathimagem
    exifdata: dict[str | Any, Any] = {}
    img = Image.open(img)

    exifdataraw = img._getexif()

    if exifdataraw is None:
        img.close()
        movefile(pathimagem)
        print("Não existe tags.")
    else:
        for tag, value in exifdataraw.items():
            img_exif_dict = dict(exifdataraw)
            decodedtag = ExifTags.TAGS.get(tag, tag)
            exifdata[decodedtag] = value

    return exifdata


def listfilesdirectory():
    folder = folderpicture
    exclude_directories = set(['temp'])
    listfiles = []
    for directory, subfolder, files in os.walk(folder):
        subfolder[:] = [d for d in subfolder if d not in exclude_directories]
        for file in files:
            pathfile = os.path.join(os.path.realpath(directory), file)
            listfiles.append(pathfile)
    return listfiles


def movefile(pathimagem):
    pathdestiny = os.path.dirname(os.path.abspath(pathimagem)) + "\\temp\\" + os.path.basename(pathimagem)
    shutil.move(pathimagem, pathdestiny)


def existdataraw(data, key):
    if key in data:
        return data[key]
    return None


def testconverterro():
    valor = {'ImageWidth': 4608, 'ImageLength': 3456, 'GPSInfo': {1: 'S', 2: (2.0, 54.0, 26.719199), 3: 'W', 4: (40.0, 51.0, 21.22164)}, 'ResolutionUnit': 2, 'ExifOffset': 238, 'Make': 'samsung', 'Model': 'SM-N975F', 'Software': 'N975FXXU1ASJ2', 'Orientation': 1, 'DateTime': '2019:11:22 13:23:17', 'YCbCrPositioning': 1, 'XResolution': 72.0, 'YResolution': 72.0, 'ExifVersion': b'0220', 'ShutterSpeedValue': 0.0007739938080495357, 'ApertureValue': 2.27, 'DateTimeOriginal': '2019:11:22 13:23:17', 'DateTimeDigitized': '2019:11:22 13:23:17', 'BrightnessValue': 23.55, 'ExposureBiasValue': 0.0, 'MaxApertureValue': 2.52, 'MeteringMode': 2, 'Flash': 0, 'FocalLength': 1.8, 'ColorSpace': 1, 'ExifImageWidth': 4608, 'DigitalZoomRatio': 1.0, 'FocalLengthIn35mmFilm': 13, 'SceneCaptureType': 0, 'ExifImageHeight': 3456, 'ExposureTime': 0.0007739938080495357, 'FNumber': 2.2, 'ImageUniqueID': 'O16XLMA00SM', 'ExposureProgram': 2, 'ISOSpeedRatings': 50, 'ExposureMode': 0, 'WhiteBalance': 0}
    converter = json.dumps(valor)
    return converter


if __name__ == '__main__':
    print('Inicio do processo: %s' % (datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')))
    imageanalyzer()
    print('Fim do processo: %s' % (datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')))

    # print_tag_image()
    #retorno = testconverterro()
    #print(retorno)

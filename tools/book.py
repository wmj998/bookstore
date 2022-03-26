import os
import time

from PIL import Image


class UploadImage:
    ALLOWED_EXTENSIONS = ['tif', 'pjp', 'xbm', 'jxl', 'svgz', 'jpg', 'jpeg', 'ico', 'tiff', 'gif', 'svg', 'jfif', 'webp', 'png', 'bmp', 'pjpeg', 'avif']

    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in cls.ALLOWED_EXTENSIONS

    @staticmethod
    def re_filename(uid):
        return time.strftime('%Y%m%d%H%M%S') + str(uid) + '.png'

    @staticmethod
    def transfer(infile, outfile, width=540, height=831):
        in_image = Image.open(infile)
        out_image = in_image.resize(size=(width, height))
        out_image.save(outfile)

    @classmethod
    def main(cls, image, uid):
        if cls.allowed_file(filename=image.filename):
            filename = cls.re_filename(uid=uid)
            image_path = os.path.join(os.getcwd(), 'static/images/book/') + filename
            cls.transfer(infile=image, outfile=image_path)
            return os.path.join('images/book', filename)

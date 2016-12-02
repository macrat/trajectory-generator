import itertools
import glob

import cv2
import numpy


def make_bg(fname):
    vid = cv2.VideoCapture(fname)

    bg = vid.read()[1].astype(numpy.uint64)
    count = 1

    while True:
        ok, img = vid.read()
        if not ok:
            break

        bg += img
        count += 1

    vid.release()

    return (bg.astype(numpy.float64) / count).astype(numpy.uint8)


def make_image(fname, bg, video_name, step=10):
    vid = cv2.VideoCapture(fname)

    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'X264'), 60.0, (1280, 720))

    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(bg, cv2.COLOR_GRAY2BGR).astype(numpy.float32)

    for i in itertools.count():
        print('\r{}'.format(i), end='')

        ok, frame = vid.read()
        if not ok:
            break

        diff = cv2.absdiff(bg, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        mask = numpy.array([(diff > numpy.average(diff) * 4) * (1.0 if ((i + 1) % step == 0) else 0.1)] * 3).transpose((1, 2, 0))

        img = img * (1.0 - mask) + frame * mask

        cv2.imshow('progress', img.astype(numpy.uint8))
        out.write(img.astype(numpy.uint8))
        cv2.waitKey(1)

    vid.release()
    out.release()

    print()

    return img.astype(numpy.uint8)


if __name__ == '__main__':
    ls = glob.glob('original/*.mp4')
    for i, fname in enumerate(ls):
        print('{0: 3}/{1: 3} [{2:6.1%}] {3}'.format(i + 1, len(ls), i / len(ls), fname))

        id_ = int(fname[len('original/'):-len('.mp4')])
        bg = make_bg(fname)
        img = make_image(fname, bg, 'tmp/{0:04}.mp4'.format(id_))
        cv2.imwrite('image/{0:04}.jpg'.format(id_), img)

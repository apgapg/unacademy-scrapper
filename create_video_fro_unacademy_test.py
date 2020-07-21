import ffmpeg

import json

with open('video_test/events.json') as f:
    data = json.load(f)
rawImgSeq = list(filter(lambda x: ('a' in x) and (x.get('a') == (
    'start') or x.get('a') == ('move') or x.get('a') == ('end')), data))

PAD = {
    'width': '768',
    'height': '600',
    'x': '(ow-iw)/2',
    'y': '(oh-ih)/2',
    'color': 'black'
}

stream = ffmpeg.concat(
    ffmpeg.input('video_test/2.jpeg', loop=1, t=4)
    .filter('scale', size='768:600', force_original_aspect_ratio='decrease')
    .filter_("pad", **PAD),
    ffmpeg.input('video_test/3.jpeg', loop=1, t=4)
    .filter('scale', size='768:600', force_original_aspect_ratio='decrease')
    .filter_("pad", **PAD),
    ffmpeg.input('video_test/4.jpeg', loop=1, t=6)
    .filter('scale', size='768:600', force_original_aspect_ratio='decrease')
    .filter_("pad", **PAD),
)

time = 0
for e in rawImgSeq[0:1]:
    if e.get('a') == 'start':
        time = float(e.get('t'))
    stream = ffmpeg.drawbox(stream, (e.get('p')['x'])*768, (e.get('p')['y'])*600, 40, 40,
                            color='red@0.2', thickness=40, enable=f'between(t,{time},{time+1})')


# .filter('scale', "'min(600,iw)':min'(600,ih)':force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2")
stream = ffmpeg.output(stream, 'video_test/out.mp4')
stream = ffmpeg.overwrite_output(stream)
ffmpeg.run(stream)

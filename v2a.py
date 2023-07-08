import moviepy.editor as mp
import glob, os, sys, tqdm

videoFilePath = 'workVideo'
targetAudioFilePath = 'propAudio'
videoFiles = os.listdir(videoFilePath)

needConvert = len(videoFiles)
if needConvert > 0:
    print(f'=== There are {needConvert} video files ===')
    for videoFile in videoFiles:    
        print('\t',videoFile)
    print('=============================')
else:
    print('=== There are no video files ===')
    sys.exit()

for i, v in tqdm.tqdm(enumerate(videoFiles), total=len(videoFiles)):
    videoFile = os.path.join(videoFilePath, v)
    # Define the Video Clip
    clip = mp.VideoFileClip(videoFile)

    # Extracting the Audio from the Video
    audioFileName = v.split('.')[0] + '.mp3'
    clip.audio.write_audiofile(os.path.join(targetAudioFilePath, audioFileName))
    print(f'=== {v} is done ===')

import moviepy.editor as mp
import glob, os, sys, tqdm, time

try:
    videoFilePath = sys.argv[1]
except:
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

start_time = time.time()

for i, v in tqdm.tqdm(enumerate(videoFiles), total=len(videoFiles)):
    videoFile = os.path.join(videoFilePath, v)
    # Define the Video Clip
    clip = mp.VideoFileClip(videoFile)

    # Extracting the Audio from the Video
    audioFileName = v.split('.')[0] + '.mp3'
    clip.audio.write_audiofile(os.path.join(targetAudioFilePath, audioFileName))
    print(f'=== {v} is done ===')

# End time measurement
end_time = time.time()
execution_time = end_time - start_time

print(f"Program executed in: {execution_time} seconds.")

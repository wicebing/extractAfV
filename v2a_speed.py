import moviepy.editor as mp
import os, sys, tqdm, time
import concurrent.futures

def convert_to_audio(videoFile, targetAudioFilePath):
    # Define the Video Clip
    clip = mp.VideoFileClip(videoFile)

    # Extracting the Audio from the Video
    audioFileName = os.path.split(videoFile)[1].split('.')[0] + '.mp3'  # Extract only filename from the path
    clip.audio.write_audiofile(os.path.join(targetAudioFilePath, audioFileName))
    # Close the video file clip
    clip.close()
    print(f'=== {videoFile} is done ===')

try:
    videoFilePath = sys.argv[2]
except:
    videoFilePath = 'workVideo'

try:
    max_workers = sys.argv[1]
    max_workers = min(os.cpu_count(), int(max_workers))
except:
    max_workers = 1 # Adjust this to your preference

targetAudioFilePath = 'propAudio'
videoFiles = [os.path.join(videoFilePath, v) for v in os.listdir(videoFilePath)]

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
# Set max workers to number of CPU cores you want to use
print(f'=== Using {max_workers} workers ===')
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    for _ in tqdm.tqdm(executor.map(convert_to_audio, videoFiles, [targetAudioFilePath]*len(videoFiles)), total=len(videoFiles)):
        pass

# End time measurement
end_time = time.time()
execution_time = end_time - start_time

print(f"Program executed in: {execution_time} seconds.")
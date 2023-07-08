import moviepy.editor as mp
import os
import sys
import time
import concurrent.futures
import tqdm

def get_video_files(video_folder_path):
    video_files = [os.path.join(video_folder_path, v) for v in os.listdir(video_folder_path)]
    return video_files

def convert_to_audio(video_file, target_audio_folder_path):
    audio_file_name = os.path.splitext(os.path.basename(video_file))[0] + '.mp3'
    audio_file_path = os.path.join(target_audio_folder_path, audio_file_name)

    with mp.VideoFileClip(video_file) as clip:
        clip.audio.write_audiofile(audio_file_path)

    print(f'=== {video_file} is done ===')

def main(video_folder_path, max_workers):
    video_files = get_video_files(video_folder_path)

    need_convert = len(video_files)

    if need_convert > 0:
        print(f'=== There are {need_convert} video files ===')
        for video_file in video_files:
            print('\t', video_file)
        print('=============================')
    else:
        print('=== There are no video files ===')
        sys.exit()

    target_audio_folder_path = 'propAudio'
    os.makedirs(target_audio_folder_path, exist_ok=True)

    start_time = time.time()

    print(f'=== Using {max_workers} workers ===')
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in tqdm.tqdm(executor.map(convert_to_audio, video_files, [target_audio_folder_path]*len(video_files)), total=len(video_files)):
            pass

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Program executed in: {execution_time} seconds.")

if __name__ == "__main__":
    try:
        video_folder_path = sys.argv[1]
    except IndexError:
        print('No video folder path provided. Using default "workVideo" folder.')
        video_folder_path = 'workVideo'

    try:
        max_workers = int(sys.argv[2])
        max_workers = min(os.cpu_count(), max_workers)
    except (IndexError, ValueError):
        print('Invalid or no value for maximum workers provided. Using default value 1.')
        max_workers = 1

    main(video_folder_path, max_workers)

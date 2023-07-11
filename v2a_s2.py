import moviepy.editor as mp
import os
import sys
import time
import concurrent.futures
import tqdm
import logging
import csv

def setup_logging():
    log_dir = 'log'
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(filename=os.path.join(log_dir, 'log.txt'), level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def get_video_files(video_folder_path):
    video_files = [os.path.join(video_folder_path, v) for v in os.listdir(video_folder_path)]
    return video_files

def convert_to_audio(video_file, target_audio_folder_path):
    audio_file_name = os.path.splitext(os.path.basename(video_file))[0] + '.mp3'
    audio_file_path = os.path.join(target_audio_folder_path, audio_file_name)
    try:
        with mp.VideoFileClip(video_file) as clip:
            clip.audio.write_audiofile(audio_file_path)
        print(f'=== {video_file} is done ===')
    except Exception as e:
        logging.error(f'Failed to convert {os.path.basename(video_file)} due to {e}')
        return os.path.basename(video_file)

def main(video_folder_path, max_workers):
    setup_logging()
    video_files = get_video_files(video_folder_path)

    need_convert = len(video_files)

    if need_convert > 0:
        print(f'=== There are {need_convert} video files ===')
        # for video_file in video_files:
        #     print('\t', video_file)
        print('=============================')
    else:
        print('=== There are no video files ===')
        sys.exit()

    target_audio_folder_path = 'propAudio'
    os.makedirs(target_audio_folder_path, exist_ok=True)

    start_time = time.time()
    failed_files = []

    print(f'=== Using {max_workers} workers ===')
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(tqdm.tqdm(executor.map(convert_to_audio, video_files, [target_audio_folder_path]*len(video_files)), total=len(video_files)))
        failed_files = [r for r in results if r is not None]

    with open('failed_files.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for file in failed_files:
            writer.writerow([file])

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Program executed in: {execution_time} seconds.")

if __name__ == "__main__":
    try:
        video_folder_path = sys.argv[2]
    except IndexError:
        print('No video folder path provided. Using default "workVideo" folder.')
        video_folder_path = 'workVideo'

    try:
        max_workers = int(sys.argv[1])
        max_workers = min(os.cpu_count(), max_workers)
    except (IndexError, ValueError):
        print('Invalid or no value for maximum workers provided. Using default value 1.')
        max_workers = 1

    main(video_folder_path, max_workers)

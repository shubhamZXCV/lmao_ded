from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from PIL import Image
import os
import tempfile
import shutil
from transitions import crossfadein, crossfadeout, slide_in, slide_out
import imageio

HEIGHT = 900
WIDTH = 1600

def images_to_video(images_path, video_path, durations, transition_array, music_path, fps=1):
    temp_folder = tempfile.mkdtemp()  # Create a temporary folder for resized images
    
    # Resize and convert images to JPEG format and save them in the temp folder

    images = []

    for img_path in images_path:
        img = Image.open(img_path)
        # Convert RGBA images to RGB
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        resized_img = img.resize((WIDTH, HEIGHT))
        # Convert image to JPEG format
        img_base_name = os.path.splitext(os.path.split(img_path)[1])[0]
        images.append(os.path.split(img_path)[1])
        jpeg_path = os.path.join(temp_folder, img_base_name + ".jpeg")
        print(jpeg_path)
        resized_img.save(jpeg_path, "JPEG")

    print(images)

    # Create ImageSequenceClip from the extended list of images
    
    totalTime = 0
    # for img, duration in zip(images, durations):
    #     img_base_name = os.path.splitext(img)[0]
    #     totalTime += duration
        # for _ in range(int(duration * fps)):
        #     extended_images.append(os.path.join(temp_folder, img_base_name + ".jpeg")) 

    print(images)

    clips = []
    for img, duration in zip(images, durations):
        extended_images = []
        img_base_name = os.path.splitext(img)[0]
        for _ in range(int(duration * fps)):
            print(os.path.join(temp_folder, img_base_name + ".jpeg"))
            extended_images.append(os.path.join(temp_folder, img_base_name + ".jpeg"))
        clip = ImageSequenceClip(extended_images, fps=fps)
        # clip = clip.with_start(totalTime)
        totalTime += duration
        clips.append(clip)

    # Create ImageSequenceClip from the extended list of images
    # clip = ImageSequenceClip(extended_images, fps=fps)

    print(clips)
        
    transition_index = 0
    final_clips = []

    final_clips.append(clips[0].with_start(0))

    print(durations)

    duration = durations[0]

    for i in range(len(clips) - 1):
        print(i)
        current_clip = clips[i]
        next_clip = clips[i + 1]

        final_clip = None

        transition_type = transition_array[transition_index]

        if transition_type == 0:  # None
            final_clip = CompositeVideoClip([current_clip, next_clip])
        elif transition_type == 1:  # Crossfade
            final_clip = CompositeVideoClip([current_clip.fx(crossfadein, 1), next_clip.fx(crossfadeout, 1)])
        elif transition_type == 2:  # Slide in left
            final_clip = CompositeVideoClip([current_clip, next_clip.fx(slide_in, 1, "left")])
        elif transition_type == 3:  # Slide in right
            final_clip = CompositeVideoClip([current_clip, next_clip.fx(slide_in, 1, "right")])
        elif transition_type == 4:  # Slide in top
            final_clip = CompositeVideoClip([current_clip, next_clip.fx(slide_in, 1, "top")])
        elif transition_type == 5:  # Slide in bottom
            final_clip = CompositeVideoClip([current_clip, next_clip.fx(slide_in, 1, "bottom")])
        elif transition_type == 6:  # Slide out bottom
            final_clip = CompositeVideoClip([current_clip, next_clip.fx(slide_in, 1, "bottom")])
        

        final_clip = final_clip.with_start(duration)
        duration += durations[i + 1]
        final_clips.append(final_clip)

        # final_clips = final_clips.subclip(0, totalTime)

        transition_index += 1


    # final_clips.append(clips[-1].subclip(0, durations[-1] / 2))


    # # Load the background music
    audio_clip = AudioFileClip(music_path)

    # Create a single CompositeVideoClip from the list of final clips
    composite_clip = CompositeVideoClip(final_clips)

    print(clips)

    # composite_clip = CompositeVideoClip(clips)

    # Temporary folder to store frame images
    temp_frame_folder = tempfile.mkdtemp()

    # Save the frames as images in the temporary folder
    frame_paths = []
    for i, frame in enumerate(composite_clip.iter_frames(fps=fps)):
        frame_path = os.path.join(temp_frame_folder, f"frame_{i:05d}.png")
        imageio.imwrite(frame_path, frame)
        frame_paths.append(frame_path)

    # Create ImageSequenceClip from the list of frame images
    print(frame_paths)
    clip = ImageSequenceClip(frame_paths, fps=fps)

    # Set the background music
    clip = clip.with_audio(audio_clip)

    # Trim the video to the required length
    clip = clip.subclip(0, totalTime)

    # Write the video file
    clip.write_videofile(video_path)

    # Clean up: delete the temporary folder and its contents
    shutil.rmtree(temp_frame_folder)


# Example usage
if __name__ == "__main__":
    image_folder = "static/images_dup"
    video_path = "Output_Video.mp4"
    music_path = "static/audio/sample.mp3" 
    
    # this is the duration in sec
    durations = [4,4,4,4,4] 

    transition_array = [2,6,4,5]
    
    images_to_video(image_folder, video_path, durations, music_path, transition_array, fps=10)
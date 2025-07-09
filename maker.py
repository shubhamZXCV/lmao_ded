from moviepy import ImageSequenceClip, AudioFileClip, CompositeVideoClip
from PIL import Image
import os, tempfile, shutil, imageio
from transitions import crossfadein, crossfadeout, slide_in, slide_out

HEIGHT, WIDTH = 900, 1600

def images_to_video(images_path, video_path, durations, transition_array, music_path, fps=1):
    temp_folder = tempfile.mkdtemp()
    processed_images = []
    for img_path in images_path:
        img = Image.open(img_path)
        if img.mode == 'RGBA': img = img.convert('RGB')
        img = img.resize((WIDTH, HEIGHT))
        base = os.path.splitext(os.path.basename(img_path))[0]
        jpeg = os.path.join(temp_folder, base + ".jpeg")
        img.save(jpeg, "JPEG")
        processed_images.append(jpeg)

    clips = [ImageSequenceClip([p]*int(d*fps), fps=fps)
             for p, d in zip(processed_images, durations)]

    final_clips = [clips[0].with_start(0)]
    current_start = durations[0]

    for i in range(len(clips)-1):
        current, nxt = clips[i], clips[i+1]
        tr = transition_array[i] if i < len(transition_array) else 0

        if tr == 0:
            final = CompositeVideoClip([current, nxt])
        elif tr == 1:
            current_fx = crossfadein(current, 1)
            next_fx = crossfadeout(nxt, 1)
            final = CompositeVideoClip([current_fx, next_fx])
        elif 2 <= tr <= 5:
            side = ["left","right","top","bottom"][tr-2]
            nxt_fx = slide_in(nxt, 1, side)
            final = CompositeVideoClip([current, nxt_fx])
        elif tr == 6:
            nxt_fx = slide_out(nxt, 1, "bottom")
            final = CompositeVideoClip([current, nxt_fx])
        else:
            final = CompositeVideoClip([current, nxt])

        final_clips.append(final.with_start(current_start))
        current_start += durations[i+1]

    composite = CompositeVideoClip(final_clips)
    frame_folder = tempfile.mkdtemp()
    frames = []
    for idx, frame in enumerate(composite.iter_frames(fps=fps, dtype="uint8")):
        path = os.path.join(frame_folder, f"f{idx:05d}.png")
        imageio.imwrite(path, frame)
        frames.append(path)

    video = ImageSequenceClip(frames, fps=fps).with_audio(AudioFileClip(music_path))
    video = video.subclipped(0, sum(durations))
    video.write_videofile(video_path)

    shutil.rmtree(frame_folder)
    shutil.rmtree(temp_folder)


if __name__ == "__main__":
    img_folder = "static/images_dup"
    images = [os.path.join(img_folder, f) for f in sorted(os.listdir(img_folder))
              if f.lower().endswith((".png",".jpg",".jpeg"))]
    images_to_video(images, "Output_Video.mp4",
                    [4,4,4,4,4], [2,6,4,5], "static/audio/sample.mp3", fps=10)

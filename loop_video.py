# loop_video.py

import argparse
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips

def main():
    p = argparse.ArgumentParser(
        description="Loop a video for a given number of hours."
    )
    p.add_argument("input_file", help="Path to the source video (e.g., input.mp4)")
    p.add_argument(
        "-t", "--hours", type=int, default=12,
        help="Total length (in hours) of the output loop"
    )
    p.add_argument(
        "-o", "--output", default="output.mp4",
        help="Name of the output file (default: output.mp4)"
    )
    args = p.parse_args()

    clip = VideoFileClip(args.input_file)
    clip_dur = clip.duration
    desired = args.hours * 3600
    loops = int(desired // clip_dur) + 1

    print(f"Looping {args.input_file}: {clip_dur/60:.2f}min × {loops} → {args.hours}h")
    clips = [clip] * loops
    final = concatenate_videoclips(clips).subclipped(0, desired)
    final.write_videofile(
        args.output,
        codec="libx264", audio_codec="aac",
        threads=4, preset="medium"
    )
    print("Done!")

if __name__ == "__main__":
    main()

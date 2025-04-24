# ascii_video.py
import os
import numpy as np
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from app.ASCCI.IMAGEN.ascii_image import image_to_ascii_from_pil,ascii_to_image

def video_to_ascii(
    video_path: str,
    output_path: str,
    width: int = 80,
    output_format: str = 'mp4',
    font_path: str = None,
    font_size: int = 12,
    bg_color: str = "white",
    fg_color: str = "black"
) -> None:
    clip = VideoFileClip(video_path)

    if output_format in ('text', 'image'):
        os.makedirs(output_path, exist_ok=True)
        for idx, frame in enumerate(clip.iter_frames(fps=clip.fps, dtype="uint8")):
            pil = Image.fromarray(frame)
            ascii_str = image_to_ascii_from_pil(pil, width)
            if output_format == 'text':
                path = os.path.join(output_path, f"frame_{idx:05d}.txt")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(ascii_str)
            else:
                img = ascii_to_image(ascii_str, font_path, font_size, bg_color, fg_color)
                img.save(os.path.join(output_path, f"frame_{idx:05d}.png"))
        clip.close()
        return

    if output_format == 'mp4':
        frames = []
        for frame in clip.iter_frames(fps=clip.fps, dtype="uint8"):
            pil = Image.fromarray(frame)
            ascii_str = image_to_ascii_from_pil(pil, width)
            img = ascii_to_image(ascii_str, font_path, font_size, bg_color, fg_color)
            frames.append(np.array(img))
        clip.close()
        seq = ImageSequenceClip(frames, fps=clip.fps)
        seq.write_videofile(
            output_path,
            codec='libx264',
            audio=False
        )
        seq.close()
        return

    clip.close()
    raise ValueError(f"Formato '{output_format}' no soportado")

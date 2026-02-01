import os
import uuid
import subprocess
import time
from typing import Dict
from gtts import gTTS
from pydub import AudioSegment
import torch
from diffusers import StableDiffusionPipeline


class VideoService:
    def __init__(self):
        self.pipe = None
        self._load_model()
    
    def _load_model(self):
        """Load Stable Diffusion model once"""
        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16
            ).to("cuda")
        except Exception as e:
            print(f"Warning: Could not load GPU model, falling back to CPU: {e}")
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5"
            )
    
    def _ensure_directories(self):
        """Create necessary directories"""
        os.makedirs("tmp/images", exist_ok=True)
        os.makedirs("tmp/audio", exist_ok=True)
        os.makedirs("output/videos", exist_ok=True)
    
    def _generate_image(self, prompt: str, idx: int) -> str:
        """Generate image for a scene"""
        image = self.pipe(prompt, num_inference_steps=20).images[0]
        img_path = f"tmp/images/scene_{idx}.png"
        image.save(img_path)
        return img_path
    
    def _generate_audio(self, text: str, language: str, idx: int) -> tuple:
        """Generate audio for a scene"""
        audio_mp3 = f"tmp/audio/scene_{idx}.mp3"
        tts = gTTS(text=text, lang=language)
        tts.save(audio_mp3)
        
        # Convert to wav
        audio_wav = audio_mp3.replace(".mp3", ".wav")
        subprocess.run(["ffmpeg", "-y", "-i", audio_mp3, audio_wav], check=True)
        
        # Get duration
        audio_duration = AudioSegment.from_file(audio_wav).duration_seconds
        
        return audio_wav, audio_duration
    
    def _create_video_segment(self, img_path: str, audio_wav: str, duration: float, idx: int) -> str:
        """Create a video segment from image and audio"""
        segment_path = f"tmp/segment_{idx}.mp4"
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", img_path,
            "-i", audio_wav,
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            segment_path
        ], check=True)
        return segment_path
    
    def _concatenate_segments(self, segments: list) -> str:
        """Concatenate all video segments"""
        concat_file = "tmp/segments.txt"
        with open(concat_file, "w") as f:
            for seg in segments:
                f.write(f"file '{os.path.abspath(seg)}'\n")
        
        output_video = f"output/videos/course_{uuid.uuid4().hex}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_video
        ], check=True)
        
        return output_video
    
    def generate_course_video(self, course_data: Dict) -> str:
        """Generate a complete course video from course data"""
        start_time = time.time()
        
        self._ensure_directories()
        segments = []
        
        for idx, scene in enumerate(course_data["scenes"]):
            # Generate image
            prompt = f"{course_data.get('style', 'cartoon')}, {scene['title']}, {scene['content']}"
            img_path = self._generate_image(prompt, idx)
            
            # Generate audio
            audio_wav, audio_duration = self._generate_audio(
                scene["content"], 
                course_data.get("language", "fr"), 
                idx
            )
            
            # Create video segment
            segment_path = self._create_video_segment(img_path, audio_wav, audio_duration, idx)
            segments.append(segment_path)
        
        # Concatenate all segments
        output_video = self._concatenate_segments(segments)
        
        processing_time = time.time() - start_time
        print(f"Video generated in {processing_time:.2f} seconds")
        
        return output_video


# Global instance
video_service = VideoService()

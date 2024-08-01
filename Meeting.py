import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import time

def extract_audio(video_path):
    video = mp.VideoFileClip(video_path)
    audio_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    video.audio.write_audiofile(audio_file_path)
    video.close()  # Ensure the video file is closed
    return audio_file_path

def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_wav(audio_path)
    temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    
    chunk_duration_ms = 5000  # 5 seconds
    total_duration_ms = len(audio)
    chunks = (total_duration_ms // chunk_duration_ms) + (1 if total_duration_ms % chunk_duration_ms != 0 else 0)
    text = ""
    
    start_time = time.time()
    progress_bar = st.progress(0)
    progress_text = st.empty()
    
    for i in range(chunks):
        chunk_start = i * chunk_duration_ms
        chunk_end = min(chunk_start + chunk_duration_ms, total_duration_ms)
        audio_chunk = audio[chunk_start:chunk_end]
        audio_chunk.export(temp_audio_path, format="wav")
        
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)
        
        try:
            chunk_text = recognizer.recognize_google(audio_data)
            text += chunk_text + " "
        except sr.UnknownValueError:
            text += "[Unintelligible] "
        except sr.RequestError as e:
            text += f"[Error: {e}] "
        
        # Update the progress
        progress_percentage = int(((i + 1) / chunks) * 100)
        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / (i + 1)) * chunks
        estimated_time_remaining = estimated_total_time - elapsed_time
        
        progress_bar.progress(progress_percentage)
        progress_text.text(f"Transcription Progress: {progress_percentage}% - Estimated Time Remaining: {int(estimated_time_remaining)} seconds")
    
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)
    
    return text

# Streamlit UI
st.title("Video Transcription - SBA Info Solutions")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])
if uploaded_file:
    with st.spinner('Extracting audio and converting to text...'):
        video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        audio_path = extract_audio(video_path)
        result_text = convert_audio_to_text(audio_path)
        
        st.subheader("Transcription Text")
        st.text_area("Transcription", result_text, height=300)
        
        # Remove temporary files
        os.remove(video_path)
        os.remove(audio_path)
        
        st.success("Audio extracted and converted to text successfully!")

import streamlit as st
import openai
import os
import tempfile


st.set_page_config(
    page_title="Speech to Text Converter",
    page_icon="🎙️",
    layout="centered"
)

os.environ["OPENAI_API_KEY"] = "sk-ds-team-general-uRHEpM4v8JyZPznqvmSMT3BlbkFJPIMx3gi9v6BQOn58RbSN"
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.warning("⚠️ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

def transcribe_audio(audio_file):
    """Transcribe an audio file using OpenAI's Whisper model"""
    try:
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp_file:
            
            tmp_file.write(audio_file.getvalue())
            tmp_path = tmp_file.name
        
        
        with open(tmp_path, "rb") as audio:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio
            )
        
        
        os.unlink(tmp_path)
        
        return transcript.text
    
    except Exception as e:
        
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        st.error(f"Error during transcription: {str(e)}")
        return None

st.title("🎙️ Speech to Text Converter")

uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "mp4", "wav", "m4a", "webm", "mpga", "ogg"])

if uploaded_file is not None:
    
    st.audio(uploaded_file, format=f"audio/{uploaded_file.type.split('/')[1]}")
    
    
    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio(uploaded_file)
            
            if transcript:
                st.success("Transcription Complete!")
                
                
                st.subheader("Transcript")
                st.markdown(transcript)
                
                
                st.download_button(
                    label="Download Transcript",
                    data=transcript,
                    file_name="transcript.txt",
                    mime="text/plain"
                )

st.markdown("---")
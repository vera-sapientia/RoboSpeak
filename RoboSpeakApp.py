import io
from gtts import gTTS
import streamlit as st

# Page setup
st.set_page_config(
    page_title="RoboSpeaker",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom styling for a polished card layout
st.markdown(
    """
    <style>
        .block-container {
            max-width: 650px;
            padding-top: 3rem;
            padding-bottom: 2rem;
        }
        .header-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .header-sub {
            color: #6c757d;
            font-size: 0.95rem;
            margin-bottom: 2rem;
        }
    </style>
    <div class="header-title">🎙️ RoboSpeaker</div>
    <div class="header-sub">Built by Aastha &bull; Modern Text-to-Speech</div>
""",
    unsafe_allow_html=True,
)

# User inputs
text_input = st.text_area(
    "What would you like me to say?",
    placeholder="Type something clear, funny, or wise...",
    height=140,
)

col1, col2 = st.columns([1, 1])

with col1:
    accent = st.selectbox(
        "Voice Accent",
        options=["com", "co.uk", "ca", "co.in", "com.au"],
        format_func=lambda x: {
            "com": "US English",
            "co.uk": "British English",
            "ca": "Canadian English",
            "co.in": "Indian English",
            "com.au": "Australian English",
        }[x],
    )

with col2:
    speed = st.selectbox(
        "Speech Speed",
        options=[False, True],
        format_func=lambda x: "Normal" if not x else "Slow",
    )

# Action button
speak_button = st.button("🔊 Speak", type="primary", use_container_width=True)

if speak_button:
    clean_text = text_input.strip()
    if not clean_text:
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Generating voice..."):
            try:
                # Generate audio in-memory to avoid saving clutter to disk
                tts = gTTS(text=clean_text, lang="en", tld=accent, slow=speed)
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)

                # Render HTML5 audio player and autoplay
                st.audio(audio_fp, format="audio/mp3", autoplay=True)
                st.success("Playback ready!")
            except Exception as e:
                st.error(f"Error generating speech: {e}")
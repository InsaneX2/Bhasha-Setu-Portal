"""
Interactive Audio Visualizer & Equalizer Component for BhashaSetu
"""

import time
import base64
import streamlit as st
import streamlit.components.v1 as components


def render_audio_player(audio_b64: str, mime_type: str = "audio/wav"):
    """Render native audio player alongside interactive animated equalizer."""
    if not audio_b64:
        return

    # Standard fallback stream
    try:
        st.audio(data=base64.b64decode(audio_b64), format=mime_type)
    except Exception:
        pass

    # Custom animated equalizer widget
    unique_id = f"aud_{int(time.time() * 1000)}"

    player_html = f"""
    <style>
        body {{ margin: 0; padding: 0; background: transparent; font-family: 'Plus Jakarta Sans', sans-serif; }}
        .player-box {{
            display: flex; align-items: center; justify-content: space-between;
            background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 10px; padding: 10px 18px; margin-top: 8px;
        }}
        .eq-group {{ display: flex; align-items: center; gap: 12px; }}
        .equalizer {{ display: flex; align-items: flex-end; height: 26px; gap: 4px; }}
        .bar {{
            width: 5px; height: 4px; background: linear-gradient(180deg, #38bdf8 0%, #6366f1 100%);
            border-radius: 3px; box-shadow: 0 0 8px rgba(56, 189, 248, 0.7); transition: height 0.15s ease;
        }}
        .equalizer.animating .bar {{ animation: bounce 1.1s infinite ease-in-out alternate; }}
        .equalizer.animating .bar:nth-child(1) {{ animation-delay: 0.1s; height: 35%; }}
        .equalizer.animating .bar:nth-child(2) {{ animation-delay: 0.3s; height: 75%; }}
        .equalizer.animating .bar:nth-child(3) {{ animation-delay: 0.0s; height: 100%; }}
        .equalizer.animating .bar:nth-child(4) {{ animation-delay: 0.4s; height: 55%; }}
        .equalizer.animating .bar:nth-child(5) {{ animation-delay: 0.2s; height: 85%; }}
        @keyframes bounce {{ 0% {{ transform: scaleY(0.2); }} 100% {{ transform: scaleY(1.1); }} }}
        .status-lbl {{ font-size: 0.85rem; color: #94a3b8; font-weight: 500; }}
        .btn-repeat {{
            display: flex; align-items: center; gap: 6px; background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white; border: none; border-radius: 6px; padding: 6px 14px; font-size: 0.85rem;
            font-weight: 600; cursor: pointer; transition: all 0.2s ease;
        }}
        .btn-repeat:hover {{ transform: translateY(-1px); box-shadow: 0 0 12px rgba(37, 99, 235, 0.6); }}
    </style>
    <div class="player-box">
        <div class="eq-group">
            <div class="equalizer" id="eq_{unique_id}">
                <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
            </div>
            <span class="status-lbl" id="lbl_{unique_id}">Ready for playback</span>
        </div>
        <button class="btn-repeat" id="btn_{unique_id}" onclick="toggleReplay()">🔁 Repeat Pronunciation</button>
    </div>
    <audio id="{unique_id}" src="data:{mime_type};base64,{audio_b64}" preload="auto"></audio>
    <script>
        const aud = document.getElementById("{unique_id}");
        const eq = document.getElementById("eq_{unique_id}");
        const lbl = document.getElementById("lbl_{unique_id}");
        const btn = document.getElementById("btn_{unique_id}");
        function onPlay() {{ eq.classList.add("animating"); lbl.innerText = "Playing native pronunciation..."; btn.innerHTML = "⏸ Pause"; }}
        function onStop() {{ eq.classList.remove("animating"); lbl.innerText = "Audio ready"; btn.innerHTML = "🔁 Repeat"; }}
        aud.onplay = onPlay; aud.onpause = onStop; aud.onended = onStop;
        function toggleReplay() {{ if (aud.paused) {{ aud.currentTime = 0; aud.play(); }} else {{ aud.pause(); }} }}
        const p = aud.play();
        if (p !== undefined) {{ p.catch(() => {{ onStop(); lbl.innerText = "Click to play audio"; btn.innerHTML = "▶ Play Pronunciation"; }}); }}
    </script>
    """
    components.html(player_html, height=75)

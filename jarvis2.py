import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import screen_brightness_control as sbc
import ctypes
import urllib.parse
import re
import math
import random
import time as _time
import threading
import queue
import json
import os
import shutil
import hashlib
import concurrent.futures
from pathlib import Path
import xml.etree.ElementTree as ET
from html import unescape
import collections
import atexit
try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    _HAS_PSUTIL = False
try:
    import pythoncom
    import win32com.client
    import win32event
    _HAS_WIN32COM = True
    _HAS_WIN32EVENT = True
except Exception:
    _HAS_WIN32COM = False
    _HAS_WIN32EVENT = False
import wave
import struct
import winsound

# ── Calibrate Windows Multimedia Timer for Rock-Solid 60 FPS (16.6ms) ──
try:
    ctypes.windll.winmm.timeBeginPeriod(1)
    atexit.register(lambda: ctypes.windll.winmm.timeEndPeriod(1))
except Exception:
    pass




# ╔══════════════════════════════════════════════════════════════════╗
# ║  THEMES & CURATED SCI-FI COLOR PALETTES                          ║
# ╚══════════════════════════════════════════════════════════════════╝

THEMES = {
    "cyan": {
        "name": "CYBER CYAN (J.A.R.V.I.S)",
        "cyan":       "#00e5ff",
        "cyan_br":    "#40ffff",
        "cyan_dim":   "#006878",
        "cyan_faint": "#001e24",
        "border":     "#0c283e",
        "border_gl":  "#0f6890",
        "border_br":  "#18a0d0",
        "accent":     "#00e5ff",
        "glow":       "#d0f8ff",
    },
    "green": {
        "name": "MATRIX NEON (HACKER HUD)",
        "cyan":       "#20ff80",
        "cyan_br":    "#69ff9f",
        "cyan_dim":   "#085828",
        "cyan_faint": "#022410",
        "border":     "#083016",
        "border_gl":  "#127838",
        "border_br":  "#1ec058",
        "accent":     "#20ff80",
        "glow":       "#d0ffe8",
    },
    "amber": {
        "name": "SOLAR AMBER (WAR MACHINE)",
        "cyan":       "#ffaa30",
        "cyan_br":    "#ffcc66",
        "cyan_dim":   "#604010",
        "cyan_faint": "#281802",
        "border":     "#382006",
        "border_gl":  "#855010",
        "border_br":  "#d4881a",
        "accent":     "#ffaa30",
        "glow":       "#fff2d0",
    },
    "purple": {
        "name": "QUANTUM PURPLE (NEBULA)",
        "cyan":       "#c084fc",
        "cyan_br":    "#e9d5ff",
        "cyan_dim":   "#581c87",
        "cyan_faint": "#22043a",
        "border":     "#320654",
        "border_gl":  "#7e22ce",
        "border_br":  "#a855f7",
        "accent":     "#c084fc",
        "glow":       "#f3e8ff",
    },
    "crimson": {
        "name": "CRIMSON RED (MARK 85 ALERT)",
        "cyan":       "#ff3355",
        "cyan_br":    "#ff8899",
        "cyan_dim":   "#771122",
        "cyan_faint": "#2b040a",
        "border":     "#3d0a12",
        "border_gl":  "#991133",
        "border_br":  "#e02040",
        "accent":     "#ff3355",
        "glow":       "#ffe0e6",
    },
}

# Active color palette dictionary
C = {
    "void":       "#010408",
    "bg":         "#030810",
    "surface":    "#06111e",
    "surface_hi": "#0a1a2e",
    "panel":      "#02070f",
    "text":       "#d6eff7",
    "text_dim":   "#628e9e",
    "muted":      "#324d5e",
    "green":      "#20ff80",
    "green_dim":  "#084828",
    "amber":      "#ffaa30",
    "amber_dim":  "#604010",
    "red":        "#ff2040",
    "red_dim":    "#501018",
    "white":      "#ffffff",
    "purple":     "#a855f7",
    "purple_dim": "#4a1880",
}
C.update(THEMES["cyan"])

FN = "Consolas"
FN_UI = "Segoe UI"
CONFIG_FILE = Path(__file__).resolve().parent / "hud_config.json"


# ╔══════════════════════════════════════════════════════════════════╗
# ║  PERSISTENT HUD CONFIGURATION                                    ║
# ╚══════════════════════════════════════════════════════════════════╝

DEFAULT_CONFIG = {
    "theme": "cyan",
    "input_language": "auto",
    "default_location": "Uttar Pradesh, India",
    "column_order": ["lp", "cp", "rp"],
    "center_order": ["term", "wave", "quick", "hardware"],
    "voice_rate": 175,
    "voice_index": 0,
    "voice_name": "Microsoft David Desktop - English (United States)",
    "tts_engine": "sapi",
    "elevenlabs_voice_id": "IRHApOXLvnW57QJPQH2P",
    "elevenlabs_voice_name": "Adam - American, Dark and Tough",
    "elevenlabs_api_key": "",
    "ai_provider": "auto",
    "ai_api_key": "",
    "ai_model": "llama-3.3-70b-versatile",
    "ollama_url": "http://localhost:11434",
    "wake_word_enabled": True,
    "sfx_enabled": True,
    "voice_input_timeout": 10.0,
    "voice_phrase_time_limit": 20.0,
    "visible": {
        "lp": True,
        "cp": True,
        "rp": True,
        "term": True,
        "wave": True,
        "quick": True,
        "hardware": True,
        "rain": True,
        "metrics": True,
    },
    "quick_cmds": [
        ["⟫ Live Weather",            "what is the weather today",     "METEO"],
        ["⟫ Breaking News",           "latest news headlines",         "GLOBAL NEWS"],
        ["⟫ Autoplay Believer",       "play Believer on YouTube",      "MEDIA DISPATCH"],
        ["⟫ Tech Intelligence",       "latest technology news",        "TECH INTEL"],
        ["⟫ Who is Elon Musk",        "Who is Elon Musk",              "WIKI INTEL"],
        ["⟫ System Volume Boost",     "volume up",                     "HARDWARE"],
    ],
}

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                cfg = dict(DEFAULT_CONFIG)
                cfg.update(saved)
                return cfg
        except Exception as e:
            print("Config load error:", e)
    return dict(DEFAULT_CONFIG)

def save_config():
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(hud_config, f, indent=2)
    except Exception as e:
        print("Config save error:", e)

hud_config = load_config()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  GLOBAL STATE & ANIMATION TRACKERS                               ║
# ╚══════════════════════════════════════════════════════════════════╝

_anim = {
    "listening": False,
    "processing": False,
    "speaking": False,
    "edit_mode": False,
    "reactor_angle": 0.0,
    "pulse_phase": 0.0,
    "scan_angle": 0.0,
    "boot_done": False,
    "boot_step": 0,
    "particles": [],
    "data_rain_cols": [],
    "ripples": [],
    "last_answer": "",
    # ── 60 FPS Engine & Cybernetic Matrix System ──
    "fps_target": 60,
    "fps_actual": 60.0,
    "frame_count": 0,
    "last_frame_time": _time.perf_counter(),
    "fps_history": collections.deque(maxlen=30),
    "matrix_mode": "core",       # "core", "neural", "vox", "hex"
    "matrix_speed_mult": 1.0,    # 1.0, 1.5, 2.0, 0.5, 0.0 (freeze)
    "matrix_mouse_pos": None,    # (x, y)
    "matrix_ripples": [],        # shockwave ripples from clicks [{x, y, r, max_r, alpha, clr}]
    "matrix_sparks": [],         # cyber spark drag trails [{x, y, vx, vy, alpha, clr}]
    "matrix_inspect_node": "",
    "matrix_tokens": collections.deque(maxlen=60),
    "core_audio_level": 0.0,
}

def matrix_push_token(token):
    """Pushes a real-time core telemetry token into the Matrix stream queue."""
    try:
        clean_tok = re.sub(r"[^A-Za-z0-9:_.\-/%]", "", str(token)).strip().upper()
        if clean_tok and len(clean_tok) <= 24:
            _anim["matrix_tokens"].append(clean_tok)
    except Exception:
        pass

_stream_queue = []
_stream_active = False

def clean_for_speech(text):
    if not text:
        return ""
    t = str(text)

    # 1. Code blocks and inline code
    t = re.sub(r'```[\s\S]*?```', ' Code block displayed on terminal. ', t)
    t = re.sub(r'`([^`]*)`', r'\1', t)

    # 2. HTML / XML tags & entities (prevents SAPI SSML parser crashes & errors)
    t = re.sub(r'</?[a-zA-Z][^>]*>', ' ', t)
    t = re.sub(r'&amp;', ' and ', t, flags=re.IGNORECASE)
    t = re.sub(r'&lt;', ' less than ', t, flags=re.IGNORECASE)
    t = re.sub(r'&gt;', ' greater than ', t, flags=re.IGNORECASE)
    t = re.sub(r'&quot;|&#39;|&apos;', ' ', t, flags=re.IGNORECASE)
    t = re.sub(r'&deg;', ' degrees ', t, flags=re.IGNORECASE)
    t = re.sub(r'&nbsp;', ' ', t, flags=re.IGNORECASE)
    t = re.sub(r'(?<=\s)<(?=\s|\d|[a-zA-Z])', ' less than ', t)
    t = re.sub(r'(?<=\s)>(?=\s|\d|[a-zA-Z])', ' greater than ', t)
    t = re.sub(r'[<>]', ' ', t)

    # 3. Strip decorative sci-fi HUD frames, dividers & box characters
    t = re.sub(r'[-═─━_]{3,}', ' ', t)
    t = re.sub(r'[╔╗╚╝║┃◈◉◎●◌▸⟫▶◀▲▼✓✕✔✗■◻★☆•·●◆◇▪▫]', ' ', t)

    # 4. Strip emojis and miscellaneous pictographs (prevents SAPI surrogate decoding buzzing/cracking)
    t = re.sub(r'[\U00010000-\U0010ffff]', ' ', t)
    t = re.sub(r'[\u2600-\u27bf\ufe00-\ufe0f\u200b-\u200d]', ' ', t)

    # 5. Normalize curly quotes and em-dashes
    t = re.sub(r'[\u201c\u201d\u201e\u201f]', ' ', t)
    t = re.sub(r'[\u2018\u2019]', "'", t)
    t = re.sub(r'[\u2014\u2013]', ', ', t)

    # 6. Expand bracketed index like [01] to Headline 1:
    t = re.sub(r'\[0?([1-9])\]', r'Headline \1: ', t)
    t = re.sub(r'\[[0-9a-zA-Z]{1,4}\]', ' ', t)

    # 7. Remove raw URLs and UI hints
    t = re.sub(r'https?://\S+|www\.\S+', ' ', t)
    t = re.sub(r'\b(?:Click\s+\[READ\]\s+to\s+re-hear|Click\s+\[CLR\]\s+to\s+clear)\b', '', t, flags=re.IGNORECASE)

    # 8. Units & symbols expansion for natural prosody
    t = re.sub(r'\bdeg\s*C\b|°C', ' degrees Celsius ', t, flags=re.IGNORECASE)
    t = re.sub(r'\bdeg\s*F\b|°F', ' degrees Fahrenheit ', t, flags=re.IGNORECASE)
    t = re.sub(r'\bkm/h\b|\bkmph\b', ' kilometers per hour ', t, flags=re.IGNORECASE)
    t = re.sub(r'\bkm\b', ' kilometers ', t, flags=re.IGNORECASE)
    t = re.sub(r'%', ' percent ', t)
    t = re.sub(r'&', ' and ', t)
    t = re.sub(r'\$(\d+(?:\.\d+)?)', r'\1 dollars', t)
    t = re.sub(r'\bwttr\.in\b', ' weather network ', t, flags=re.IGNORECASE)

    # 9. Numbered lists: '1. ' or '1) ' -> 'Point 1, ' so trailing period doesn't trigger sentence splitting
    t = re.sub(r'(?m)^\s*(\d+)[\.\)]\s+', r'Point \1, ', t)
    t = re.sub(r'(?<=\s)(\d+)[\.\)]\s+', r'Point \1, ', t)

    # 10. Abbreviations protection & expansion (stops premature period sentence fragmentation)
    t = re.sub(r'\bDr\.\s*', 'Doctor ', t)
    t = re.sub(r'\bMr\.\s*', 'Mister ', t)
    t = re.sub(r'\bMrs\.\s*', 'Missus ', t)
    t = re.sub(r'\bMs\.\s*', 'Mizz ', t)
    t = re.sub(r'\bProf\.\s*', 'Professor ', t)
    t = re.sub(r'\bSt\.\s*', 'Saint ', t)
    t = re.sub(r'\bvs\.\s*|\bv\.\s*', 'versus ', t)
    t = re.sub(r'\be\.g\.,?\s*', 'for example, ', t)
    t = re.sub(r'\bi\.e\.,?\s*', 'that is, ', t)
    t = re.sub(r'\betc\.\s*', 'etcetera. ', t)
    t = re.sub(r'\bapprox\.\s*', 'approximately ', t)
    t = re.sub(r'\bNo\.\s*(\d+)', r'Number \1', t)
    t = re.sub(r'(?i)\bU\.S\.A\.(?=\s|$)', 'USA', t)
    t = re.sub(r'(?i)\bU\.S\.(?=\s|$)', 'US', t)
    t = re.sub(r'(?i)\bp\.m\.(?=\s|$)', 'PM', t)
    t = re.sub(r'(?i)\ba\.m\.(?=\s|$)', 'AM', t)

    # 11. Clean Markdown syntax, formatting symbols, and parenthetical prosody
    t = re.sub(r'[*#_~^]', '', t)
    t = re.sub(r'\"', '', t)
    t = re.sub(r'\(([^)]*)\)', r', \1, ', t)
    t = re.sub(r'\[([^\]]*)\]', r', \1, ', t)
    t = re.sub(r'(?<=\w)/(?=\w)', ' or ', t)
    t = re.sub(r'[|/\\+=]+', ', ', t)
    t = re.sub(r'\s+[-–—]+\s+', ', ', t)
    t = re.sub(r':(?=\s)', ',', t)

    # 12. Convert line breaks into natural pauses
    lines = [line.strip() for line in t.splitlines() if line.strip()]
    punctuated = []
    for line in lines:
        if not re.search(r'[.!?:;]$', line):
            line += '.'
        punctuated.append(line)
    res = ' '.join(punctuated)

    # 13. Clean up multiple punctuation and whitespace (protecting decimal numbers like 89.6 or 0.05)
    res = re.sub(r'\.{2,}', '. ', res)
    res = re.sub(r'[,][\s,]*[,]', ', ', res)
    res = re.sub(r',\s*\.', '.', res)
    res = re.sub(r'\.\s*,', '.', res)
    res = re.sub(r'\s*,\s*', ', ', res)
    res = re.sub(r'(?<!\d)\s*\.\s*(?!\d)', '. ', res)
    res = re.sub(r'\s+', ' ', res)
    return res.strip()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  HIGH-FIDELITY CYBERNETIC SOUND EFFECTS (SFX) ENGINE             ║
# ╚══════════════════════════════════════════════════════════════════╝

SFX_DIR = Path(__file__).resolve().parent / "sfx"
VOICES_DIR = Path(__file__).resolve().parent / "voices"
VOICES_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = Path(__file__).resolve().parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def init_sfx_library():
    """Synthesizes high-fidelity 44.1kHz sci-fi audio effects into sfx/ if missing."""
    SFX_DIR.mkdir(parents=True, exist_ok=True)
    SR = 44100

    def _save(filename, samples):
        target = SFX_DIR / filename
        if target.exists():
            return
        try:
            with wave.open(str(target), "w") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(SR)
                raw = bytearray()
                for s in samples:
                    val = max(-32767, min(32767, int(float(s) * 32767)))
                    raw.extend(struct.pack("<h", val))
                wf.writeframes(raw)
        except Exception as e:
            print(f"SFX synthesis note ({filename}):", e)

    # 1. Boot Sound (Cinematic Power-Up Chord)
    if not (SFX_DIR / "boot.wav").exists():
        dur = 1.0
        total_s = int(SR * dur)
        samples_boot = []
        for i in range(total_s):
            t = i / SR
            sub_f = 80 + 80 * (t / dur)
            sub = math.sin(2 * math.pi * sub_f * t) * (1 - t / dur) * 0.35
            env = (t / 0.15) if t < 0.15 else math.exp(-2.8 * (t - 0.15))
            chord = (
                math.sin(2 * math.pi * 440 * t) +
                0.8 * math.sin(2 * math.pi * 659.25 * t) +
                0.6 * math.sin(2 * math.pi * 880 * t) +
                0.4 * math.sin(2 * math.pi * 1318.5 * t * 1.002)
            ) * env * 0.22
            shimmer = math.sin(2 * math.pi * 2637 * t) * math.exp(-4.5 * t) * 0.15
            samples_boot.append(sub + chord + shimmer)
        _save("boot.wav", samples_boot)

    # 2. Transmit (Digital telemetry frequency chirp)
    if not (SFX_DIR / "transmit.wav").exists():
        dur = 0.20
        total_s = int(SR * dur)
        samples_tx = []
        for i in range(total_s):
            t = i / dur
            freq = 1300 + 1600 * t
            env = math.sin(math.pi * t)
            s = (math.sin(2 * math.pi * freq * (i / SR)) + 0.3 * math.sin(4 * math.pi * freq * (i / SR))) * env * 0.35
            samples_tx.append(s)
        _save("transmit.wav", samples_tx)

    # 3. Sonar Ping (Microphone acoustic capture)
    if not (SFX_DIR / "sonar.wav").exists():
        dur = 0.65
        total_s = int(SR * dur)
        samples_sonar = [0.0] * total_s
        for i in range(total_s):
            t = i / SR
            env = math.exp(-8.0 * t)
            samples_sonar[i] += (math.sin(2 * math.pi * 1760 * t) + 0.25 * math.sin(2 * math.pi * 3520 * t)) * env * 0.45
        echo_start = int(0.20 * SR)
        for i in range(echo_start, total_s):
            t = (i - echo_start) / SR
            samples_sonar[i] += math.sin(2 * math.pi * 1760 * t) * math.exp(-9.0 * t) * 0.15
        _save("sonar.wav", samples_sonar)

    # 4. Downlink (Harmonic 4-note telemetry chime)
    if not (SFX_DIR / "downlink.wav").exists():
        notes = [659.25, 830.61, 987.77, 1318.51]
        n_dur = 0.11
        tail = 0.38
        tot_dur = len(notes) * n_dur + tail
        total_s = int(SR * tot_dur)
        samples_dl = [0.0] * total_s
        for idx, freq in enumerate(notes):
            start = int(idx * n_dur * SR)
            for i in range(int((n_dur + tail) * SR)):
                pos = start + i
                if pos >= total_s: break
                t = i / SR
                env = math.exp(-5.5 * t)
                s = (math.sin(2 * math.pi * freq * t) + 0.35 * math.sin(2 * math.pi * freq * 2 * t) + 0.15 * math.sin(2 * math.pi * freq * 3 * t)) * env * 0.30
                samples_dl[pos] += s
        _save("downlink.wav", samples_dl)

    # 5. Switch (Futuristic voice & mode morpher)
    if not (SFX_DIR / "switch.wav").exists():
        dur = 0.32
        total_s = int(SR * dur)
        samples_sw = []
        for i in range(total_s):
            t = i / dur
            freq = 480 + 640 * math.sin(math.pi * t)
            env = max(0.0, math.sin(math.pi * t)) ** 0.8
            s = (math.sin(2 * math.pi * freq * (i / SR)) + 0.25 * math.sin(2 * math.pi * freq * 2.01 * (i / SR))) * env * 0.35
            samples_sw.append(s)
        _save("switch.wav", samples_sw)

    # 6. Ack (Subtle hardware feedback)
    if not (SFX_DIR / "ack.wav").exists():
        dur = 0.10
        total_s = int(SR * dur)
        samples_ack = []
        for i in range(total_s):
            t = i / SR
            f = 1900 if i < total_s // 2 else 2500
            env = math.exp(-35.0 * (t % (dur / 2)))
            samples_ack.append(math.sin(2 * math.pi * f * t) * env * 0.3)
        _save("ack.wav", samples_ack)

    # 7. Alert (Attention pulse)
    if not (SFX_DIR / "alert.wav").exists():
        dur = 0.45
        total_s = int(SR * dur)
        samples_alert = [0.0] * total_s
        for i in range(int(0.18 * SR)):
            t = i / SR
            samples_alert[i] += math.sin(2 * math.pi * 784 * t) * math.exp(-6.0 * t) * 0.35
        p2_start = int(0.20 * SR)
        for i in range(p2_start, int(0.42 * SR)):
            t = (i - p2_start) / SR
            samples_alert[i] += math.sin(2 * math.pi * 587.33 * t) * math.exp(-6.0 * t) * 0.35
        _save("alert.wav", samples_alert)

init_sfx_library()

def play_sfx(name, force=False):
    """Plays an asynchronous sci-fi sound effect if sfx_enabled is True."""
    if not force and not hud_config.get("sfx_enabled", True):
        return
    # Guard: prevent sound effects from colliding with active speech output
    if not force and _anim.get("speaking", False):
        return
    try:
        p_wav = SFX_DIR / f"{name}.wav"
        p_mp3 = SFX_DIR / f"{name}.mp3"
        if p_wav.exists():
            winsound.PlaySound(str(p_wav), winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif p_mp3.exists():
            play_audio_file(p_mp3, async_play=True)
        else:
            init_sfx_library()
            if p_wav.exists():
                winsound.PlaySound(str(p_wav), winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print(f"SFX error ({name}):", e)


_audio_stop_event = threading.Event()

def play_audio_file(file_path, async_play=True):
    """
    Plays an audio file (.mp3, .wav) reliably on Windows.
    For .wav files, winsound is used.
    For .mp3 files, win32com WMPlayer.OCX is used.
    """
    try:
        p = Path(file_path).resolve()
        if not p.exists():
            print(f"[AUDIO] File not found: {p}")
            return False

        ext = p.suffix.lower()
        if ext == ".wav":
            flags = winsound.SND_FILENAME
            if async_play:
                flags |= winsound.SND_ASYNC
            winsound.PlaySound(str(p), flags)
            return True
        elif ext == ".mp3":
            def _play_mp3():
                try:
                    if _HAS_WIN32COM:
                        pythoncom.CoInitialize()
                        # To prevent Windows Media Player from locking the master voice file in voices/,
                        # copy to a transient playback file in cache/
                        play_copy = CACHE_DIR / f"play_{int(_time.time() * 1000) % 1000000}.mp3"
                        target_to_play = p
                        try:
                            shutil.copyfile(str(p), str(play_copy))
                            target_to_play = play_copy
                        except Exception:
                            pass

                        _audio_stop_event.clear()
                        wmp = win32com.client.Dispatch("WMPlayer.OCX")
                        media = wmp.newMedia(str(target_to_play))
                        wmp.currentPlaylist.appendItem(media)
                        wmp.controls.play()

                        # Monitor playback completion and properly release COM handles
                        t0 = _time.time()
                        has_started = False
                        while _time.time() - t0 < 35:
                            if _audio_stop_event.is_set():
                                try:
                                    wmp.controls.stop()
                                    wmp.close()
                                    wmp.currentPlaylist.clear()
                                except Exception:
                                    pass
                                break
                            state = getattr(wmp, "playState", 0)
                            if state == 3:  # 3 = Playing
                                has_started = True
                            elif has_started and state in (1, 8):  # 1=stopped, 8=mediaEnded
                                break
                            _time.sleep(0.05)

                        try:
                            wmp.controls.stop()
                            wmp.close()
                            wmp.currentPlaylist.clear()
                        except Exception:
                            pass

                        # Clean up transient play copy
                        if target_to_play == play_copy:
                            try:
                                play_copy.unlink(missing_ok=True)
                            except Exception:
                                pass
                except Exception as e:
                    print("[AUDIO] MP3 playback note:", e)
            if async_play:
                threading.Thread(target=_play_mp3, daemon=True).start()
            else:
                _play_mp3()
            return True
    except Exception as ex:
        print("[AUDIO] Play error:", ex)
    return False


def download_elevenlabs_voice(voice_id="IRHApOXLvnW57QJPQH2P"):
    """
    Downloads voice preview audio and metadata for an ElevenLabs voice ID.
    Works for any shared or community voice without requiring an API key.
    Employs lock-resistant atomic file replacement to prevent [Errno 13] on Windows.
    Returns (success: bool, info_dict: dict, file_path: str, message: str)
    """
    try:
        url = f"https://api.elevenlabs.io/v1/shared-voices/{voice_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        meta_file = VOICES_DIR / f"{voice_id}.json"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        preview_url = data.get("preview_url")
        if not preview_url:
            for vl in data.get("verified_languages", []):
                if vl.get("preview_url"):
                    preview_url = vl["preview_url"]
                    break

        if not preview_url:
            return False, data, None, "No preview audio URL found in voice metadata."

        out_audio = VOICES_DIR / f"elevenlabs_{voice_id}_preview.mp3"
        temp_dl = VOICES_DIR / f"elevenlabs_{voice_id}_dl_{int(_time.time())}.tmp"

        aud_req = urllib.request.Request(preview_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(aud_req, timeout=25) as a_resp:
            audio_bytes = a_resp.read()

        with open(temp_dl, "wb") as tf:
            tf.write(audio_bytes)

        # Atomic replacement with Windows handle-lock recovery
        if out_audio.exists():
            try:
                os.replace(temp_dl, out_audio)
            except PermissionError:
                # If existing out_audio is currently open by a media player or process, rename it to .old and place new file
                old_bak = VOICES_DIR / f"elevenlabs_{voice_id}_preview_{int(_time.time())}.old"
                try:
                    os.rename(out_audio, old_bak)
                    os.replace(temp_dl, out_audio)
                except Exception:
                    # Final fallback: copy bytes
                    shutil.copyfile(str(temp_dl), str(out_audio))
                    temp_dl.unlink(missing_ok=True)
        else:
            os.replace(temp_dl, out_audio)

        # Clean up any leftover .old files if unblocked
        for old_f in VOICES_DIR.glob(f"elevenlabs_{voice_id}_*.old"):
            try:
                old_f.unlink(missing_ok=True)
            except Exception:
                pass

        return True, data, str(out_audio), f"Voice '{data.get('name')}' downloaded successfully ({out_audio.stat().st_size // 1024} KB)."
    except Exception as e:
        return False, {}, None, str(e)


def get_elevenlabs_voice_status(voice_id="IRHApOXLvnW57QJPQH2P"):
    """Returns information on whether the voice preview and metadata are cached locally."""
    audio_path = VOICES_DIR / f"elevenlabs_{voice_id}_preview.mp3"
    meta_path = VOICES_DIR / f"{voice_id}.json"
    is_downloaded = audio_path.exists() and audio_path.stat().st_size > 1000
    meta = {}
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception:
            pass
    return {
        "downloaded": is_downloaded,
        "audio_path": str(audio_path) if is_downloaded else None,
        "size_kb": (audio_path.stat().st_size // 1024) if is_downloaded else 0,
        "name": meta.get("name", "Adam - American, Dark and Tough"),
        "accent": meta.get("accent", "american"),
        "gender": meta.get("gender", "male"),
        "description": meta.get("description", "A tough hero, weathered by years of experience. American accent."),
        "voice_id": voice_id
    }


def audition_elevenlabs_voice(voice_id="IRHApOXLvnW57QJPQH2P"):
    """Auditions the downloaded ElevenLabs voice sample."""
    audio_path = VOICES_DIR / f"elevenlabs_{voice_id}_preview.mp3"
    if not audio_path.exists():
        success, meta, p, msg = download_elevenlabs_voice(voice_id)
        if not success:
            speak(f"Unable to download ElevenLabs voice. Error: {msg}")
            return False
        audio_path = Path(p)

    status = get_elevenlabs_voice_status(voice_id)
    terminal_feed_log("VOICE", f"Auditioning ElevenLabs Voice: {status['name']} (ID: {voice_id})")
    _safe_ui_update(lambda: set_status(f"◈  AUDITIONING ELEVENLABS: {status['name'][:24]}...", C.get("cyan_br", "#40ffff")))
    play_audio_file(audio_path, async_play=True)
    return True


def synthesize_elevenlabs_speech(text, voice_id="IRHApOXLvnW57QJPQH2P", api_key=None):
    """
    Synthesizes custom text into speech using ElevenLabs Neural TTS API.
    Requires a valid ElevenLabs API key.
    """
    if not api_key:
        api_key = hud_config.get("elevenlabs_api_key", "").strip()
    if not api_key:
        return False, None, "ElevenLabs API key not configured."

    import hashlib
    text_hash = hashlib.md5(f"{voice_id}_{text}".encode("utf-8")).hexdigest()
    cache_file = CACHE_DIR / f"el_{text_hash[:16]}.mp3"
    if cache_file.exists() and cache_file.stat().st_size > 500:
        return True, str(cache_file), None

    def _call_api(vid):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
        payload = json.dumps({
            "text": text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "xi-api-key": api_key,
                "User-Agent": "JARVIS-AI-Voice-Assistant/2.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            return resp.read()

    try:
        try:
            content = _call_api(voice_id)
        except urllib.error.HTTPError as he:
            # If community library voice is restricted on free tier (HTTP 402), fallback to built-in Adam
            if he.code == 402 and voice_id == "IRHApOXLvnW57QJPQH2P":
                terminal_feed_log("TTS", "Library voice requires subscription; generating via official Adam neural core.")
                content = _call_api("pNInz6obpgDQGcFmaJgB")
            else:
                raise

        temp_cf = CACHE_DIR / f"el_{text_hash[:16]}_{int(_time.time())}.tmp"
        with open(temp_cf, "wb") as cf:
            cf.write(content)
        try:
            os.replace(temp_cf, cache_file)
        except Exception:
            shutil.copyfile(str(temp_cf), str(cache_file))
            temp_cf.unlink(missing_ok=True)
        return True, str(cache_file), None
    except Exception as ex:
        return False, None, str(ex)


def synthesize_hindi_speech(text):
    """
    Synthesizes native Hindi text into natural speech audio via Google Translate TTS.
    Caches audio to cache/hi_<hash>.mp3 for instant zero-latency replay.
    """
    if not text or not str(text).strip():
        return False, None, "Empty text."

    clean = str(text).strip()
    text_hash = hashlib.md5(clean.encode("utf-8")).hexdigest()
    cache_file = CACHE_DIR / f"hi_{text_hash[:16]}.mp3"
    if cache_file.exists() and cache_file.stat().st_size > 300:
        return True, str(cache_file), None

    try:
        encoded = urllib.parse.quote(clean[:200])
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded}&tl=hi&client=tw-ob"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=6)
        if res.status_code == 200 and len(res.content) > 300:
            temp_cf = CACHE_DIR / f"hi_{text_hash[:16]}_{int(_time.time())}.tmp"
            with open(temp_cf, "wb") as cf:
                cf.write(res.content)
            try:
                os.replace(temp_cf, cache_file)
            except Exception:
                shutil.copyfile(str(temp_cf), str(cache_file))
                temp_cf.unlink(missing_ok=True)
            return True, str(cache_file), None
        return False, None, f"HTTP {res.status_code}"
    except Exception as ex:
        return False, None, str(ex)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  VOICE MANAGER & DISCOVERY ENGINE                                ║
# ╚══════════════════════════════════════════════════════════════════╝

_available_voices = []

def get_available_voices():
    global _available_voices
    if _available_voices:
        return _available_voices

    voices_found = []
    try:
        if _HAS_WIN32COM:
            pythoncom.CoInitialize()
            v = win32com.client.Dispatch("SAPI.SpVoice")
            sapi_v = v.GetVoices()
            for i in range(sapi_v.Count):
                item = sapi_v.Item(i)
                desc = item.GetDescription()
                vid = item.Id
                is_fem = any(k in desc.lower() for k in ("zira", "female", "eva", "hazel", "susan", "heera"))
                tag = "NEURAL FEMALE" if is_fem else "TACTICAL MALE"
                alias = "F.R.I.D.A.Y" if is_fem else "J.A.R.V.I.S"
                voices_found.append({
                    "index": i,
                    "name": desc,
                    "id": vid,
                    "alias": alias,
                    "tag": tag,
                    "is_female": is_fem,
                })
    except Exception as e:
        print("Voice discovery note (SAPI):", e)

    if not voices_found:
        try:
            eng = pyttsx3.init()
            for i, pv in enumerate(eng.getProperty("voices")):
                is_fem = any(k in pv.name.lower() for k in ("zira", "female", "eva", "hazel", "susan", "heera"))
                tag = "NEURAL FEMALE" if is_fem else "TACTICAL MALE"
                alias = "F.R.I.D.A.Y" if is_fem else "J.A.R.V.I.S"
                voices_found.append({
                    "index": i,
                    "name": pv.name,
                    "id": pv.id,
                    "alias": alias,
                    "tag": tag,
                    "is_female": is_fem,
                })
        except Exception:
            pass

    if not voices_found:
        voices_found = [{
            "index": 0,
            "name": "System Default Voice",
            "id": "default",
            "alias": "J.A.R.V.I.S",
            "tag": "TACTICAL MALE",
            "is_female": False,
        }]

    _available_voices = voices_found
    return _available_voices

def switch_voice_profile(voice_index, speak_confirm=True, cmd_id=None):
    voices = get_available_voices()
    if not (0 <= voice_index < len(voices)):
        return False
    vinfo = voices[voice_index]
    hud_config["voice_index"] = voice_index
    hud_config["voice_name"] = vinfo["name"]
    save_config()

    _tts_queue.put(("SET_VOICE", voice_index))
    play_sfx("switch")

    terminal_feed_log("VOICE", f"Speech core shifted to {vinfo['alias']} ({vinfo['tag']})")

    if speak_confirm:
        if cmd_id is not None and cmd_id != _current_command_id:
            return True
        confirm_text = (
            f"Voice profile updated to {vinfo['alias']} neural core. Online and at your service, sir."
            if vinfo["is_female"] else
            f"Voice profile updated to {vinfo['alias']} tactical core. Ready for your command, sir."
        )
        speak(confirm_text, cmd_id=cmd_id)

    return True

def switch_voice_by_query(query_or_index, speak_confirm=True, cmd_id=None):
    voices = get_available_voices()
    target_idx = None

    if isinstance(query_or_index, int):
        target_idx = query_or_index
    else:
        q = str(query_or_index).lower()
        if any(k in q for k in ("female", "zira", "friday", "girl", "woman", "lady")):
            for v in voices:
                if v["is_female"]:
                    target_idx = v["index"]
                    break
        elif any(k in q for k in ("male", "david", "jarvis", "boy", "man", "guy")):
            for v in voices:
                if not v["is_female"]:
                    target_idx = v["index"]
                    break
        else:
            for v in voices:
                if q in v["name"].lower() or q in v["alias"].lower():
                    target_idx = v["index"]
                    break

    if target_idx is None:
        cur_idx = hud_config.get("voice_index", 0)
        target_idx = (cur_idx + 1) % len(voices)

    return switch_voice_profile(target_idx, speak_confirm=speak_confirm, cmd_id=cmd_id)

def audition_voice(voice_index):
    voices = get_available_voices()
    if 0 <= voice_index < len(voices):
        v = voices[voice_index]
        sample = (
            "F.R.I.D.A.Y neural core active. All atmospheric, cognitive, and flight diagnostics ready for your command, sir."
            if v["is_female"] else
            "J.A.R.V.I.S tactical core active. All systems, sensors, and telemetry are functioning within nominal parameters, sir."
        )
        _tts_queue.put(("AUDITION_VOICE", voice_index, sample))


# ╔══════════════════════════════════════════════════════════════════╗
# ║  PERSISTENT TTS VOICE ENGINE (QUEUE DAEMON THREAD)               ║
# ╚══════════════════════════════════════════════════════════════════╝

_tts_queue = queue.Queue()
_tts_skip_flag = False
_tts_interrupt_event = threading.Event()
_current_command_id = 0
_command_lock = threading.Lock()
_active_speaker = None

def _safe_ui_update(fn):
    try:
        if "root" in globals() and root:
            root.after(0, fn)
    except Exception:
        pass

def stop_speaking(flush_queue=True):
    """
    Instantly halts any active speech output (SAPI, pyttsx3, WMP audio)
    and flushes pending sentences from previous commands so new commands
    can proceed immediately.
    """
    global _tts_skip_flag, _active_speaker
    _tts_skip_flag = True
    _tts_interrupt_event.set()
    _audio_stop_event.set()

    if _active_speaker:
        try:
            if _active_speaker[0] == "sapi":
                if _HAS_WIN32COM:
                    try:
                        pythoncom.CoInitialize()
                    except Exception:
                        pass
                # SVSFPurgeBeforeSpeak (2) purges pending and active audio immediately
                _active_speaker[1].Speak("", 2)
            elif _active_speaker[0] == "pyttsx3":
                _active_speaker[1].stop()
        except Exception:
            pass

    try:
        winsound.PlaySound(None, winsound.SND_PURGE)
    except Exception:
        pass

    if flush_queue:
        while not _tts_queue.empty():
            try:
                _tts_queue.get_nowait()
                _tts_queue.task_done()
            except Exception:
                break

    _anim["speaking"] = False

def terminate_previous_command(reason="Preempted by new user command"):
    """
    Instantly terminates any currently executing command, halts audio and TTS playback,
    clears pending typewriter streams and execution pipelines, and increments the
    command generation ID so all pending worker threads abort immediately.
    """
    global _current_command_id
    with _command_lock:
        _current_command_id += 1
        new_cmd_id = _current_command_id

    # 1. Instantly halt any TTS speech playback and purge pending sentences
    stop_speaking(flush_queue=True)

    # 2. Flush typewriter telemetry stream
    _stream_queue.clear()

    # 3. Reset animation & processing states
    _anim["processing"] = False
    _anim["speaking"] = False

    # 4. Telemetry logging if terminal exists
    if "terminal_feed_log" in globals():
        _safe_ui_update(lambda: terminal_feed_log("COMMAND", f"Preempted core #{new_cmd_id - 1}. Active core: #{new_cmd_id} ({reason})"))

    return new_cmd_id

def _tts_daemon_loop():
    global _tts_skip_flag, _active_speaker
    speaker = None

    def _apply_voice(spk, idx):
        if not spk: return
        try:
            if spk[0] == "sapi":
                v_coll = spk[1].GetVoices()
                if 0 <= idx < v_coll.Count:
                    spk[1].Voice = v_coll.Item(idx)
                    try:
                        spk[1].AllowAudioOutputFormatChangesOnNextSet = True
                        fmt = win32com.client.Dispatch("SAPI.SpAudioFormat")
                        fmt.Type = 22  # SAFT22kHz16BitMono
                        spk[1].AudioOutputStream.Format = fmt
                    except Exception:
                        pass
            elif spk[0] == "pyttsx3":
                p_v = spk[1].getProperty("voices")
                if 0 <= idx < len(p_v):
                    spk[1].setProperty("voice", p_v[idx].id)
        except Exception as ve:
            print("Voice apply note:", ve)

    def _wait_speech_done(spk, target_cmd_id=None):
        """
        Smoothly waits for speech synthesis completion using native Win32 kernel events.
        Releases the Python GIL during the wait, avoids COM mutex polling, and completely
        prevents audio DAC buffer underruns, stutter, and cracking artifacts.
        """
        if spk[0] == "sapi":
            try:
                h_event = spk[1].SpeakCompleteEvent()
            except Exception:
                h_event = None

            while True:
                if _HAS_WIN32EVENT and h_event:
                    rc = win32event.WaitForSingleObject(h_event, 50)
                    if rc == win32event.WAIT_OBJECT_0:
                        break
                else:
                    _time.sleep(0.05)
                    try:
                        if spk[1].Status.RunningState == 1:
                            break
                    except Exception:
                        if spk[1].WaitUntilDone(10):
                            break

                # Handle user interruption, skip, or command preemption
                if _tts_skip_flag or _tts_interrupt_event.is_set() or (target_cmd_id is not None and target_cmd_id < _current_command_id):
                    try:
                        spk[1].Speak("", 2)  # SVSFPurgeBeforeSpeak
                    except Exception:
                        pass
                    return False
            return True
        return True

    # Priority 1: Native Windows SAPI.SpVoice via win32com (direct C++ COM, no deadlocks)
    try:
        if _HAS_WIN32COM:
            pythoncom.CoInitialize()
            sapi_voice = win32com.client.Dispatch("SAPI.SpVoice")
            sapi_voice.Rate = 0
            sapi_voice.Volume = 100
            init_idx = hud_config.get("voice_index", 0)
            voices = sapi_voice.GetVoices()
            if 0 <= init_idx < voices.Count:
                sapi_voice.Voice = voices.Item(init_idx)
            try:
                sapi_voice.AllowAudioOutputFormatChangesOnNextSet = True
                fmt = win32com.client.Dispatch("SAPI.SpAudioFormat")
                fmt.Type = 22  # SAFT22kHz16BitMono
                sapi_voice.AudioOutputStream.Format = fmt
            except Exception:
                pass
            speaker = ("sapi", sapi_voice)
            _active_speaker = speaker
            print(f"J.A.R.V.I.S Native SAPI Speech Engine Online. Active: {sapi_voice.Voice.GetDescription()}")
    except Exception as se:
        print("Native SAPI initialization note:", se)

    # Priority 2: pyttsx3 fallback
    if not speaker:
        try:
            ctypes.windll.ole32.CoInitialize(None)
        except Exception:
            pass
        try:
            pyttsx_eng = pyttsx3.init()
            pyttsx_eng.setProperty("rate", hud_config.get("voice_rate", 175))
            pyttsx_eng.setProperty("volume", 1.0)
            p_voices = pyttsx_eng.getProperty("voices")
            init_idx = hud_config.get("voice_index", 0)
            if 0 <= init_idx < len(p_voices):
                pyttsx_eng.setProperty("voice", p_voices[init_idx].id)
            speaker = ("pyttsx3", pyttsx_eng)
            _active_speaker = speaker
            print("J.A.R.V.I.S pyttsx3 Speech Engine Online.")
        except Exception as pe:
            print("pyttsx3 fallback error:", pe)

    while True:
        try:
            item = _tts_queue.get()
            if item is None:
                break

            cmd_id = None
            if isinstance(item, tuple) and len(item) == 3 and item[0] == "SPEAK":
                cmd_id, text = item[1], item[2]
            elif isinstance(item, tuple) and item[0] == "SET_VOICE":
                _apply_voice(speaker, item[1])
                _tts_queue.task_done()
                continue
            elif isinstance(item, tuple) and item[0] == "AUDITION_VOICE":
                aud_idx, aud_text = item[1], item[2]
                saved_idx = hud_config.get("voice_index", 0)
                _apply_voice(speaker, aud_idx)
                _safe_ui_update(lambda: set_status("◈  AUDITIONING VOICE PROFILE...", C.get("cyan_br", "#40ffff")))
                try:
                    winsound.PlaySound(None, winsound.SND_PURGE)
                except Exception:
                    pass
                try:
                    if speaker[0] == "sapi":
                        speaker[1].Speak(aud_text, 17)
                        _wait_speech_done(speaker)
                    elif speaker[0] == "pyttsx3":
                        speaker[1].say(aud_text)
                        speaker[1].runAndWait()
                except Exception as ae:
                    print("Audition speak error:", ae)
                _apply_voice(speaker, saved_idx)
                _safe_ui_update(lambda: set_status("◎  SYSTEMS NOMINAL", C.get("cyan", "#00e5ff")))
                _tts_queue.task_done()
                continue
            elif isinstance(item, tuple) and item[0] == "AUDITION_ELEVENLABS":
                vid = item[1]
                audition_elevenlabs_voice(vid)
                _tts_queue.task_done()
                continue
            elif isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], int):
                cmd_id, text = item[0], item[1]
            else:
                text = item

            # Preemption check: if newer command has been dispatched, drop this item
            if cmd_id is not None and cmd_id < _current_command_id:
                _tts_queue.task_done()
                continue

            if not text or not speaker:
                _tts_queue.task_done()
                continue

            if _tts_interrupt_event.is_set() or _tts_skip_flag:
                _tts_queue.task_done()
                continue

            _anim["speaking"] = True

            # Clean and expand symbols so the complete result is spoken naturally
            cleaned_text = clean_for_speech(text)

            # Check if ElevenLabs Neural Cloud TTS is active
            tts_mode = hud_config.get("tts_engine", "sapi")
            el_key = hud_config.get("elevenlabs_api_key", "").strip()
            el_voice = hud_config.get("elevenlabs_voice_id", "IRHApOXLvnW57QJPQH2P")
            if tts_mode == "elevenlabs" and el_key:
                if cmd_id is not None and cmd_id < _current_command_id:
                    _tts_queue.task_done()
                    continue
                _safe_ui_update(lambda: set_status("◈  ELEVENLABS NEURAL TTS...", C.get("cyan_br", "#40ffff")))
                succ, el_audio, err = synthesize_elevenlabs_speech(cleaned_text, el_voice, el_key)
                if _tts_interrupt_event.is_set() or (cmd_id is not None and cmd_id < _current_command_id):
                    _tts_queue.task_done()
                    continue
                if succ and el_audio:
                    play_audio_file(el_audio, async_play=False)
                    if _tts_queue.empty() and not _anim.get("processing", False):
                        _anim["speaking"] = False
                        _safe_ui_update(lambda: set_status("◎  SYSTEMS NOMINAL", C.get("cyan", "#00e5ff")))
                    _tts_queue.task_done()
                    continue
                else:
                    terminal_feed_log("TTS", f"ElevenLabs fallback to SAPI: {err}")

            # Dynamic rate adjustment (mapped to prevent diphone chopping and phase cracking)
            try:
                rate_val = hud_config.get("voice_rate", 175)
                if speaker[0] == "sapi":
                    # Nominal rate 165-195 WPM maps to Rate 0 (natural diphone delivery without cracking)
                    if 165 <= rate_val <= 195:
                        speaker[1].Rate = 0
                    elif rate_val > 195:
                        speaker[1].Rate = max(1, min(2, int((rate_val - 195) / 25) + 1))
                    else:
                        speaker[1].Rate = max(-2, min(-1, int((rate_val - 165) / 25) - 1))
                elif speaker[0] == "pyttsx3":
                    speaker[1].setProperty("rate", rate_val)
            except Exception:
                pass

            has_devanagari = bool(re.search(r'[\u0900-\u097F]', cleaned_text))

            if not has_devanagari:
                # ── Rock-Solid Continuous Speech Stream (English / Latin Script) ──
                # Unified audio stream prevents sound card DAC re-initialization pops,
                # eliminates clicks/cracks between sentences, and maintains natural prosody.
                snippet = cleaned_text[:38].replace("\n", " ").strip()
                _safe_ui_update(lambda sn=snippet: set_status(f"◈  SPEAKING: {sn}...", C.get("cyan_br", "#40ffff")))

                # Purge any active winsound playback so SFX does not collide with speech
                try:
                    winsound.PlaySound(None, winsound.SND_PURGE)
                except Exception:
                    pass

                # Brief 50ms audio buffer stabilization to prevent DAC underruns
                _time.sleep(0.05)

                try:
                    if speaker[0] == "sapi":
                        # Flag 1 = SVSFlagsAsync, Flag 16 = SVSFIsNotXML -> 17
                        # Prevents SAPI from misinterpreting <, >, & as SSML tags which caused mid-sentence breaks
                        speaker[1].Speak(cleaned_text, 17)
                        _wait_speech_done(speaker, cmd_id)
                    elif speaker[0] == "pyttsx3":
                        speaker[1].say(cleaned_text)
                        speaker[1].runAndWait()
                except Exception as tts_err:
                    print("TTS playback error:", tts_err)

            else:
                # ── Bilingual Hindi/English Adaptive Sentence Pipeline ──
                # Devanagari text is synthesized via Google Translate TTS (split into <= 180 char chunks)
                sentences = [s.strip() for s in re.split(r'(?<=[.!?।])\s+', cleaned_text) if s.strip()]
                if not sentences:
                    sentences = [cleaned_text]

                for idx, s in enumerate(sentences):
                    if _tts_skip_flag or _tts_interrupt_event.is_set() or (cmd_id is not None and cmd_id < _current_command_id):
                        break
                    if not s:
                        continue

                    snippet = s[:36].replace("\n", " ")
                    _safe_ui_update(lambda sn=snippet: set_status(f"◈  SPEAKING: {sn}...", C.get("cyan_br", "#40ffff")))

                    # Native Hindi speech synthesis for Devanagari text
                    if re.search(r'[\u0900-\u097F]', s):
                        succ_hi, hi_audio, err_hi = synthesize_hindi_speech(s)
                        if succ_hi and hi_audio:
                            play_audio_file(hi_audio, async_play=False)
                            continue

                    try:
                        if speaker[0] == "sapi":
                            speaker[1].Speak(s, 17)
                            if not _wait_speech_done(speaker, cmd_id):
                                break
                        elif speaker[0] == "pyttsx3":
                            speaker[1].say(s)
                            speaker[1].runAndWait()
                    except Exception as tts_err:
                        print("TTS sentence playback error:", tts_err)

            _tts_queue.task_done()

            # When queue is empty, return status to nominal
            if _tts_queue.empty() and not _anim.get("processing", False):
                _anim["speaking"] = False
                _safe_ui_update(lambda: set_status("◎  SYSTEMS NOMINAL", C.get("cyan", "#00e5ff")))

        except Exception as loop_err:
            print("TTS daemon loop error:", loop_err)
            _anim["speaking"] = False

# Launch persistent singleton TTS daemon thread
threading.Thread(target=_tts_daemon_loop, daemon=True).start()

def speak(text, interrupt=False, block=False, cmd_id=None):
    global _tts_skip_flag
    if not text:
        return

    matrix_push_token("VOX:SYNTH")
    for _w in str(text).split()[:4]:
        if len(_w) > 2:
            matrix_push_token(_w)

    # If this speech belongs to an older preempted command, drop it immediately
    if cmd_id is not None and cmd_id < _current_command_id:
        return

    if interrupt:
        stop_speaking(flush_queue=True)

    _tts_interrupt_event.clear()
    _tts_skip_flag = False

    effective_cmd_id = cmd_id if cmd_id is not None else _current_command_id
    _tts_queue.put(("SPEAK", effective_cmd_id, text))
    if block:
        _tts_queue.join()



# ╔══════════════════════════════════════════════════════════════════╗
# ║  VOICE RECOGNITION PIPELINE (BILINGUAL HINDI & ENGLISH)          ║
# ╚══════════════════════════════════════════════════════════════════╝

def is_devanagari(text):
    return bool(re.search(r'[\u0900-\u097F]', str(text)))

HINDI_CITY_MAP = {
    "दिल्ली": "Delhi",
    "नई दिल्ली": "New Delhi",
    "मुंबई": "Mumbai",
    "कोलकाता": "Kolkata",
    "चेन्नई": "Chennai",
    "बेंगलुरु": "Bengaluru",
    "बैंगलोर": "Bengaluru",
    "हैदराबाद": "Hyderabad",
    "पुणे": "Pune",
    "जयपुर": "Jaipur",
    "लखनऊ": "Lucknow",
    "कानपुर": "Kanpur",
    "वाराणसी": "Varanasi",
    "बनारस": "Varanasi",
    "आगरा": "Agra",
    "पटना": "Patna",
    "भोपाल": "Bhopal",
    "इंदौर": "Indore",
    "अहमदाबाद": "Ahmedabad",
    "सूरत": "Surat",
    "चंडीगढ़": "Chandigarh",
    "लंदन": "London",
    "पेरिस": "Paris",
    "न्यूयॉर्क": "New York",
    "टोक्यो": "Tokyo",
    "दुबई": "Dubai",
    "उत्तर प्रदेश": "Uttar Pradesh, India",
    "भारत": "India",
}

HINDI_PLATFORMS = {
    "गूगल": "google",
    "यूट्यूब": "youtube",
    "विकिपीडिया": "wikipedia",
    "गिटहब": "github",
    "फेसबुक": "facebook",
    "इंस्टाग्राम": "instagram",
    "ट्विटर": "twitter",
    "लिंक्डइन": "linkedin",
    "अमेज़न": "amazon",
    "फ्लिपकार्ट": "flipkart",
    "रेडिट": "reddit",
    "नेटफ्लिक्स": "netflix",
    "जीमेल": "gmail",
    "व्हाट्सएप": "whatsapp",
    "हॉटस्टार": "hotstar",
    "स्पॉटिफ़ाई": "spotify",
}

HINDI_CONVERSATIONAL_INTENTS = {
    r"^(?:नमस्ते|नमस्कार|प्रणाम|हैलो|हाय|शुभ\s*(?:प्रभात|संध्या|दोपहर)|namaste|namaskar|pranam|shubh\s+prabhat)(?:\s|$|\b|[?!.,])":
        "नमस्ते महोदय! J.A.R.V.I.S के सभी न्यूरल कोर और सेंसर्स सक्रिय हैं। आज मैं आपकी क्या सेवा कर सकता हूँ?",
    r"^(?:तुम\s*कौन\s*हो|आप\s*कौन\s*हैं|तुम्हारा\s*नाम\s*क्या\s*है|अपना\s*परिचय\s*दो|तुम\s*क्या\s*हो|tum\s+kaun\s+ho|aap\s+kaun\s+hai(?:n)?|tumhara\s+naam\s+kya\s+hai|apna\s+parichay\s+do)(?:\s|$|\b|[?!.,])":
        "मैं J.A.R.V.I.S हूँ, आपका होलोग्राफिक एआई पर्सनल असिस्टेंट। मैं वेब इंटेलिजेंस, मौसम, ताज़ा समाचार, यूट्यूब मीडिया और सिस्टम कंट्रोल्स में आपकी पूरी सहायता कर सकता हूँ।",
    r"^(?:(?:आप|तुम)?\s*(?:कैसे|कैसी)\s*(?:हो|हैं)|क्या\s*हाल\s*है|सब\s*ठीक\s*है|हाल\s*चाल\s*बताओ|(?:aap\s+|tum\s+)?kaise\s+(?:ho|hai(?:n)?)|kya\s+haal\s+hai|sab\s+theek\s+hai)(?:\s|$|\b|[?!.,])":
        "मेरे सभी न्यूरल कोर और सेंसर्स पूरी क्षमता से काम कर रहे हैं, महोदय। आज का क्या आदेश है?",
    r"^(?:तुम\s*क्या\s*कर\s*सकते\s*हो|क्या\s*काम\s*कर\s*सकते\s*हो|मदद|सहायता|फीचर्स\s*बताओ|कमांड्स|tum\s+kya\s+kar\s+sakte\s+ho|kya\s+kya\s+kar\s+sakte\s+ho|help\s+karo)(?:\s|$|\b|[?!.,])":
        "मैं हिंदी और अंग्रेजी दोनों भाषाओं में आपके आदेश समझ सकता हूँ। मैं मौसम की लाइव जानकारी, ताज़ा समाचार, यूट्यूब पर गाने बजाना, गूगल या विकिपीडिया पर खोजना और वॉल्यूम व ब्राइटनेस बदलना कर सकता हूँ।",
    r"^(?:धन्यवाद|शुक्रिया|बहुत\s*बढ़िया|शाबाश|बहुत\s*अच्छा|थैंक\s*यू|dhanyawad|shukriya|bahut\s+badhiya|shabash)(?:\s|$|\b|[?!.,])":
        "आपका बहुत-बहुत स्वागत है, महोदय! आपके अगले निर्देश के लिए तत्पर हूँ।",
    r"^(?:तुम्हें\s*किसने\s*बनाया|तुम्हारा\s*निर्माता\s*कौन\s*है|किसने\s*बनाया\s*है\s*तुम्हें|tumhe\s+kisne\s+banaya|tumhara\s+creator\s+kaun\s+hai)(?:\s|$|\b|[?!.,])":
        "मुझे टोनी स्टार्क के J.A.R.V.I.S से प्रेरित होकर आपकी सेवा और वर्कस्टेशन सहायता के लिए एक उन्नत एआई असिस्टेंट के रूप में विकसित किया गया है।",
}

def is_hindi_intent_or_phrase(text):
    t = str(text).strip().lower()
    if is_devanagari(t):
        return True
    hindi_keywords = {
        "namaste", "namaskar", "pranam", "kaise", "samay", "kya", "mausam", "batao", "chalao", "bajao",
        "kholo", "aawaz", "badhao", "shant", "shukriya", "dhanyawad", "samachar",
        "khabar", "roshni", "tumhara", "parichay", "tum", "kaun", "aap", "ho", "hai",
        "hain", "haal", "theek", "baje", "karo", "suno", "gaana", "gana", "geet",
        "tapman", "samay", "waqt", "kitne"
    }
    words = re.findall(r'\b\w+\b', t)
    return any(w in hindi_keywords for w in words)

def is_english_intent_or_phrase(text):
    t = str(text).strip().lower()
    en_keywords = [
        "what", "who", "time", "weather", "play", "open", "volume", "brightness",
        "news", "search", "increase", "decrease", "mute", "hello", "how", "switch"
    ]
    return any(w in t for w in en_keywords)

def normalize_and_boost_audio(audio, target_peak=26000, max_gain=6.5):
    """
    Advanced Far-Field Digital Audio Pre-Amp, DC-Offset Removal, & Automatic Gain Control (AGC):
    1. Eliminates microphone DC bias offset (zero-centering the waveform).
    2. Calculates true RMS acoustic energy and updates _anim["core_audio_level"] in real-time.
    3. Normalizes and amplifies quiet, low-sound, or distant voice commands with a soft-knee limiter.
    4. Guards against noise-floor amplification on absolute silence.
    """
    if audio is None:
        return audio
    try:
        raw_frames = audio.frame_data
        width = audio.sample_width
        rate = audio.sample_rate
        if width != 2 or not raw_frames:
            return audio

        count = len(raw_frames) // 2
        if count == 0:
            return audio

        samples = list(struct.unpack(f"<{count}h", raw_frames))

        # 1. DC Offset Removal (Centering the baseline)
        dc_bias = sum(samples) // count
        if abs(dc_bias) > 25:
            samples = [s - dc_bias for s in samples]

        # 2. Peak and RMS Level Computation
        peak = max(abs(s) for s in samples) if samples else 0
        step = max(1, count // 2000)
        sum_sq = sum(s * s for s in samples[::step])
        approx_rms = math.sqrt(sum_sq / max(1, count // step)) if samples else 0

        # Update core acoustic energy for visual waveform/matrix reactivity
        _anim["core_audio_level"] = min(1.0, approx_rms / 12000.0)

        # 3. Guard against amplifying silence/noise-floor (< 80) or already loud audio (peak >= 18000)
        if peak < 80 or peak >= 18000:
            if abs(dc_bias) > 25:
                cleaned_frames = struct.pack(f"<{count}h", *[max(-32767, min(32767, s)) for s in samples])
                return sr.AudioData(cleaned_frames, rate, width)
            return audio

        # 4. Soft-Knee Dynamic Gain calculation
        gain = min(max_gain, float(target_peak) / max(float(peak), 200.0))
        if gain <= 1.05:
            return audio

        amplified = [max(-32767, min(32767, int(s * gain))) for s in samples]
        amplified_frames = struct.pack(f"<{count}h", *amplified)
        return sr.AudioData(amplified_frames, rate, width)
    except Exception:
        return audio

_speech_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4, thread_name_prefix="speech_race")

def recognize_speech_multilingual(recognizer, audio):
    """
    Multilingual speech recognition engine with concurrent English/Hindi analysis,
    robust 5.0s network timeout handling, and smart en-US fallback.
    """
    audio = normalize_and_boost_audio(audio)
    lang_mode = hud_config.get("input_language", "auto").lower()

    if lang_mode == "en":
        try:
            return recognizer.recognize_google(audio, language="en-IN").strip()
        except Exception:
            return recognizer.recognize_google(audio, language="en-US").strip()

    if lang_mode == "hi":
        return recognizer.recognize_google(audio, language="hi-IN").strip()

    # Dual Auto Mode: Concurrent race with early-exit heuristics
    def _rec(lang_code):
        try:
            res = recognizer.recognize_google(audio, language=lang_code)
            return (lang_code, res.strip() if res else None)
        except Exception:
            return (lang_code, None)

    results = {}
    futures = [_speech_executor.submit(_rec, "en-IN"), _speech_executor.submit(_rec, "hi-IN")]
    try:
        for future in concurrent.futures.as_completed(futures, timeout=5.0):
            try:
                lang, text = future.result()
                if text:
                    results[lang] = text
                    # Fast-exit heuristic 1: Hindi intent or Devanagari script
                    if lang == "hi-IN" and (is_devanagari(text) or is_hindi_intent_or_phrase(text)):
                        return text
                    # Fast-exit heuristic 2: English command or conversational phrase
                    if lang == "en-IN" and is_english_intent_or_phrase(text):
                        return text
            except Exception:
                pass
    except concurrent.futures.TimeoutError:
        pass

    res_en = results.get("en-IN")
    res_hi = results.get("hi-IN")

    if res_hi and not res_en:
        return res_hi
    if res_en and not res_hi:
        return res_en
    if res_hi and res_en:
        if is_devanagari(res_hi) and is_hindi_intent_or_phrase(res_hi):
            return res_hi
        if is_english_intent_or_phrase(res_en):
            return res_en
        return res_hi if is_devanagari(res_hi) else res_en

    # Fallback to en-US if dual race produced no result
    try:
        res_us = recognizer.recognize_google(audio, language="en-US").strip()
        if res_us:
            return res_us
    except Exception:
        pass

    raise sr.UnknownValueError("Speech pattern unrecognized across English and Hindi feeds.")

def normalize_voice_command(raw_query):
    """
    Intelligent acoustic command sanitizer and intent normalizer:
    - Strips wake words and conversational filler ('Jarvis', 'Hey Jarvis', 'Please', 'Can you', 'Could you').
    - Strips spoken punctuation artifacts ('question mark', 'full stop', 'comma', 'exclamation mark').
    - Translates common conversational prefixes into direct actionable directives.
    - Preserves Devanagari and Latin Hindi commands with multi-pass stripping.
    """
    if not raw_query:
        return ""
    q = str(raw_query).strip()

    # 1. Wake word stripping (multi-pass for repeated wake words)
    for _ in range(2):
        is_wake, is_standalone, cleaned, is_hi = parse_wake_word_query(q)
        if is_wake and not is_standalone and cleaned:
            q = cleaned

    # 2. Conversational padding prefixes (bilingual English + Hindi)
    padding_prefixes = [
        r"^(?:please|plz|kindly)\s+",
        r"^(?:tell\s+me\s+)\b",
        r"^(?:can\s+you\s+(?:please\s+)?(?:tell\s+me\s+)?)\b",
        r"^(?:could\s+you\s+(?:please\s+)?(?:tell\s+me\s+)?)\b",
        r"^(?:would\s+you\s+(?:please\s+)?(?:tell\s+me\s+)?)\b",
        r"^(?:will\s+you\s+(?:please\s+)?(?:tell\s+me\s+)?)\b",
        r"^(?:i\s+want\s+you\s+to\s+)\b",
        r"^(?:i\s+need\s+you\s+to\s+)\b",
        r"^(?:just\s+)\b",
        r"^(?:kripya|zara|kripaya)\s+",
        r"^(?:kya\s+tum\s+(?:mujhe\s+)?(?:bata\s+sakte\s+ho)?)\b",
        r"^(?:mujhe\s+batao\s+)\b",
        r"^(?:कृपया\s+(?:मुझे\s+)?(?:बताओ\s+|बताइए\s+)?)\b",
        r"^(?:कृपया\s+)",
        r"^(?:जरा\s+(?:बताओ\s+|बताइए\s+)?)\b",
        r"^(?:मुझे\s+बताओ\s+)\b",
    ]
    # Multi-pass strip to handle combinations like "Please tell me..." or "Could you please tell me..."
    for _ in range(3):
        prev = q
        for pattern in padding_prefixes:
            q = re.sub(pattern, "", q, flags=re.IGNORECASE).strip()
        if q == prev:
            break

    # 3. Strip trailing politeness / punctuation words
    trailing_patterns = [
        r"\b(?:please|thank\s+you|thanks|kripya|dhanyawad|shukriya|धन्यवाद|शुक्रिया)$",
        r"\b(?:question\s+mark|full\s+stop|period|exclamation\s+mark)$",
    ]
    for pattern in trailing_patterns:
        q = re.sub(pattern, "", q, flags=re.IGNORECASE).strip()

    # 4. Remove leading/trailing stray punctuation marks
    q = q.strip(" ,.?!;:-\"' \t\n\r")
    return q or str(raw_query).strip()

_mic_lock = threading.Lock()
_wake_word_running = True
_wake_word_thread = None
_calibrated_energy_threshold = None
_voice_capture_lock = threading.Lock()
_is_voice_capturing = False
_manual_capture_active = threading.Event()
_mic_abort_requested = threading.Event()
_last_mic_click_time = 0.0

def _precalibrate_microphone():
    global _calibrated_energy_threshold
    try:
        with _mic_lock:
            rec = sr.Recognizer()
            with sr.Microphone() as source:
                rec.adjust_for_ambient_noise(source, duration=0.20)
                # Far-field sensitive clamp: min 90, max 260.
                # In noisy room (fans/AC), never let threshold rise above 260 so quiet voices are heard.
                # In quiet room, allows down to 90 for ultra-soft speech detection.
                _calibrated_energy_threshold = max(90, min(260, rec.energy_threshold))
                print(f"J.A.R.V.I.S Audio Array Pre-Calibrated: Energy Threshold = {_calibrated_energy_threshold:.1f}")
    except Exception as e:
        print("Microphone pre-calibration note:", e)

def parse_wake_word_query(raw_query):
    """
    Checks if a query contains 'jarvis' as a wake word.
    Returns (is_wake, is_standalone, cleaned_query, is_hindi)
    """
    if not raw_query:
        return False, False, "", False
    q = raw_query.strip()
    is_hi = bool(re.search(r'[\u0900-\u097F]', q)) or any(w in q.lower() for w in ('suno', 'bhai', 'shri'))
    wake_pattern = r'^(?:hey\s+|ok\s+|hello\s+|hi\s+|listen\s+|suno\s+|call\s+|wake\s+up\s+|wake\s+|activate\s+|हे\s+|सुनो\s+)?(?:jarvis|जार्विस)\b[\s,:!\-]*'
    m = re.search(wake_pattern, q, flags=re.IGNORECASE)
    if m:
        cleaned = q[m.end():].strip()
        is_standalone = len(cleaned) == 0 or cleaned.lower() in ("wake up", "are you there", "listen to me", "sun rahe ho", "kaha ho", "active", "online", "please")
        return True, is_standalone, cleaned, is_hi
    if q.lower() in ('jarvis', 'hey jarvis', 'ok jarvis', 'hello jarvis', 'hi jarvis', 'call jarvis', 'wake up jarvis', 'जार्विस', 'हे जार्विस', 'सुनो जार्विस'):
        return True, True, "", is_hi
    return False, False, q, is_hi

_wake_greeting_active = False

def activate_wake_greeting(is_hindi=False):
    """
    Terminates any previously running command, greets with 'Yes sir, how do I help you?'
    and immediately activates voice command capture so the user can speak hands-free.
    """
    global _wake_greeting_active
    # Instantly terminate any running or speaking previous command!
    cmd_id = terminate_previous_command(reason="Wake-word calling ('Jarvis')")

    def _run():
        global _wake_greeting_active
        _wake_greeting_active = True
        try:
            trigger_ripple()
            play_sfx("sonar")
            greeting = "हाँ महोदय, मैं आपकी क्या सहायता कर सकता हूँ?" if is_hindi else "Yes sir, how do I help you?"
            _safe_ui_update(lambda: terminal_feed_log("WAKE WORD", f"JARVIS activated. Greeting: '{greeting}'"))
            _safe_ui_update(lambda: set_status("◉  WAKE ACTIVATED // YES SIR", C["cyan_br"]))
            # Speak greeting synchronously in this worker thread using new cmd_id
            speak(greeting, block=True, cmd_id=cmd_id)
        finally:
            _wake_greeting_active = False

        # If not preempted while speaking greeting, immediately start voice command capture
        if cmd_id == _current_command_id:
            run_mic_capture_async()

    threading.Thread(target=_run, daemon=True).start()

def _wake_word_daemon():
    rec = sr.Recognizer()
    rec.energy_threshold = 200        # Far-field sensitive base threshold
    rec.dynamic_energy_threshold = True
    rec.dynamic_energy_ratio = 1.15   # Sensitive trigger: 15% above noise floor
    rec.dynamic_energy_adjustment_damping = 0.10
    rec.pause_threshold = 0.28        # Ultra-fast wake word silence detection
    rec.non_speaking_duration = 0.18   # Quick release
    rec.phrase_threshold = 0.12        # Catch brief "Jarvis" onset in 120ms

    while _wake_word_running:
        if not hud_config.get("wake_word_enabled", True):
            _time.sleep(1.0)
            continue
        if not _anim.get("boot_done", False):
            _time.sleep(0.5)
            continue
        # Pause wake listening if manual voice capture is active, mic is listening, or wake greeting is playing
        if _is_voice_capturing or _manual_capture_active.is_set() or _anim.get("listening") or _wake_greeting_active:
            _time.sleep(0.15)
            continue

        acquired = _mic_lock.acquire(blocking=False)
        if not acquired:
            _time.sleep(0.20)
            continue

        audio = None
        try:
            if _is_voice_capturing or _manual_capture_active.is_set():
                audio = None
            else:
                with sr.Microphone() as source:
                    # Instant yield hook: if user clicks Start Listening, abort immediately within ~60ms
                    orig_read = source.stream.read
                    def _wake_read(size):
                        if _is_voice_capturing or _manual_capture_active.is_set():
                            raise sr.WaitTimeoutError("Yielding mic to manual voice capture")
                        return orig_read(size)
                    source.stream.read = _wake_read

                    # Maintain calibrated sensitivity without running blocking adjust_for_ambient_noise on every tick
                    if _calibrated_energy_threshold is not None:
                        rec.energy_threshold = min(240, _calibrated_energy_threshold)
                    audio = rec.listen(source, timeout=0.9, phrase_time_limit=2.5)
        except sr.WaitTimeoutError:
            audio = None
        except Exception:
            audio = None
        finally:
            _mic_lock.release()

        if audio is None or not _wake_word_running:
            continue
        if not hud_config.get("wake_word_enabled", True):
            continue
        if _is_voice_capturing or _manual_capture_active.is_set() or _anim.get("listening") or _wake_greeting_active:
            continue

        # Dynamic Far-Field AGC Pre-Amp for low-sound and distant wake-word calling
        audio = normalize_and_boost_audio(audio)

        phrase = ""
        try:
            phrase = rec.recognize_google(audio, language="en-IN").strip().lower()
        except Exception:
            try:
                phrase = rec.recognize_google(audio, language="hi-IN").strip()
            except Exception:
                phrase = ""

        if phrase:
            is_wake, is_standalone, cleaned, is_hi = parse_wake_word_query(phrase)
            if is_wake:
                print(f"[WAKE WORD DETECTED]: '{phrase}' -> standalone={is_standalone}, cleaned='{cleaned}'")
                if is_standalone:
                    activate_wake_greeting(is_hindi=is_hi)
                elif cleaned:
                    play_sfx("sonar")
                    trigger_ripple()
                    _safe_ui_update(lambda c=cleaned: dispatch_command(c))

def take_command():
    global _calibrated_energy_threshold
    recognizer = sr.Recognizer()
    # High-speed responsive & far-field sensitive acoustic tuning for single-take capture
    recognizer.pause_threshold = 0.80        # Generous 800ms cut-off (prevents premature cut-offs when pausing naturally)
    recognizer.non_speaking_duration = 0.40  # Retains 400ms leading/trailing audio to preserve initial syllables
    recognizer.phrase_threshold = 0.15       # Immediate speech onset detection (150ms)
    recognizer.dynamic_energy_threshold = True
    recognizer.dynamic_energy_ratio = 1.15   # Trigger on low-sound speech (15% above ambient)
    recognizer.dynamic_energy_adjustment_damping = 0.12

    # Configurable acoustic listening timeout and phrase duration limit
    v_timeout = float(hud_config.get("voice_input_timeout", 10.0))
    p_limit = float(hud_config.get("voice_phrase_time_limit", 20.0))

    with _mic_lock:
        with sr.Microphone() as source:
            # Immediate responsive abort hook: if user clicks Stop Listening, exit immediately
            orig_read = source.stream.read
            def _manual_read(size):
                if _mic_abort_requested.is_set():
                    raise sr.WaitTimeoutError("Manual mic capture cancelled by user")
                return orig_read(size)
            source.stream.read = _manual_read

            # Instantly apply calibrated energy threshold without blocking 80ms or measuring speaker echo
            if _calibrated_energy_threshold is not None:
                recognizer.energy_threshold = max(90, min(240, _calibrated_energy_threshold))
            else:
                recognizer.energy_threshold = 160

            # UI indicates LIVE listening precisely when audio stream is active and recording
            _safe_ui_update(lambda: set_status(f"◉  LISTENING... [SPEAK YOUR COMMAND ({int(v_timeout)}s)]", C["green"]))
            _safe_ui_update(lambda: set_substatus("Audio stream online. Speak your command now."))
            _anim["listening"] = True
            try:
                audio = recognizer.listen(source, timeout=v_timeout, phrase_time_limit=p_limit)
                _safe_ui_update(lambda: set_status("◈  ANALYZING NEURAL SPEECH...", C["amber"]))
                _safe_ui_update(lambda: set_substatus("Converting audio pattern to neural command..."))
                _anim["listening"] = False
                _anim["processing"] = True

                # Apply Far-Field AGC Pre-Amp for low-sound and distance speech
                audio = normalize_and_boost_audio(audio)
                query = recognize_speech_multilingual(recognizer, audio)
                if query:
                    clean_query = query.strip()
                    _safe_ui_update(lambda: set_status(f"✓  HEARD: \"{clean_query[:28]}\"", C["cyan_br"]))
                    matrix_push_token("VOX:RECOGNIZED")
                    for w in clean_query.split()[:3]:
                        matrix_push_token(w)
                    return clean_query
                return None
            except sr.WaitTimeoutError:
                if _mic_abort_requested.is_set():
                    _safe_ui_update(lambda: set_status("◎  VOICE INPUT STOPPED", C["cyan_dim"]))
                    _safe_ui_update(lambda: set_substatus("Voice command capture cancelled by user."))
                else:
                    play_sfx("alert")
                    _safe_ui_update(lambda: set_status("◌  NO SPEECH DETECTED // TAP MIC TO RETRY", C["red"]))
                    _safe_ui_update(lambda: set_substatus(f"Listening timed out after {int(v_timeout)}s. Click Start Listening or say 'Hey Jarvis'."))
                return None
            except sr.UnknownValueError:
                play_sfx("alert")
                _safe_ui_update(lambda: set_status("◌  SPEECH UNRECOGNIZED // PLEASE REPEAT", C["red"]))
                _safe_ui_update(lambda: set_substatus("Could not understand voice pattern. Try speaking closer to microphone."))
                return None
            except sr.RequestError as req_err:
                play_sfx("alert")
                print("Speech API Network Request Error:", req_err)
                _safe_ui_update(lambda: set_status("◌  SPEECH NETWORK TIMEOUT", C["amber"]))
                _safe_ui_update(lambda: set_substatus("Google Speech API network request timed out."))
                return None
            except Exception as e:
                print("Microphone/API Error:", e)
                play_sfx("alert")
                _safe_ui_update(lambda: set_status("◌  AUDIO INPUT FAULT", C["red"]))
                return None
            finally:
                _anim["listening"] = False


# ╔══════════════════════════════════════════════════════════════════╗
# ║  AI PERSONAL ASSISTANT & WEB INTELLIGENCE SEARCH ENGINE          ║
# ╚══════════════════════════════════════════════════════════════════╝

CONVERSATIONAL_INTENTS = {
    r"^(?:hello|hi|hey|greetings|good\s+(?:morning|afternoon|evening))\b": 
        "Greetings, sir. All quantum HUD systems are online and standing by for your command.",
    r"^(?:who\s+are\s+you|what\s+is\s+your\s+name|introduce\s+yourself)\b": 
        "I am J.A.R.V.I.S, your holographic AI personal assistant. I can search the web for live intelligence, report meteorological forecasts, stream breaking news, play YouTube media, and control system hardware.",
    r"^(?:how\s+are\s+you|how\s+are\s+things|status\s+check)\b": 
        "All neural cores and telemetry sensors are operating at peak efficiency, sir. How may I assist you today?",
    r"^(?:what\s+can\s+you\s+do|help|show\s+features)\b": 
        "I can answer questions by searching live web intelligence, stream breaking news headlines, report weather forecasts, autoplay YouTube videos, and adjust system volume and brightness in both English and Hindi.",
    r"^(?:thank\s+you|thanks|great\s+job|well\s+done)\b": 
        "You are very welcome, sir. Standing by for your next instruction.",
    r"^(?:who\s+created\s+you|who\s+made\s+you|who\s+is\s+your\s+creator)\b":
        "I was developed as a holographic AI voice assistant inspired by Tony Stark's J.A.R.V.I.S to assist you with intelligent workstation workflows.",
}

def check_conversational_query(query):
    q = query.strip().lower()
    for pattern, response in HINDI_CONVERSATIONAL_INTENTS.items():
        if re.search(pattern, q, re.IGNORECASE):
            return response
    for pattern, response in CONVERSATIONAL_INTENTS.items():
        if re.search(pattern, q, re.IGNORECASE):
            return response
    return None

def clean_search_query(query):
    patterns = [
        r"^(?:who\s+is|what\s+is|tell\s+me\s+about|explain|define|search\s+internet\s+for|search\s+web\s+for|search\s+google\s+for|search\s+for|search)\s+",
        r"^(?:क्या\s+है|कौन\s+है|कहाँ\s+है|के\s+बारे\s+में\s+बताओ|बताओ|जानकारी\s+दो)\s+",
        r"\s+(?:on\s+google|in\s+google|on\s+wikipedia|in\s+wikipedia|on\s+the\s+web|on\s+internet)$",
        r"\s+(?:क्या\s+है|कौन\s+है|कहाँ\s+है|के\s+बारे\s+में\s+बताओ|बताओ)$",
    ]
    cleaned = query.strip()
    for p in patterns:
        cleaned = re.sub(p, "", cleaned, flags=re.IGNORECASE).strip()
    return cleaned if cleaned else query.strip()

def get_acronym(text):
    words = re.findall(r'[a-zA-Z0-9]+', text)
    return ''.join(w[0] for w in words).upper()

def generate_speech_summary(text, max_chars=320, is_hindi=False):
    t = re.sub(r'```[\s\S]*?```', ' Code block displayed on terminal. ', text)
    t = re.sub(r'`[^`]*`', '', t)
    t = re.sub(r'[*_#~|>\-\+]', '', t)
    t = re.sub(r'----------------+.*', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    sentences = re.split(r'(?<=[.!?।])\s+', t)
    selected = []
    curr = 0
    for s in sentences:
        s_clean = s.strip()
        if not s_clean:
            continue
        if any(skip in s_clean.lower() for skip in ('source:', 'telemetry', 'result:', 'status:', 'details:')):
            continue
        if curr + len(s_clean) <= max_chars or not selected:
            selected.append(s_clean)
            curr += len(s_clean)
        else:
            break
    summary = " ".join(selected).strip()
    if not summary:
        summary = t[:max_chars].strip()
    return clean_for_speech(summary)

def evaluate_math_expression(query):
    q = query.lower().strip()
    q_clean = re.sub(r'^(?:what\s+is|calculate|solve|evaluate|compute|tell\s+me|find|kitna\s+hota\s+hai|kya\s+hai)\s+', '', q).strip()
    q_clean = re.sub(r'[\?\.!]+$', '', q_clean).strip()
    
    # Check percentage
    m_pct = re.search(r'(\d+(?:\.\d+)?)\s*(?:%|percent|pratishat)\s+of\s+(\d+(?:\.\d+)?)', q_clean)
    if m_pct:
        pct = float(m_pct.group(1))
        val = float(m_pct.group(2))
        res = (pct / 100.0) * val
        res_str = f"{res:g}"
        return {
            "needed_web": False,
            "found": True,
            "is_math": True,
            "expr": f"{pct}% of {val}",
            "result": res_str,
            "title": f"CALCULATION: {pct}% OF {val}",
            "source": "CALCULATION TELEMETRY // PERCENTAGE CORE",
            "full_text": (
                "------------------------------------------------------------\n"
                "   CALCULATION TELEMETRY // PERCENTAGE CORE                 \n"
                "------------------------------------------------------------\n"
                f"EXPRESSION:     {pct}% of {val}\n"
                f"RESULT:         {res_str}\n"
                f"DETAILS:        {pct} percent of {val} is exactly {res_str}.\n"
                "------------------------------------------------------------"
            ),
            "speech_text": f"{pct} percent of {val} is {res_str}."
        }
    
    # Mathematical words mapping
    expr = q_clean
    word_map = {
        'plus': '+', 'jod': '+', 'jodo': '+', 'aur': '+',
        'minus': '-', 'ghatao': '-', 'kam': '-',
        'times': '*', 'multiplied by': '*', 'multiply by': '*', 'into': '*', 'guna': '*', 'x': '*',
        'divided by': '/', 'divide by': '/', 'over': '/', 'bhag': '/', 'bhaag': '/',
        'to the power of': '**', 'power': '**', 'squared': '**2', 'cubed': '**3'
    }
    for w, sym in word_map.items():
        expr = re.sub(r'\b' + re.escape(w) + r'\b', sym, expr)
    
    # Square root
    m_sqrt = re.search(r'(?:square\s+root\s+of|sqrt)\s+(\d+(?:\.\d+)?)', expr)
    if m_sqrt:
        val = float(m_sqrt.group(1))
        res = math.isqrt(int(val)) if val.is_integer() and math.isqrt(int(val))**2 == int(val) else math.sqrt(val)
        res_str = f"{res:g}"
        return {
            "needed_web": False,
            "found": True,
            "is_math": True,
            "expr": f"sqrt({val})",
            "result": res_str,
            "title": f"CALCULATION: SQRT({val})",
            "source": "CALCULATION TELEMETRY // SQUARE ROOT",
            "full_text": (
                "------------------------------------------------------------\n"
                "   CALCULATION TELEMETRY // SQUARE ROOT CORE                \n"
                "------------------------------------------------------------\n"
                f"EXPRESSION:     sqrt({val})\n"
                f"RESULT:         {res_str}\n"
                "------------------------------------------------------------"
            ),
            "speech_text": f"The square root of {val} is {res_str}."
        }
    
    # Check if expr looks like arithmetic
    expr_clean = expr.replace(' ', '')
    if re.match(r'^[0-9\.\+\-\*\/\(\)\^%]+$', expr_clean) and any(op in expr_clean for op in '+-*/^%'):
        safe_expr = expr_clean.replace('^', '**')
        try:
            res = eval(safe_expr, {'__builtins__': None}, {'math': math})
            res_str = f"{res:g}" if isinstance(res, float) else str(res)
            return {
                "needed_web": False,
                "found": True,
                "is_math": True,
                "expr": expr_clean,
                "result": res_str,
                "title": f"CALCULATION: {expr_clean}",
                "source": "CALCULATION TELEMETRY // ARITHMETIC CORE",
                "full_text": (
                    "------------------------------------------------------------\n"
                    "   CALCULATION TELEMETRY // ARITHMETIC CORE                 \n"
                    "------------------------------------------------------------\n"
                    f"EXPRESSION:     {expr_clean}\n"
                    f"RESULT:         {res_str}\n"
                    f"CALCULATION:    Evaluation completed with mathematical precision.\n"
                    "------------------------------------------------------------"
                ),
                "speech_text": f"The result of {expr_clean} is {res_str}."
            }
        except Exception:
            pass
            
    return {"is_math": False}

CONCEPT_DISAMBIGUATION = {
    "why is the sky blue": "Rayleigh scattering",
    "why is sky blue": "Rayleigh scattering",
    "how does a rocket engine work": "Rocket engine",
    "how do airplanes fly": "Lift (force)",
    "how planes fly": "Lift (force)",
    "how does an airplane fly": "Lift (force)",
    "why do leaves change color": "Autumn leaf color",
    "what is black hole": "Black hole",
    "what are black holes": "Black hole",
    "how does the internet work": "Internet",
    "how do neural networks work": "Artificial neural network",
    "what is quantum computing": "Quantum computing",
    "what is photosynthesis": "Photosynthesis",
    "theory of relativity": "Theory of relativity",
    "what is relativity": "Theory of relativity",
    "how does gps work": "Global Positioning System",
    "what is dna": "DNA",
    "what is artificial intelligence": "Artificial intelligence",
    "what is machine learning": "Machine learning",
}

def extract_comparison_entities(query):
    q = query.strip()
    m1 = re.search(r'(?:difference|differences|comparison)\s+(?:between|of)?\s+([a-zA-Z0-9\+\#\.\s]+?)\s+(?:and|vs|versus)\s+([a-zA-Z0-9\+\#\.\s]+)', q, re.IGNORECASE)
    if m1:
        return m1.group(1).strip(), m1.group(2).strip()
    m2 = re.search(r'(?:compare)\s+([a-zA-Z0-9\+\#\.\s]+?)\s+(?:and|with|to|vs|versus)\s+([a-zA-Z0-9\+\#\.\s]+)', q, re.IGNORECASE)
    if m2:
        return m2.group(1).strip(), m2.group(2).strip()
    m3 = re.search(r'([a-zA-Z0-9\+\#\.\u0900-\u097F\s]+?)\s+(?:aur|और|तथा|vs)\s+([a-zA-Z0-9\+\#\.\u0900-\u097F\s]+?)\s+(?:me|mein|में)\s+(?:kya\s+|क्या\s+)?(?:antar|difference|bhed|फ़र्क|अंतर)', q, re.IGNORECASE)
    if m3:
        return m3.group(1).strip(), m3.group(2).strip()
    return None

def fetch_deep_wikipedia(entity):
    headers = {"User-Agent": "Jarvis-HUD-Intel/3.8 (https://github.com/alok-kumar8765/jarvis-ai-voice-assistant)"}
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {"action": "query", "list": "search", "srsearch": entity, "format": "json", "utf8": 1, "srlimit": 5}
        res = requests.get(search_url, params=params, headers=headers, timeout=5)
        if res.status_code == 200:
            items = res.json().get("query", {}).get("search", [])
            if not items:
                return None
            
            best_title = items[0]["title"]
            best_score = -1
            ent_upper = entity.upper()
            ent_lower = entity.lower()
            ent_words = set(re.findall(r'[a-zA-Z0-9]+', ent_lower))

            for it in items:
                t = it["title"]
                score = 0
                if t.lower() == ent_lower:
                    score += 10
                if ent_upper == get_acronym(t):
                    score += 25
                t_words = set(re.findall(r'[a-zA-Z0-9]+', t.lower()))
                score += len(ent_words.intersection(t_words)) * 2
                if score > best_score:
                    best_score = score
                    best_title = t

            ext_url = "https://en.wikipedia.org/w/api.php"
            ext_params = {"action": "query", "prop": "extracts", "explaintext": 1, "exintro": 1, "titles": best_title, "format": "json", "redirects": 1}
            ext_res = requests.get(ext_url, params=ext_params, headers=headers, timeout=5)
            pages = ext_res.json().get("query", {}).get("pages", {})
            for pid, pdata in pages.items():
                if pid != "-1":
                    return {"title": pdata.get("title", best_title), "text": pdata.get("extract", "").strip()}
    except Exception as e:
        print("fetch_deep_wikipedia error:", e)
    return None

def synthesize_entity_comparison(query, is_hindi=False):
    entities = extract_comparison_entities(query)
    if not entities:
        return None
    e1, e2 = entities
    d1 = fetch_deep_wikipedia(e1)
    d2 = fetch_deep_wikipedia(e2)
    if not d1 and not d2:
        return None

    title1 = d1["title"] if d1 else e1.title()
    text1 = d1["text"] if d1 else "Information currently restricted."
    title2 = d2["title"] if d2 else e2.title()
    text2 = d2["text"] if d2 else "Information currently restricted."

    p1 = "\n\n".join([p.strip() for p in text1.split("\n") if len(p.strip()) > 30][:2])
    p2 = "\n\n".join([p.strip() for p in text2.split("\n") if len(p.strip()) > 30][:2])

    lines = [
        "============================================================",
        f"   COMPARATIVE INTELLIGENCE MATRIX // {title1.upper()} vs {title2.upper()}",
        "============================================================",
        f"◈ ENTITY 1: {title1.upper()}",
        p1,
        "",
        "------------------------------------------------------------",
        f"◈ ENTITY 2: {title2.upper()}",
        p2,
        "============================================================",
        "Tactical comparison compiled from authoritative intelligence."
    ]
    full_text = "\n".join(lines)
    
    s1 = p1.split(".")[0].strip() if p1 else ""
    s2 = p2.split(".")[0].strip() if p2 else ""
    if is_hindi:
        speech = f"{title1} और {title2} का तुलनात्मक विवरण तैयार है। {s1}। जबकि {s2}।"
    else:
        speech = f"Comparative analysis between {title1} and {title2}. {s1}. In contrast, {s2}."
        
    return {
        "needed_web": True,
        "found": True,
        "source": f"INTEL MATRIX // {title1.upper()} VS {title2.upper()}",
        "title": f"{title1} vs {title2}",
        "full_text": full_text,
        "speech_text": clean_for_speech(speech),
    }

def query_ai_model(query, is_hindi=False):
    """
    Directly queries active AI Neural Model (Groq, Google Gemini, OpenAI, or Ollama).
    Returns dict with {found: True, source: '...', title: '...', full_text: '...', speech_text: '...'}
    or None if no AI model is configured or if the query fails.
    """
    provider = hud_config.get("ai_provider", "auto").lower()
    api_key = hud_config.get("ai_api_key", "").strip() or (
        os.environ.get("GROQ_API_KEY", "").strip() or
        os.environ.get("GEMINI_API_KEY", "").strip() or
        os.environ.get("OPENAI_API_KEY", "").strip()
    )
    ollama_url = hud_config.get("ollama_url", "http://localhost:11434").strip()
    model_name = hud_config.get("ai_model", "").strip()

    if provider == "auto":
        if api_key.startswith("gsk_") or os.environ.get("GROQ_API_KEY"):
            provider = "groq"
        elif api_key.startswith("AIza") or os.environ.get("GEMINI_API_KEY"):
            provider = "gemini"
        elif api_key.startswith("sk-") or os.environ.get("OPENAI_API_KEY"):
            provider = "openai"
        elif api_key:
            provider = "groq"
        else:
            try:
                r_ol = requests.get(f"{ollama_url}/api/tags", timeout=1.0)
                if r_ol.status_code == 200:
                    provider = "ollama"
            except Exception:
                return None

    if not api_key and provider != "ollama":
        return None

    sys_prompt = (
        "You are J.A.R.V.I.S, an advanced, tactical, and articulate artificial intelligence assistant "
        "inspired by Tony Stark's system. Provide highly accurate, comprehensive, and detailed responses. "
        "Structure your answers clearly using bullet points, sections, or formatted code blocks where applicable. "
        "Avoid conversational fluff. If the user asks in Hindi, respond in natural, polite Hindi."
    )

    try:
        if provider == "groq":
            target_model = model_name if model_name and any(m in model_name.lower() for m in ("llama", "mixtral")) else "llama-3.3-70b-versatile"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            body = {
                "model": target_model,
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": query}
                ],
                "temperature": 0.5,
                "max_tokens": 1024
            }
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body, timeout=12)
            if res.status_code == 200:
                answer = res.json()["choices"][0]["message"]["content"].strip()
                return {
                    "needed_web": True,
                    "found": True,
                    "source": f"NEURAL AI CORE // GROQ ({target_model.upper()})",
                    "title": query.title()[:45],
                    "full_text": answer,
                    "speech_text": generate_speech_summary(answer, is_hindi=is_hindi),
                }

        elif provider == "gemini":
            target_model = model_name if model_name and "gemini" in model_name.lower() else "gemini-2.0-flash"
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={api_key}"
            body = {
                "system_instruction": {"parts": [{"text": sys_prompt}]},
                "contents": [{"parts": [{"text": query}]}],
                "generationConfig": {"temperature": 0.5, "maxOutputTokens": 1024}
            }
            res = requests.post(gemini_url, headers={"Content-Type": "application/json"}, json=body, timeout=12)
            if res.status_code == 200:
                answer = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                return {
                    "needed_web": True,
                    "found": True,
                    "source": f"NEURAL AI CORE // GOOGLE ({target_model.upper()})",
                    "title": query.title()[:45],
                    "full_text": answer,
                    "speech_text": generate_speech_summary(answer, is_hindi=is_hindi),
                }

        elif provider == "openai":
            target_model = model_name if model_name and "gpt" in model_name.lower() else "gpt-4o-mini"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            body = {
                "model": target_model,
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": query}
                ],
                "temperature": 0.5,
                "max_tokens": 1024
            }
            res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body, timeout=12)
            if res.status_code == 200:
                answer = res.json()["choices"][0]["message"]["content"].strip()
                return {
                    "needed_web": True,
                    "found": True,
                    "source": f"NEURAL AI CORE // OPENAI ({target_model.upper()})",
                    "title": query.title()[:45],
                    "full_text": answer,
                    "speech_text": generate_speech_summary(answer, is_hindi=is_hindi),
                }

        elif provider == "ollama":
            target_model = model_name if model_name else "llama3"
            body = {
                "model": target_model,
                "messages": [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": query}
                ],
                "stream": False
            }
            res = requests.post(f"{ollama_url}/v1/chat/completions", json=body, timeout=15)
            if res.status_code == 200:
                answer = res.json()["choices"][0]["message"]["content"].strip()
                return {
                    "needed_web": True,
                    "found": True,
                    "source": f"NEURAL AI CORE // LOCAL OLLAMA ({target_model.upper()})",
                    "title": query.title()[:45],
                    "full_text": answer,
                    "speech_text": generate_speech_summary(answer, is_hindi=is_hindi),
                }
    except Exception as e:
        print(f"AI Model ({provider}) error:", e)

    return None

def fetch_hindi_wikipedia(query):
    headers = {"User-Agent": "Jarvis-HUD-Bilingual/3.8"}
    clean_q = clean_search_query(query)

    try:
        search_url = "https://hi.wikipedia.org/w/api.php"
        search_params = {"action": "query", "list": "search", "srsearch": clean_q, "format": "json", "utf8": 1, "srlimit": 5}
        search_res = requests.get(search_url, params=search_params, headers=headers, timeout=5)
        if search_res.status_code == 200:
            items = search_res.json().get("query", {}).get("search", [])
            if items:
                best_title = items[0]["title"]
                ext_url = "https://hi.wikipedia.org/w/api.php"
                ext_params = {
                    "action": "query",
                    "prop": "extracts",
                    "explaintext": 1,
                    "exintro": 1,
                    "titles": best_title,
                    "format": "json",
                    "redirects": 1
                }
                ext_res = requests.get(ext_url, params=ext_params, headers=headers, timeout=5)
                if ext_res.status_code == 200:
                    pages = ext_res.json().get("query", {}).get("pages", {})
                    for pid, pdata in pages.items():
                        if pid != "-1":
                            extract = pdata.get("extract", "").strip()
                            if extract and len(extract) > 40:
                                return {
                                    "needed_web": True,
                                    "found": True,
                                    "source": "WIKIPEDIA हिन्दी // आधिकारिक संग्रह",
                                    "title": pdata.get("title", best_title),
                                    "full_text": extract,
                                    "speech_text": generate_speech_summary(extract, is_hindi=True),
                                }
    except Exception as e:
        print("Hindi Wikipedia API error:", e)
    return None

def search_internet_data(query):
    # 1. Determine whether conversational reply is applicable
    conv_reply = check_conversational_query(query)
    if conv_reply:
        return {
            "needed_web": False,
            "found": True,
            "source": "JARVIS NEURAL CORE",
            "title": "ASSISTANT DIRECTIVE",
            "full_text": conv_reply,
            "speech_text": conv_reply,
        }

    # 2. Precision Mathematical & Calculation Core
    math_eval = evaluate_math_expression(query)
    if math_eval and math_eval.get("is_math"):
        return math_eval

    # 3. AI Neural Model Engine (Groq / Gemini / OpenAI / Ollama)
    ai_result = query_ai_model(query, is_hindi=is_devanagari(query))
    if ai_result:
        return ai_result

    # 4. Multi-Entity Comparison Synthesizer (e.g. Difference between X and Y)
    comp_result = synthesize_entity_comparison(query, is_hindi=is_devanagari(query))
    if comp_result:
        return comp_result

    # 5. Hindi Wikipedia if Devanagari query
    if is_devanagari(query):
        hi_wiki = fetch_hindi_wikipedia(query)
        if hi_wiki:
            return hi_wiki

    # 6. Scientific & Conceptual Disambiguation
    q_lower = query.lower().strip()
    target_concept = None
    for pattern_q, canonical_title in CONCEPT_DISAMBIGUATION.items():
        if pattern_q in q_lower:
            target_concept = canonical_title
            break

    entity = target_concept if target_concept else clean_search_query(query)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

    # 7. DuckDuckGo Instant Answers API
    try:
        ddg_url = "https://api.duckduckgo.com/"
        params = {"q": entity, "format": "json", "no_html": 1, "skip_disambig": 1}
        res = requests.get(ddg_url, params=params, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            abstract = data.get("AbstractText", "").strip()
            heading = data.get("Heading", entity)
            source = data.get("AbstractSource", "DuckDuckGo Intel")
            if abstract and len(abstract) > 50:
                return {
                    "needed_web": True,
                    "found": True,
                    "source": f"{source.upper()} // INSTANT INTEL",
                    "title": heading,
                    "full_text": abstract,
                    "speech_text": generate_speech_summary(abstract, is_hindi=is_devanagari(query)),
                }
    except Exception as e:
        print("DuckDuckGo API error:", e)

    # 8. Deep Encyclopedic Knowledge Retrieval (Wikipedia)
    deep_wiki = fetch_deep_wikipedia(entity)
    if deep_wiki and len(deep_wiki.get("text", "")) > 60:
        return {
            "needed_web": True,
            "found": True,
            "source": "WIKIPEDIA // OFFICIAL ARCHIVE",
            "title": deep_wiki["title"],
            "full_text": deep_wiki["text"],
            "speech_text": generate_speech_summary(deep_wiki["text"], is_hindi=is_devanagari(query)),
        }

    # 9. Live Web Search & Multi-Source Synthesis (DuckDuckGo Lite)
    try:
        r = requests.post("https://lite.duckduckgo.com/lite/", data={"q": query}, headers=headers, timeout=6)
        if r.status_code == 200:
            tds = re.findall(r'<td[^>]*>(.*?)</td>', r.text, re.DOTALL)
            collected_snippets = []
            collected_sources = []
            for t in tds:
                txt = unescape(re.sub(r'<[^>]+>', '', t)).strip()
                if txt.startswith("http://") or txt.startswith("https://") or ("." in txt and "/" in txt and " " not in txt):
                    domain = txt.split("/")[0].replace("www.", "")
                    if domain and domain not in collected_sources:
                        collected_sources.append(domain)
                elif len(txt) > 40 and "duckduckgo" not in txt.lower():
                    clean_snip = re.sub(r"\[[a-z0-9]\]", "", txt).strip()
                    clean_snip = re.sub(r"\s+", " ", clean_snip)
                    if clean_snip not in collected_snippets:
                        collected_snippets.append(clean_snip)

            if collected_snippets:
                # Relevance validation to prevent random suggestions
                q_words = [w.lower() for w in re.findall(r'\b[a-zA-Z0-9]{3,}\b', query) if w.lower() not in ('who', 'what', 'why', 'how', 'when', 'where', 'the', 'is', 'are', 'was', 'were', 'for', 'about')]
                relevant = any(w in collected_snippets[0].lower() for w in q_words) if q_words else True
                if relevant:
                    full_body = "\n\n".join(collected_snippets[:4])
                    sources_str = ", ".join(collected_sources[:2]) if collected_sources else "Web Intelligence"
                    return {
                        "needed_web": True,
                        "found": True,
                        "source": f"WEB TELEMETRY // {sources_str.upper()}",
                        "title": query.title()[:45],
                        "full_text": full_body,
                        "speech_text": generate_speech_summary(full_body, is_hindi=is_devanagari(query)),
                    }
    except Exception as e:
        print("Live web search error:", e)

    # 10. Clear Not Found Notice - Do not guess or make up info!
    lines = [
        "------------------------------------------------------------",
        "   WEB TELEMETRY // NO VERIFIED INFORMATION FOUND           ",
        "------------------------------------------------------------",
        f"I searched the web for '{query}' but could not locate reliable,",
        "verified data from trusted sources.",
        "",
        "Status: No trustworthy source confirmed. Hallucination prevented.",
        "Tip: Please verify the query or try rephrasing your question.",
        "------------------------------------------------------------",
    ]
    return {
        "needed_web": True,
        "found": False,
        "source": "WEB TELEMETRY // UNVERIFIED",
        "title": query.title()[:45],
        "full_text": "\n".join(lines),
        "speech_text": f"I searched the web, but I could not find verified data on {entity}. Please try rephrasing your question.",
    }


# ╔══════════════════════════════════════════════════════════════════╗
# ║  UNIVERSAL WEB NAVIGATION & INTERNET RESOLUTION ENGINE           ║
# ╚══════════════════════════════════════════════════════════════════╝

KNOWN_PLATFORMS = {
    "google": "https://www.google.com/",
    "youtube": "https://www.youtube.com/",
    "github": "https://github.com/",
    "amazon": "https://www.amazon.com/",
    "flipkart": "https://www.flipkart.com/",
    "reddit": "https://www.reddit.com/",
    "netflix": "https://www.netflix.com/",
    "chatgpt": "https://chatgpt.com/",
    "openai": "https://openai.com/",
    "spotify": "https://open.spotify.com/",
    "twitter": "https://twitter.com/",
    "x": "https://x.com/",
    "instagram": "https://www.instagram.com/",
    "facebook": "https://www.facebook.com/",
    "linkedin": "https://www.linkedin.com/",
    "wikipedia": "https://www.wikipedia.org/",
    "gmail": "https://mail.google.com/",
    "whatsapp": "https://web.whatsapp.com/",
    "stackoverflow": "https://stackoverflow.com/",
    "stack overflow": "https://stackoverflow.com/",
    "cricbuzz": "https://www.cricbuzz.com/",
    "twitch": "https://www.twitch.tv/",
    "discord": "https://discord.com/app",
    "pinterest": "https://www.pinterest.com/",
    "medium": "https://medium.com/",
    "canva": "https://www.canva.com/",
    "imdb": "https://www.imdb.com/",
    "quora": "https://www.quora.com/",
    "swiggy": "https://www.swiggy.com/",
    "zomato": "https://www.zomato.com/",
    "coursera": "https://www.coursera.org/",
    "udemy": "https://www.udemy.com/",
    "geeksforgeeks": "https://www.geeksforgeeks.org/",
    "hackerrank": "https://www.hackerrank.com/",
    "leetcode": "https://leetcode.com/",
    "tradingview": "https://www.tradingview.com/",
    "moneycontrol": "https://www.moneycontrol.com/",
    "hotstar": "https://www.hotstar.com/",
    "jiocinema": "https://www.jiocinema.com/",
    "telegram": "https://web.telegram.org/",
    "yahoo": "https://www.yahoo.com/",
    "bing": "https://www.bing.com/",
    "duckduckgo": "https://duckduckgo.com/",
    "apple": "https://www.apple.com/",
    "microsoft": "https://www.microsoft.com/",
}

def _launch_browser_website(display_name, url, cmd_id=None, is_hindi=False):
    """Logs telemetry, sets HUD status, speaks confirmation, and launches browser."""
    if cmd_id is not None and cmd_id != _current_command_id:
        return
    play_sfx("downlink")
    terminal_feed_log("WEB", f"Opening {display_name} ⟫ {url}")
    _safe_ui_update(lambda: set_status(f"🌐  OPENING {display_name.upper()}...", C.get("cyan_br", "#40ffff")))
    if is_hindi:
        speak(f"{display_name.title()} खोला जा रहा है, महोदय।", cmd_id=cmd_id)
    else:
        speak(f"Opening {display_name}, sir.", cmd_id=cmd_id)
    webbrowser.open(url)

def resolve_and_open_website(raw_query, cmd_id=None):
    """
    Extracts the target website from the user command, resolves the canonical URL
    via instant platform mappings or live internet search, and opens it in the browser.
    """
    if cmd_id is not None and cmd_id != _current_command_id:
        return False, "Preempted by newer command."

    is_hi = is_devanagari(raw_query) or any(k in raw_query.lower() for k in ("kholo", "open karo"))
    target = raw_query.strip().lower()
    # Remove leading action verbs
    target = re.sub(
        r"^(?:open|launch|go to|navigate to|browse to|browse|visit|connect to|access|kholo|open\s+karo|खोलो|ओपन\s*करो)\s+",
        "", target
    ).strip()
    # Remove descriptor noise words
    target = re.sub(r"^(?:the\s+website\s+of|website\s+of|the\s+site\s+of|site\s+of|the\s+official\s+website\s+of|the\s+official\s+site\s+of|the\s+portal\s+of|website|site|webpage|page)\s+", "", target).strip()
    target = re.sub(r"\s+(?:website|site|webpage|page|portal|homepage|kholo|open\s+karo|खोलो|ओपन\s*करो|वेबसाइट\s*खोलो|साइट\s*खोलो)$", "", target).strip()

    if target in HINDI_PLATFORMS:
        target = HINDI_PLATFORMS[target]
    for h_k, h_v in HINDI_PLATFORMS.items():
        if h_k in target:
            target = target.replace(h_k, h_v).strip()

    if not target:
        return False, "Target website name could not be identified."

    if cmd_id is not None and cmd_id != _current_command_id:
        return False, "Preempted by newer command."

    # 1. Direct URL check
    if re.match(r"^(?:https?:\/\/)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:\/.*)?$", target):
        url = target if target.startswith("http") else "https://" + target
        display_name = target.replace("https://", "").replace("http://", "").split("/")[0]
        _launch_browser_website(display_name.title(), url, cmd_id=cmd_id, is_hindi=is_hi)
        return True, f"Opening {display_name}."

    # 2. Known popular platforms dictionary (instant zero-latency open)
    clean_key = target.replace(" ", "")
    if target in KNOWN_PLATFORMS:
        _launch_browser_website(target.title(), KNOWN_PLATFORMS[target], cmd_id=cmd_id, is_hindi=is_hi)
        return True, f"Opening {target.title()}."
    if clean_key in KNOWN_PLATFORMS:
        _launch_browser_website(target.title(), KNOWN_PLATFORMS[clean_key], cmd_id=cmd_id, is_hindi=is_hi)
        return True, f"Opening {target.title()}."

    # 3. Live Internet Query via DuckDuckGo to extract official canonical URL
    terminal_feed_log("WEB", f"Querying Internet for official website: '{target}'...")
    try:
        query_str = urllib.parse.quote_plus(f"{target} official website")
        ddg_url = f"https://html.duckduckgo.com/html/?q={query_str}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(ddg_url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        if cmd_id is not None and cmd_id != _current_command_id:
            return False, "Preempted by newer command."

        # Extract redirect links
        links = re.findall(r'href=["\']/l/\?uddg=([^"\'&]+)', html)
        for link in links:
            decoded = urllib.parse.unquote(link)
            if decoded.startswith("http") and not any(skip in decoded for skip in ["duckduckgo.com", "google.com", "bing.com", "yahoo.com"]):
                _launch_browser_website(target.title(), decoded, cmd_id=cmd_id)
                return True, f"Opening {target.title()}."

        # Fallback to result__url pattern
        raw_urls = re.findall(r'class=["\']result__url["\'][^>]*>([^<]+)<', html)
        for ru in raw_urls:
            clean_u = ru.strip().replace(" ", "")
            if clean_u:
                final_u = clean_u if clean_u.startswith("http") else "https://" + clean_u
                _launch_browser_website(target.title(), final_u, cmd_id=cmd_id)
                return True, f"Opening {target.title()}."
    except Exception as e:
        print(f"Web resolution note for '{target}':", e)

    if cmd_id is not None and cmd_id != _current_command_id:
        return False, "Preempted by newer command."

    # 4. Canonical Domain Guess or Google Search
    if " " not in target:
        fallback_url = f"https://www.{target}.com"
    else:
        fallback_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(target)}"

    _launch_browser_website(target.title(), fallback_url, cmd_id=cmd_id)
    return True, f"Opening {target.title()}."


# ╔══════════════════════════════════════════════════════════════════╗
# ║  HARDWARE CONTROLS                                               ║
# ╚══════════════════════════════════════════════════════════════════╝

def get_brightness():
    try:
        val = sbc.get_brightness()
        return int(val[0] if isinstance(val, list) else val)
    except Exception:
        return None

def set_brightness(val):
    try:
        val = max(0, min(100, int(val)))
        sbc.set_brightness(val)
        terminal_feed_log("HARDWARE", f"Display brightness set to {val}%.")
        speak(f"Brightness set to {val} percent.")
    except Exception as e:
        print("Brightness error:", e)

def press_volume_key(key_code, times=5):
    try:
        for _ in range(times):
            ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)
            ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)
    except Exception as e:
        print("Volume control error:", e)

def volume_up():
    press_volume_key(0xAF, 5)
    terminal_feed_log("HARDWARE", "System volume increased (+10%).")
    speak("Volume increased.")

def volume_down():
    press_volume_key(0xAE, 5)
    terminal_feed_log("HARDWARE", "System volume decreased (-10%).")
    speak("Volume decreased.")

def volume_mute():
    press_volume_key(0xAD, 1)
    terminal_feed_log("HARDWARE", "System audio output muted.")
    speak("Volume muted.")

# ╔══════════════════════════════════════════════════════════════════╗
# ║  METEOROLOGICAL INTELLIGENCE (WTTR.IN SATELLITE TELEMETRY)       ║
# ╚══════════════════════════════════════════════════════════════════╝

def extract_weather_location(query):
    q = query.strip()
    # Check Hindi city matches first if present
    for city_hi, mapped in HINDI_CITY_MAP.items():
        if city_hi in q:
            return mapped

    # Check Hindi regex patterns
    m_hi = re.search(r"([^\s]+)\s+(?:का|में|के|की)\s+(?:मौसम|तापमान)", q)
    if m_hi:
        c = m_hi.group(1).strip()
        return HINDI_CITY_MAP.get(c, c)

    m_hi2 = re.search(r"(?:मौसम|तापमान)\s+(?:बताओ|दिखाओ|कैसा\s+है)?\s*([^\s]+)", q)
    if m_hi2:
        c = m_hi2.group(1).strip()
        if c in HINDI_CITY_MAP:
            return HINDI_CITY_MAP[c]

    # Hinglish patterns: "delhi ka mausam", "mumbai me weather"
    m_hing = re.search(r"([a-zA-Z]+)\s+(?:ka|me|mein)\s+(?:mausam|weather|temperature)", q, re.IGNORECASE)
    if m_hing:
        return m_hing.group(1).strip().title()

    q_lower = q.lower()
    m = re.search(r"(?:weather|temperature|climate|forecast)\s+(?:in|of|at|for)\s+([a-zA-Z\s]+)", q_lower)
    if m:
        loc = m.group(1).strip()
        loc = re.sub(r"\b(today|now|right now|currently|please|jarvis)\b", "", loc).strip()
        if loc:
            return loc.title()

    m = re.search(r"^([a-zA-Z\s]+?)\s+(?:weather|temperature|climate|forecast)$", q_lower)
    if m:
        candidate = m.group(1).strip()
        stop_words = {
            "what is the", "what is", "what's the", "whats the", "tell me the",
            "tell me", "how is the", "how is", "check the", "check", "the", "current",
            "today's", "today", "live", "show", "give me"
        }
        if candidate not in stop_words and not any(candidate.startswith(sw) for sw in ["what", "how", "tell", "show", "check"]):
            return candidate.title()

    return None

def fetch_weather(location=None, is_hindi=False):
    headers = {"User-Agent": "Jarvis-HUD-Meteo/3.2"}
    target = location or hud_config.get("default_location", "Uttar Pradesh, India")
    url = f"https://wttr.in/{urllib.parse.quote(target)}?format=j1"

    res = requests.get(url, headers=headers, timeout=6)
    if res.status_code != 200:
        raise Exception(f"Atmospheric link status {res.status_code}")

    data = res.json()
    cur = data.get("current_condition", [{}])[0]
    area_obj = data.get("nearest_area", [{}])[0]
    area_name = area_obj.get("areaName", [{}])[0].get("value", "").strip()
    region_name = area_obj.get("region", [{}])[0].get("value", "").strip()
    country_name = area_obj.get("country", [{}])[0].get("value", "").strip()

    t_clean = target.strip().title()
    t_lower = target.strip().lower()

    if country_name and t_lower == country_name.lower():
        city = country_name
        loc_display = country_name
    elif region_name and (region_name.lower() in t_lower or all(w in t_lower for w in region_name.lower().split())):
        city = region_name
        loc_display = f"{region_name}, {country_name}" if country_name else region_name
    elif area_name and (area_name.lower() in t_lower or t_lower in area_name.lower()):
        city = area_name
        loc_display = f"{area_name}, {country_name}" if country_name else area_name
    elif country_name and country_name.lower() in t_lower:
        city = t_clean
        loc_display = t_clean
    else:
        city = t_clean
        loc_display = f"{t_clean}, {country_name}" if country_name else t_clean

    temp_c = cur.get("temp_C", "N/A")
    temp_f = cur.get("temp_F", "N/A")
    feels_c = cur.get("FeelsLikeC", temp_c)
    desc = cur.get("weatherDesc", [{}])[0].get("value", "Clear").strip()
    humidity = cur.get("humidity", "N/A")
    wind = cur.get("windspeedKmph", "N/A")
    uv = cur.get("uvIndex", "N/A")
    vis = cur.get("visibility", "N/A")

    lines = [
        "------------------------------------------------------------",
        "   METEOROLOGICAL SATELLITE TELEMETRY // wttr.in            ",
        "------------------------------------------------------------",
        f"LOCATION:       {loc_display.upper()}",
        f"TEMPERATURE:    {temp_c} deg C ({temp_f} deg F) | Feels like: {feels_c} deg C",
        f"CONDITIONS:     {desc}",
        f"HUMIDITY:       {humidity}%",
        f"WIND VELOCITY:  {wind} km/h",
        f"UV INDEX:       {uv} | Visibility: {vis} km",
        "------------------------------------------------------------",
        "Atmospheric telemetry synchronized with orbital satellites."
    ]
    report_text = "\n".join(lines)
    if is_hindi:
        speech_text = (
            f"{loc_display} में वर्तमान तापमान {temp_c} डिग्री सेल्सियस है, स्थिति {desc}। "
            f"आर्द्रता {humidity} प्रतिशत और हवा की गति {wind} किलोमीटर प्रति घंटा है।"
        )
    else:
        speech_text = (
            f"Current meteorological telemetry for {loc_display}. "
            f"Conditions: {desc}. "
            f"Temperature is {temp_c} degrees Celsius, {temp_f} degrees Fahrenheit, with a feels-like temperature of {feels_c} degrees Celsius. "
            f"Relative humidity is {humidity} percent. "
            f"Wind velocity is {wind} kilometers per hour. "
            f"UV index is {uv}, with visibility of {vis} kilometers. "
            f"Atmospheric telemetry synchronized with orbital satellites."
        )

    return {
        "city": city,
        "full_text": report_text,
        "speech_text": speech_text,
    }

def weather_telemetry(location=None, cmd_id=None, is_hindi=False):
    if cmd_id is not None and cmd_id != _current_command_id:
        return
    root.after(0, lambda: set_status("◈  SYNCHRONIZING ORBITAL WEATHER LINK...", C["amber"]))
    try:
        data = fetch_weather(location, is_hindi=is_hindi)
        if cmd_id is not None and cmd_id != _current_command_id:
            return
        _anim["last_answer"] = data["full_text"]
        root.after(0, lambda: terminal_feed_intel("METEOROLOGICAL SATELLITE", f"WEATHER TELEMETRY // {data['city'].upper()}", data["full_text"]))
        speak(data["speech_text"], cmd_id=cmd_id)
    except Exception as e:
        if cmd_id is not None and cmd_id != _current_command_id:
            return
        print("Weather telemetry error:", e)
        err_msg = f"Unable to establish weather telemetry uplink: {e}"
        root.after(0, lambda: terminal_feed_log("METEO FAULT", err_msg))
        if is_hindi:
            speak("मैं इस समय मौसम की जानकारी प्राप्त करने में असमर्थ रहा।", cmd_id=cmd_id)
        else:
            speak("I was unable to retrieve the weather data at this moment.", cmd_id=cmd_id)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  LIVE NEWS FEED INTELLIGENCE (GOOGLE NEWS RSS DISPATCHES)        ║
# ╚══════════════════════════════════════════════════════════════════╝

def extract_news_intent(query):
    q = query.strip().lower()
    m = re.search(r"news\s+(?:about|on|regarding)\s+(.+)", q)
    if m:
        sub = m.group(1).strip()
        if sub:
            return None, None, sub

    if any(k in q for k in ("tech", "technology", "gadget", "software", "ai")):
        return "TECHNOLOGY", "TECHNOLOGY INTEL", None
    if any(k in q for k in ("business", "economy", "stock", "market", "finance")):
        return "BUSINESS", "FINANCIAL INTEL", None
    if any(k in q for k in ("sport", "cricket", "football", "soccer", "nba")):
        return "SPORTS", "SPORTS TELEMETRY", None
    if any(k in q for k in ("world", "global", "international")):
        return "WORLD", "GLOBAL DISPATCHES", None

    return None, "TOP BREAKING HEADLINES", None

def fetch_news(topic_code=None, topic_name="TOP BREAKING HEADLINES", search_query=None, lang="en"):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    if lang == "hi":
        if search_query:
            encoded = urllib.parse.quote_plus(search_query)
            url = f"https://news.google.com/rss/search?q={encoded}&hl=hi&gl=IN&ceid=IN:hi"
            title_header = f"समाचार बुलेटिन // {search_query}"
        else:
            url = "https://news.google.com/rss?hl=hi&gl=IN&ceid=IN:hi"
            title_header = "लाइव उपग्रह समाचार // मुख्य समाचार"
    else:
        if search_query:
            encoded = urllib.parse.quote_plus(search_query)
            url = f"https://news.google.com/rss/search?q={encoded}&hl=en-IN&gl=IN&ceid=IN:en"
            title_header = f"NEWS FEED // {search_query.upper()}"
        elif topic_code:
            url = f"https://news.google.com/rss/headlines/section/topic/{topic_code}?hl=en-IN&gl=IN&ceid=IN:en"
            title_header = f"NEWS FEED // {topic_name}"
        else:
            url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
            title_header = "GLOBAL BREAKING NEWS // HEADLINES"

    res = requests.get(url, headers=headers, timeout=6)
    if res.status_code != 200:
        raise Exception(f"News feed downlink returned HTTP {res.status_code}")

    root_el = ET.fromstring(res.content)
    items = root_el.findall(".//item")
    if not items:
        raise Exception("No news dispatches located in satellite feed.")

    lines = [
        "------------------------------------------------------------",
        f"   {title_header}   ",
        "------------------------------------------------------------",
    ]
    spoken_headlines = []

    for i, it in enumerate(items[:4], 1):
        raw_title = it.find("title").text or "Untitled Dispatch"
        if " - " in raw_title:
            headline, source = raw_title.rsplit(" - ", 1)
        else:
            headline, source = raw_title, "Google News"

        headline = headline.strip()
        source = source.strip()
        lines.append(f"[{i:02d}] {headline}")
        lines.append(f"     Source: {source}")
        lines.append("")

        if lang == "hi":
            spoken_headlines.append(f"समाचार {i}: {headline}, {source} द्वारा।")
        else:
            spoken_headlines.append(f"Headline {i}: {headline}, reported by {source}.")

    lines.append("------------------------------------------------------------")
    if lang == "hi":
        lines.append("लाइव उपग्रह समाचार फ़ीड अद्यतन।")
    else:
        lines.append("Live satellite news feed updated. Click [READ] to re-hear.")

    full_text = "\n".join(lines).strip()
    if lang == "hi":
        speech_text = (
            f"लाइव उपग्रह समाचार बुलेटिन। "
            + " ".join(spoken_headlines[:3])
            + " समाचार अपडेट समाप्त।"
        )
    else:
        speech_text = (
            f"Live satellite news telemetry. {topic_name}. "
            + " ".join(spoken_headlines)
            + " Live news feed synchronized."
        )

    return {
        "title": title_header,
        "full_text": full_text,
        "speech_text": speech_text,
    }

def news_telemetry(topic_code=None, topic_name="TOP BREAKING HEADLINES", search_query=None, cmd_id=None, lang="en"):
    if cmd_id is not None and cmd_id != _current_command_id:
        return
    status_text = "◈  DOWNLINKING HINDI NEWS TELEMETRY..." if lang == "hi" else "◈  DOWNLINKING GLOBAL NEWS TELEMETRY..."
    root.after(0, lambda: set_status(status_text, C["amber"]))
    try:
        data = fetch_news(topic_code, topic_name, search_query, lang=lang)
        if cmd_id is not None and cmd_id != _current_command_id:
            return
        _anim["last_answer"] = data["full_text"]
        header_tag = "HINDI NEWS FEED" if lang == "hi" else "GLOBAL NEWS FEED"
        root.after(0, lambda: terminal_feed_intel(header_tag, data["title"], data["full_text"]))
        speak(data["speech_text"], cmd_id=cmd_id)
    except Exception as e:
        if cmd_id is not None and cmd_id != _current_command_id:
            return
        print("News telemetry error:", e)
        err_msg = f"Unable to establish news telemetry link: {e}"
        root.after(0, lambda: terminal_feed_log("NEWS FAULT", err_msg))
        if lang == "hi":
            speak("मैं इस समय ताज़ा समाचार प्राप्त करने में असमर्थ रहा।", cmd_id=cmd_id)
        else:
            speak("I was unable to retrieve the latest news dispatches at this moment.", cmd_id=cmd_id)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  UNIVERSAL YOUTUBE VIDEO DISCOVERY & AUTOPLAY ENGINE             ║
# ╚══════════════════════════════════════════════════════════════════╝

def extract_youtube_query(query):
    q = query.strip()
    patterns = [
        # Hindi Devanagari video search & find patterns
        r"^(?:यूट्यूब\s*पर|यूट्यूब\s*में)\s*(?:के\s+)?(?:वीडियो\s+)?(.+?)\s*(?:ढूंढो|सर्च\s*करो|खोजो|दिखाओ)$",
        r"^(?:यूट्यूब\s*पर|यूट्यूब\s*में)\s*(.+?)\s*(?:का\s+वीडियो|के\s+वीडियो)?\s*(?:ढूंढो|सर्च\s*करो|खोजो|दिखाओ)$",
        r"^यूट्यूब\s*(?:खोलो|ओपन\s*करो)\s*और\s*(.+?)\s*(?:ढूंढो|सर्च\s*करो|खोजो|दिखाओ)$",
        # Hindi Devanagari playback patterns
        r"^(?:यूट्यूब\s*पर|यूट्यूब\s*में)\s*(.+?)\s*(?:चलाओ|बजाओ|सुनाओ|प्ले\s*करो)$",
        r"^यूट्यूब\s*(?:खोलो|ओपन\s*करो)\s*और\s*(.+?)\s*(?:चलाओ|बजाओ|प्ले\s*करो)$",
        r"^(?:गाना|सॉन्ग|वीडियो|गीत)?\s*(?:चलाओ|बजाओ|सुनाओ|प्ले\s*करो)\s+(.+)$",
        r"^(.+?)\s*(?:गाना|गीत|भजन|सॉन्ग|वीडियो)\s*(?:चलाओ|बजाओ|सुनाओ)$",
        r"^(?:चलाओ|बजाओ|सुनाओ|प्ले\s*करो)\s+(.+)$",
        # Hinglish find & search patterns
        r"^(?:youtube\s+par\s+)?(.+?)\s+(?:video\s+dhundo|video\s+dikhao|search\s+karo|dhundo|dikhao)$",
        r"^youtube\s+(?:kholo|open\s+karo)\s+aur\s+(.+?)\s+(?:dhundo|search\s+karo)$",
        # Hinglish playback patterns
        r"^(?:youtube\s+par\s+)?(.+?)\s+(?:gana\s+bajao|gana\s+chalao|song\s+chalao|chalao|bajao)$",
        r"^(?:gana\s+chalao|song\s+chalao|play\s+karo|chalao|bajao|sunao)\s+(.+)$",
        # English find, search & watch video patterns
        r"(?:find|search)\s+(?:video\s+(?:of|for|about)\s+|videos\s+(?:of|for|about)\s+|video\s+|videos\s+)?(.+?)\s+(?:on|in)\s+youtube",
        r"(?:find|search)\s+(?:on|in)\s+youtube\s+(?:for\s+)?(?:video\s+(?:of|for|about)\s+|videos\s+(?:of|for|about)\s+|video\s+|videos\s+)?(.+)",
        r"(?:show\s+me|show)\s+(?:videos\s+of\s+|video\s+of\s+|videos\s+|video\s+)?(.+?)\s+(?:on|in)\s+youtube",
        r"watch\s+(?:video\s+(?:of|for|about)\s+|video\s+)?(.+?)\s+(?:on|in)\s+youtube",
        r"watch\s+(?:video\s+(?:of|for|about)\s+|video\s+)?(.+)",
        r"open\s+youtube\s+and\s+(?:find|search|play)\s+(.+)",
        r"(?:can\s+you\s+)?play\s+(?:video|song|track|music)?\s*(.+?)\s+(?:on|in)\s+youtube",
        r"play\s+youtube\s+(.+)",
        r"youtube\s+play\s+(.+)",
        r"search\s+youtube\s+(?:for\s+)?(.+)",
        r"search\s+(.+?)\s+on\s+youtube",
        r"play\s+(?:video|song|track|music)?\s*(.+)",
    ]
    for p in patterns:
        m = re.search(p, q, re.IGNORECASE)
        if m:
            extracted = m.group(1).strip()
            extracted = re.sub(r"\s+(?:on|in)\s+youtube$", "", extracted, flags=re.IGNORECASE).strip()
            extracted = re.sub(r"\s+(?:चलाओ|बजाओ|सुनाओ|ढूंढो|सर्च\s*करो|खोजो|दिखाओ|play|on\s+youtube)$", "", extracted, flags=re.IGNORECASE).strip()
            extracted = re.sub(r"^(?:video\s+of|videos\s+of|song\s+of)\s+", "", extracted, flags=re.IGNORECASE).strip()
            extracted = re.sub(r"\s+(?:video|song|geet|gana|गाना|गीत|सॉन्ग|वीडियो)$", "", extracted, flags=re.IGNORECASE).strip()
            if extracted:
                return extracted
    return q

def youtube_play(query, cmd_id=None, is_hindi=False):
    if cmd_id is not None and cmd_id != _current_command_id:
        return
    clean = query.strip()
    if not clean:
        if is_hindi:
            speak("आप यूट्यूब पर कौन सा वीडियो देखना या सुनना चाहेंगे?", cmd_id=cmd_id)
        else:
            speak("What video would you like me to find on YouTube?", cmd_id=cmd_id)
        return

    root.after(0, lambda: terminal_feed_log("MEDIA DISPATCH", f"Scanning global YouTube catalog for: '{clean}'..."))
    root.after(0, lambda: set_status("◈  SEARCHING YOUTUBE CATALOG...", C["amber"]))

    video_info = None
    try:
        encoded = urllib.parse.quote_plus(clean)
        search_url = f"https://www.youtube.com/results?search_query={encoded}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        }
        res = requests.get(search_url, headers=headers, timeout=6)
        if res.status_code == 200:
            # 1. Primary extraction: Parse ytInitialData JSON for rich video metadata
            m = re.search(r'var ytInitialData = ({.*?});</script>', res.text)
            if m:
                try:
                    data = json.loads(m.group(1))
                    contents = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
                    for sec in contents:
                        for item in sec.get("itemSectionRenderer", {}).get("contents", []):
                            vr = item.get("videoRenderer")
                            if vr and vr.get("videoId"):
                                v_id = vr.get("videoId")
                                v_title = vr.get("title", {}).get("runs", [{}])[0].get("text", clean)
                                v_channel = vr.get("ownerText", {}).get("runs", [{}])[0].get("text", "YouTube Creator")
                                v_len = vr.get("lengthText", {}).get("simpleText", "")
                                video_info = {
                                    "id": v_id,
                                    "title": v_title,
                                    "channel": v_channel,
                                    "duration": v_len,
                                    "url": f"https://www.youtube.com/watch?v={v_id}"
                                }
                                break
                        if video_info:
                            break
                except Exception as ex_json:
                    print("YouTube ytInitialData JSON parse note:", ex_json)

            # 2. Fallback regex extraction if JSON navigation missed
            if not video_info:
                matches = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', res.text)
                for vid in matches:
                    if len(vid) == 11:
                        video_info = {
                            "id": vid,
                            "title": clean.title(),
                            "channel": "YouTube",
                            "duration": "",
                            "url": f"https://www.youtube.com/watch?v={vid}"
                        }
                        break
    except Exception as e:
        print("YouTube video search error:", e)

    if cmd_id is not None and cmd_id != _current_command_id:
        return

    if video_info:
        vid_id = video_info["id"]
        v_title = video_info["title"]
        v_channel = video_info["channel"]
        v_dur = video_info["duration"]
        video_url = video_info["url"]

        dur_text = f" [{v_dur}]" if v_dur else ""
        log_content = (
            f"Universal Video Match Identified: [ID: {vid_id}]\n"
            f"Title: {v_title}{dur_text}\n"
            f"Channel / Creator: {v_channel}\n"
            f"Stream URL: {video_url}\n"
            f"Status: Direct browser video playback stream initiated."
        )

        clean_spoken_title = re.sub(r"[|/].*$", "", v_title).strip()
        if len(clean_spoken_title) > 60:
            clean_spoken_title = clean_spoken_title[:57] + "..."

        if is_hindi:
            yt_speech = f"यूट्यूब पर '{clean_spoken_title}' मिल गया है। वीडियो शुरू किया जा रहा है, महोदय।"
        else:
            yt_speech = f"Found '{clean_spoken_title}' by {v_channel} on YouTube. Initiating playback now, sir."

        root.after(0, lambda: terminal_feed_intel("MEDIA DISPATCH", f"YOUTUBE VIDEO // {clean.upper()}", log_content))
        _anim["last_answer"] = f"Playing '{v_title}' on YouTube: {video_url}"
        speak(yt_speech, cmd_id=cmd_id)
        webbrowser.open(video_url)
    else:
        fallback_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(clean)}"
        if is_hindi:
            fallback_speech = f"यूट्यूब पर {clean} के वीडियो खोज परिणाम खोले जा रहे हैं।"
        else:
            fallback_speech = f"Dispatched YouTube video search for {clean}, sir."
        root.after(0, lambda: terminal_feed_intel("MEDIA DISPATCH", f"YOUTUBE SEARCH // {clean.upper()}", f"Direct ID scan timed out. Dispatched search results for '{clean}'."))
        _anim["last_answer"] = f"YouTube video search for: {clean}"
        speak(fallback_speech, cmd_id=cmd_id)
        webbrowser.open(fallback_url)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  SPOTIFY MUSIC STREAMING & DESKTOP DISPATCH ENGINE               ║
# ╚══════════════════════════════════════════════════════════════════╝

def extract_spotify_query(query):
    q = query.strip()
    patterns = [
        # Hindi Devanagari patterns
        r"^(?:स्पॉटिफ़ाई\s*पर|स्पॉटिफ़ाई\s*में)\s*(?:गाना|गीत|सॉन्ग)?\s*(.+?)\s*(?:चलाओ|बजाओ|सुनाओ|प्ले\s*करो)$",
        r"^स्पॉटिफ़ाई\s*(?:खोलो|ओपन\s*करो)\s*और\s*(.+?)\s*(?:चलाओ|बजाओ|सुनाओ|प्ले\s*करो)$",
        r"^(?:गाना|सॉन्ग|गीत)?\s*(?:चलाओ|बजाओ|सुनाओ)\s+(.+?)\s+(?:स्पॉटिफ़ाई\s*पर|स्पॉटिफ़ाई\s*में)$",
        r"^(?:स्पॉटिफ़ाई\s*पर|स्पॉटिफ़ाई\s*में)\s+(.+)$",
        # Hinglish patterns
        r"^(?:spotify\s+par|spotify\s+me|spotify\s+mein)\s+(?:gana|song|music)?\s*(.+?)\s*(?:chalao|bajao|sunao|play\s+karo)$",
        r"^spotify\s+(?:kholo|open\s+karo)\s+aur\s+(.+?)\s+(?:chalao|bajao|sunao)$",
        r"^(?:gana|song|music)?\s*(?:chalao|bajao|sunao)\s+(.+?)\s+(?:spotify\s+par|spotify\s+me)$",
        r"^(?:spotify\s+par|spotify\s+me)\s+(.+)$",
        # English patterns
        r"open\s+spotify\s+and\s+play\s+(.+)",
        r"(?:can\s+you\s+)?play\s+(?:song|track|music|artist|album|playlist)?\s*(.+?)\s+(?:on|in)\s+spotify",
        r"play\s+spotify\s+(.+)",
        r"spotify\s+play\s+(.+)",
        r"search\s+spotify\s+(?:for\s+)?(.+)",
        r"search\s+(.+?)\s+on\s+spotify",
        r"on\s+spotify\s+play\s+(.+)",
    ]
    for p in patterns:
        m = re.search(p, q, re.IGNORECASE)
        if m:
            extracted = m.group(1).strip()
            extracted = re.sub(r"\s+(?:on|in)\s+spotify$", "", extracted, flags=re.IGNORECASE).strip()
            extracted = re.sub(r"\s+(?:चलाओ|बजाओ|सुनाओ|play|on\s+spotify)$", "", extracted, flags=re.IGNORECASE).strip()
            extracted = re.sub(r"^(?:song|track|music|gana|geet)\s+", "", extracted, flags=re.IGNORECASE).strip()
            extracted = re.sub(r"\s+(?:gana|song|geet|गाना|गीत|सॉन्ग)$", "", extracted, flags=re.IGNORECASE).strip()
            if extracted:
                return extracted
    m_fall = re.search(r"play\s+(.+?)\s+(?:on|in)\s+spotify", q, re.IGNORECASE)
    if m_fall:
        return m_fall.group(1).strip()
    return q

def resolve_spotify_media(query):
    """
    Discovers exact Spotify track, artist, album, or playlist URI from query.
    Falls back to search URI if no direct match is identified.
    """
    clean = query.strip()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    candidates = [f"spotify track {clean}", f"spotify {clean}"]
    for sq in candidates:
        try:
            r = requests.post("https://lite.duckduckgo.com/lite/", data={"q": sq}, headers=headers, timeout=4)
            if r.status_code == 200:
                matches = re.findall(r"open\.spotify\.com(?:/intl-[a-z]+)?/(track|artist|album|playlist)/([a-zA-Z0-9]{22})", r.text)
                if matches:
                    m_type, m_id = matches[0]
                    resolved_title = clean.title()
                    try:
                        oe = requests.get(f"https://open.spotify.com/oembed?url=https://open.spotify.com/{m_type}/{m_id}", timeout=2).json()
                        if oe.get("title"):
                            resolved_title = oe.get("title")
                    except Exception:
                        pass
                    return {
                        "type": m_type,
                        "id": m_id,
                        "title": resolved_title,
                        "desktop_uri": f"spotify:{m_type}:{m_id}",
                        "web_url": f"https://open.spotify.com/{m_type}/{m_id}",
                        "is_direct": True,
                    }
        except Exception as ex:
            print("Spotify resolution note:", ex)

    encoded_q = urllib.parse.quote(clean)
    return {
        "type": "search",
        "id": None,
        "title": clean.title(),
        "desktop_uri": f"spotify:search:{encoded_q}",
        "web_url": f"https://open.spotify.com/search/{encoded_q}",
        "is_direct": False,
    }


def spotify_play(query, cmd_id=None, is_hindi=False):
    if cmd_id is not None and cmd_id != _current_command_id:
        return
    clean = query.strip()
    if not clean:
        if is_hindi:
            speak("आप स्पॉटिफ़ाई पर कौन सा गाना या कलाकार सुनना चाहेंगे?", cmd_id=cmd_id)
        else:
            speak("What song or artist would you like to play on Spotify?", cmd_id=cmd_id)
        return

    root.after(0, lambda: terminal_feed_log("MEDIA DISPATCH", f"Resolving Spotify audio catalog for: '{clean}'..."))
    root.after(0, lambda: set_status("◈  DISPATCHING SPOTIFY AUDIO STREAM...", C["amber"]))

    media_info = resolve_spotify_media(clean)
    if cmd_id is not None and cmd_id != _current_command_id:
        return

    desktop_uri = media_info["desktop_uri"]
    web_url = media_info["web_url"]
    matched_title = media_info["title"]
    is_direct = media_info["is_direct"]
    m_type = media_info["type"].upper()

    log_content = (
        f"Media Target: Spotify Audio Streaming Network\n"
        f"Target Match: {matched_title} [{m_type}]\n"
        f"Desktop Protocol: {desktop_uri}\n"
        f"Web Stream URL: {web_url}\n"
        f"Status: Direct audio playback stream dispatched."
    )

    clean_spoken_title = re.sub(r"[|/].*$", "", matched_title).strip()
    if len(clean_spoken_title) > 60:
        clean_spoken_title = clean_spoken_title[:57] + "..."

    if is_hindi:
        sp_speech = (
            f"स्पॉटिफ़ाई पर '{clean_spoken_title}' मिल गया है। गाना शुरू किया जा रहा है, महोदय।"
            if is_direct else
            f"स्पॉटिफ़ाई पर '{clean}' चलाया जा रहा है, महोदय।"
        )
    else:
        sp_speech = f"Playing '{clean_spoken_title}' on Spotify, sir. Initiating audio playback now."

    root.after(0, lambda: terminal_feed_intel("MEDIA DISPATCH", f"SPOTIFY // {clean.upper()}", log_content))
    _anim["last_answer"] = f"Playing '{matched_title}' on Spotify: {web_url}"
    speak(sp_speech, cmd_id=cmd_id)

    # Trigger native Windows desktop Spotify client with web fallback
    try:
        os.startfile(desktop_uri)
    except Exception as ex:
        print("Spotify desktop URI note, falling back to browser:", ex)
        webbrowser.open(web_url)

    # Initiate playback trigger in background thread
    def _trigger_playback_daemon():
        _time.sleep(1.2)
        try:
            def _enum_cb(hwnd, _):
                if ctypes.windll.user32.IsWindowVisible(hwnd):
                    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buff = ctypes.create_unicode_buffer(length + 1)
                        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                        if "spotify" in buff.value.lower():
                            ctypes.windll.user32.SetForegroundWindow(hwnd)
                            return False
                return True
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
            ctypes.windll.user32.EnumWindows(EnumWindowsProc(_enum_cb), 0)
        except Exception:
            pass

        _time.sleep(0.4)
        try:
            # Dispatch Media Play/Pause virtual key (VK_MEDIA_PLAY_PAUSE = 0xB3)
            ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
        except Exception:
            pass

    threading.Thread(target=_trigger_playback_daemon, daemon=True).start()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  COMMAND EXECUTION THREAD                                        ║
# ╚══════════════════════════════════════════════════════════════════╝

def execute_command_thread(raw_query, cmd_id=None):
    global _current_command_id
    if cmd_id is None:
        cmd_id = _current_command_id

    if not raw_query:
        if cmd_id == _current_command_id:
            _anim["processing"] = False
            set_status("◎  SYSTEMS NOMINAL", C["cyan"])
        return

    if cmd_id != _current_command_id:
        return

    query = raw_query.strip().lower()
    trigger_ripple()
    play_sfx("transmit")

    if cmd_id != _current_command_id:
        return

    _safe_ui_update(lambda: terminal_feed_user(raw_query))
    _safe_ui_update(lambda: set_status("◈  PROCESSING TELEMETRY...", C["amber"]))
    _anim["processing"] = True

    # ── Wake Word Calling & Prefix Stripping ──────────────────────
    is_wake, is_standalone, cleaned_query, is_hi = parse_wake_word_query(raw_query)
    if is_wake and is_standalone:
        activate_wake_greeting(is_hindi=is_hi)
        _finish_command(cmd_id)
        return
    elif is_wake and cleaned_query:
        raw_query = cleaned_query
        query = raw_query.strip().lower()

    # ── Intelligent Command Normalization & Padding Stripping ─────
    norm_q = normalize_voice_command(raw_query)
    if norm_q:
        raw_query = norm_q
        query = norm_q.lower()

    # ── Ambient Wake Word Control Commands ────────────────────────
    if any(k in query for k in ("enable wake word", "turn on wake word", "wake word on", "activate wake word", "hands free on", "hands free mode on")):
        play_sfx("switch")
        hud_config["wake_word_enabled"] = True
        save_config()
        update_wake_button_ui()
        terminal_feed_log("CONFIG", "Ambient Wake Word detection ENABLED. Say 'Jarvis' or 'Hey Jarvis' to activate.")
        speak("Ambient wake word detection enabled, sir. Call Jarvis anytime to begin.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    if any(k in query for k in ("disable wake word", "turn off wake word", "wake word off", "deactivate wake word", "mute wake word", "hands free off")):
        play_sfx("switch")
        hud_config["wake_word_enabled"] = False
        save_config()
        update_wake_button_ui()
        terminal_feed_log("CONFIG", "Ambient Wake Word detection MUTED.")
        speak("Ambient wake word detection has been muted, sir.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # ── Explicit Stop / Cancel / Terminate Commands ──────────────
    if query in ("stop", "cancel", "terminate", "quiet", "shut up", "abort", "halt", "pause", "chup", "shant", "ruko") or any(
        query.startswith(k) for k in ("stop listening", "stop talking", "stop speaking", "cancel command", "terminate command", "ruko", "shant raho")
    ) or any(k in raw_query for k in ("रुको", "चुप रहो", "शांत रहो", "बंद करो")):
        terminate_previous_command(reason="Explicit user stop command")
        play_sfx("ack")
        terminal_feed_log("COMMAND", "All active tasks, telemetry, and speech terminated by user request.")
        speak("Standing by, sir.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # ── Fast Precision Math Evaluation (< 1ms Local Engine) ────────
    math_res = evaluate_math_expression(raw_query)
    if math_res and math_res.get("found"):
        if cmd_id != _current_command_id:
            return
        play_sfx("ack")
        terminal_feed_intel("MATH CORE", f"PRECISION EVALUATION // {math_res['expr']}", math_res["full_text"])
        _anim["last_answer"] = f"Result of {math_res['expr']} is {math_res['result']}"
        speak(math_res["speech_text"], cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # ── Fast Conversational Dialogue (< 1ms Local Intent Engine) ───
    conv_resp = check_conversational_query(raw_query)
    if conv_resp:
        if cmd_id != _current_command_id:
            return
        play_sfx("ack")
        is_hi_conv = is_devanagari(raw_query) or is_hindi_intent_or_phrase(raw_query)
        tag = "संवाद" if is_hi_conv else "CONVERSATIONAL"
        terminal_feed_intel("AI ASSISTANT", f"{tag} // DIALOGUE", conv_resp)
        _anim["last_answer"] = conv_resp
        speak(conv_resp, cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # ── Language Ingestion Mode Commands ──────────────────────────
    if any(k in query for k in (
        "switch to hindi", "hindi mode", "speak in hindi", "talk in hindi",
        "activate hindi", "hindi language", "hindi me baat karo", "hindi mein baat karo"
    )) or any(k in raw_query for k in ("हिंदी में बात करो", "हिंदी मोड", "हिंदी भाषा", "हिंदी चुनो", "हिंदी सक्रिय करो")):
        play_sfx("switch")
        hud_config["input_language"] = "hi"
        save_config()
        if "lang_btn" in globals() and lang_btn:
            _safe_ui_update(lambda: lang_btn.config(text=get_lang_button_text()))
        terminal_feed_log("LANGUAGE", "Hindi Exclusive Mode active (hi-IN). हिंदी मोड सक्रिय कर दिया गया है।")
        speak("हिंदी भाषा मोड सक्रिय कर दिया गया है, महोदय। अब मैं हिंदी में आपके आदेश सुनने के लिए तैयार हूँ।", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    if any(k in query for k in (
        "switch to english", "english mode", "speak in english", "talk in english",
        "activate english", "english language", "english me baat karo"
    )) or any(k in raw_query for k in ("अंग्रेजी में बात करो", "अंग्रेजी मोड", "इंग्लिश मोड", "इंग्लिश भाषा")):
        play_sfx("switch")
        hud_config["input_language"] = "en"
        save_config()
        if "lang_btn" in globals() and lang_btn:
            _safe_ui_update(lambda: lang_btn.config(text=get_lang_button_text()))
        terminal_feed_log("LANGUAGE", "English Exclusive Mode active (en-IN).")
        speak("English language mode activated, sir. Ready for your instructions.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    if any(k in query for k in (
        "switch to dual", "dual mode", "dual language", "bilingual mode",
        "auto language", "switch to auto", "hindi and english", "both languages"
    )) or any(k in raw_query for k in ("दोनों भाषाएं", "द्विभाषी मोड", "ऑटो मोड", "हिंदी और अंग्रेजी")):
        play_sfx("switch")
        hud_config["input_language"] = "auto"
        save_config()
        if "lang_btn" in globals() and lang_btn:
            _safe_ui_update(lambda: lang_btn.config(text=get_lang_button_text()))
        terminal_feed_log("LANGUAGE", "Bilingual Dual Mode (Hindi + English) active. Listening for both languages.")
        speak("Dual language mode active, sir. I can now seamlessly understand both Hindi and English inputs.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # Voice Profile Switch Commands
    if any(k in query for k in (
        "change voice", "switch voice", "switch the voice", "change the voice",
        "switch to female voice", "switch to female", "female voice",
        "switch to male voice", "switch to male", "male voice",
        "switch to zira", "switch to david", "switch to friday", "switch to jarvis",
        "voice zira", "voice david", "voice friday", "voice jarvis",
        "zira voice", "david voice", "friday voice", "jarvis voice",
        "alternate voice", "toggle voice"
    )):
        switch_voice_by_query(query, speak_confirm=True, cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # Audition / Preview Voice Command
    if any(k in query for k in ("preview voice", "test voice", "audition voice", "voice test", "voice preview")):
        voices = get_available_voices()
        cur_idx = hud_config.get("voice_index", 0)
        vinfo = voices[cur_idx] if cur_idx < len(voices) else voices[0]
        sample = (
            "F.R.I.D.A.Y neural core active. All systems, sensors, and telemetry ready for your command, sir."
            if vinfo["is_female"] else
            "J.A.R.V.I.S tactical core active. Ready for your instruction, sir."
        )
        terminal_feed_log("VOICE", f"Auditioning active voice: {vinfo['alias']} ({vinfo['name']})")
        speak(sample, cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # Cybernetic Sound Effects Commands
    if any(k in query for k in ("enable sound effects", "enable sfx", "turn on sound effects", "turn on sfx", "unmute sound effects", "unmute sfx")):
        hud_config["sfx_enabled"] = True
        save_config()
        play_sfx("switch", force=True)
        terminal_feed_log("AUDIO", "Cybernetic sound effects suite enabled.")
        speak("Cybernetic sound effects have been activated.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    if any(k in query for k in ("disable sound effects", "disable sfx", "turn off sound effects", "turn off sfx", "mute sound effects", "mute sfx")):
        hud_config["sfx_enabled"] = False
        save_config()
        terminal_feed_log("AUDIO", "Cybernetic sound effects suite muted.")
        speak("Cybernetic sound effects have been muted.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    if any(k in query for k in ("open voice lab", "open audio lab", "voice lab", "audio lab", "voice settings", "audio settings", "open ai lab", "ai lab", "ai settings", "model settings")):
        root.after(0, open_voice_audio_modal)
        speak("Opening Voice, Audio, and AI Neural Model Lab.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # AI Neural Model Provider & Key Commands
    if any(k in query for k in ("set ai key", "set api key", "save ai key", "set groq key", "set gemini key", "set openai key")):
        parts = raw_query.strip().split()
        if len(parts) >= 4:
            new_key = parts[-1].strip()
            hud_config["ai_api_key"] = new_key
            if "groq" in query or new_key.startswith("gsk_"):
                hud_config["ai_provider"] = "groq"
            elif "gemini" in query or new_key.startswith("AIza"):
                hud_config["ai_provider"] = "gemini"
            elif "openai" in query or new_key.startswith("sk-"):
                hud_config["ai_provider"] = "openai"
            save_config()
            play_sfx("ack")
            terminal_feed_log("AI CORE", f"AI API Key updated. Active Provider: {hud_config['ai_provider'].upper()}")
            speak(f"AI neural model API key saved. Active provider set to {hud_config['ai_provider']}.", cmd_id=cmd_id)
            _finish_command(cmd_id)
            return

    if any(k in query for k in ("switch model to", "set model to", "switch ai to", "use model", "ai model")):
        if "groq" in query:
            hud_config["ai_provider"] = "groq"
            hud_config["ai_model"] = "llama-3.3-70b-versatile"
            save_config()
            play_sfx("switch")
            speak("Switched AI neural model provider to Groq with Llama 3.3 70B.", cmd_id=cmd_id)
            _finish_command(cmd_id)
            return
        elif "gemini" in query:
            hud_config["ai_provider"] = "gemini"
            hud_config["ai_model"] = "gemini-2.0-flash"
            save_config()
            play_sfx("switch")
            speak("Switched AI neural model provider to Google Gemini 2.0 Flash.", cmd_id=cmd_id)
            _finish_command(cmd_id)
            return
        elif "openai" in query or "chatgpt" in query:
            hud_config["ai_provider"] = "openai"
            hud_config["ai_model"] = "gpt-4o-mini"
            save_config()
            play_sfx("switch")
            speak("Switched AI neural model provider to OpenAI GPT 4o mini.", cmd_id=cmd_id)
            _finish_command(cmd_id)
            return
        elif "ollama" in query or "local model" in query:
            hud_config["ai_provider"] = "ollama"
            save_config()
            play_sfx("switch")
            speak("Switched AI neural model provider to local offline Ollama.", cmd_id=cmd_id)
            _finish_command(cmd_id)
            return

    if query in ("test ai model", "test ai", "test neural model", "check ai link"):
        test_res = query_ai_model("Hello, confirm J.A.R.V.I.S neural core link in one sentence.")
        if test_res and test_res.get("found"):
            play_sfx("downlink")
            terminal_feed_log("AI CORE", f"AI Model Link Verified: {test_res['source']}")
            speak(f"AI neural link verified online via {test_res['source']}.", cmd_id=cmd_id)
        else:
            play_sfx("alert")
            speak("AI neural link test failed or no API key is configured. Hybrid offline telemetry is active.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # Multilingual Language Engine Controls (Voice & Text)
    if any(k in query for k in (
        "switch to hindi", "hindi mode", "set language to hindi", "speak in hindi", "talk in hindi",
        "hindi me baat karo", "hindi bolo", "hindi bhasha", "hindi mode chalu karo"
    )) or any(k in raw_query for k in ("हिंदी में बात करो", "हिंदी मोड", "हिंदी भाषा", "हिंदी बोलो", "हिंदी मोड चालू करो")):
        play_sfx("switch")
        hud_config["input_language"] = "hi"
        save_config()
        _safe_ui_update(lambda: update_lang_button_ui())
        _safe_ui_update(lambda: set_substatus("Input: HINDI (hi-IN)"))
        terminal_feed_log("CONFIG", "Language Mode shifted to HINDI EXCLUSIVE (hi-IN).")
        speak("हिंदी भाषा मोड सक्रिय कर दिया गया है। अब आप हिंदी में आदेश दे सकते हैं।", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    if any(k in query for k in (
        "switch to english", "english mode", "set language to english", "speak in english",
        "talk in english", "angrezi mode", "english me baat karo", "english bolo"
    )) or any(k in raw_query for k in ("अंग्रेजी मोड", "इंग्लिश मोड", "अंग्रेजी में बात करो", "इंग्लिश बोलो")):
        play_sfx("switch")
        hud_config["input_language"] = "en"
        save_config()
        _safe_ui_update(lambda: update_lang_button_ui())
        _safe_ui_update(lambda: set_substatus("Input: ENGLISH (en-IN)"))
        terminal_feed_log("CONFIG", "Language Mode shifted to ENGLISH EXCLUSIVE (en-IN).")
        speak("Language mode set to English exclusive. All inputs will be recognized in English.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    if any(k in query for k in (
        "dual language", "bilingual mode", "auto language", "switch to dual language",
        "switch to dual mode", "switch to bilingual", "hindi aur english", "dono bhasha"
    )) or any(k in raw_query for k in ("बायलिंगुअल मोड", "दोनों भाषाएं", "हिंदी और अंग्रेजी", "ड्यूल मोड")):
        play_sfx("switch")
        hud_config["input_language"] = "auto"
        save_config()
        _safe_ui_update(lambda: update_lang_button_ui())
        _safe_ui_update(lambda: set_substatus("Input: DUAL (HI/EN)"))
        terminal_feed_log("CONFIG", "Language Mode shifted to DUAL AUTO (Hindi + English).")
        speak("Bilingual dual recognition engine activated. You may speak in both Hindi and English.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # ElevenLabs Neural Voice Commands
    if any(k in query for k in ("download voice", "download elevenlabs voice", "download eleven labs voice", "download eleven labs", "download adam voice", "download voice sample")):
        play_sfx("downlink")
        terminal_feed_log("VOICE", "Downloading ElevenLabs voice IRHApOXLvnW57QJPQH2P (Adam)...")
        speak("Downloading ElevenLabs voice profile Adam, Voice ID IRHApOXLvnW57QJPQH2P.", cmd_id=cmd_id)
        def _bg_dl(captured_id=cmd_id):
            succ, meta, path, msg = download_elevenlabs_voice("IRHApOXLvnW57QJPQH2P")
            if captured_id != _current_command_id:
                return
            if succ:
                terminal_feed_log("VOICE", f"ElevenLabs Voice Downloaded: {meta.get('name', 'Adam')}")
                speak("ElevenLabs voice profile Adam downloaded successfully. Auditioning downloaded sample now.", cmd_id=captured_id)
                _time.sleep(0.5)
                if captured_id == _current_command_id:
                    audition_elevenlabs_voice("IRHApOXLvnW57QJPQH2P")
            else:
                terminal_feed_log("VOICE", f"Download failed: {msg}")
                speak(f"Voice download failed. Reason: {msg}", cmd_id=captured_id)
        threading.Thread(target=_bg_dl, daemon=True).start()
        _finish_command(cmd_id)
        return

    if any(k in query for k in ("audition elevenlabs", "audition eleven labs", "audition adam", "play elevenlabs", "play eleven labs", "play voice sample", "audition voice sample", "play adam voice")):
        play_sfx("ack")
        audition_elevenlabs_voice("IRHApOXLvnW57QJPQH2P")
        _finish_command(cmd_id)
        return

    if any(k in query for k in ("switch to elevenlabs", "use elevenlabs", "switch to eleven labs", "use eleven labs", "switch to adam voice", "switch to adam", "activate elevenlabs")):
        play_sfx("switch")
        hud_config["tts_engine"] = "elevenlabs"
        save_config()
        el_key = hud_config.get("elevenlabs_api_key", "").strip()
        if el_key:
            terminal_feed_log("VOICE", "ElevenLabs Neural Voice Core Activated.")
            speak("ElevenLabs neural voice engine activated with voice ID IRHApOXLvnW57QJPQH2P.", cmd_id=cmd_id)
        else:
            terminal_feed_log("VOICE", "ElevenLabs Voice Selected (Sample downloaded). API key required for live TTS.")
            speak("ElevenLabs voice profile Adam is selected. Voice sample is downloaded and ready. To generate dynamic live speech, please add your ElevenLabs API key in the Voice Lab modal. Offline speech will continue using Microsoft David.", cmd_id=cmd_id)
            _time.sleep(0.5)
            if cmd_id == _current_command_id:
                audition_elevenlabs_voice("IRHApOXLvnW57QJPQH2P")
        _finish_command(cmd_id)
        return

    if any(k in query for k in ("switch to sapi", "switch to windows voice", "switch to offline voice", "use sapi", "use offline voice")):
        play_sfx("switch")
        hud_config["tts_engine"] = "sapi"
        save_config()
        terminal_feed_log("VOICE", "Speech engine shifted to Windows offline SAPI.")
        speak("Speech engine switched to Windows offline voice.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # Voice Input Capture Timeout Control Commands
    if any(k in query for k in (
        "voice timeout", "input timeout", "mic timeout", "listening timeout",
        "set timeout to", "change timeout to", "increase timeout", "decrease timeout",
        "timeout badhao", "timeout kam karo"
    )):
        nums = re.findall(r"\d+", query)
        cur_to = float(hud_config.get("voice_input_timeout", 10.0))
        if nums:
            new_to = max(4.0, min(30.0, float(nums[0])))
        elif any(k in query for k in ("increase", "more", "longer", "badhao")):
            new_to = min(30.0, cur_to + 3.0)
        elif any(k in query for k in ("decrease", "less", "shorter", "kam")):
            new_to = max(4.0, cur_to - 3.0)
        else:
            new_to = 10.0
        hud_config["voice_input_timeout"] = new_to
        save_config()
        play_sfx("ack")
        terminal_feed_log("CONFIG", f"Voice input listening timeout set to {new_to:.1f} seconds.")
        if is_hi_query or "badhao" in query or "kam" in query:
            speak(f"वॉइस इनपुट टाइमआउट {int(new_to)} सेकंड पर सेट कर दिया गया है।", cmd_id=cmd_id)
        else:
            speak(f"Voice input listening timeout has been set to {int(new_to)} seconds.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # Tactical Military Radio & Emergency Alerts
    if any(k in query for k in (
        "military radio", "tactical radio", "man down", "we have a man down",
        "radio comms", "tactical comms", "combat comms", "emergency radio",
        "red alert", "tactical alert", "combat alert"
    )):
        play_sfx("tactical_radio", force=True)
        terminal_feed_log("COMMS", "TACTICAL COMBAT COMMS: 'We have a man down!' (US Military Radio)")
        trigger_ripple()
        _safe_ui_update(lambda: set_status("⚠️  TACTICAL COMBAT COMMS ACTIVE", C.get("amber", "#ffaa00")))
        _time.sleep(1.8)
        if cmd_id != _current_command_id:
            return
        speak("Tactical military radio transmission received. Emergency alert broadcast acknowledged, sir.", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    is_hi_query = is_devanagari(raw_query) or is_hindi_intent_or_phrase(raw_query)

    # Volume
    if any(k in query for k in (
        "volume up", "increase volume", "volume increase", "turn up volume", "turn volume up",
        "raise volume", "make it louder", "louder", "aawaz badhao", "sound badhao", "volume badhao", "aawaz tej karo"
    )) or any(k in raw_query for k in ("आवाज बढ़ाओ", "आवाज तेज करो", "वॉल्यूम बढ़ाओ", "साउंड बढ़ाओ", "आवाज ज्यादा करो", "वॉल्यूम तेज करो")):
        play_sfx("ack")
        volume_up()
        if is_hi_query:
            speak("आवाज बढ़ा दी गई है, महोदय।", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return
    if any(k in query for k in (
        "volume down", "decrease volume", "volume decrease", "turn down volume", "turn volume down",
        "lower volume", "make it quiet", "quieter", "aawaz kam karo", "sound kam karo", "volume kam karo", "aawaz dheemi karo"
    )) or any(k in raw_query for k in ("आवाज कम करो", "आवाज धीमी करो", "वॉल्यूम कम करो", "साउंड कम करो", "आवाज घटाओ")):
        play_sfx("ack")
        volume_down()
        if is_hi_query:
            speak("आवाज कम कर दी गई है, महोदय।", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return
    if query == "mute" or "mute volume" in query or any(k in query for k in ("mute karo", "aawaz band karo", "chup raho", "chup ho jao", "shant raho", "mute audio", "silence")) or any(k in raw_query for k in ("म्यूट करो", "आवाज बंद करो", "शांत रहो", "चुप रहो", "खामोश रहो")):
        play_sfx("ack")
        volume_mute()
        if is_hi_query:
            speak("ऑडियो म्यूट कर दिया गया है।", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # Brightness
    if any(k in query for k in (
        "increase brightness", "brightness increase", "brightness up", "turn up brightness", "turn brightness up",
        "raise brightness", "make screen brighter", "brighter", "brightness badhao", "roshni badhao"
    )) or any(k in raw_query for k in ("ब्राइटनेस बढ़ाओ", "रोशनी बढ़ाओ", "स्क्रीन की रोशनी तेज करो", "ब्राइटनेस तेज करो")):
        play_sfx("ack")
        cur = get_brightness()
        if cur is not None: set_brightness(min(100, cur + 10))
        if is_hi_query or "roshni" in query or "badhao" in query:
            speak("स्क्रीन ब्राइटनेस बढ़ा दी गई है।", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return
    if any(k in query for k in (
        "decrease brightness", "brightness decrease", "brightness down", "turn down brightness", "turn brightness down",
        "lower brightness", "dim screen", "darker", "dimmer", "brightness kam karo", "roshni kam karo"
    )) or any(k in raw_query for k in ("ब्राइटनेस कम करो", "रोशनी कम करो", "स्क्रीन की रोशनी धीमी करो", "स्क्रीन ब्राइटनेस कम करो")):
        play_sfx("ack")
        cur = get_brightness()
        if cur is not None: set_brightness(max(0, cur - 10))
        if is_hi_query or "roshni" in query or "kam karo" in query:
            speak("स्क्रीन ब्राइटनेस कम कर दी गई है।", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return
    if "set brightness" in query or ("brightness" in query and "karo" in query) or ("ब्राइटनेस" in raw_query and ("करो" in raw_query or "प्रतिशत" in raw_query)):
        play_sfx("ack")
        nums = re.findall(r"\d+", raw_query)
        if nums:
            val = int(nums[0])
            set_brightness(val)
            if is_hi_query or "karo" in query:
                speak(f"ब्राइटनेस {val} प्रतिशत पर सेट कर दी गई है।", cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # Universal Internet Web Navigation Engine
    if (
        any(query.startswith(pfx) for pfx in ("open ", "launch ", "go to ", "navigate to ", "browse to ", "browse ", "visit ", "access ", "kholo ", "open karo "))
        or any(raw_query.endswith(sfx) for sfx in ("खोलो", "ओपन करो", "वेबसाइट खोलो", "साइट खोलो"))
        or any(raw_query.startswith(pfx) for pfx in ("खोलो ", "ओपन करो "))
        or re.search(r"\b(?:open|launch|go to|navigate to|browse to|browse|visit|access|kholo|open\s+karo)\s+(?:the\s+)?(?:website|site|portal)\b", query)
        or re.search(r"^(?:https?:\/\/)?(?:[a-zA-Z0-9-]+\.)+(?:com|org|net|io|in|edu|gov|ai|co|tv|app|dev|me)(?:\/.*)?$", query)
    ):
        # Exclude commands handled specifically elsewhere
        if not any(ex in query for ex in (
            "voice lab", "audio lab", "voice settings", "audio settings",
            "open youtube and play", "and play on youtube", "play on youtube",
            "open spotify and play", "and play on spotify", "play on spotify", "play in spotify"
        )) and not any(ex in raw_query for ex in ("यूट्यूब पर", "यूट्यूब में", "चलाओ", "बजाओ", "स्पॉटिफ़ाई पर", "स्पॉटिफ़ाई में")):
            succ, msg = resolve_and_open_website(raw_query, cmd_id=cmd_id)
            if succ:
                _finish_command(cmd_id)
                return

    # Chronometer / Time Query (12-Hour Format)
    if any(k in query for k in (
        "what is the time", "what's the time", "whats the time", "tell me the time",
        "what time is it", "current time", "samay kya hua hai", "time kya hua hai",
        "kitne baje hai", "samay batao", "time batao", "kya time ho raha hai", "waqt kya hai"
    )) or query in ("time", "samay", "समय", "टाइम") or any(k in raw_query for k in (
        "समय क्या हुआ है", "समय क्या है", "टाइम क्या हुआ है", "टाइम क्या है",
        "कितने बजे हैं", "समय बताओ", "टाइम बताओ", "वक्त क्या हुआ है", "घड़ी में क्या समय है", "समय", "टाइम"
    )):
        if cmd_id != _current_command_id:
            return
        time_12 = _time.strftime("%I:%M %p")
        time_full = _time.strftime("%I:%M:%S %p")
        date_full = _time.strftime("%A, %d %B %Y")
        time_text = f"Current Local Time: {time_full}\nDate: {date_full}\nFormat: 12-Hour Chronometer (AM/PM)"
        if is_devanagari(raw_query) or any(w in query for w in ("samay", "kitne", "baje", "waqt")):
            time_speech = f"वर्तमान समय है {time_12}। आज {date_full} है।"
            _anim["last_answer"] = f"वर्तमान समय: {time_12} ({date_full})"
        else:
            time_speech = f"Current local time is {time_full}, on {date_full}. 12-hour chronometer mode active."
            _anim["last_answer"] = f"The current time is {time_full} on {date_full}."
        _safe_ui_update(lambda: terminal_feed_intel("CHRONOMETER", "12-HOUR TIME TELEMETRY", time_text))
        speak(time_speech, cmd_id=cmd_id)
        _finish_command(cmd_id)
        return

    # Location Configuration
    if any(k in query for k in (
        "set default location", "change default location", "save default location",
        "save my default location", "set my default location", "update default location",
        "set location to", "change location to"
    )):
        m = re.search(
            r"(?:set|change|save|update)(?:\s+my)?\s+default\s+location(?:\s+for\s+this\s+assistant)?(?:\s+to|\s+is|\s+as)?\s+([a-zA-Z\s,]+)",
            query
        )
        if not m:
            m = re.search(r"(?:set|change)\s+location\s+to\s+([a-zA-Z\s,]+)", query)
        if m:
            raw_loc = m.group(1).strip().strip(",").strip()
            if "uttar pradesh" in raw_loc.lower() and "india" in raw_loc.lower():
                new_loc = "Uttar Pradesh, India"
            else:
                new_loc = raw_loc.title()
            hud_config["default_location"] = new_loc
            save_config()
            terminal_feed_log("CONFIG", f"Default meteorological location updated to: {new_loc}")
            speak(f"Default location has been set to {new_loc}.", cmd_id=cmd_id)
            _finish_command(cmd_id)
            return

    # Weather Telemetry
    if (any(w in query for w in ("weather", "temperature", "climate", "forecast", "mausam", "tapman")) or any(w in raw_query for w in ("मौसम", "तापमान", "क्लाइमेट", "फोरकास्ट", "बारिश"))) and not query.startswith("who is"):
        loc = extract_weather_location(raw_query)
        is_hi_w = is_devanagari(raw_query) or any(w in query for w in ("mausam", "tapman"))
        weather_telemetry(loc, cmd_id=cmd_id, is_hindi=is_hi_w)
        _finish_command(cmd_id)
        return

    # News Intelligence Feed
    if any(w in query for w in ("news", "headline", "headlines", "samachar", "khabar", "khabarein")) or any(w in raw_query for w in ("समाचार", "ताज़ा खबरें", "ताज़ा समाचार", "खबरें", "न्यूज़")):
        is_hi_n = is_devanagari(raw_query) or any(w in query for w in ("samachar", "khabar", "khabarein"))
        if is_hi_n:
            news_telemetry(lang="hi", cmd_id=cmd_id)
        else:
            topic_code, topic_name, search_q = extract_news_intent(query)
            news_telemetry(topic_code, topic_name, search_q, cmd_id=cmd_id, lang="en")
        _finish_command(cmd_id)
        return

    # Spotify Music Streaming Integration
    if (
        any(w in query for w in (
            "on spotify", "in spotify", "play spotify", "spotify play",
            "open spotify and play", "search spotify"
        ))
        or (query.startswith("spotify ") and not query in ("spotify", "spotify open", "spotify kholo"))
        or any(w in raw_query for w in (
            "स्पॉटिफ़ाई पर", "स्पॉटिफ़ाई में", "स्पॉटिफ़ाई चलाओ", "स्पॉटिफ़ाई बजाओ",
            "स्पॉटिफ़ाई खोलो और चलाओ"
        ))
        or (any(w in query for w in ("spotify par", "spotify me", "spotify mein")) and any(w in query for w in ("chalao", "bajao", "sunao", "play", "gana", "song")))
    ):
        sp_q = extract_spotify_query(raw_query)
        if sp_q:
            is_hi_sp = is_devanagari(raw_query) or any(w in query for w in ("chalao", "bajao", "sunao", "gana"))
            spotify_play(sp_q, cmd_id=cmd_id, is_hindi=is_hi_sp)
            _finish_command(cmd_id)
            return

    # Universal YouTube Video Discovery & Autoplay
    if (
        any(w in query for w in (
            "play on youtube", "play in youtube", "play youtube", "youtube play",
            "search youtube", "open youtube and play", "open youtube and find", "open youtube and search",
            "youtube par", "gana chalao", "gana bajao", "song chalao", "chalao", "bajao",
            "find video", "find on youtube", "search on youtube", "watch on youtube",
            "watch video", "video dhundo", "video dikhao", "show me video", "show video"
        ))
        or query.startswith("play ")
        or query.startswith("watch ")
        or any(w in raw_query for w in (
            "यूट्यूब पर", "यूट्यूब में", "चलाओ", "बजाओ", "गाना चलाओ", "गीत चलाओ", "सुनाओ",
            "वीडियो ढूंढो", "वीडियो दिखाओ", "वीडियो चलाओ", "सर्च करो"
        ))
    ):
        yt_q = extract_youtube_query(raw_query)
        if yt_q:
            is_hi_yt = is_devanagari(raw_query) or any(w in query for w in ("chalao", "bajao", "gana", "dhundo", "dikhao"))
            youtube_play(yt_q, cmd_id=cmd_id, is_hindi=is_hi_yt)
            _finish_command(cmd_id)
            return

    # Internet Intelligence Search
    if cmd_id != _current_command_id:
        return
    status_prompt = "◈  खोज जारी है..." if is_devanagari(raw_query) else "◈  QUERYING GLOBAL INTELLIGENCE..."
    _safe_ui_update(lambda: set_status(status_prompt, C["amber"]))
    data = search_internet_data(raw_query)
    if cmd_id != _current_command_id:
        return
    _anim["last_answer"] = data["full_text"]

    _safe_ui_update(lambda: terminal_feed_intel(data["source"], data["title"], data["full_text"]))
    speak(data["speech_text"], cmd_id=cmd_id)
    _finish_command(cmd_id)

def _finish_command(cmd_id=None):
    if cmd_id is not None and cmd_id != _current_command_id:
        return
    _anim["processing"] = False
    trigger_ripple()
    if not _anim.get("speaking", False) and _tts_queue.empty():
        _safe_ui_update(lambda: set_status("◎  SYSTEMS NOMINAL", C["cyan"]))

def dispatch_command(query_text):
    if not query_text or not str(query_text).strip():
        return

    # Instantly terminate previous running command and allocate new generation ID
    cmd_id = terminate_previous_command(reason=f"Dispatched: {str(query_text).strip()[:32]}")

    terminal_feed_log("COMMAND", f"Preempting previous speech. Dispatched core #{cmd_id}: {str(query_text).strip()[:32]}")
    threading.Thread(target=execute_command_thread, args=(query_text, cmd_id), daemon=True).start()

def toggle_voice_command_capture():
    """
    Main user-facing toggle for Start / Stop Listening.
    Strictly prevents multiple instances and concurrent thread loading:
    - If listening is currently active, immediately stops and cancels it.
    - If listening is inactive, starts a single, isolated capture instance.
    - Rejects rapid accidental double-clicks via a 350ms debounce window.
    """
    global _is_voice_capturing, _last_mic_click_time
    now = _time.time()
    if now - _last_mic_click_time < 0.35:
        return
    _last_mic_click_time = now

    if _is_voice_capturing:
        cancel_voice_command_capture()
    else:
        start_voice_command_capture()

def cancel_voice_command_capture():
    """Instantly cancels active voice capture and restores systems nominal."""
    global _is_voice_capturing
    _mic_abort_requested.set()
    _manual_capture_active.clear()
    _anim["listening"] = False
    _anim["processing"] = False
    _safe_ui_update(lambda: set_status("◎  VOICE INPUT STOPPED", C["cyan_dim"]))
    _safe_ui_update(lambda: set_substatus("Workstation ready. Click Start Listening or say 'Hey Jarvis'."))
    if "mic_btn" in globals() and mic_btn:
        _safe_ui_update(lambda: mic_btn.config(text="  ▶  START LISTENING  ", bg=C["cyan_dim"], fg=C["text"]))

def start_voice_command_capture():
    """Launches voice command capture within a single isolated instance without multiple loading."""
    global _is_voice_capturing
    with _voice_capture_lock:
        if _is_voice_capturing:
            return  # Single-instance guard: ignore duplicate triggers

        _is_voice_capturing = True
        _mic_abort_requested.clear()
        _manual_capture_active.set()  # Signals wake-word listener to yield within 60ms

    # Update UI immediately so the user experiences zero lag
    if "mic_btn" in globals() and mic_btn:
        _safe_ui_update(lambda: mic_btn.config(text="  ◼  STOP LISTENING  ", bg=C["red_dim"], fg=C["text"]))
    set_status("◉  OPENING AUDIO SENSORS...", C["amber"])
    set_substatus("Connecting high-sensitivity audio stream...")
    trigger_ripple()

    threading.Thread(target=_run_voice_capture_worker, daemon=True).start()

def _run_voice_capture_worker():
    global _is_voice_capturing
    try:
        # Preempt any previous speaking command so microphone input is crystal clear
        terminate_previous_command(reason="Voice capture opened")
        matrix_push_token("MIC:ACTIVE")
        matrix_push_token("VOX:STREAM")
        matrix_push_token("AGC:ONLINE")

        query = take_command()

        if query and not _mic_abort_requested.is_set():
            dispatch_command(query)
        elif not _mic_abort_requested.is_set():
            _safe_ui_update(lambda: set_status("◎  SYSTEMS NOMINAL", C["cyan"]))
            _safe_ui_update(lambda: set_substatus("Workstation ready. Standing by for command."))
    except Exception as e:
        print("[MIC CAPTURE WORKER ERROR]:", e)
        _safe_ui_update(lambda: set_status("◌  MIC CAPTURE ERROR", C["red"]))
    finally:
        with _voice_capture_lock:
            _is_voice_capturing = False
            _manual_capture_active.clear()
            _mic_abort_requested.clear()
        _anim["listening"] = False
        _anim["processing"] = False
        if "mic_btn" in globals() and mic_btn:
            _safe_ui_update(lambda: mic_btn.config(text="  ▶  START LISTENING  ", bg=C["cyan_dim"], fg=C["text"]))

def run_mic_capture_async():
    """Single-instance entry point (also used when wake word triggers standalone greeting)."""
    start_voice_command_capture()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  FRONTEND GUI INITIALIZATION                                     ║
# ╚══════════════════════════════════════════════════════════════════╝

root = tk.Tk()
root.title("J.A.R.V.I.S  ┃  Holographic Workstation & Neural HUD  v3.0")
root.geometry("1160x800")
root.minsize(960, 700)
root.configure(bg=C["void"])

root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

def _label(parent, text, sz=10, fg=None, fn=None, wt="normal", **kw):
    return tk.Label(parent, text=text, font=(fn or FN, sz, wt), fg=fg or C["text"], bg=parent.cget("bg"), **kw)

def _hud(parent, text, sz=8, fg=None):
    return tk.Label(parent, text=f"┃ {text}", font=(FN, sz, "bold"), fg=fg or C["muted"], bg=parent.cget("bg"), anchor="w")

def _sep(parent, row, col=0, span=1):
    s = tk.Frame(parent, bg=C["border"], height=1)
    s.grid(row=row, column=col, columnspan=span, sticky="ew", padx=14, pady=3)
    return s

def _lerp_color(c1, c2, t):
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{max(0,min(r,255)):02x}{max(0,min(g,255)):02x}{max(0,min(b,255)):02x}"

def set_status(text, color=None):
    if "status_label" in globals() and status_label:
        _safe_ui_update(lambda: status_label.config(text=text, fg=color or C["cyan"]))

def set_substatus(text, color=None):
    if "substatus" in globals() and substatus:
        _safe_ui_update(lambda: substatus.config(text=text, fg=color or C["text_dim"]))


def trigger_ripple():
    _anim["ripples"].append({"r": 28, "alpha": 1.0})


# ══════════════════ STARFIELD BACKGROUND CANVAS ══════════════
bg_cv = tk.Canvas(root, bg=C["void"], highlightthickness=0)
bg_cv.place(relx=0, rely=0, relwidth=1, relheight=1)

for _ in range(55):
    _anim["particles"].append({
        "x": random.randint(0, 1200),
        "y": random.randint(0, 850),
        "vx": random.uniform(-0.25, 0.25),
        "vy": random.uniform(-0.15, 0.15),
        "size": random.choice([1, 1, 1, 2, 2, 3]),
        "brightness": random.uniform(0.15, 0.6),
    })

overlay = tk.Frame(root, bg=C["void"])
overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
overlay.columnconfigure(0, weight=1)
overlay.rowconfigure(2, weight=1)


# ─── HEADER BAR (GLASSMORPHIC STYLE) ─────────────────────────
hdr = tk.Frame(overlay, bg=C["void"])
hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(10, 4))

brand = tk.Frame(hdr, bg=C["void"])
brand.pack(side="left")

mini_cv = tk.Canvas(brand, width=28, height=28, bg=C["void"], highlightthickness=0)
mini_cv.pack(side="left", padx=(0, 8))
mini_cv.create_oval(2, 2, 26, 26, outline=C["cyan"], width=2, tags="m_out")
mini_cv.create_oval(6, 6, 22, 22, fill=C["cyan_dim"], outline=C["cyan"], width=1, tags="m_mid")
mini_cv.create_oval(11, 11, 17, 17, fill=C["cyan_br"], outline="", tags="m_core")

title_brand_lbl = _label(brand, "J.A.R.V.I.S", 16, C["cyan_br"], FN, "bold")
title_brand_lbl.pack(side="left")
_label(brand, "//", 16, C["border_gl"], FN, "bold").pack(side="left", padx=(6, 6))
_label(brand, "HOLOGRAPHIC NEURAL WORKSTATION", 9, C["muted"], FN).pack(side="left", pady=(4, 0))

# Customizer Toggle Button
edit_btn = tk.Button(
    hdr, text=" ⚡ CUSTOMIZE HUD [OFF] ", font=(FN, 8, "bold"),
    bg="#071726", fg=C["text_dim"], activebackground=C["border_gl"], activeforeground=C["cyan_br"],
    bd=0, padx=12, pady=5, cursor="hand2", command=lambda: toggle_customizer(),
)
edit_btn.pack(side="left", padx=(18, 0))

voice_lab_btn = tk.Button(
    hdr, text=" 🎙️ VOICE & AUDIO LAB ", font=(FN, 8, "bold"),
    bg="#071726", fg=C["cyan_br"], activebackground=C["border_gl"], activeforeground=C["white"],
    bd=0, padx=12, pady=5, cursor="hand2", command=lambda: open_voice_audio_modal(),
)
voice_lab_btn.pack(side="left", padx=(8, 0))

info = tk.Frame(hdr, bg=C["void"])
info.pack(side="right")

date_lbl = tk.Label(info, text="", font=(FN, 8), fg=C["muted"], bg=C["void"])
date_lbl.pack(side="left", padx=(0, 12))

clock_lbl = tk.Label(info, text="12 : 00 : 00 AM", font=(FN, 11, "bold"), fg=C["cyan_dim"], bg=C["void"])
clock_lbl.pack(side="left", padx=(0, 12))

dot_cv = tk.Canvas(info, width=10, height=10, bg=C["void"], highlightthickness=0)
dot_cv.pack(side="left", padx=(0, 6))
dot_cv.create_oval(2, 2, 8, 8, fill=C["green"], outline=C["green_dim"], width=1, tags="dot")

online_lbl = _label(info, "CORE ONLINE", 8, C["green"], FN, "bold")
online_lbl.pack(side="left")

hdr_sep = tk.Canvas(overlay, height=2, bg=C["void"], highlightthickness=0)
hdr_sep.grid(row=0, column=0, sticky="sew", padx=16)
hdr_sep.bind("<Configure>", lambda e: _draw_hdr_sep())

def _draw_hdr_sep():
    hdr_sep.delete("all")
    w = hdr_sep.winfo_width()
    hdr_sep.create_line(0, 1, w, 1, fill=C["border"], width=1)
    mid = w // 2
    hdr_sep.create_line(mid - 140, 0, mid + 140, 0, fill=C["border_gl"], width=2)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  HUD CUSTOMIZATION DRAWER                                        ║
# ╚══════════════════════════════════════════════════════════════════╝

customizer_drawer = tk.Frame(overlay, bg="#020812", highlightbackground=C["border_gl"], highlightthickness=1)
customizer_drawer.columnconfigure(0, weight=1)

drawer_content = tk.Frame(customizer_drawer, bg="#020812", padx=14, pady=8)
drawer_content.grid(row=0, column=0, sticky="ew")
drawer_content.columnconfigure(0, weight=3)
drawer_content.columnconfigure(1, weight=3)
drawer_content.columnconfigure(2, weight=4)
drawer_content.columnconfigure(3, weight=2)

# Theme Palette Box
theme_box = tk.Frame(drawer_content, bg="#040e1a", padx=8, pady=6, highlightbackground=C["border"], highlightthickness=1)
theme_box.grid(row=0, column=0, sticky="nsew", padx=3)
_label(theme_box, "🎨 COLOR THEME MORPHER", 8, C["amber"], FN, "bold").pack(anchor="w", pady=(0, 4))
theme_btn_frame = tk.Frame(theme_box, bg="#040e1a")
theme_btn_frame.pack(fill="x")
for tk_id, tdata in THEMES.items():
    tk.Button(
        theme_btn_frame, text=f"◈ {tk_id.upper()}", font=(FN, 7, "bold"),
        bg=tdata["border"], fg=tdata["cyan_br"], bd=0, padx=5, pady=2, cursor="hand2",
        command=lambda t=tk_id: apply_theme(t),
    ).pack(side="left", padx=1)

# Position Presets Box
layout_box = tk.Frame(drawer_content, bg="#040e1a", padx=8, pady=6, highlightbackground=C["border"], highlightthickness=1)
layout_box.grid(row=0, column=1, sticky="nsew", padx=3)
_label(layout_box, "📐 POSITION PRESETS", 8, C["amber"], FN, "bold").pack(anchor="w", pady=(0, 4))
layout_btn_frame = tk.Frame(layout_box, bg="#040e1a")
layout_btn_frame.pack(fill="x")

def apply_preset(order):
    hud_config["column_order"] = list(order)
    regrid_all_panels()
    save_config()

tk.Button(layout_btn_frame, text="⊞ DEFAULT", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, padx=5, pady=2, cursor="hand2", command=lambda: apply_preset(["lp", "cp", "rp"])).pack(side="left", padx=1)
tk.Button(layout_btn_frame, text="◫ INTEL-LEFT", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, padx=5, pady=2, cursor="hand2", command=lambda: apply_preset(["cp", "lp", "rp"])).pack(side="left", padx=1)
tk.Button(layout_btn_frame, text="⇄ SWAP SIDES", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, padx=5, pady=2, cursor="hand2", command=lambda: swap_side_panels()).pack(side="left", padx=1)

def swap_side_panels():
    order = hud_config["column_order"]
    if len(order) == 3:
        order[0], order[2] = order[2], order[0]
        regrid_all_panels()
        save_config()

# Module Visibility Box
toggles_box = tk.Frame(drawer_content, bg="#040e1a", padx=8, pady=6, highlightbackground=C["border"], highlightthickness=1)
toggles_box.grid(row=0, column=2, sticky="nsew", padx=3)
_label(toggles_box, "🎛️ MODULE VISIBILITY", 8, C["amber"], FN, "bold").pack(anchor="w", pady=(0, 3))
check_frame = tk.Frame(toggles_box, bg="#040e1a")
check_frame.pack(fill="x")
module_vars = {}
for m_key, m_name in (
    ("lp", "Reactor"), ("cp", "Terminal"), ("rp", "Data Rain"),
    ("wave", "Waveform"), ("quick", "Quick Deck"), ("hardware", "Controls")
):
    var = tk.BooleanVar(value=hud_config["visible"].get(m_key, True))
    module_vars[m_key] = var
    cb = tk.Checkbutton(
        check_frame, text=m_name, variable=var, font=(FN, 7),
        bg="#040e1a", fg=C["text"], selectcolor="#082438", activebackground="#040e1a",
        command=lambda k=m_key, v=var: toggle_module_visibility(k, v.get()),
    )
    cb.pack(side="left", padx=1)

def toggle_module_visibility(module_key, is_visible):
    hud_config["visible"][module_key] = is_visible
    if module_key in ("lp", "cp", "rp"): regrid_all_panels()
    else: regrid_center_modules()
    save_config()

# Action Profile Box
actions_box = tk.Frame(drawer_content, bg="#040e1a", padx=8, pady=6, highlightbackground=C["border"], highlightthickness=1)
actions_box.grid(row=0, column=3, sticky="nsew", padx=3)
_label(actions_box, "💾 HUD PROFILE", 8, C["amber"], FN, "bold").pack(anchor="w", pady=(0, 4))
act_btn_frame = tk.Frame(actions_box, bg="#040e1a")
act_btn_frame.pack(fill="x")
tk.Button(act_btn_frame, text="✎ SHORTCUTS", font=(FN, 7), bg=C["border_gl"], fg=C["text"], bd=0, padx=5, pady=2, cursor="hand2", command=lambda: open_shortcut_editor()).pack(side="left", padx=1)
tk.Button(act_btn_frame, text="🎙️ VOICE LAB", font=(FN, 7), bg=C["panel"], fg=C["cyan_br"], bd=0, padx=5, pady=2, cursor="hand2", command=lambda: open_voice_audio_modal()).pack(side="left", padx=1)
tk.Button(act_btn_frame, text="↺ RESET", font=(FN, 7), bg=C["red_dim"], fg=C["text"], bd=0, padx=5, pady=2, cursor="hand2", command=lambda: reset_to_default_layout()).pack(side="left", padx=1)

def toggle_customizer():
    _anim["edit_mode"] = not _anim["edit_mode"]
    if _anim["edit_mode"]:
        customizer_drawer.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 6))
        edit_btn.config(text=" ⚡ CUSTOMIZE HUD [ACTIVE] ", bg=C["amber_dim"], fg=C["amber"])
        set_status("◈  HUD CUSTOMIZER ACTIVE — REPOSITION MODULES", C["amber"])
    else:
        customizer_drawer.grid_remove()
        edit_btn.config(text=" ⚡ CUSTOMIZE HUD [OFF] ", bg="#071726", fg=C["text_dim"])
        set_status("◎  SYSTEMS NOMINAL", C["cyan"])
    for strip in panel_control_strips.values():
        if _anim["edit_mode"]: strip.grid()
        else: strip.grid_remove()


# ─── MAIN 3-PANEL DISPLAY CONTAINER ──────────────────────────
main = tk.Frame(overlay, bg=C["void"])
main.grid(row=2, column=0, sticky="nsew", padx=16, pady=(2, 0))
main.rowconfigure(0, weight=1)

panels = {}
panel_control_strips = {}
panel_weights = {"lp": 3, "cp": 6, "rp": 2}


# ═══════════════════════ LEFT PANEL: HOLOGRAPHIC ARC REACTOR ═
lp = tk.Frame(main, bg=C["surface"], highlightbackground=C["border"], highlightthickness=1)
panels["lp"] = lp
lp.columnconfigure(0, weight=1)

lp_strip = tk.Frame(lp, bg="#020912", highlightbackground=C["border_gl"], highlightthickness=1)
panel_control_strips["lp"] = lp_strip
lp_strip.grid(row=0, column=0, sticky="ew", padx=4, pady=2)
_label(lp_strip, "⠿ ARC REACTOR", 8, C["amber"], FN, "bold").pack(side="left", padx=4)
tk.Button(lp_strip, text="◀", font=(FN, 7), bg=C["panel"], fg=C["text"], bd=0, command=lambda: shift_panel("lp", -1)).pack(side="right", padx=1)
tk.Button(lp_strip, text="▶", font=(FN, 7), bg=C["panel"], fg=C["text"], bd=0, command=lambda: shift_panel("lp", 1)).pack(side="right", padx=1)
lp_strip.grid_remove()

_hud(lp, "CORE STATUS & REACTOR").grid(row=1, column=0, sticky="w", padx=14, pady=(6, 0))

lp.rowconfigure(2, weight=1)
reactor_cv = tk.Canvas(lp, bg=C["surface"], highlightthickness=0)
reactor_cv.grid(row=2, column=0, sticky="nsew", padx=6, pady=(0, 0))

status_label = _label(lp, "◎  INITIALIZING...", 11, C["cyan"], FN, "bold")
status_label.grid(row=3, column=0, pady=(2, 1))

substatus = _label(lp, "Running system diagnostics", 8, C["text_dim"], FN)
substatus.grid(row=4, column=0, pady=(0, 6))

mic_btn = tk.Button(
    lp, text="  ▶  START LISTENING  ",
    font=(FN, 10, "bold"), bg=C["cyan_dim"], fg=C["text"],
    activebackground=C["cyan"], activeforeground=C["void"],
    bd=0, padx=14, pady=8, cursor="hand2",
    command=toggle_voice_command_capture,
)
mic_btn.grid(row=5, column=0, sticky="ew", padx=14, pady=(0, 6))

def _mic_enter(e):
    if _is_voice_capturing or _anim.get("listening"):
        mic_btn.config(bg=C["red"], fg=C["text"])
    else:
        mic_btn.config(bg=C["cyan"], fg=C["void"])

def _mic_leave(e):
    if _is_voice_capturing or _anim.get("listening"):
        mic_btn.config(bg=C["red_dim"], fg=C["text"])
    else:
        mic_btn.config(bg=C["cyan_dim"], fg=C["text"])

mic_btn.bind("<Enter>", _mic_enter)
mic_btn.bind("<Leave>", _mic_leave)

def get_lang_button_text():
    mode = hud_config.get("input_language", "auto")
    if mode == "auto":
        return "🌐 LANG: DUAL (HI/EN)"
    elif mode == "hi":
        return "🌐 LANG: HINDI (hi-IN)"
    else:
        return "🌐 LANG: ENGLISH (en-IN)"

def update_lang_button_ui():
    if "lang_btn" in globals() and lang_btn:
        lang_btn.config(text=get_lang_button_text())

def cycle_input_language():
    play_sfx("switch")
    current = hud_config.get("input_language", "auto")
    if current == "auto":
        new_lang = "hi"
    elif current == "hi":
        new_lang = "en"
    else:
        new_lang = "auto"
    hud_config["input_language"] = new_lang
    save_config()
    update_lang_button_ui()
    if new_lang == "auto":
        terminal_feed_log("CONFIG", "Language Mode set to DUAL AUTO (Hindi + English).")
        set_substatus("Input: DUAL (HI/EN)")
        speak("Bilingual dual recognition active. Hindi and English supported.")
    elif new_lang == "hi":
        terminal_feed_log("CONFIG", "Language Mode set to HINDI EXCLUSIVE (hi-IN).")
        set_substatus("Input: HINDI (hi-IN)")
        speak("हिंदी भाषा मोड सक्रिय।")
    else:
        terminal_feed_log("CONFIG", "Language Mode set to ENGLISH EXCLUSIVE (en-IN).")
        set_substatus("Input: ENGLISH (en-IN)")
        speak("English exclusive mode active.")

lang_btn = tk.Button(
    lp, text=get_lang_button_text(),
    font=(FN, 8, "bold"), bg=C["panel"], fg=C["cyan_br"],
    activebackground=C["cyan_dim"], activeforeground=C["text"],
    bd=0, padx=10, pady=5, cursor="hand2",
    command=cycle_input_language
)
lang_btn.grid(row=6, column=0, sticky="ew", padx=14, pady=(0, 6))

def get_wake_button_text():
    enabled = hud_config.get("wake_word_enabled", True)
    return "👂 WAKE: ON (HEY JARVIS)" if enabled else "👂 WAKE: OFF (MUTED)"

def update_wake_button_ui():
    if "wake_btn" in globals() and wake_btn:
        enabled = hud_config.get("wake_word_enabled", True)
        _safe_ui_update(lambda: wake_btn.config(
            text=get_wake_button_text(),
            fg=C["cyan_br"] if enabled else C["muted"]
        ))

def toggle_wake_word_ui():
    play_sfx("switch")
    hud_config["wake_word_enabled"] = not hud_config.get("wake_word_enabled", True)
    save_config()
    update_wake_button_ui()
    if hud_config["wake_word_enabled"]:
        terminal_feed_log("CONFIG", "Ambient Wake Word detection ENABLED. Say 'Jarvis' or 'Hey Jarvis' to activate.")
        set_substatus("Wake Word: ON")
        speak("Ambient wake word detection active. Say Jarvis anytime to activate.")
    else:
        terminal_feed_log("CONFIG", "Ambient Wake Word detection MUTED.")
        set_substatus("Wake Word: MUTED")
        speak("Wake word detection disabled.")

wake_btn = tk.Button(
    lp, text=get_wake_button_text(),
    font=(FN, 8, "bold"), bg=C["panel"],
    fg=C["cyan_br"] if hud_config.get("wake_word_enabled", True) else C["muted"],
    activebackground=C["cyan_dim"], activeforeground=C["text"],
    bd=0, padx=10, pady=5, cursor="hand2",
    command=toggle_wake_word_ui
)
wake_btn.grid(row=7, column=0, sticky="ew", padx=14, pady=(0, 6))

_sep(lp, 8)
_hud(lp, "INTELLIGENCE CHANNELS").grid(row=9, column=0, sticky="w", padx=14, pady=(2, 3))

caps = (
    ("▸ DUCKDUCKGO", "Instant Facts & Summaries", C["cyan"]),
    ("▸ WIKIPEDIA",  "Global & Hindi Archive",     C["green"]),
    ("▸ MULTILINGUAL", "English & Hindi Native TTS", C["amber"]),
    ("▸ HARDWARE",   "Display & Audio Controls",   C["purple"]),
)
for ci, (nm, desc, clr) in enumerate(caps, start=10):
    rf = tk.Frame(lp, bg=C["surface"])
    rf.grid(row=ci, column=0, sticky="ew", padx=14, pady=1)
    _label(rf, nm, 8, clr, FN, "bold", width=12, anchor="w").pack(side="left")
    _label(rf, desc, 7, C["muted"], FN, anchor="w").pack(side="left")



# ═══════════════════════ CENTER PANEL: COMMAND & TELEMETRY ═══
cp = tk.Frame(main, bg=C["surface"], highlightbackground=C["border"], highlightthickness=1)
panels["cp"] = cp
cp.columnconfigure(0, weight=1)
cp.rowconfigure(1, weight=1)

cp_strip = tk.Frame(cp, bg="#020912", highlightbackground=C["border_gl"], highlightthickness=1)
panel_control_strips["cp"] = cp_strip
cp_strip.grid(row=0, column=0, sticky="ew", padx=4, pady=2)
_label(cp_strip, "⠿ INTELLIGENCE CENTER", 8, C["amber"], FN, "bold").pack(side="left", padx=4)
tk.Button(cp_strip, text="◀", font=(FN, 7), bg=C["panel"], fg=C["text"], bd=0, command=lambda: shift_panel("cp", -1)).pack(side="right", padx=1)
tk.Button(cp_strip, text="▶", font=(FN, 7), bg=C["panel"], fg=C["text"], bd=0, command=lambda: shift_panel("cp", 1)).pack(side="right", padx=1)
cp_strip.grid_remove()

center_submodules = {}

# ── Sub-module 1: Intelligence Terminal & Input ──────
term_container = tk.Frame(cp, bg=C["surface"])
center_submodules["term"] = term_container
term_container.columnconfigure(0, weight=1)
term_container.rowconfigure(1, weight=1)

term_hdr_frame = tk.Frame(term_container, bg=C["surface"])
term_hdr_frame.grid(row=0, column=0, sticky="ew", padx=14, pady=(2, 2))
_hud(term_hdr_frame, "DECRYPTED DATA FEED // LIVE TELEMETRY").pack(side="left")

term_move_frame = tk.Frame(term_hdr_frame, bg=C["surface"])
term_move_frame.pack(side="right")
tk.Button(term_move_frame, text="▲", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, command=lambda: shift_center_submodule("term", -1)).pack(side="left", padx=1)
tk.Button(term_move_frame, text="▼", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, command=lambda: shift_center_submodule("term", 1)).pack(side="left", padx=1)

term_frame = tk.Frame(term_container, bg=C["panel"], highlightbackground=C["border_gl"], highlightthickness=1)
term_frame.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 4))
term_frame.columnconfigure(0, weight=1)
term_frame.rowconfigure(1, weight=1)

# Terminal Toolbar
term_top = tk.Frame(term_frame, bg="#01060e", padx=6, pady=3)
term_top.grid(row=0, column=0, sticky="ew")
_label(term_top, "● LIVE INTEL STREAM", 8, C["cyan"], FN, "bold").pack(side="left")
_label(term_top, "// ENCRYPTED SECURE", 7, C["muted"], FN).pack(side="left", padx=6)

def copy_answer_to_clipboard():
    if _anim.get("last_answer"):
        root.clipboard_clear()
        root.clipboard_append(_anim["last_answer"])
        terminal_feed_log("CLIPBOARD", "Latest answer copied to clipboard.")

def reread_answer():
    if _anim.get("last_answer"):
        global _current_command_id
        with _command_lock:
            _current_command_id += 1
            cmd_id = _current_command_id
        stop_speaking(flush_queue=True)
        speak(_anim["last_answer"], interrupt=True, cmd_id=cmd_id)

def clear_terminal():
    term_text.config(state="normal")
    term_text.delete("1.0", "end")
    term_text.insert("end", "◈ Terminal cleared. Ready for input.\n", "sys")
    term_text.config(state="disabled")

tk.Button(term_top, text="[CLR]", font=(FN, 7), bg="#040e1a", fg=C["text_dim"], bd=0, cursor="hand2", command=clear_terminal).pack(side="right", padx=1)
tk.Button(term_top, text="[🔊 READ]", font=(FN, 7), bg="#040e1a", fg=C["text_dim"], bd=0, cursor="hand2", command=reread_answer).pack(side="right", padx=1)
tk.Button(term_top, text="[📋 COPY]", font=(FN, 7), bg="#040e1a", fg=C["text_dim"], bd=0, cursor="hand2", command=copy_answer_to_clipboard).pack(side="right", padx=1)

term_text = tk.Text(
    term_frame, bg=C["panel"], fg=C["text"], font=(FN, 9),
    wrap="word", relief="flat", bd=0, padx=8, pady=4, height=7,
)
term_text.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 4))
term_text.tag_config("user", foreground=C["green"], font=(FN, 9, "bold"))
term_text.tag_config("source", foreground=C["amber"], font=(FN, 8, "bold"))
term_text.tag_config("ai", foreground=C["cyan_br"], font=(FN, 9))
term_text.tag_config("sys", foreground=C["text_dim"], font=(FN, 8))

term_text.insert("end", "◈ J.A.R.V.I.S Workstation Online.\n", "sys")
term_text.insert("end", "◈ Speak via mic, type query, or use interactive hardware controls below.\n", "sys")
term_text.config(state="disabled")

# Sleek Search Bar with Focus Glow
input_bar = tk.Frame(term_container, bg=C["surface"], highlightbackground=C["border"], highlightthickness=1)
input_bar.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 4))
input_bar.columnconfigure(0, weight=1)

query_entry = tk.Entry(
    input_bar, bg="#040e1a", fg=C["text"], insertbackground=C["cyan"],
    font=(FN, 9), bd=0,
)
query_entry.grid(row=0, column=0, sticky="ew", padx=8, pady=5)

def _on_focus_in(e): input_bar.config(highlightbackground=C["cyan"])
def _on_focus_out(e): input_bar.config(highlightbackground=C["border"])
query_entry.bind("<FocusIn>", _on_focus_in)
query_entry.bind("<FocusOut>", _on_focus_out)

def on_transmit_click():
    txt = query_entry.get().strip()
    if txt:
        play_sfx("transmit")
        query_entry.delete(0, "end")
        dispatch_command(txt)

query_entry.bind("<Return>", lambda e: on_transmit_click())

transmit_btn = tk.Button(
    input_bar, text=" TRANSMIT ⟫ ", font=(FN, 8, "bold"),
    bg=C["border_gl"], fg=C["text"], activebackground=C["cyan"], activeforeground=C["void"],
    bd=0, padx=10, pady=4, cursor="hand2", command=on_transmit_click,
)
transmit_btn.grid(row=0, column=1, padx=(0, 3), pady=3)


# ── Sub-module 2: Holographic Audio Waveform ─────────
wave_container = tk.Frame(cp, bg=C["surface"])
center_submodules["wave"] = wave_container
wave_container.columnconfigure(0, weight=1)

wave_hdr_frame = tk.Frame(wave_container, bg=C["surface"])
wave_hdr_frame.grid(row=0, column=0, sticky="ew", padx=14, pady=(1, 1))
_hud(wave_hdr_frame, "AUDIO WAVEFORM TELEMETRY").pack(side="left")

wave_move_frame = tk.Frame(wave_hdr_frame, bg=C["surface"])
wave_move_frame.pack(side="right")
tk.Button(wave_move_frame, text="▲", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, command=lambda: shift_center_submodule("wave", -1)).pack(side="left", padx=1)
tk.Button(wave_move_frame, text="▼", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, command=lambda: shift_center_submodule("wave", 1)).pack(side="left", padx=1)

wave_cv = tk.Canvas(wave_container, height=54, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
wave_cv.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 4))

wave_cv.bind("<Configure>", lambda e: _draw_wave_center())
def _draw_wave_center():
    wave_cv.delete("center_line")
    w = wave_cv.winfo_width()
    h = wave_cv.winfo_height()
    if w > 10:
        wave_cv.create_line(0, h // 2, w, h // 2, fill=C["border"], width=1, dash=(4, 4), tags="center_line")


# ── Sub-module 3: Interactive Hardware Controls ──────
hw_container = tk.Frame(cp, bg=C["surface"])
center_submodules["hardware"] = hw_container
hw_container.columnconfigure(0, weight=1)

hw_hdr_frame = tk.Frame(hw_container, bg=C["surface"])
hw_hdr_frame.grid(row=0, column=0, sticky="ew", padx=14, pady=(1, 1))
_hud(hw_hdr_frame, "HARDWARE DECK // ONE-TOUCH CONTROLS").pack(side="left")

hw_move_frame = tk.Frame(hw_hdr_frame, bg=C["surface"])
hw_move_frame.pack(side="right")
tk.Button(hw_move_frame, text="▲", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, command=lambda: shift_center_submodule("hardware", -1)).pack(side="left", padx=1)
tk.Button(hw_move_frame, text="▼", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, command=lambda: shift_center_submodule("hardware", 1)).pack(side="left", padx=1)

hw_controls_frame = tk.Frame(hw_container, bg=C["surface"])
hw_controls_frame.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 4))
hw_controls_frame.columnconfigure(0, weight=1)
hw_controls_frame.columnconfigure(1, weight=1)

# Brightness Bar
b_box = tk.Frame(hw_controls_frame, bg="#020912", padx=6, pady=4, highlightbackground=C["border"], highlightthickness=1)
b_box.grid(row=0, column=0, sticky="ew", padx=(0, 3))
_label(b_box, "🔆 BRIGHTNESS", 7, C["amber"], FN, "bold").pack(side="left", padx=(0, 6))
for bp in (25, 50, 75, 100):
    tk.Button(
        b_box, text=f"{bp}%", font=(FN, 7), bg="#041220", fg=C["text_dim"], bd=0, padx=5, pady=1, cursor="hand2",
        command=lambda v=bp: set_brightness(v),
    ).pack(side="left", padx=1)

# Volume Bar
v_box = tk.Frame(hw_controls_frame, bg="#020912", padx=6, pady=4, highlightbackground=C["border"], highlightthickness=1)
v_box.grid(row=0, column=1, sticky="ew", padx=(3, 0))
_label(v_box, "🔊 VOLUME", 7, C["cyan"], FN, "bold").pack(side="left", padx=(0, 6))
tk.Button(v_box, text="-10%", font=(FN, 7), bg="#041220", fg=C["text_dim"], bd=0, padx=5, pady=1, cursor="hand2", command=volume_down).pack(side="left", padx=1)
tk.Button(v_box, text="+10%", font=(FN, 7), bg="#041220", fg=C["text_dim"], bd=0, padx=5, pady=1, cursor="hand2", command=volume_up).pack(side="left", padx=1)
tk.Button(v_box, text="MUTE", font=(FN, 7), bg="#28080c", fg=C["red"], bd=0, padx=5, pady=1, cursor="hand2", command=volume_mute).pack(side="left", padx=1)


# ── Sub-module 4: Quick Command Cards ────────────────
quick_container = tk.Frame(cp, bg=C["surface"])
center_submodules["quick"] = quick_container
quick_container.columnconfigure(0, weight=1)

quick_hdr_frame = tk.Frame(quick_container, bg=C["surface"])
quick_hdr_frame.grid(row=0, column=0, sticky="ew", padx=14, pady=(1, 1))
_hud(quick_hdr_frame, "QUICK ACCESS CARDS").pack(side="left")

quick_move_frame = tk.Frame(quick_hdr_frame, bg=C["surface"])
quick_move_frame.pack(side="right")
tk.Button(quick_move_frame, text="▲", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, command=lambda: shift_center_submodule("quick", -1)).pack(side="left", padx=1)
tk.Button(quick_move_frame, text="▼", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, command=lambda: shift_center_submodule("quick", 1)).pack(side="left", padx=1)

qf = tk.Frame(quick_container, bg=C["surface"])
qf.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 6))
qf.columnconfigure(0, weight=1)
qf.columnconfigure(1, weight=1)

quick_buttons_widgets = []

def rebuild_quick_buttons():
    for b in quick_buttons_widgets:
        b.destroy()
    quick_buttons_widgets.clear()

    for qi, qdata in enumerate(hud_config["quick_cmds"]):
        qlabel = qdata[0]
        qcmd = qdata[1]
        qbadge = qdata[2] if len(qdata) > 2 else "INTEL"

        ri, ci_q = divmod(qi, 2)
        card = tk.Frame(qf, bg="#020912", highlightbackground=C["border"], highlightthickness=1)
        card.grid(row=ri, column=ci_q, sticky="ew", padx=3, pady=2)
        card.columnconfigure(0, weight=1)

        b_btn = tk.Button(
            card, text=f"{qlabel}  [{qbadge}]", font=(FN, 8),
            bg="#020912", fg=C["text_dim"], activebackground=C["border_gl"], activeforeground=C["cyan_br"],
            anchor="w", bd=0, padx=8, pady=5, cursor="hand2",
            command=lambda c=qcmd: (play_sfx("ack"), dispatch_command(c)),
        )
        b_btn.pack(fill="x")

        def _ce(e, cd=card, btn=b_btn):
            cd.config(highlightbackground=C["cyan"])
            btn.config(fg=C["cyan"])
        def _cl(e, cd=card, btn=b_btn):
            cd.config(highlightbackground=C["border"])
            btn.config(fg=C["text_dim"])
        b_btn.bind("<Enter>", _ce)
        b_btn.bind("<Leave>", _cl)
        quick_buttons_widgets.append(card)

rebuild_quick_buttons()


# ═══════════════════════ RIGHT PANEL: MATRIX STREAM & METRICS 
rp = tk.Frame(main, bg=C["surface"], highlightbackground=C["border"], highlightthickness=1)
panels["rp"] = rp
rp.columnconfigure(0, weight=1)
rp.rowconfigure(2, weight=1)

rp_strip = tk.Frame(rp, bg="#020912", highlightbackground=C["border_gl"], highlightthickness=1)
panel_control_strips["rp"] = rp_strip
rp_strip.grid(row=0, column=0, sticky="ew", padx=4, pady=2)
_label(rp_strip, "⠿ MATRIX DATA", 8, C["amber"], FN, "bold").pack(side="left", padx=4)
tk.Button(rp_strip, text="◀", font=(FN, 7), bg=C["panel"], fg=C["text"], bd=0, command=lambda: shift_panel("rp", -1)).pack(side="right", padx=1)
tk.Button(rp_strip, text="▶", font=(FN, 7), bg=C["panel"], fg=C["text"], bd=0, command=lambda: shift_panel("rp", 1)).pack(side="right", padx=1)
rp_strip.grid_remove()

# Header + Interactive Controls Deck
rp_hdr = tk.Frame(rp, bg=C["surface"])
rp_hdr.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 2))
_hud(rp_hdr, "MATRIX DATA STREAM").pack(side="left")

matrix_ctrl_deck = tk.Frame(rp_hdr, bg=C["surface"])
matrix_ctrl_deck.pack(side="right")

fps_badge_lbl = _label(matrix_ctrl_deck, "⚡ 60.0 FPS", 7, C["green"], FN, "bold")
fps_badge_lbl.pack(side="right", padx=(4, 0))

def trigger_matrix_ripple(x, y, max_r=90):
    _anim["matrix_ripples"].append({
        "x": x,
        "y": y,
        "r": 4.0,
        "max_r": max_r,
        "alpha": 1.0,
        "clr": C["cyan_br"] if not _anim["listening"] else C["green"],
    })
    if len(_anim["matrix_ripples"]) > 6:
        _anim["matrix_ripples"].pop(0)

def trigger_matrix_emp():
    play_sfx("switch")
    w = max(rain_cv.winfo_width(), 100)
    h = max(rain_cv.winfo_height(), 100)
    trigger_matrix_ripple(w // 2, h // 2, max_r=max(w, h))
    matrix_push_token("EMP:PULSE")
    matrix_push_token("60FPS:SYNC")

def cycle_matrix_speed():
    speeds = [1.0, 1.5, 2.0, 0.5, 0.0]
    labels = ["1.0X", "1.5X", "2.0X", "0.5X", "FREEZE"]
    cur = _anim.get("matrix_speed_mult", 1.0)
    idx = speeds.index(cur) if cur in speeds else 0
    nxt_idx = (idx + 1) % len(speeds)
    _anim["matrix_speed_mult"] = speeds[nxt_idx]
    speed_btn.config(text=labels[nxt_idx])
    play_sfx("switch")

def cycle_matrix_mode():
    modes = ["core", "neural", "vox", "hex"]
    cur = _anim.get("matrix_mode", "core")
    nxt = modes[(modes.index(cur) + 1) % len(modes)]
    _anim["matrix_mode"] = nxt
    mode_btn.config(text=nxt.upper())
    play_sfx("switch")
    trigger_matrix_emp()
    terminal_feed_log("MATRIX", f"Matrix telemetry mode set to {nxt.upper()}")

emp_btn = tk.Button(
    matrix_ctrl_deck, text="⚡ EMP", font=(FN, 7, "bold"),
    bg="#041220", fg=C["cyan_br"], activebackground=C["cyan"], activeforeground=C["void"],
    bd=0, padx=4, pady=1, cursor="hand2", command=trigger_matrix_emp
)
emp_btn.pack(side="right", padx=1)

speed_btn = tk.Button(
    matrix_ctrl_deck, text="1.0X", font=(FN, 7, "bold"),
    bg="#041220", fg=C["amber"], activebackground=C["amber_dim"], activeforeground=C["text"],
    bd=0, padx=4, pady=1, cursor="hand2", command=cycle_matrix_speed
)
speed_btn.pack(side="right", padx=1)

mode_btn = tk.Button(
    matrix_ctrl_deck, text="CORE", font=(FN, 7, "bold"),
    bg="#041220", fg=C["cyan"], activebackground=C["cyan_dim"], activeforeground=C["text"],
    bd=0, padx=4, pady=1, cursor="hand2", command=cycle_matrix_mode
)
mode_btn.pack(side="right", padx=1)

rain_cv = tk.Canvas(rp, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
rain_cv.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 4))

def _on_matrix_motion(event):
    _anim["matrix_mouse_pos"] = (event.x, event.y)

def _on_matrix_leave(event):
    _anim["matrix_mouse_pos"] = None

def _on_matrix_click(event):
    play_sfx("switch")
    trigger_matrix_ripple(event.x, event.y, max_r=85)
    matrix_push_token("USER:INSPECT")
    matrix_push_token(f"0x{int(event.x * 7 + event.y * 3) % 256:02X}")

def _on_matrix_drag(event):
    _anim["matrix_mouse_pos"] = (event.x, event.y)
    if len(_anim["matrix_sparks"]) < 30:
        _anim["matrix_sparks"].append({
            "x": event.x,
            "y": event.y,
            "vx": random.uniform(-2.0, 2.0),
            "vy": random.uniform(-2.0, 2.0),
            "alpha": 1.0,
            "clr": random.choice([C["cyan_br"], C["white"], C["amber"], C["green"]]),
        })

def _on_matrix_wheel(event):
    delta = event.delta
    if delta > 0:
        _anim["matrix_speed_mult"] = min(3.0, round(_anim["matrix_speed_mult"] + 0.25, 2))
    else:
        _anim["matrix_speed_mult"] = max(0.25, round(_anim["matrix_speed_mult"] - 0.25, 2))
    speed_btn.config(text=f"{_anim['matrix_speed_mult']:.1f}X")

rain_cv.bind("<Motion>", _on_matrix_motion)
rain_cv.bind("<Leave>", _on_matrix_leave)
rain_cv.bind("<Button-1>", _on_matrix_click)
rain_cv.bind("<B1-Motion>", _on_matrix_drag)
rain_cv.bind("<MouseWheel>", _on_matrix_wheel)

_sep(rp, 3)
_hud(rp, "NEURAL TELEMETRY").grid(row=4, column=0, sticky="w", padx=12, pady=(2, 2))

metrics_frame = tk.Frame(rp, bg=C["surface"])
metrics_frame.grid(row=5, column=0, sticky="ew", padx=12, pady=(0, 6))

metric_labels = {}
for mi, (mname, mval, mclr) in enumerate((
    ("CPU", "OK", C["green"]),
    ("MEM", "OK", C["green"]),
    ("MIC", "READY", C["cyan"]),
    ("NET", "ONLINE", C["green"]),
    ("TTS", "READY", C["cyan"]),
)):
    mf = tk.Frame(metrics_frame, bg=C["surface"])
    mf.pack(fill="x", pady=1)
    _label(mf, mname, 7, C["muted"], FN, "bold", width=5, anchor="w").pack(side="left")
    ml = _label(mf, mval, 7, mclr, FN, "bold")
    ml.pack(side="right")
    metric_labels[mname] = ml


# ╔══════════════════════════════════════════════════════════════════╗
# ║  LAYOUT GRID RE-ORDER ENGINE                                     ║
# ╚══════════════════════════════════════════════════════════════════╝

def regrid_all_panels():
    col_idx = 0
    for pid in hud_config["column_order"]:
        p_widget = panels[pid]
        if hud_config["visible"].get(pid, True):
            p_widget.grid(row=0, column=col_idx, sticky="nsew", padx=4, pady=2)
            main.columnconfigure(col_idx, weight=panel_weights[pid])
            col_idx += 1
        else:
            p_widget.grid_remove()

def regrid_center_modules():
    row_idx = 1
    for mid in hud_config["center_order"]:
        sub_w = center_submodules[mid]
        if hud_config["visible"].get(mid, True):
            sub_w.grid(row=row_idx, column=0, sticky="nsew", pady=(0, 2))
            cp.rowconfigure(row_idx, weight=3 if mid == "term" else 1)
            row_idx += 1
        else:
            sub_w.grid_remove()

def shift_panel(panel_id, direction):
    order = hud_config["column_order"]
    if panel_id in order:
        idx = order.index(panel_id)
        new_idx = idx + direction
        if 0 <= new_idx < len(order):
            order[idx], order[new_idx] = order[new_idx], order[idx]
            regrid_all_panels()
            save_config()

def shift_center_submodule(sub_id, direction):
    order = hud_config["center_order"]
    if sub_id in order:
        idx = order.index(sub_id)
        new_idx = idx + direction
        if 0 <= new_idx < len(order):
            order[idx], order[new_idx] = order[new_idx], order[idx]
            regrid_center_modules()
            save_config()

def reset_to_default_layout():
    global hud_config
    hud_config = dict(DEFAULT_CONFIG)
    apply_theme("cyan")
    regrid_all_panels()
    regrid_center_modules()
    rebuild_quick_buttons()
    save_config()
    set_status("◎  HUD SPECIFICATION RESET TO DEFAULT", C["cyan"])


# ─── FOOTER ──────────────────────────────────────────────────
ftr = tk.Frame(overlay, bg=C["void"])
ftr.grid(row=3, column=0, sticky="ew")
ftr.columnconfigure(0, weight=1)

ftr_status = _label(ftr, "▸  INITIALIZING WORKSTATION...", 8, C["muted"], FN, "bold")
ftr_status.pack(side="left", padx=20, pady=(3, 6))

_label(ftr, "MODULAR HUD v3.0 ┃ DDG & WIKIPEDIA ┃ SAPI5 TTS", 7, C["border_gl"], FN).pack(
    side="right", padx=20, pady=(3, 6),
)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  THEME MORPHER ENGINE                                            ║
# ╚══════════════════════════════════════════════════════════════════╝

def apply_theme(theme_id):
    if theme_id not in THEMES: return
    hud_config["theme"] = theme_id
    t = THEMES[theme_id]
    C.update(t)

    title_brand_lbl.config(fg=C["cyan_br"])
    mini_cv.itemconfig("m_out", outline=C["cyan"])
    mini_cv.itemconfig("m_mid", fill=C["cyan_dim"], outline=C["cyan"])
    mini_cv.itemconfig("m_core", fill=C["cyan_br"])

    status_label.config(fg=C["cyan"])
    mic_btn.config(bg=C["red_dim"] if (_is_voice_capturing or _anim.get("listening")) else C["cyan_dim"])
    transmit_btn.config(bg=C["border_gl"])
    query_entry.config(insertbackground=C["cyan"])

    term_frame.config(highlightbackground=C["border_gl"])
    term_text.tag_config("ai", foreground=C["cyan_br"])
    term_text.tag_config("source", foreground=C["amber"])

    if "voice_lab_btn" in globals() and voice_lab_btn:
        try: voice_lab_btn.config(fg=C["cyan_br"])
        except Exception: pass
    play_sfx("switch")
    _draw_hdr_sep()
    pulse_panel_borders()
    rebuild_quick_buttons()
    save_config()
    terminal_feed_log("THEME", f"HUD theme switched to {t['name']}")


# ╔══════════════════════════════════════════════════════════════════╗
# ║  SHORTCUT EDITOR MODAL                                           ║
# ╚══════════════════════════════════════════════════════════════════╝

def open_shortcut_editor():
    win = tk.Toplevel(root)
    win.title("J.A.R.V.I.S // Shortcut Customizer")
    win.geometry("560x430")
    win.configure(bg="#030910")
    win.transient(root)
    win.grab_set()

    _label(win, "✎ CUSTOMIZE QUICK ACCESS DECK", 11, C["cyan_br"], FN, "bold").pack(pady=(12, 4))
    _label(win, "Configure names and voice/search prompts for all 6 shortcut cards:", 8, C["text_dim"], FN).pack(pady=(0, 8))

    entries = []
    edit_box = tk.Frame(win, bg="#061220", padx=10, pady=8, highlightbackground=C["border_gl"], highlightthickness=1)
    edit_box.pack(fill="both", expand=True, padx=14, pady=(0, 8))

    for i in range(6):
        cur_lbl = hud_config["quick_cmds"][i][0] if i < len(hud_config["quick_cmds"]) else f"⟫ Card {i+1}"
        cur_cmd = hud_config["quick_cmds"][i][1] if i < len(hud_config["quick_cmds"]) else ""
        cur_badge = hud_config["quick_cmds"][i][2] if i < len(hud_config["quick_cmds"]) and len(hud_config["quick_cmds"][i]) > 2 else "INTEL"

        row_f = tk.Frame(edit_box, bg="#061220")
        row_f.pack(fill="x", pady=2)

        _label(row_f, f"#{i+1}", 8, C["amber"], FN, "bold", width=3).pack(side="left")
        e_lbl = tk.Entry(row_f, font=(FN, 8), bg="#040e1a", fg=C["text"], insertbackground=C["cyan"], width=18, bd=1)
        e_lbl.insert(0, cur_lbl)
        e_lbl.pack(side="left", padx=3)

        _label(row_f, "⟩", 8, C["border_gl"], FN).pack(side="left")
        e_cmd = tk.Entry(row_f, font=(FN, 8), bg="#040e1a", fg=C["cyan_br"], insertbackground=C["cyan"], width=28, bd=1)
        e_cmd.insert(0, cur_cmd)
        e_cmd.pack(side="left", padx=3)

        entries.append((e_lbl, e_cmd, cur_badge))

    btn_row = tk.Frame(win, bg="#030910")
    btn_row.pack(fill="x", padx=14, pady=(0, 10))

    def save_shortcuts():
        new_cmds = []
        for el, ec, bd in entries:
            l_val = el.get().strip() or "⟫ Shortcut"
            c_val = ec.get().strip() or l_val
            new_cmds.append([l_val, c_val, bd])
        hud_config["quick_cmds"] = new_cmds
        rebuild_quick_buttons()
        save_config()
        win.destroy()
        terminal_feed_log("SHORTCUTS", "Custom shortcut cards updated.")

    tk.Button(
        btn_row, text=" 💾 SAVE & APPLY ", font=(FN, 8, "bold"),
        bg=C["border_gl"], fg=C["text"], activebackground=C["cyan"], bd=0, padx=12, pady=5, cursor="hand2", command=save_shortcuts,
    ).pack(side="right", padx=3)
    tk.Button(btn_row, text=" CANCEL ", font=(FN, 8), bg=C["panel"], fg=C["text_dim"], bd=0, padx=10, pady=5, cursor="hand2", command=win.destroy).pack(side="right", padx=3)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  VOICE PERSONALITY & CYBERNETIC AUDIO LAB MODAL                  ║
# ╚══════════════════════════════════════════════════════════════════╝

def open_voice_audio_modal():
    win = tk.Toplevel(root)
    win.title("J.A.R.V.I.S // Voice & Cybernetic Audio Lab")
    win.geometry("720x680")
    win.configure(bg="#020710")
    win.transient(root)
    win.grab_set()

    _label(win, "🎙️ VOICE PERSONALITY & CYBERNETIC AUDIO LAB", 12, C["cyan_br"], FN, "bold").pack(pady=(10, 2))
    _label(win, "Manage offline SAPI synthesis cores, ElevenLabs neural voice, tempo modulation, and sci-fi audio effects:", 8, C["text_dim"], FN).pack(pady=(0, 6))

    # Scrollable container
    container = tk.Frame(win, bg="#020710")
    container.pack(fill="both", expand=True, padx=10, pady=2)

    canvas = tk.Canvas(container, bg="#020710", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    content_box = tk.Frame(canvas, bg="#020710")

    content_box.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas_window = canvas.create_window((0, 0), window=content_box, anchor="nw")
    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfig(canvas_window, width=e.width)
    )
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    win.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # 0. SECTION: BILINGUAL SPEECH & LANGUAGE ENGINE (HINDI / ENGLISH)
    lang_sec = tk.LabelFrame(
        content_box, text=" 🌐 BILINGUAL SPEECH & LANGUAGE ENGINE (HINDI / ENGLISH) ", font=(FN, 8, "bold"),
        bg="#040e1a", fg=C["cyan_br"], bd=1, highlightbackground=C["border_gl"], highlightthickness=1, padx=10, pady=8
    )
    lang_sec.pack(fill="x", pady=(0, 8))

    _label(lang_sec, "Voice Input Recognition Mode (Speech-to-Text Engine):", 8, C["text_dim"], FN).pack(anchor="w", pady=(0, 4))

    lang_btn_row = tk.Frame(lang_sec, bg="#040e1a")
    lang_btn_row.pack(fill="x", pady=2)

    lang_opt_buttons = {}

    def refresh_lang_modal_ui():
        cur_mode = hud_config.get("input_language", "auto")
        for m_key, (btn, lbl) in lang_opt_buttons.items():
            if m_key == cur_mode:
                btn.config(bg=C["cyan_dim"], fg=C["cyan_br"], text=f"✓ {lbl} [ACTIVE]")
            else:
                btn.config(bg=C["panel"], fg=C["text_dim"], text=f"  {lbl}  ")

    def set_modal_language(mode_val):
        play_sfx("switch")
        hud_config["input_language"] = mode_val
        save_config()
        refresh_lang_modal_ui()
        if "update_lang_button_ui" in globals():
            update_lang_button_ui()
        if mode_val == "auto":
            terminal_feed_log("CONFIG", "Language Mode set to DUAL AUTO (Hindi + English).")
            set_substatus("Input: DUAL (HI/EN)")
            speak("Bilingual dual recognition active. You can now speak in Hindi or English.")
        elif mode_val == "hi":
            terminal_feed_log("CONFIG", "Language Mode set to HINDI EXCLUSIVE (hi-IN).")
            set_substatus("Input: HINDI (hi-IN)")
            speak("हिंदी भाषा मोड सक्रिय कर दिया गया है।")
        else:
            terminal_feed_log("CONFIG", "Language Mode set to ENGLISH EXCLUSIVE (en-IN).")
            set_substatus("Input: ENGLISH (en-IN)")
            speak("English exclusive recognition mode active.")

    modes = [
        ("auto", "DUAL (HINDI + ENGLISH AUTO)"),
        ("en",   "ENGLISH (en-IN)"),
        ("hi",   "HINDI (hi-IN)"),
    ]
    for m_val, m_label in modes:
        b = tk.Button(
            lang_btn_row, text=m_label, font=(FN, 7, "bold"),
            bg=C["panel"], fg=C["text_dim"], activebackground=C["cyan"], bd=0, padx=8, pady=5, cursor="hand2",
            command=lambda v=m_val: set_modal_language(v)
        )
        b.pack(side="left", padx=3, fill="x", expand=True)
        lang_opt_buttons[m_val] = (b, m_label)

    refresh_lang_modal_ui()

    _label(lang_sec, "* DUAL mode concurrently evaluates Hindi (hi-IN) and English (en-IN) inputs. Automatic Devanagari voice synthesis enabled for Hindi responses.", 7, C["muted"], FN).pack(anchor="w", pady=(4, 0))

    # Acoustic capture listening timeout selector
    to_frame = tk.Frame(lang_sec, bg="#040e1a")
    to_frame.pack(fill="x", pady=(8, 2))
    _label(to_frame, "Voice Command Input Listening Timeout:", 8, C["text_dim"], FN).pack(side="left", padx=(0, 6))

    to_buttons = {}
    cur_init_to = int(float(hud_config.get("voice_input_timeout", 10.0)))
    to_badge = _label(to_frame, f"[{cur_init_to}s ACTIVE]", 8, C["cyan_br"], FN, "bold")
    to_badge.pack(side="right", padx=4)

    def set_modal_timeout(sec_val):
        play_sfx("ack")
        hud_config["voice_input_timeout"] = float(sec_val)
        save_config()
        to_badge.config(text=f"[{int(sec_val)}s ACTIVE]")
        for s_val, btn in to_buttons.items():
            if s_val == sec_val:
                btn.config(bg=C["cyan_dim"], fg=C["cyan_br"])
            else:
                btn.config(bg=C["panel"], fg=C["text_dim"])
        terminal_feed_log("CONFIG", f"Voice input listening timeout set to {sec_val}s.")

    for s_val in [6, 8, 10, 15, 20]:
        is_sel = (s_val == cur_init_to)
        b = tk.Button(
            to_frame, text=f"{s_val}s", font=(FN, 7, "bold" if is_sel else "normal"),
            bg=C["cyan_dim"] if is_sel else C["panel"],
            fg=C["cyan_br"] if is_sel else C["text_dim"],
            bd=0, padx=6, pady=2, cursor="hand2",
            command=lambda s=s_val: set_modal_timeout(s)
        )
        b.pack(side="left", padx=2)
        to_buttons[s_val] = b

    # 1. SECTION: VOICE PERSONALITY CORES (OFFLINE SAPI)
    voice_sec = tk.LabelFrame(
        content_box, text=" 🎙️ OFFLINE VOICE PROFILES (WINDOWS SAPI / PYTTSX3) ", font=(FN, 8, "bold"),
        bg="#040e1a", fg=C["amber"], bd=1, highlightbackground=C["border_gl"], highlightthickness=1, padx=10, pady=8
    )
    voice_sec.pack(fill="x", pady=(0, 8))

    voices = get_available_voices()
    voice_cards = []

    def refresh_voice_cards():
        tts_mode = hud_config.get("tts_engine", "sapi")
        active_i = hud_config.get("voice_index", 0)
        for i, (cd, bdg, act_btn) in enumerate(voice_cards):
            is_act = (i == active_i and tts_mode == "sapi")
            if is_act:
                cd.config(highlightbackground=C["cyan_br"], bg="#06182c")
                bdg.config(text="[ ✓ ACTIVE CURRENT ]", fg=C["cyan_br"])
                act_btn.config(text="✓ ACTIVATED", bg=C["border_gl"], fg=C["cyan_br"], state="disabled")
            else:
                cd.config(highlightbackground=C["border"], bg="#030b14")
                bdg.config(text="[ STANDBY ]", fg=C["muted"])
                act_btn.config(text="▶ SELECT & APPLY", bg=C["panel"], fg=C["text"], state="normal")

        # Update ElevenLabs card button
        is_el = (tts_mode == "elevenlabs")
        if "el_tog_btn" in globals_dict:
            if is_el:
                globals_dict["el_tog_btn"].config(text="✓ ACTIVE ENGINE", bg=C["border_gl"], fg=C["cyan_br"])
            else:
                globals_dict["el_tog_btn"].config(text="▶ SET AS PRIMARY TTS", bg=C["panel"], fg=C["text"])

    globals_dict = {}

    for idx, vinfo in enumerate(voices):
        card = tk.Frame(voice_sec, bg="#030b14", highlightbackground=C["border"], highlightthickness=1, padx=8, pady=6)
        card.pack(fill="x", pady=3)

        left_f = tk.Frame(card, bg=card.cget("bg"))
        left_f.pack(side="left", fill="x", expand=True)

        title_line = tk.Frame(left_f, bg=card.cget("bg"))
        title_line.pack(anchor="w")

        v_alias = vinfo.get("alias", "VOICE")
        v_tag = vinfo.get("tag", "SYNTHESIS CORE")
        _label(title_line, f"◈ {v_alias}", 9, C["cyan_br"] if vinfo.get("is_female") else C["cyan"], FN, "bold").pack(side="left")
        _label(title_line, f" // {v_tag}", 8, C["amber"], FN).pack(side="left", padx=4)

        bdg_lbl = _label(title_line, "[ STANDBY ]", 8, C["muted"], FN, "bold")
        bdg_lbl.pack(side="left", padx=6)

        _label(left_f, f"Name: {vinfo.get('name', 'Unknown')}", 7, C["text_dim"], FN).pack(anchor="w", pady=(2, 0))

        btn_f = tk.Frame(card, bg=card.cget("bg"))
        btn_f.pack(side="right")

        def _do_select(i=idx):
            play_sfx("switch")
            hud_config["tts_engine"] = "sapi"
            switch_voice_profile(i, speak_confirm=True)
            refresh_voice_cards()

        def _do_audition(i=idx):
            play_sfx("ack")
            audition_voice(i)

        act_b = tk.Button(
            btn_f, text="▶ SELECT & APPLY", font=(FN, 7, "bold"),
            bg=C["panel"], fg=C["text"], activebackground=C["cyan"], bd=0, padx=8, pady=4, cursor="hand2",
            command=_do_select
        )
        act_b.pack(side="left", padx=2)

        aud_b = tk.Button(
            btn_f, text="🔊 AUDITION", font=(FN, 7),
            bg=C["border_gl"], fg=C["text_dim"], activebackground=C["cyan_br"], bd=0, padx=8, pady=4, cursor="hand2",
            command=_do_audition
        )
        aud_b.pack(side="left", padx=2)

        voice_cards.append((card, bdg_lbl, act_b))

    # 2. SECTION: ELEVENLABS NEURAL CLOUD VOICE
    eleven_sec = tk.LabelFrame(
        content_box, text=" ⚡ ELEVENLABS NEURAL VOICE CORE (CLOUD / HIGH-FIDELITY) ", font=(FN, 8, "bold"),
        bg="#040e1a", fg=C["cyan_br"], bd=1, highlightbackground=C["border_gl"], highlightthickness=1, padx=10, pady=8
    )
    eleven_sec.pack(fill="x", pady=(0, 8))

    el_card = tk.Frame(eleven_sec, bg="#030b14", highlightbackground=C["border"], highlightthickness=1, padx=8, pady=8)
    el_card.pack(fill="x", pady=2)

    el_head = tk.Frame(el_card, bg="#030b14")
    el_head.pack(fill="x")

    el_status = get_elevenlabs_voice_status("IRHApOXLvnW57QJPQH2P")
    _label(el_head, f"◈ {el_status['name']}", 9, C["cyan_br"], FN, "bold").pack(side="left")
    _label(el_head, " // NEURAL VOICE ID: IRHApOXLvnW57QJPQH2P", 8, C["amber"], FN).pack(side="left", padx=4)

    el_badge = _label(
        el_head,
        f"[ ✓ DOWNLOADED & READY ({el_status['size_kb']} KB) ]" if el_status["downloaded"] else "[ ⬇ DOWNLOAD REQUIRED ]",
        8,
        C["green"] if el_status["downloaded"] else C["red"],
        FN, "bold"
    )
    el_badge.pack(side="left", padx=6)

    _label(
        el_card,
        f"Persona: {el_status['description']} (Accent: {el_status['accent'].capitalize()} | Gender: {el_status['gender'].capitalize()})",
        7, C["text_dim"], FN
    ).pack(anchor="w", pady=(2, 6))

    # Control buttons row
    el_btn_row = tk.Frame(el_card, bg="#030b14")
    el_btn_row.pack(fill="x", pady=(2, 6))

    def _do_audition_eleven():
        play_sfx("ack")
        audition_elevenlabs_voice("IRHApOXLvnW57QJPQH2P")

    def _do_download_eleven():
        play_sfx("downlink")
        el_down_btn.config(text="⬇ DOWNLOADING...", state="disabled")
        win.update()
        def _bg():
            succ, meta, path, msg = download_elevenlabs_voice("IRHApOXLvnW57QJPQH2P")
            def _ui():
                st = get_elevenlabs_voice_status("IRHApOXLvnW57QJPQH2P")
                if succ:
                    el_badge.config(text=f"[ ✓ DOWNLOADED ({st['size_kb']} KB) ]", fg=C["green"])
                    terminal_feed_log("VOICE", f"ElevenLabs voice sample saved ({st['size_kb']} KB).")
                else:
                    el_badge.config(text="[ DOWNLOAD ERROR ]", fg=C["red"])
                    terminal_feed_log("VOICE", f"ElevenLabs download note: {msg}")
                el_down_btn.config(text="⬇ RE-DOWNLOAD SAMPLE", state="normal")
            win.after(0, _ui)
        threading.Thread(target=_bg, daemon=True).start()

    def _toggle_eleven_engine():
        play_sfx("switch")
        cur_eng = hud_config.get("tts_engine", "sapi")
        if cur_eng == "elevenlabs":
            hud_config["tts_engine"] = "sapi"
            save_config()
            refresh_voice_cards()
            terminal_feed_log("VOICE", "Speech engine switched to Windows SAPI.")
            speak("Speech engine switched to Windows offline voice.")
        else:
            hud_config["tts_engine"] = "elevenlabs"
            save_config()
            refresh_voice_cards()
            terminal_feed_log("VOICE", "Speech engine switched to ElevenLabs Neural.")
            el_key = hud_config.get("elevenlabs_api_key", "").strip()
            if not el_key:
                speak("ElevenLabs voice core selected. Downloaded voice sample is ready. To enable dynamic live speech generation, please enter your ElevenLabs API key.")
            else:
                speak("ElevenLabs neural voice core online and active.")

    is_el_active = (hud_config.get("tts_engine", "sapi") == "elevenlabs")

    el_tog_btn = tk.Button(
        el_btn_row,
        text="✓ ACTIVE ENGINE" if is_el_active else "▶ SET AS PRIMARY TTS",
        font=(FN, 7, "bold"),
        bg=C["border_gl"] if is_el_active else C["panel"],
        fg=C["cyan_br"] if is_el_active else C["text"],
        activebackground=C["cyan"], bd=0, padx=8, pady=4, cursor="hand2",
        command=_toggle_eleven_engine
    )
    el_tog_btn.pack(side="left", padx=2)
    globals_dict["el_tog_btn"] = el_tog_btn

    tk.Button(
        el_btn_row, text="🔊 AUDITION DOWNLOADED SAMPLE", font=(FN, 7),
        bg=C["border_gl"], fg=C["text_dim"], activebackground=C["cyan_br"], bd=0, padx=8, pady=4, cursor="hand2",
        command=_do_audition_eleven
    ).pack(side="left", padx=2)

    el_down_btn = tk.Button(
        el_btn_row, text="⬇ RE-DOWNLOAD SAMPLE", font=(FN, 7),
        bg=C["border_gl"], fg=C["text_dim"], activebackground=C["cyan_br"], bd=0, padx=8, pady=4, cursor="hand2",
        command=_do_download_eleven
    )
    el_down_btn.pack(side="left", padx=2)

    # API Key row for dynamic speech generation
    api_f = tk.Frame(el_card, bg="#020810", highlightbackground=C["border"], highlightthickness=1, padx=6, pady=4)
    api_f.pack(fill="x", pady=(4, 2))

    _label(api_f, "🔑 ElevenLabs API Key (Optional for dynamic live speech):", 7, C["text_dim"], FN).pack(side="left", padx=(0, 6))

    key_entry = tk.Entry(api_f, font=(FN, 8), bg="#051525", fg=C["cyan_br"], insertbackground=C["cyan_br"], bd=1, relief="solid", show="*")
    saved_key = hud_config.get("elevenlabs_api_key", "")
    if saved_key:
        key_entry.insert(0, saved_key)
    key_entry.pack(side="left", fill="x", expand=True, padx=4)

    def _toggle_key_vis():
        if key_entry.cget("show") == "*":
            key_entry.config(show="")
            vis_btn.config(text="HIDE")
        else:
            key_entry.config(show="*")
            vis_btn.config(text="SHOW")

    vis_btn = tk.Button(api_f, text="SHOW", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, padx=6, pady=2, cursor="hand2", command=_toggle_key_vis)
    vis_btn.pack(side="left", padx=2)

    def _save_api_key():
        play_sfx("ack")
        k = key_entry.get().strip()
        hud_config["elevenlabs_api_key"] = k
        save_config()
        terminal_feed_log("CONFIG", "ElevenLabs API key updated.")
        speak("ElevenLabs API key saved successfully.")

    tk.Button(api_f, text="💾 SAVE KEY", font=(FN, 7, "bold"), bg=C["cyan_dim"], fg=C["cyan_br"], bd=0, padx=8, pady=2, cursor="hand2", command=_save_api_key).pack(side="left", padx=2)

    _label(el_card, "* Voice sample is saved locally in voices/ and plays offline. Free API key from elevenlabs.io enables live dynamic TTS.", 7, C["muted"], FN).pack(anchor="w", pady=(2, 0))

    refresh_voice_cards()

    # 3. SECTION: SPEECH RATE (TEMPO)
    rate_sec = tk.LabelFrame(
        content_box, text=" ⚡ SPEECH TEMPO & RATE MODULATION ", font=(FN, 8, "bold"),
        bg="#040e1a", fg=C["amber"], bd=1, highlightbackground=C["border_gl"], highlightthickness=1, padx=10, pady=6
    )
    rate_sec.pack(fill="x", pady=(0, 8))

    rate_btns_frame = tk.Frame(rate_sec, bg="#040e1a")
    rate_btns_frame.pack(fill="x")

    rate_var_lbl = _label(rate_btns_frame, f"Current Rate: {hud_config.get('voice_rate', 175)} WPM  ⟫", 8, C["text"], FN)
    rate_var_lbl.pack(side="left", padx=(0, 10))

    def set_rate(r_val):
        play_sfx("ack")
        hud_config["voice_rate"] = r_val
        save_config()
        rate_var_lbl.config(text=f"Current Rate: {r_val} WPM  ⟫")
        speak(f"Speech tempo set to {r_val} words per minute.")

    for r_lbl, r_num in (("150 WPM [CALM]", 150), ("175 WPM [NOMINAL]", 175), ("200 WPM [TACTICAL]", 200), ("230 WPM [TURBO]", 230)):
        tk.Button(
            rate_btns_frame, text=r_lbl, font=(FN, 7),
            bg=C["panel"], fg=C["text_dim"], activebackground=C["cyan"], bd=0, padx=6, pady=3, cursor="hand2",
            command=lambda v=r_num: set_rate(v)
        ).pack(side="left", padx=2)

    # 4. SECTION: HOLOGRAPHIC SOUND EFFECTS (SFX) SUITE
    sfx_sec = tk.LabelFrame(
        content_box, text=" 🔊 CYBERNETIC SOUND EFFECTS SUITE (BEST MULTIPLE AUDIOS) ", font=(FN, 8, "bold"),
        bg="#040e1a", fg=C["amber"], bd=1, highlightbackground=C["border_gl"], highlightthickness=1, padx=10, pady=8
    )
    sfx_sec.pack(fill="both", expand=True, pady=(0, 8))

    sfx_top_bar = tk.Frame(sfx_sec, bg="#040e1a")
    sfx_top_bar.pack(fill="x", pady=(0, 6))

    _label(sfx_top_bar, "Master SFX Controller: ", 8, C["text_dim"], FN).pack(side="left")

    def toggle_sfx_master():
        cur = hud_config.get("sfx_enabled", True)
        hud_config["sfx_enabled"] = not cur
        save_config()
        if hud_config["sfx_enabled"]:
            play_sfx("switch", force=True)
            sfx_tog_btn.config(text=" 🔊 SFX ENGINE: ACTIVE [ENABLED] ", bg=C["green_dim"], fg=C["green"])
            terminal_feed_log("AUDIO", "Cybernetic sound effects suite enabled.")
        else:
            sfx_tog_btn.config(text=" 🔇 SFX ENGINE: MUTED [DISABLED] ", bg=C["red_dim"], fg=C["red"])
            terminal_feed_log("AUDIO", "Cybernetic sound effects suite muted.")

    is_on = hud_config.get("sfx_enabled", True)
    sfx_tog_btn = tk.Button(
        sfx_top_bar,
        text=" 🔊 SFX ENGINE: ACTIVE [ENABLED] " if is_on else " 🔇 SFX ENGINE: MUTED [DISABLED] ",
        font=(FN, 8, "bold"),
        bg=C["green_dim"] if is_on else C["red_dim"],
        fg=C["green"] if is_on else C["red"],
        bd=0, padx=10, pady=3, cursor="hand2",
        command=toggle_sfx_master
    )
    sfx_tog_btn.pack(side="left", padx=6)

    _label(sfx_sec, "Interactive Holographic Soundboard — Click any button to audition the audio waveform:", 7, C["text_dim"], FN).pack(anchor="w", pady=(0, 6))

    soundboard = tk.Frame(sfx_sec, bg="#040e1a")
    soundboard.pack(fill="both", expand=True)

    sfx_list = [
        ("boot",     "1. BOOT CHORD",      "Iron Man suit cinematic power-up chord"),
        ("transmit", "2. TRANSMIT CHIRP",  "Digital holographic frequency chirp"),
        ("sonar",    "3. SONAR PING",      "Submarine microphone acoustic capture ping"),
        ("downlink", "4. DATA DOWNLINK",   "Harmonic 4-note telemetry decrypted chime"),
        ("switch",   "5. VOICE SWITCH",    "Futuristic voice & mode morph sweep"),
        ("ack",            "6. HARDWARE ACK",    "Crisp tactile dual-tone feedback click"),
        ("alert",          "7. CYBER ALERT",     "Dual-pulse holographic attention alert"),
        ("tactical_radio", "8. TACTICAL RADIO",  "Combat radio: 'We have a man down!'"),
    ]

    for s_idx, (s_code, s_name, s_desc) in enumerate(sfx_list):
        r_i, c_i = divmod(s_idx, 2)
        s_cell = tk.Frame(soundboard, bg="#030b14", highlightbackground=C["border"], highlightthickness=1, padx=6, pady=4)
        s_cell.grid(row=r_i, column=c_i, sticky="nsew", padx=3, pady=2)
        soundboard.columnconfigure(c_i, weight=1)

        b_play = tk.Button(
            s_cell, text=f"▶  {s_name}", font=(FN, 8, "bold"),
            bg="#051525", fg=C["cyan_br"], activebackground=C["cyan"], activeforeground=C["void"],
            bd=0, padx=8, pady=4, cursor="hand2", anchor="w",
            command=lambda code=s_code: play_sfx(code, force=True)
        )
        b_play.pack(fill="x")
        _label(s_cell, s_desc, 7, C["text_dim"], FN, anchor="w").pack(fill="x", padx=2, pady=(2, 0))

    # 5. SECTION: AI NEURAL MODEL & HIGH-PRECISION REASONING LAB
    ai_sec = tk.LabelFrame(
        content_box, text=" 🧠 AI NEURAL MODEL & HIGH-PRECISION REASONING LAB ", font=(FN, 8, "bold"),
        bg="#040e1a", fg=C["cyan_br"], bd=1, highlightbackground=C["border_gl"], highlightthickness=1, padx=10, pady=8
    )
    ai_sec.pack(fill="x", pady=(0, 8))

    _label(ai_sec, "Configure Advanced AI LLM Inference for In-Depth Explanations, Coding & Accurate Reasoning:", 8, C["text_dim"], FN).pack(anchor="w", pady=(0, 4))

    def _get_ai_status_text():
        prov = hud_config.get("ai_provider", "auto").upper()
        key = hud_config.get("ai_api_key", "")
        if key:
            masked = key[:6] + "..." + key[-4:] if len(key) > 12 else "CONFIGURED"
            return f"● ACTIVE: {prov} ({hud_config.get('ai_model', 'LLAMA 3.3 70B').upper()})  [KEY: {masked}]"
        return "● ACTIVE: HYBRID NEURAL ARCHIVE (Precision Math + Deep Wikipedia + Web Intel)"

    ai_status_lbl = _label(ai_sec, _get_ai_status_text(), 8, C["green"], FN, "bold")
    ai_status_lbl.pack(anchor="w", pady=(0, 6))

    prov_row = tk.Frame(ai_sec, bg="#040e1a")
    prov_row.pack(fill="x", pady=2)

    _label(prov_row, "Provider: ", 8, C["text_dim"], FN).pack(side="left", padx=(0, 4))

    prov_opts = [
        ("Auto-Detect", "auto", "llama-3.3-70b-versatile"),
        ("Groq (Free)", "groq", "llama-3.3-70b-versatile"),
        ("Gemini (Free)", "gemini", "gemini-2.0-flash"),
        ("OpenAI", "openai", "gpt-4o-mini"),
        ("Local Ollama", "ollama", "llama3"),
    ]

    def _select_ai_provider(p_val, def_model):
        hud_config["ai_provider"] = p_val
        if def_model:
            hud_config["ai_model"] = def_model
        save_config()
        ai_status_lbl.config(text=_get_ai_status_text())
        play_sfx("switch")

    for p_name, p_code, def_m in prov_opts:
        tk.Button(
            prov_row, text=p_name, font=(FN, 7),
            bg=C["panel"], fg=C["text_dim"], activebackground=C["cyan"], bd=0, padx=6, pady=2, cursor="hand2",
            command=lambda c=p_code, m=def_m: _select_ai_provider(c, m)
        ).pack(side="left", padx=2)

    key_row = tk.Frame(ai_sec, bg="#040e1a")
    key_row.pack(fill="x", pady=(6, 2))

    _label(key_row, "API Key: ", 8, C["text_dim"], FN).pack(side="left", padx=(0, 4))

    ai_key_entry = tk.Entry(key_row, font=(FN, 8), bg="#020813", fg=C["text"], insertbackground=C["cyan"], show="*", bd=1, relief="solid")
    ai_key_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
    if hud_config.get("ai_api_key"):
        ai_key_entry.insert(0, hud_config["ai_api_key"])

    def _toggle_key_vis():
        if ai_key_entry.cget("show") == "*":
            ai_key_entry.config(show="")
            show_btn.config(text="👁 HIDE")
        else:
            ai_key_entry.config(show="*")
            show_btn.config(text="👁 SHOW")

    show_btn = tk.Button(key_row, text="👁 SHOW", font=(FN, 7), bg=C["panel"], fg=C["text_dim"], bd=0, padx=6, pady=2, cursor="hand2", command=_toggle_key_vis)
    show_btn.pack(side="left", padx=(0, 4))

    def _save_ai_key():
        new_k = ai_key_entry.get().strip()
        hud_config["ai_api_key"] = new_k
        if new_k.startswith("gsk_"):
            hud_config["ai_provider"] = "groq"
            hud_config["ai_model"] = "llama-3.3-70b-versatile"
        elif new_k.startswith("AIza"):
            hud_config["ai_provider"] = "gemini"
            hud_config["ai_model"] = "gemini-2.0-flash"
        elif new_k.startswith("sk-"):
            hud_config["ai_provider"] = "openai"
            hud_config["ai_model"] = "gpt-4o-mini"
        save_config()
        ai_status_lbl.config(text=_get_ai_status_text())
        play_sfx("ack")
        terminal_feed_log("AI CORE", f"AI Model settings saved. Active: {hud_config['ai_provider'].upper()}")

    tk.Button(key_row, text="💾 SAVE KEY", font=(FN, 7, "bold"), bg=C["cyan_dim"], fg=C["cyan_br"], bd=0, padx=8, pady=2, cursor="hand2", command=_save_ai_key).pack(side="left", padx=(0, 4))

    def _test_ai_connection():
        ai_status_lbl.config(text="● TESTING NEURAL LINK...", fg=C["amber"])
        win.update()
        res = query_ai_model("Confirm J.A.R.V.I.S connection in 5 words.")
        if res and res.get("found"):
            ai_status_lbl.config(text=f"● ONLINE: {res['source']}", fg=C["green"])
            play_sfx("downlink")
        else:
            ai_status_lbl.config(text="● OFFLINE: Key invalid or offline. Hybrid fallback active.", fg=C["red"])
            play_sfx("alert")

    tk.Button(key_row, text="⚡ TEST LINK", font=(FN, 7, "bold"), bg=C["amber_dim"], fg=C["amber"], bd=0, padx=8, pady=2, cursor="hand2", command=_test_ai_connection).pack(side="left")

    _label(ai_sec, "* Free Groq Key: console.groq.com | Free Gemini Key: aistudio.google.com | Ollama (Local): localhost:11434", 7, C["muted"], FN).pack(anchor="w", pady=(4, 0))

    # Footer Actions
    footer_f = tk.Frame(win, bg="#020710", padx=14, pady=8)
    footer_f.pack(fill="x")

    def _close_modal():
        save_config()
        win.destroy()

    tk.Button(
        footer_f, text=" 💾 SAVE & CLOSE ", font=(FN, 8, "bold"),
        bg=C["border_gl"], fg=C["text"], activebackground=C["cyan"], bd=0, padx=14, pady=5, cursor="hand2",
        command=_close_modal
    ).pack(side="right", padx=3)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  TERMINAL TELEMETRY & TYPEWRITER                                 ║
# ╚══════════════════════════════════════════════════════════════════╝

def terminal_feed_user(query):
    matrix_push_token("USER")
    for _w in str(query).split()[:4]:
        if len(_w) > 2:
            matrix_push_token(_w)
    ts = _time.strftime("%I:%M:%S %p")
    term_text.config(state="normal")
    term_text.insert("end", f"\n[{ts}] USER   ⟩ {query}\n", "user")
    term_text.see("end")
    term_text.config(state="disabled")

def terminal_feed_log(source, text):
    matrix_push_token(source)
    for _w in str(text).split()[:3]:
        if len(_w) > 2:
            matrix_push_token(_w)
    ts = _time.strftime("%I:%M:%S %p")
    term_text.config(state="normal")
    term_text.insert("end", f"[{ts}] {source} ⟩ {text}\n", "sys")
    term_text.see("end")
    term_text.config(state="disabled")

def terminal_feed_intel(source, title, text, auto_speak=False, speech_text=None):
    matrix_push_token(source)
    matrix_push_token(title)
    play_sfx("downlink")
    ts = _time.strftime("%I:%M:%S %p")
    term_text.config(state="normal")
    term_text.insert("end", f"[{ts}] SOURCE ⟩ {source} // {title}\n[{ts}] JARVIS ⟩ ", "source")
    term_text.see("end")
    term_text.config(state="disabled")
    stream_typewriter(text + "\n", tag="ai")
    if auto_speak:
        to_speak = speech_text if speech_text else text
        speak(to_speak)

def stream_typewriter(text, tag="ai", char_delay=12):
    global _stream_active
    for ch in text:
        _stream_queue.append((ch, tag))
    if not _stream_active:
        _stream_active = True
        root.after(char_delay, lambda: _typewriter_step(char_delay))

def _typewriter_step(char_delay):
    global _stream_active
    if _stream_queue:
        chars_to_insert = []
        cur_tag = "ai"
        for _ in range(3):
            if _stream_queue:
                c, t = _stream_queue.pop(0)
                chars_to_insert.append(c)
                cur_tag = t
            else:
                break
        if chars_to_insert:
            term_text.config(state="normal")
            term_text.insert("end", "".join(chars_to_insert), cur_tag)
            term_text.see("end")
            term_text.config(state="disabled")
        root.after(char_delay, lambda: _typewriter_step(char_delay))
    else:
        _stream_active = False


# ╔══════════════════════════════════════════════════════════════════╗
# ║  60 FPS UNIFIED MASTER RENDERING & CYBERNETIC ANIMATION ENGINES  ║
# ╚══════════════════════════════════════════════════════════════════╝

def animate_reactor_step(dt):
    w = reactor_cv.winfo_width()
    h = reactor_cv.winfo_height()
    if w < 40 or h < 40:
        return

    RCX, RCY = w // 2, h // 2
    base_r = min(w, h) * 0.44

    # Determine dynamic state reactivity & energy
    if _anim["listening"]:
        c1, c2, c3 = C["green"], C["green_dim"], C["cyan_dim"]
        rot_speed = 3.6
        scan_speed = 4.8
        energy_level = 1.0
    elif _anim["speaking"]:
        c1, c2, c3 = C["cyan_br"], C["cyan"], C["cyan_dim"]
        rot_speed = 3.0
        scan_speed = 3.8
        energy_level = 0.85
    elif _anim["processing"]:
        c1, c2, c3 = C["amber"], C["amber_dim"], C["cyan_dim"]
        rot_speed = 2.4
        scan_speed = 4.2
        energy_level = 0.65
    else:
        c1, c2, c3 = C["cyan"], C["cyan_dim"], C["border"]
        rot_speed = 1.4
        scan_speed = 2.0
        energy_level = 0.25

    # 60 FPS Frame-rate independent delta scaling
    dt_scale = dt * 60.0
    _anim["reactor_angle"] = (_anim["reactor_angle"] + rot_speed * dt_scale) % 360
    _anim["scan_angle"] = (_anim["scan_angle"] + scan_speed * dt_scale) % 360
    a = _anim["reactor_angle"]

    # Redraw all elements dynamically scaled to base_r
    reactor_cv.delete("all")

    # 1. Outer Tech Grid (dynamically scaled)
    for i in range(-5, 6):
        off = i * (base_r * 0.18)
        reactor_cv.create_line(RCX + off, RCY - base_r * 1.08, RCX + off, RCY + base_r * 1.08, fill=C["cyan_faint"], width=1, dash=(1, 8))
        reactor_cv.create_line(RCX - base_r * 1.08, RCY + off, RCX + base_r * 1.08, RCY + off, fill=C["cyan_faint"], width=1, dash=(1, 8))

    # 2. 12 Stator Teeth (scaled to base_r)
    for st_i in range(12):
        st_ang = math.radians(st_i * 30 + a * 0.2)
        st_r1, st_r2 = base_r * 0.94, base_r * 1.03
        sx1, sy1 = RCX + st_r1 * math.cos(st_ang), RCY - st_r1 * math.sin(st_ang)
        sx2, sy2 = RCX + st_r2 * math.cos(st_ang), RCY - st_r2 * math.sin(st_ang)
        reactor_cv.create_line(sx1, sy1, sx2, sy2, fill=C["border_gl"], width=2)

    # 3. Outer Dashed Boundary Circle
    reactor_cv.create_oval(RCX - base_r * 0.98, RCY - base_r * 0.98, RCX + base_r * 0.98, RCY + base_r * 0.98, outline=C["border"], width=1, dash=(4, 6))

    # 4. Crosshair Guide Lines
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        reactor_cv.create_line(RCX + dx * base_r * 0.35, RCY + dy * base_r * 0.35, RCX + dx * base_r * 0.98, RCY + dy * base_r * 0.98, fill=C["cyan_faint"], width=1)

    # 5. Segmented Ring 1: Outer 4 Arcs
    r1 = base_r * 0.86
    for i in range(4):
        reactor_cv.create_arc(RCX - r1, RCY - r1, RCX + r1, RCY + r1, start=a + i * 90, extent=50, outline=c2, width=2, style="arc")

    # 6. Segmented Ring 2: Mid 3 Arcs (counter-rotating)
    r2 = base_r * 0.65
    a2 = (-a * 1.6) % 360
    for i in range(3):
        reactor_cv.create_arc(RCX - r2, RCY - r2, RCX + r2, RCY + r2, start=a2 + i * 120, extent=60, outline=c1, width=2, style="arc")

    # 7. Segmented Ring 3: Inner Fast 6 Arcs
    r3 = base_r * 0.44
    a3 = (a * 3.0) % 360
    for i in range(6):
        reactor_cv.create_arc(RCX - r3, RCY - r3, RCX + r3, RCY + r3, start=a3 + i * 60, extent=20, outline=c3, width=1, style="arc")

    # 8. Radar Holographic Sweep Beam + Trail
    sweep_a = math.radians(_anim["scan_angle"])
    sweep_r = base_r * 0.88
    sx = RCX + sweep_r * math.cos(sweep_a)
    sy = RCY - sweep_r * math.sin(sweep_a)

    for trail_i in range(5):
        trail_a = _anim["scan_angle"] - trail_i * 4
        ta = math.radians(trail_a)
        tx = RCX + sweep_r * math.cos(ta)
        ty = RCY - sweep_r * math.sin(ta)
        alpha = 1.0 - trail_i * 0.2
        trail_c = _lerp_color(C["void"], c1, alpha * 0.3)
        reactor_cv.create_line(RCX, RCY, tx, ty, fill=trail_c, width=1)

    reactor_cv.create_line(RCX, RCY, sx, sy, fill=c1, width=1)

    # 9. Dynamic Energy Nodes (disperse further when active)
    for pi in range(8):
        p_angle = math.radians(a * (1.5 + pi * 0.3) + pi * 45)
        dispersion = base_r * (0.36 + 0.14 * energy_level + 0.04 * math.sin(a * 0.04 + pi))
        px = RCX + dispersion * math.cos(p_angle)
        py = RCY - dispersion * math.sin(p_angle)
        p_size = 2 + int(energy_level > 0.5)
        reactor_cv.create_oval(px - p_size, py - p_size, px + p_size, py + p_size, fill=c1, outline="")

    # 10. Expanding Ripples
    new_ripples = []
    for rip in _anim["ripples"]:
        rr = rip["r"]
        ra = rip["alpha"]
        if ra > 0.05:
            rc = _lerp_color(C["surface"], c1, ra)
            reactor_cv.create_oval(RCX - rr, RCY - rr, RCX + rr, RCY + rr, outline=rc, width=2)
            rip["r"] += 180.0 * dt
            rip["alpha"] -= 1.8 * dt
            if rip["r"] < base_r * 1.15:
                new_ripples.append(rip)
    _anim["ripples"] = new_ripples

    # 11. Responsive Neural Core Glow & Star
    _anim["pulse_phase"] = (_anim["pulse_phase"] + 0.07 * (1.0 + energy_level) * dt_scale) % (2 * math.pi)
    p = 0.5 + 0.5 * math.sin(_anim["pulse_phase"])
    core_r = base_r * (0.24 + 0.06 * energy_level * p)
    glow_r = core_r * 0.6
    center_r = core_r * 0.26

    # Colors
    if _anim["listening"]: gr, gg, gb = 0, int(130 + p * 125), int(50 + p * 78)
    elif _anim["processing"]: gr, gg, gb = int(170 + p * 85), int(100 + p * 70), int(p * 30)
    elif _anim["speaking"]: gr, gg, gb = 0, int(180 + p * 75), int(200 + p * 55)
    else: gr, gg, gb = 0, int(90 + p * 140), int(140 + p * 115)

    core_glow_clr = f"#{min(gr,255):02x}{min(gg,255):02x}{min(gb,255):02x}"
    center_glow = _lerp_color("#88ccdd", C["white"], 0.7 + 0.3 * p)

    # Core base ring
    reactor_cv.create_oval(RCX - core_r, RCY - core_r, RCX + core_r, RCY + core_r, fill="#051524", outline=c1, width=2)
    # Intermediate glow halo
    reactor_cv.create_oval(RCX - glow_r, RCY - glow_r, RCX + glow_r, RCY + glow_r, fill=core_glow_clr, outline="")
    # Inner white nucleus
    reactor_cv.create_oval(RCX - center_r, RCY - center_r, RCX + center_r, RCY + center_r, fill=center_glow, outline="")

    # Energy discharge filaments (when talking or listening)
    if _anim["listening"] or _anim["speaking"]:
        for f_i in range(4):
            f_ang = math.radians(a * 2.5 + f_i * 90)
            fx = RCX + (core_r + (r3 - core_r) * p) * math.cos(f_ang)
            fy = RCY - (core_r + (r3 - core_r) * p) * math.sin(f_ang)
            reactor_cv.create_line(RCX, RCY, fx, fy, fill=c1, width=1)


def animate_waveform_step(dt):
    wave_cv.delete("bars")
    w = wave_cv.winfo_width()
    h = wave_cv.winfo_height()

    if w < 20 or h < 20:
        return

    n_bars = 70
    bw = max(2, (w - 30) // n_bars - 1)
    total_w = bw + 1
    sx = (w - n_bars * total_w) // 2
    my = h // 2
    t = _time.time()

    for i in range(n_bars):
        if _anim["listening"]:
            base = math.sin(t * 8.0 + i * 0.3) * h * 0.38
            noise = random.randint(-6, 6)
            bh = max(4, int(abs(base) + abs(noise) + 5))
            clr = C["green"] if i % 3 != 0 else C["cyan"]
        elif _anim["speaking"]:
            base = math.sin(t * 7.0 + i * 0.4) * h * 0.34
            noise = random.randint(-5, 5)
            bh = max(4, int(abs(base) + abs(noise) + 4))
            clr = C["cyan_br"] if i % 2 == 0 else C["cyan"]
        elif _anim["processing"]:
            base = math.sin(t * 4.0 + i * 0.5) * h * 0.22
            bh = max(3, int(abs(base) + 3))
            clr = C["amber"] if i % 4 != 0 else C["amber_dim"]
        else:
            base = math.sin(t * 1.5 + i * 0.15) * 3
            bh = max(1, int(abs(base) + 1))
            clr = C["border"]

        x = sx + i * total_w
        # Studio Equalizer Mirror Effect: top half + bottom reflection
        y1 = my - bh // 2
        y2 = my + bh // 2
        wave_cv.create_rectangle(x, y1, x + bw, y2, fill=clr, outline="", tags="bars")
        # Subdued bottom mirror
        wave_cv.create_rectangle(x, y2, x + bw, y2 + bh // 4, fill=C["border"], outline="", tags="bars")


def animate_data_rain_step(dt):
    rain_cv.delete("rain")
    w = rain_cv.winfo_width()
    h = rain_cv.winfo_height()

    if w < 10 or h < 10:
        return

    # Responsive dynamic columns adapting to canvas width
    col_w = 14
    target_cols = max(10, (w - 12) // col_w)
    if len(_anim["data_rain_cols"]) != target_cols:
        _anim["data_rain_cols"] = [{
            "x": 8 + i * col_w,
            "y": random.uniform(-200, 0),
            "speed": random.uniform(0.9, 2.2),
            "length": random.randint(7, 18),
            "type": "tok" if (i % 3 == 0) else ("hex" if i % 2 == 0 else "glyph"),
            "token": "",
            "chars": [],
            "seed": random.random(),
        } for i in range(target_cols)]

    mode = _anim.get("matrix_mode", "core")
    mult = _anim.get("matrix_speed_mult", 1.0)
    mpos = _anim.get("matrix_mouse_pos")

    # Real-time core state responsiveness
    if _anim["listening"]:
        state_speed = 1.6
        lead_clr = "#ffffff"
        high_clr = C["green"]
        body_clr = C.get("green_dim", "#085828")
        dim_clr = "#022410"
        state_tag = "MIC ACTIVE"
    elif _anim["processing"]:
        state_speed = 1.45
        lead_clr = "#ffffff"
        high_clr = C["amber"]
        body_clr = C.get("amber_dim", "#7a4800")
        dim_clr = "#2b1800"
        state_tag = "PROCESSING"
    elif _anim["speaking"]:
        state_speed = 1.3
        lead_clr = "#ffffff"
        high_clr = C["cyan_br"]
        body_clr = C["cyan"]
        dim_clr = C["cyan_dim"]
        state_tag = "SPEECH OUT"
    elif _anim["edit_mode"]:
        state_speed = 1.0
        lead_clr = "#ffffff"
        high_clr = C["amber"]
        body_clr = C["border_gl"]
        dim_clr = C["border"]
        state_tag = "HUD CONFIG"
    else:
        state_speed = 1.0
        lead_clr = "#ffffff"
        high_clr = C["cyan_br"]
        body_clr = C["cyan"]
        dim_clr = C["cyan_dim"]
        state_tag = "STANDBY"

    hex_glyphs = "0123456789ABCDEF"
    sci_glyphs = "Ωλ§◈⌬⌁⚡⎊⌖0123456789ABCDEF"
    neural_glyphs = "∑∫∇√∝∯∂⊕⊗λπ0101"
    vox_glyphs = " ▂▃▄▅▆▇█"

    speed_step = mult * state_speed * 75.0 * dt

    for col in _anim["data_rain_cols"]:
        col["y"] += col["speed"] * speed_step
        if col["y"] > h + col["length"] * 14:
            col["y"] = random.uniform(-160, -20)
            col["speed"] = random.uniform(0.9, 2.2)
            col["length"] = random.randint(7, 18)
            col["chars"] = []
            if _anim["matrix_tokens"] and (col.get("type") == "tok" or random.random() < 0.35):
                col["token"] = random.choice(_anim["matrix_tokens"])
            else:
                col["token"] = ""

        tok_str = col.get("token", "")
        tok_len = len(tok_str)

        for ci in range(col["length"]):
            char_y = col["y"] + ci * 13
            if 0 <= char_y < h:
                # Hover proximity detection
                is_hover = False
                if mpos:
                    dist = math.hypot(col["x"] - mpos[0], char_y - mpos[1])
                    if dist < 36:
                        is_hover = True

                # Interactive decoded glyph or normal cybernetic glyph
                if is_hover:
                    ch = random.choice("JARVIS01OKACK")
                    fc = "#ffffff"
                    fnt = (FN, 8, "bold")
                elif ci == 0:
                    fc = lead_clr
                    fnt = (FN, 8, "bold")
                    ch = tok_str[0] if tok_str else random.choice(sci_glyphs)
                elif ci < 3:
                    fc = high_clr
                    fnt = (FN, 8)
                    ch = tok_str[ci] if ci < tok_len else random.choice(hex_glyphs)
                else:
                    fade = max(0.12, 1.0 - ci / col["length"])
                    fc = _lerp_color(dim_clr, body_clr, fade)
                    fnt = (FN, 8)
                    if ci < tok_len:
                        ch = tok_str[ci]
                    elif mode == "neural":
                        ch = random.choice(neural_glyphs)
                    elif mode == "vox":
                        ch = random.choice(vox_glyphs)
                    elif mode == "hex":
                        ch = random.choice(hex_glyphs)
                    else:
                        ch = random.choice(sci_glyphs)

                rain_cv.create_text(col["x"], char_y, text=ch, font=fnt, fill=fc, tags="rain")

    # Interactive Shockwave Ripples from clicks & EMP
    active_ripples = []
    for rip in _anim["matrix_ripples"]:
        rip["r"] += 170.0 * dt
        rip["alpha"] -= 1.8 * dt
        if rip["alpha"] > 0.04 and rip["r"] < rip.get("max_r", 90):
            rc = _lerp_color(C["void"], rip.get("clr", C["cyan_br"]), max(0.0, min(1.0, rip["alpha"])))
            rx, ry, rr = rip["x"], rip["y"], rip["r"]
            rain_cv.create_oval(rx - rr, ry - rr, rx + rr, ry + rr, outline=rc, width=2, tags="rain")
            active_ripples.append(rip)
    _anim["matrix_ripples"] = active_ripples

    # Interactive Cyber Spark Trails from mouse drag
    active_sparks = []
    for spk in _anim["matrix_sparks"]:
        spk["x"] += spk["vx"] * 60.0 * dt
        spk["y"] += spk["vy"] * 60.0 * dt
        spk["alpha"] -= 2.2 * dt
        if spk["alpha"] > 0.05 and 0 <= spk["x"] < w and 0 <= spk["y"] < h:
            sc = _lerp_color(C["void"], spk.get("clr", C["cyan_br"]), max(0.0, min(1.0, spk["alpha"])))
            sx, sy = spk["x"], spk["y"]
            rain_cv.create_oval(sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5, fill=sc, outline="", tags="rain")
            active_sparks.append(spk)
    _anim["matrix_sparks"] = active_sparks

    # Interactive Hover Crosshair & Targeting Telemetry Overlay
    if mpos:
        mx, my = mpos
        if 0 <= mx <= w and 0 <= my <= h:
            rain_cv.create_line(0, my, w, my, fill=C["cyan_faint"], width=1, dash=(2, 4), tags="rain")
            rain_cv.create_line(mx, 0, mx, h, fill=C["cyan_faint"], width=1, dash=(2, 4), tags="rain")
            cs = 8
            rain_cv.create_line(mx - cs, my - cs, mx - cs // 2, my - cs, fill=C["cyan_br"], width=1, tags="rain")
            rain_cv.create_line(mx - cs, my - cs, mx - cs, my - cs // 2, fill=C["cyan_br"], width=1, tags="rain")
            rain_cv.create_line(mx + cs, my + cs, mx + cs // 2, my + cs, fill=C["cyan_br"], width=1, tags="rain")
            rain_cv.create_line(mx + cs, my + cs, mx + cs, my + cs // 2, fill=C["cyan_br"], width=1, tags="rain")
            node_id = (int(mx * 3 + my * 7)) % 256
            act_fps = _anim.get("fps_actual", 60.0)
            rain_cv.create_text(
                8, h - 8, anchor="w",
                text=f"⌖ NODE: 0x{node_id:02X} | POS: [{mx:3d},{my:3d}] | {state_tag} | {act_fps:4.1f} FPS",
                font=(FN, 7, "bold"), fill=C["cyan_br"], tags="rain"
            )


def animate_particles_step(dt):
    bg_cv.delete("particles")
    w = bg_cv.winfo_width()
    h = bg_cv.winfo_height()

    if w < 10:
        return

    dt_scale = dt * 60.0
    for pt in _anim["particles"]:
        pt["x"] += pt["vx"] * dt_scale
        pt["y"] += pt["vy"] * dt_scale
        if pt["x"] < 0: pt["x"] = w
        if pt["x"] > w: pt["x"] = 0
        if pt["y"] < 0: pt["y"] = h
        if pt["y"] > h: pt["y"] = 0

        b = pt["brightness"]
        if _anim["listening"]: clr = _lerp_color(C["void"], C["green"], b * 0.5)
        elif _anim["speaking"]: clr = _lerp_color(C["void"], C["cyan_br"], b * 0.5)
        elif _anim["processing"]: clr = _lerp_color(C["void"], C["amber"], b * 0.4)
        else: clr = _lerp_color(C["void"], C["cyan"], b * 0.3)

        s = pt["size"]
        bg_cv.create_oval(pt["x"] - s, pt["y"] - s, pt["x"] + s, pt["y"] + s, fill=clr, outline="", tags="particles")


def pulse_panel_borders_step(dt):
    p = 0.5 + 0.5 * math.sin(_anim["pulse_phase"] * 0.8)
    if _anim["listening"]: bc = _lerp_color(C["border"], C["green"], p * 0.5)
    elif _anim["speaking"]: bc = _lerp_color(C["border"], C["cyan_br"], p * 0.5)
    elif _anim["processing"]: bc = _lerp_color(C["border"], C["amber"], p * 0.4)
    elif _anim["edit_mode"]: bc = _lerp_color(C["border_gl"], C["amber"], p * 0.6)
    else: bc = _lerp_color(C["border"], C["border_gl"], p * 0.3)

    for panel in (lp, cp, rp):
        panel.config(highlightbackground=bc)


def master_60fps_render():
    """Unified 60 FPS master animation scheduler with dynamic millisecond compensation."""
    t0 = _time.perf_counter()
    dt = t0 - _anim["last_frame_time"]
    _anim["last_frame_time"] = t0
    dt = min(max(dt, 0.001), 0.05)

    _anim["fps_history"].append(dt)
    if len(_anim["fps_history"]) >= 8:
        _anim["fps_actual"] = len(_anim["fps_history"]) / sum(_anim["fps_history"])
        _anim["frame_count"] += 1
        if _anim["frame_count"] % 12 == 0 and "fps_badge_lbl" in globals() and fps_badge_lbl:
            cur_fps = _anim["fps_actual"]
            fps_badge_lbl.config(
                text=f"⚡ {cur_fps:4.1f} FPS",
                fg=C["green"] if cur_fps >= 55 else (C["cyan_br"] if cur_fps >= 45 else C["amber"])
            )

    # 1. Arc Reactor Step
    animate_reactor_step(dt)
    # 2. Audio Waveform Step
    animate_waveform_step(dt)
    # 3. Matrix Data Stream Step
    animate_data_rain_step(dt)
    # 4. Tech Particles Step
    animate_particles_step(dt)
    # 5. Glowing Borders Step
    pulse_panel_borders_step(dt)

    t1 = _time.perf_counter()
    work_ms = (t1 - t0) * 1000.0
    delay = max(1, int(16.666 - work_ms))
    root.after(delay, master_60fps_render)


# Compatibility aliases for any external/prior invocation
def animate_reactor(): pass
def animate_waveform(): pass
def animate_data_rain(): pass
def animate_particles(): pass
def pulse_panel_borders(): pass


def update_clock():
    now = _time.strftime("%I : %M : %S %p")
    date_str = _time.strftime("%d %b %Y").upper()
    clock_lbl.config(text=now)
    date_lbl.config(text=date_str)
    sec = int(_time.time()) % 2
    clock_lbl.config(fg=C["cyan"] if sec == 0 else C["cyan_dim"])
    root.after(1000, update_clock)


def blink_dot():
    cur = dot_cv.itemcget("dot", "fill")
    if _anim["listening"]:
        nxt = C["green"] if cur == C["void"] else C["void"]
        interval = 300
    elif _anim["speaking"]:
        nxt = C["cyan"] if cur == C["void"] else C["void"]
        interval = 250
    elif _anim["processing"]:
        nxt = C["amber"] if cur == C["void"] else C["void"]
        interval = 250
    else:
        nxt = C["green"]
        interval = 2000
    dot_cv.itemconfig("dot", fill=nxt)
    root.after(interval, blink_dot)


def update_metrics():
    """Live hardware & system telemetry sampler reading real CPU% and RAM%."""
    try:
        if _HAS_PSUTIL:
            cpu_val = psutil.cpu_percent(interval=None)
            mem_val = psutil.virtual_memory().percent
            metric_labels["CPU"].config(
                text=f"{int(cpu_val):02d}%",
                fg=C["green"] if cpu_val < 70 else (C["amber"] if cpu_val < 90 else C["red"])
            )
            metric_labels["MEM"].config(
                text=f"{int(mem_val):02d}%",
                fg=C["green"] if mem_val < 75 else (C["amber"] if mem_val < 90 else C["red"])
            )
            matrix_push_token(f"CPU:{int(cpu_val)}%")
            matrix_push_token(f"MEM:{int(mem_val)}%")
        else:
            metric_labels["CPU"].config(text="OK", fg=C["green"])
            metric_labels["MEM"].config(text="OK", fg=C["green"])
    except Exception:
        pass

    metric_labels["NET"].config(text="ONLINE", fg=C["green"])

    if _anim["listening"]:
        metric_labels["MIC"].config(text="ACTIVE", fg=C["green"])
    elif _anim["processing"]:
        metric_labels["MIC"].config(text="PROC", fg=C["amber"])
    else:
        metric_labels["MIC"].config(text="READY", fg=C["cyan"])

    if _anim["speaking"]:
        metric_labels["TTS"].config(text="SPEAK", fg=C["cyan_br"])
    else:
        metric_labels["TTS"].config(text="READY", fg=C["cyan"])

    root.after(500, update_metrics)


# ── Cinematic Boot Sequence ──────────────────────────
BOOT_LINES = [
    ("Initializing holographic workstation core...", C["cyan_dim"]),
    ("Mounting neural microphone & speech array...", C["cyan_dim"]),
    ("Calibrating bilingual Hindi/English NLP engine...", C["cyan"]),
    ("Activating DuckDuckGo & Wikipedia pipelines...", C["cyan"]),
    ("Live Typewriter Telemetry engine online...", C["green_dim"]),
    ("Calibrating hardware audio & display deck...", C["green"]),
    ("All systems operational.", C["cyan_br"]),
    ("J.A.R.V.I.S  v3.0  ONLINE", C["cyan_br"]),
]

def boot_sequence():
    step = _anim["boot_step"]
    if step == 0:
        play_sfx("boot")
        threading.Thread(target=_precalibrate_microphone, daemon=True).start()

    if step < len(BOOT_LINES):
        text, color = BOOT_LINES[step]
        substatus.config(text=text, fg=color)
        progress = int((step + 1) / len(BOOT_LINES) * 100)
        status_label.config(text=f"◎  BOOT  [{progress:3d}%]", fg=C["cyan"])
        ftr_status.config(text=f"▸  BOOTING TELEMETRY  [{progress}%]")
        _anim["boot_step"] += 1
        root.after(350, boot_sequence)
    else:
        _anim["boot_done"] = True
        status_label.config(text="◎  SYSTEMS NOMINAL", fg=C["cyan"])
        substatus.config(text="Holographic Workstation Ready. Speak or type below.", fg=C["text_dim"])
        ftr_status.config(text="▸  READY FOR TRANSMISSION")
        trigger_ripple()
        trigger_ripple()
        welcome_msg = "Hello sir, JARVIS is online. How do I help you?"
        terminal_feed_log("SYSTEM", welcome_msg)
        speak(welcome_msg)
        # Launch ambient background wake-word listener
        if hud_config.get("wake_word_enabled", True):
            threading.Thread(target=_wake_word_daemon, daemon=True).start()


# ── Initialize saved layout & animation loops ────────
if hud_config.get("theme") in THEMES:
    apply_theme(hud_config["theme"])

regrid_all_panels()
regrid_center_modules()

# Launch unified 60 FPS master rendering engine
master_60fps_render()
update_clock()
blink_dot()
update_metrics()

def _on_window_close():
    try:
        ctypes.windll.winmm.timeEndPeriod(1)
    except Exception:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", _on_window_close)

def _on_root_configure(event):
    if event.widget == root:
        win_w = event.width
        if win_w < 950:
            panel_weights["lp"] = 2
            panel_weights["cp"] = 5
            panel_weights["rp"] = 1
        else:
            panel_weights["lp"] = 3
            panel_weights["cp"] = 6
            panel_weights["rp"] = 2
        col_idx = 0
        for pid in hud_config["column_order"]:
            if hud_config["visible"].get(pid, True):
                main.columnconfigure(col_idx, weight=panel_weights[pid])
                col_idx += 1

root.bind("<Configure>", _on_root_configure)
root.after(500, boot_sequence)

if __name__ == "__main__":
    root.mainloop()

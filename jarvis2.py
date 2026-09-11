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
from pathlib import Path
import xml.etree.ElementTree as ET
from html import unescape
try:
    import pythoncom
    import win32com.client
    _HAS_WIN32COM = True
except Exception:
    _HAS_WIN32COM = False
import wave
import struct
import winsound



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
    "default_location": "India",
    "column_order": ["lp", "cp", "rp"],
    "center_order": ["term", "wave", "quick", "hardware"],
    "voice_rate": 175,
    "voice_index": 0,
    "voice_name": "Microsoft David Desktop - English (United States)",
    "tts_engine": "sapi",
    "elevenlabs_voice_id": "IRHApOXLvnW57QJPQH2P",
    "elevenlabs_voice_name": "Adam - American, Dark and Tough",
    "elevenlabs_api_key": "",
    "sfx_enabled": True,
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
}

_stream_queue = []
_stream_active = False

def clean_for_speech(text):
    if not text:
        return ""
    t = str(text)
    # Remove divider lines and decorative symbols
    t = re.sub(r"[-═─━_]{3,}", " ", t)
    t = re.sub(r"[╔╗╚╝║┃◈◉◎●◌▸⟫▶◀▲▼✓✕✔✗■◻★☆•]", " ", t)
    # Expand bracketed index like [01] to Headline 1:
    t = re.sub(r"\[0?([1-9])\]", r"Headline \1: ", t)
    # Remove academic/wiki citation brackets like [1], [12], [a], [b]
    t = re.sub(r"\[[0-9a-zA-Z]{1,3}\]", " ", t)
    # Remove raw URLs
    t = re.sub(r"https?://\S+|www\.\S+", " ", t)
    # Strip UI hints
    t = re.sub(r"\b(?:Click\s+\[READ\]\s+to\s+re-hear|Click\s+\[CLR\]\s+to\s+clear)\b", "", t, flags=re.IGNORECASE)
    # Expand units & abbreviations for natural speech
    t = re.sub(r"\bdeg\s*C\b|°C", " degrees Celsius ", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdeg\s*F\b|°F", " degrees Fahrenheit ", t, flags=re.IGNORECASE)
    t = re.sub(r"\bkm/h\b|\bkmph\b", " kilometers per hour ", t, flags=re.IGNORECASE)
    t = re.sub(r"\bkm\b", " kilometers ", t, flags=re.IGNORECASE)
    t = re.sub(r"%", " percent ", t)
    t = re.sub(r"&", " and ", t)
    t = re.sub(r"\bwttr\.in\b", " weather network ", t, flags=re.IGNORECASE)
    t = re.sub(r"[|/]{2,}", ". ", t)
    t = re.sub(r"[|]+", ". ", t)
    # Convert line breaks to periods if line does not end with terminal punctuation
    lines = [line.strip() for line in t.splitlines() if line.strip()]
    punctuated = []
    for line in lines:
        if not re.search(r"[.!?:;]$", line):
            line += "."
        punctuated.append(line)
    res = " ".join(punctuated)
    # Normalize multiple punctuation and whitespaces
    res = re.sub(r"\.+", ".", res)
    res = re.sub(r"\s+", " ", res)
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

                        wmp = win32com.client.Dispatch("WMPlayer.OCX")
                        media = wmp.newMedia(str(target_to_play))
                        wmp.currentPlaylist.appendItem(media)
                        wmp.controls.play()

                        # Monitor playback completion and properly release COM handles
                        t0 = _time.time()
                        while _time.time() - t0 < 35:
                            state = getattr(wmp, "playState", 0)
                            if state in (1, 8):  # 1=stopped, 8=mediaEnded, 10=ready
                                break
                            _time.sleep(0.1)

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

def switch_voice_profile(voice_index, speak_confirm=True):
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
        confirm_text = (
            f"Voice profile updated to {vinfo['alias']} neural core. Online and at your service, sir."
            if vinfo["is_female"] else
            f"Voice profile updated to {vinfo['alias']} tactical core. Ready for your command, sir."
        )
        speak(confirm_text)

    return True

def switch_voice_by_query(query_or_index, speak_confirm=True):
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

    return switch_voice_profile(target_idx, speak_confirm=speak_confirm)

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

def _safe_ui_update(fn):
    try:
        if "root" in globals() and root:
            root.after(0, fn)
    except Exception:
        pass

def _tts_daemon_loop():
    global _tts_skip_flag
    speaker = None

    def _apply_voice(spk, idx):
        if not spk: return
        try:
            if spk[0] == "sapi":
                v_coll = spk[1].GetVoices()
                if 0 <= idx < v_coll.Count:
                    spk[1].Voice = v_coll.Item(idx)
            elif spk[0] == "pyttsx3":
                p_v = spk[1].getProperty("voices")
                if 0 <= idx < len(p_v):
                    spk[1].setProperty("voice", p_v[idx].id)
        except Exception as ve:
            print("Voice apply note:", ve)

    # Priority 1: Native Windows SAPI.SpVoice via win32com (direct C++ COM, no deadlocks)
    try:
        if _HAS_WIN32COM:
            pythoncom.CoInitialize()
            sapi_voice = win32com.client.Dispatch("SAPI.SpVoice")
            sapi_voice.Rate = 1
            sapi_voice.Volume = 100
            init_idx = hud_config.get("voice_index", 0)
            voices = sapi_voice.GetVoices()
            if 0 <= init_idx < voices.Count:
                sapi_voice.Voice = voices.Item(init_idx)
            speaker = ("sapi", sapi_voice)
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
            print("J.A.R.V.I.S pyttsx3 Speech Engine Online.")
        except Exception as pe:
            print("pyttsx3 fallback error:", pe)

    while True:
        try:
            item = _tts_queue.get()
            if item is None:
                break

            if isinstance(item, tuple) and item[0] == "SET_VOICE":
                _apply_voice(speaker, item[1])
                _tts_queue.task_done()
                continue

            if isinstance(item, tuple) and item[0] == "AUDITION_VOICE":
                aud_idx, aud_text = item[1], item[2]
                saved_idx = hud_config.get("voice_index", 0)
                _apply_voice(speaker, aud_idx)
                _safe_ui_update(lambda: set_status("◈  AUDITIONING VOICE PROFILE...", C.get("cyan_br", "#40ffff")))
                try:
                    if speaker[0] == "sapi":
                        speaker[1].Speak(aud_text, 0)
                    elif speaker[0] == "pyttsx3":
                        speaker[1].say(aud_text)
                        speaker[1].runAndWait()
                except Exception as ae:
                    print("Audition speak error:", ae)
                _apply_voice(speaker, saved_idx)
                _safe_ui_update(lambda: set_status("◎  SYSTEMS NOMINAL", C.get("cyan", "#00e5ff")))
                _tts_queue.task_done()
                continue

            if isinstance(item, tuple) and item[0] == "AUDITION_ELEVENLABS":
                vid = item[1]
                audition_elevenlabs_voice(vid)
                _tts_queue.task_done()
                continue

            text = item
            if not text or not speaker:
                _tts_queue.task_done()
                continue

            _tts_skip_flag = False
            _anim["speaking"] = True

            # Clean and expand symbols so the complete result is spoken naturally
            cleaned_text = clean_for_speech(text)

            # Check if ElevenLabs Neural Cloud TTS is active
            tts_mode = hud_config.get("tts_engine", "sapi")
            el_key = hud_config.get("elevenlabs_api_key", "").strip()
            el_voice = hud_config.get("elevenlabs_voice_id", "IRHApOXLvnW57QJPQH2P")
            if tts_mode == "elevenlabs" and el_key:
                _safe_ui_update(lambda: set_status("◈  ELEVENLABS NEURAL TTS...", C.get("cyan_br", "#40ffff")))
                succ, el_audio, err = synthesize_elevenlabs_speech(cleaned_text, el_voice, el_key)
                if succ and el_audio:
                    play_audio_file(el_audio, async_play=False)
                    if _tts_queue.empty() and not _anim.get("processing", False):
                        _anim["speaking"] = False
                        _safe_ui_update(lambda: set_status("◎  SYSTEMS NOMINAL", C.get("cyan", "#00e5ff")))
                    _tts_queue.task_done()
                    continue
                else:
                    terminal_feed_log("TTS", f"ElevenLabs fallback to SAPI: {err}")

            # Split into sentence chunks so long outputs are never truncated
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', cleaned_text) if s.strip()]
            if not sentences:
                sentences = [cleaned_text]

            # Dynamic rate adjustment
            try:
                rate_val = hud_config.get("voice_rate", 175)
                if speaker[0] == "sapi":
                    speaker[1].Rate = max(-10, min(10, int((rate_val - 175) / 15)))
                elif speaker[0] == "pyttsx3":
                    speaker[1].setProperty("rate", rate_val)
            except Exception:
                pass

            for idx, s in enumerate(sentences):
                if _tts_skip_flag:
                    break
                if not s:
                    continue

                snippet = s[:36].replace("\n", " ")
                _safe_ui_update(lambda sn=snippet: set_status(f"◈  SPEAKING: {sn}...", C.get("cyan_br", "#40ffff")))

                try:
                    if speaker[0] == "sapi":
                        speaker[1].Speak(s, 0)
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

def speak(text, interrupt=False, block=False):
    global _tts_skip_flag
    if not text:
        return
    if interrupt:
        _tts_skip_flag = True
        while not _tts_queue.empty():
            try:
                _tts_queue.get_nowait()
                _tts_queue.task_done()
            except Exception:
                break
    _tts_queue.put(text)
    if block:
        _tts_queue.join()



# ╔══════════════════════════════════════════════════════════════════╗
# ║  VOICE RECOGNITION PIPELINE                                      ║
# ╚══════════════════════════════════════════════════════════════════╝

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        play_sfx("sonar")
        root.after(0, lambda: set_status("◉  VOICE CAPTURE ACTIVE", C["green"]))
        _anim["listening"] = True
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            root.after(0, lambda: set_status("◈  ANALYZING AUDIO SIGNAL...", C["amber"]))
            _anim["listening"] = False
            _anim["processing"] = True
            query = recognizer.recognize_google(audio, language="en-in")
            return query.lower().strip()
        except sr.WaitTimeoutError:
            play_sfx("alert")
            root.after(0, lambda: set_status("◌  NO AUDIO SIGNAL DETECTED", C["red"]))
            return None
        except sr.UnknownValueError:
            play_sfx("alert")
            root.after(0, lambda: set_status("◌  SPEECH PATTERN UNRECOGNIZED", C["red"]))
            return None
        except Exception as e:
            print("Microphone/API Error:", e)
            play_sfx("alert")
            root.after(0, lambda: set_status("◌  AUDIO INPUT FAULT", C["red"]))
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
        "I can answer questions by searching live web intelligence, stream breaking news headlines, report weather forecasts, autoplay YouTube videos, and adjust system volume and brightness.",
    r"^(?:thank\s+you|thanks|great\s+job|well\s+done)\b": 
        "You are very welcome, sir. Standing by for your next instruction.",
    r"^(?:who\s+created\s+you|who\s+made\s+you|who\s+is\s+your\s+creator)\b":
        "I was developed as a holographic AI voice assistant inspired by Tony Stark's J.A.R.V.I.S to assist you with intelligent workstation workflows.",
}

def check_conversational_query(query):
    q = query.strip().lower()
    for pattern, response in CONVERSATIONAL_INTENTS.items():
        if re.search(pattern, q):
            return response
    return None

def clean_search_query(query):
    patterns = [
        r"^(?:who\s+is|what\s+is|tell\s+me\s+about|explain|define|search\s+internet\s+for|search\s+web\s+for|search\s+google\s+for|search\s+for|search)\s+",
        r"\s+(?:on\s+google|in\s+google|on\s+wikipedia|in\s+wikipedia|on\s+the\s+web|on\s+internet)$",
    ]
    cleaned = query.strip()
    for p in patterns:
        cleaned = re.sub(p, "", cleaned, flags=re.IGNORECASE).strip()
    return cleaned if cleaned else query.strip()

def search_internet_data(query):
    # 1. Determine whether Internet information is needed
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

    entity = clean_search_query(query)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

    # 2. DuckDuckGo Instant Answers API
    try:
        ddg_url = "https://api.duckduckgo.com/"
        params = {"q": entity, "format": "json", "no_html": 1, "skip_disambig": 1}
        res = requests.get(ddg_url, params=params, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            abstract = data.get("AbstractText", "").strip()
            heading = data.get("Heading", entity)
            source = data.get("AbstractSource", "DuckDuckGo Intel")
            if abstract and len(abstract) > 30:
                return {
                    "needed_web": True,
                    "found": True,
                    "source": f"{source.upper()} // INSTANT INTEL",
                    "title": heading,
                    "full_text": abstract,
                    "speech_text": clean_for_speech(abstract),
                }
    except Exception as e:
        print("DuckDuckGo API error:", e)

    # 3. Wikipedia Official REST API
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {"action": "query", "list": "search", "srsearch": entity, "format": "json", "utf8": 1, "srlimit": 1}
        search_res = requests.get(search_url, params=search_params, headers=headers, timeout=5)
        if search_res.status_code == 200:
            s_data = search_res.json()
            items = s_data.get("query", {}).get("search", [])
            if items:
                title = items[0]["title"]
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title, safe='')}"
                sum_res = requests.get(summary_url, headers=headers, timeout=5)
                if sum_res.status_code == 200:
                    extract = sum_res.json().get("extract", "").strip()
                    if extract and len(extract) > 40:
                        return {
                            "needed_web": True,
                            "found": True,
                            "source": "WIKIPEDIA // OFFICIAL ARCHIVE",
                            "title": title,
                            "full_text": extract,
                            "speech_text": clean_for_speech(extract),
                        }
    except Exception as e:
        print("Wikipedia API error:", e)

    # 4. Live Web Search & Multi-Source Synthesis (DuckDuckGo Lite)
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
                elif len(txt) > 40 and not "duckduckgo" in txt.lower():
                    clean_snip = re.sub(r"\[[a-z0-9]\]", "", txt).strip()
                    clean_snip = re.sub(r"\s+", " ", clean_snip)
                    if clean_snip not in collected_snippets:
                        collected_snippets.append(clean_snip)

            if collected_snippets:
                # Relevance validation to prevent random suggestions
                q_words = [w.lower() for w in re.findall(r'\b[a-zA-Z0-9]{3,}\b', query) if w.lower() not in ('who', 'what', 'why', 'how', 'when', 'where', 'the', 'is', 'are', 'was', 'were', 'for', 'about')]
                relevant = any(w in collected_snippets[0].lower() for w in q_words) if q_words else True
                if relevant:
                    full_body = "\n\n".join(collected_snippets[:3])
                    sources_str = ", ".join(collected_sources[:2]) if collected_sources else "Web Intelligence"
                    
                    return {
                        "needed_web": True,
                        "found": True,
                        "source": f"WEB TELEMETRY // {sources_str.upper()}",
                        "title": query.title(),
                        "full_text": full_body,
                        "speech_text": clean_for_speech(full_body),
                    }
    except Exception as e:
        print("Live web search error:", e)

    # 5. Clear Not Found Notice - Do not guess or make up info!
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
        "title": query.title(),
        "full_text": "\n".join(lines),
        "speech_text": f"I searched the web, but I could not find verified data on {entity}. Please try rephrasing your question.",
    }



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
    q = query.strip().lower()
    m = re.search(r"(?:weather|temperature|climate|forecast)\s+(?:in|of|at|for)\s+([a-zA-Z\s]+)", q)
    if m:
        loc = m.group(1).strip()
        loc = re.sub(r"\b(today|now|right now|currently|please|jarvis)\b", "", loc).strip()
        if loc:
            return loc

    m = re.search(r"^([a-zA-Z\s]+?)\s+(?:weather|temperature|climate|forecast)$", q)
    if m:
        candidate = m.group(1).strip()
        stop_words = {
            "what is the", "what is", "what's the", "whats the", "tell me the",
            "tell me", "how is the", "how is", "check the", "check", "the", "current",
            "today's", "today", "live", "show", "give me"
        }
        if candidate not in stop_words and not any(candidate.startswith(sw) for sw in ["what", "how", "tell", "show", "check"]):
            return candidate

    return None

def fetch_weather(location=None):
    headers = {"User-Agent": "Jarvis-HUD-Meteo/3.2"}
    target = location or hud_config.get("default_location", "India")
    url = f"https://wttr.in/{urllib.parse.quote(target)}?format=j1"

    res = requests.get(url, headers=headers, timeout=6)
    if res.status_code != 200:
        raise Exception(f"Atmospheric link status {res.status_code}")

    data = res.json()
    cur = data.get("current_condition", [{}])[0]
    area_obj = data.get("nearest_area", [{}])[0]
    city = area_obj.get("areaName", [{}])[0].get("value", target)
    country = area_obj.get("country", [{}])[0].get("value", "")
    loc_display = f"{city}, {country}" if country else city

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

def weather_telemetry(location=None):
    root.after(0, lambda: set_status("◈  SYNCHRONIZING ORBITAL WEATHER LINK...", C["amber"]))
    try:
        data = fetch_weather(location)
        _anim["last_answer"] = data["full_text"]
        root.after(0, lambda: terminal_feed_intel("METEOROLOGICAL SATELLITE", f"WEATHER TELEMETRY // {data['city'].upper()}", data["full_text"]))
        speak(data["speech_text"])
    except Exception as e:
        print("Weather telemetry error:", e)
        err_msg = f"Unable to establish weather telemetry uplink: {e}"
        root.after(0, lambda: terminal_feed_log("METEO FAULT", err_msg))
        speak("I was unable to retrieve the weather data at this moment.")


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

def fetch_news(topic_code=None, topic_name="TOP BREAKING HEADLINES", search_query=None):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
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

        spoken_headlines.append(f"Headline {i}: {headline}, reported by {source}.")

    lines.append("------------------------------------------------------------")
    lines.append("Live satellite news feed updated. Click [READ] to re-hear.")

    full_text = "\n".join(lines).strip()
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

def news_telemetry(topic_code=None, topic_name="TOP BREAKING HEADLINES", search_query=None):
    root.after(0, lambda: set_status("◈  DOWNLINKING GLOBAL NEWS TELEMETRY...", C["amber"]))
    try:
        data = fetch_news(topic_code, topic_name, search_query)
        _anim["last_answer"] = data["full_text"]
        root.after(0, lambda: terminal_feed_intel("GLOBAL NEWS FEED", data["title"], data["full_text"]))
        speak(data["speech_text"])
    except Exception as e:
        print("News telemetry error:", e)
        err_msg = f"Unable to establish news telemetry link: {e}"
        root.after(0, lambda: terminal_feed_log("NEWS FAULT", err_msg))
        speak("I was unable to retrieve the latest news dispatches at this moment.")


# ╔══════════════════════════════════════════════════════════════════╗
# ║  SMART YOUTUBE AUTO-PLAY & DIRECT STREAMING                      ║
# ╚══════════════════════════════════════════════════════════════════╝

def extract_youtube_query(query):
    q = query.strip()
    patterns = [
        r"open\s+youtube\s+and\s+play\s+(.+)",
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
            if extracted:
                return extracted
    return q

def youtube_play(query):
    clean = query.strip()
    if not clean:
        speak("What would you like me to play on YouTube?")
        return

    root.after(0, lambda: terminal_feed_log("MEDIA DISPATCH", f"Scanning YouTube stream for: '{clean}'..."))
    root.after(0, lambda: set_status("◈  LOCATING YOUTUBE VIDEO STREAM...", C["amber"]))

    video_id = None
    try:
        encoded = urllib.parse.quote_plus(clean)
        search_url = f"https://www.youtube.com/results?search_query={encoded}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        res = requests.get(search_url, headers=headers, timeout=6)
        if res.status_code == 200:
            matches = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', res.text)
            for vid in matches:
                if len(vid) == 11:
                    video_id = vid
                    break
    except Exception as e:
        print("YouTube video scrape error:", e)

    if video_id:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        log_content = (
            f"Exact Video Match Identified: [ID: {video_id}]\n"
            f"Target URL: {video_url}\n"
            f"Status: Browser stream initiated with direct autoplay enabled."
        )
        yt_speech = f"Identified exact video match for {clean}. Initiating browser stream with direct autoplay enabled."
        root.after(0, lambda: terminal_feed_intel("MEDIA DISPATCH", f"YOUTUBE AUTOPLAY // {clean.upper()}", log_content))
        _anim["last_answer"] = f"Playing {clean} on YouTube: {video_url}"
        speak(yt_speech)
        webbrowser.open(video_url)
    else:
        fallback_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(clean)}"
        fallback_speech = f"Direct ID scan timed out. Dispatched search results for {clean} on YouTube."
        root.after(0, lambda: terminal_feed_intel("MEDIA DISPATCH", f"YOUTUBE SEARCH // {clean.upper()}", f"Direct ID scan timed out. Dispatched search results for '{clean}'."))
        _anim["last_answer"] = f"YouTube search results for: {clean}"
        speak(fallback_speech)
        webbrowser.open(fallback_url)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  COMMAND EXECUTION THREAD                                        ║
# ╚══════════════════════════════════════════════════════════════════╝

def execute_command_thread(raw_query):
    if not raw_query:
        _anim["processing"] = False
        set_status("◎  SYSTEMS NOMINAL", C["cyan"])
        return

    query = raw_query.strip().lower()
    trigger_ripple()
    play_sfx("transmit")

    root.after(0, lambda: terminal_feed_user(raw_query))
    root.after(0, lambda: set_status("◈  PROCESSING TELEMETRY...", C["amber"]))
    _anim["processing"] = True

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
        switch_voice_by_query(query, speak_confirm=True)
        _finish_command()
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
        speak(sample)
        _finish_command()
        return

    # Cybernetic Sound Effects Commands
    if any(k in query for k in ("enable sound effects", "enable sfx", "turn on sound effects", "turn on sfx", "unmute sound effects", "unmute sfx")):
        hud_config["sfx_enabled"] = True
        save_config()
        play_sfx("switch", force=True)
        terminal_feed_log("AUDIO", "Cybernetic sound effects suite enabled.")
        speak("Cybernetic sound effects have been activated.")
        _finish_command()
        return

    if any(k in query for k in ("disable sound effects", "disable sfx", "turn off sound effects", "turn off sfx", "mute sound effects", "mute sfx")):
        hud_config["sfx_enabled"] = False
        save_config()
        terminal_feed_log("AUDIO", "Cybernetic sound effects suite muted.")
        speak("Cybernetic sound effects have been muted.")
        _finish_command()
        return

    if any(k in query for k in ("open voice lab", "open audio lab", "voice lab", "audio lab", "voice settings", "audio settings")):
        root.after(0, open_voice_audio_modal)
        speak("Opening Voice and Cybernetic Audio Lab.")
        _finish_command()
        return

    # ElevenLabs Neural Voice Commands
    if any(k in query for k in ("download voice", "download elevenlabs voice", "download eleven labs voice", "download eleven labs", "download adam voice", "download voice sample")):
        play_sfx("downlink")
        terminal_feed_log("VOICE", "Downloading ElevenLabs voice IRHApOXLvnW57QJPQH2P (Adam)...")
        speak("Downloading ElevenLabs voice profile Adam, Voice ID IRHApOXLvnW57QJPQH2P.")
        def _bg_dl():
            succ, meta, path, msg = download_elevenlabs_voice("IRHApOXLvnW57QJPQH2P")
            if succ:
                terminal_feed_log("VOICE", f"ElevenLabs Voice Downloaded: {meta.get('name', 'Adam')}")
                speak("ElevenLabs voice profile Adam downloaded successfully. Auditioning downloaded sample now.")
                _time.sleep(0.5)
                audition_elevenlabs_voice("IRHApOXLvnW57QJPQH2P")
            else:
                terminal_feed_log("VOICE", f"Download failed: {msg}")
                speak(f"Voice download failed. Reason: {msg}")
        threading.Thread(target=_bg_dl, daemon=True).start()
        _finish_command()
        return

    if any(k in query for k in ("audition elevenlabs", "audition eleven labs", "audition adam", "play elevenlabs", "play eleven labs", "play voice sample", "audition voice sample", "play adam voice")):
        play_sfx("ack")
        audition_elevenlabs_voice("IRHApOXLvnW57QJPQH2P")
        _finish_command()
        return

    if any(k in query for k in ("switch to elevenlabs", "use elevenlabs", "switch to eleven labs", "use eleven labs", "switch to adam voice", "switch to adam", "activate elevenlabs")):
        play_sfx("switch")
        hud_config["tts_engine"] = "elevenlabs"
        save_config()
        el_key = hud_config.get("elevenlabs_api_key", "").strip()
        if el_key:
            terminal_feed_log("VOICE", "ElevenLabs Neural Voice Core Activated.")
            speak("ElevenLabs neural voice engine activated with voice ID IRHApOXLvnW57QJPQH2P.")
        else:
            terminal_feed_log("VOICE", "ElevenLabs Voice Selected (Sample downloaded). API key required for live TTS.")
            speak("ElevenLabs voice profile Adam is selected. Voice sample is downloaded and ready. To generate dynamic live speech, please add your ElevenLabs API key in the Voice Lab modal. Offline speech will continue using Microsoft David.")
            _time.sleep(0.5)
            audition_elevenlabs_voice("IRHApOXLvnW57QJPQH2P")
        _finish_command()
        return

    if any(k in query for k in ("switch to sapi", "switch to windows voice", "switch to offline voice", "use sapi", "use offline voice")):
        play_sfx("switch")
        hud_config["tts_engine"] = "sapi"
        save_config()
        terminal_feed_log("VOICE", "Speech engine shifted to Windows offline SAPI.")
        speak("Speech engine switched to Windows offline voice.")
        _finish_command()
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
        speak("Tactical military radio transmission received. Emergency alert broadcast acknowledged, sir.")
        _finish_command()
        return

    # Volume
    if any(k in query for k in ("volume up", "increase volume", "volume increase")):
        play_sfx("ack")
        volume_up()
        _finish_command()
        return
    if any(k in query for k in ("volume down", "decrease volume", "volume decrease")):
        play_sfx("ack")
        volume_down()
        _finish_command()
        return
    if query == "mute" or "mute volume" in query:
        play_sfx("ack")
        volume_mute()
        _finish_command()
        return

    # Brightness
    if any(k in query for k in ("increase brightness", "brightness increase", "brightness up")):
        play_sfx("ack")
        cur = get_brightness()
        if cur is not None: set_brightness(min(100, cur + 10))
        _finish_command()
        return
    if any(k in query for k in ("decrease brightness", "brightness decrease", "brightness down")):
        play_sfx("ack")
        cur = get_brightness()
        if cur is not None: set_brightness(max(0, cur - 10))
        _finish_command()
        return
    if "set brightness" in query:
        play_sfx("ack")
        nums = re.findall(r"\d+", query)
        if nums: set_brightness(int(nums[0]))
        _finish_command()
        return

    # Direct Web Navigation
    if query in ("open google", "launch google"):
        terminal_feed_log("WEB", "Opening Google.")
        speak("Opening Google.")
        webbrowser.open("https://www.google.com/")
        _finish_command()
        return
    if query in ("open youtube", "launch youtube"):
        terminal_feed_log("WEB", "Opening YouTube.")
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com/")
        _finish_command()
        return
    if query in ("open wikipedia", "launch wikipedia"):
        terminal_feed_log("WEB", "Opening Wikipedia.")
        speak("Opening Wikipedia.")
        webbrowser.open("https://www.wikipedia.org/")
        _finish_command()
        return

    # Chronometer / Time Query (12-Hour Format)
    if any(k in query for k in ("what is the time", "what's the time", "whats the time", "tell me the time", "what time is it", "current time")) or query == "time":
        time_12 = _time.strftime("%I:%M %p")
        time_full = _time.strftime("%I:%M:%S %p")
        date_full = _time.strftime("%A, %d %B %Y")
        time_text = f"Current Local Time: {time_full}\nDate: {date_full}\nFormat: 12-Hour Chronometer (AM/PM)"
        time_speech = f"Current local time is {time_full}, on {date_full}. 12-hour chronometer mode active."
        _anim["last_answer"] = f"The current time is {time_full} on {date_full}."
        root.after(0, lambda: terminal_feed_intel("CHRONOMETER", "12-HOUR TIME TELEMETRY", time_text))
        speak(time_speech)
        _finish_command()
        return

    # Location Configuration
    if any(k in query for k in ("set default location to", "set my default location to", "set location to", "change default location to")):
        m = re.search(r"(?:set\s+(?:my\s+)?default\s+location\s+to|set\s+location\s+to|change\s+default\s+location\s+to)\s+([a-zA-Z\s]+)", query)
        if m:
            new_loc = m.group(1).strip().title()
            hud_config["default_location"] = new_loc
            save_config()
            terminal_feed_log("CONFIG", f"Default meteorological location updated to: {new_loc}")
            speak(f"Default location has been set to {new_loc}.")
            _finish_command()
            return

    # Weather Telemetry
    if any(w in query for w in ("weather", "temperature", "climate", "forecast")) and not query.startswith("who is"):
        loc = extract_weather_location(query)
        weather_telemetry(loc)
        _finish_command()
        return

    # News Intelligence Feed
    if any(w in query for w in ("news", "headline", "headlines")):
        topic_code, topic_name, search_q = extract_news_intent(query)
        news_telemetry(topic_code, topic_name, search_q)
        _finish_command()
        return

    # YouTube Smart Autoplay
    if any(w in query for w in ("play on youtube", "play in youtube", "play youtube", "youtube play", "search youtube", "open youtube and play")) or query.startswith("play "):
        yt_q = extract_youtube_query(query)
        if yt_q:
            youtube_play(yt_q)
            _finish_command()
            return

    # Internet Intelligence Search
    root.after(0, lambda: set_status("◈  QUERYING GLOBAL INTELLIGENCE...", C["amber"]))
    data = search_internet_data(query)
    _anim["last_answer"] = data["full_text"]

    root.after(0, lambda: terminal_feed_intel(data["source"], data["title"], data["full_text"]))
    speak(data["speech_text"])
    _finish_command()

def _finish_command():
    _anim["processing"] = False
    trigger_ripple()
    if not _anim.get("speaking", False) and _tts_queue.empty():
        _safe_ui_update(lambda: set_status("◎  SYSTEMS NOMINAL", C["cyan"]))

def dispatch_command(query_text):
    threading.Thread(target=execute_command_thread, args=(query_text,), daemon=True).start()

def run_mic_capture_async():
    set_status("◉  LISTENING FOR COMMAND...", C["green"])
    mic_btn.config(text="  ◼  LISTENING...  ", bg=C["red_dim"], fg=C["text"])
    trigger_ripple()

    query = take_command()
    mic_btn.config(text="  ▶  START LISTENING  ", bg=C["cyan_dim"], fg=C["text"])

    if query:
        dispatch_command(query)
    else:
        _anim["listening"] = False
        _anim["processing"] = False
        set_status("◎  SYSTEMS NOMINAL", C["cyan"])


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
    status_label.config(text=text, fg=color or C["cyan"])

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
    command=lambda: threading.Thread(target=run_mic_capture_async, daemon=True).start(),
)
mic_btn.grid(row=5, column=0, sticky="ew", padx=14, pady=(0, 6))

def _mic_enter(e):
    if not _anim["listening"]: mic_btn.config(bg=C["cyan"], fg=C["void"])
def _mic_leave(e):
    if not _anim["listening"]: mic_btn.config(bg=C["cyan_dim"], fg=C["text"])
mic_btn.bind("<Enter>", _mic_enter)
mic_btn.bind("<Leave>", _mic_leave)

_sep(lp, 6)
_hud(lp, "INTELLIGENCE CHANNELS").grid(row=7, column=0, sticky="w", padx=14, pady=(2, 3))

caps = (
    ("▸ DUCKDUCKGO", "Instant Facts & Summaries", C["cyan"]),
    ("▸ WIKIPEDIA",  "Global REST Archive",        C["green"]),
    ("▸ SAPI5 TTS",  "Simultaneous Voice Read",    C["amber"]),
    ("▸ HARDWARE",   "Display & Audio Controls",   C["purple"]),
)
for ci, (nm, desc, clr) in enumerate(caps, start=8):
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
        speak(_anim["last_answer"], interrupt=True)

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

_hud(rp, "MATRIX DATA STREAM").grid(row=1, column=0, sticky="w", padx=12, pady=(6, 2))

rain_cv = tk.Canvas(rp, bg=C["panel"], highlightbackground=C["border"], highlightthickness=1)
rain_cv.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 4))

for col_i in range(12):
    _anim["data_rain_cols"].append({
        "x": 8 + col_i * 13,
        "chars": [],
        "speed": random.uniform(0.8, 1.9),
        "y": random.randint(-180, 0),
        "length": random.randint(6, 16),
    })

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
    mic_btn.config(bg=C["cyan_dim"])
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
    ts = _time.strftime("%I:%M:%S %p")
    term_text.config(state="normal")
    term_text.insert("end", f"\n[{ts}] USER   ⟩ {query}\n", "user")
    term_text.see("end")
    term_text.config(state="disabled")

def terminal_feed_log(source, text):
    ts = _time.strftime("%I:%M:%S %p")
    term_text.config(state="normal")
    term_text.insert("end", f"[{ts}] {source} ⟩ {text}\n", "sys")
    term_text.see("end")
    term_text.config(state="disabled")

def terminal_feed_intel(source, title, text, auto_speak=False, speech_text=None):
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
# ║  11 SIMULTANEOUS ANIMATION ENGINES                               ║
# ╚══════════════════════════════════════════════════════════════════╝

def animate_reactor():
    w = reactor_cv.winfo_width()
    h = reactor_cv.winfo_height()
    if w < 40 or h < 40:
        root.after(100, animate_reactor)
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

    _anim["reactor_angle"] = (_anim["reactor_angle"] + rot_speed) % 360
    _anim["scan_angle"] = (_anim["scan_angle"] + scan_speed) % 360
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
            rip["r"] += 3
            rip["alpha"] -= 0.03
            if rip["r"] < base_r * 1.1:
                new_ripples.append(rip)
    _anim["ripples"] = new_ripples

    # 11. Responsive Neural Core Glow & Star
    _anim["pulse_phase"] = (_anim["pulse_phase"] + 0.07 * (1.0 + energy_level)) % (2 * math.pi)
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

    root.after(35, animate_reactor)


def animate_waveform():
    wave_cv.delete("bars")
    w = wave_cv.winfo_width()
    h = wave_cv.winfo_height()

    if w < 20 or h < 20:
        root.after(200, animate_waveform)
        return

    n_bars = 70
    bw = max(2, (w - 30) // n_bars - 1)
    total_w = bw + 1
    sx = (w - n_bars * total_w) // 2
    my = h // 2
    t = _time.time()

    for i in range(n_bars):
        if _anim["listening"]:
            base = math.sin(t * 8 + i * 0.3) * h * 0.38
            noise = random.randint(-7, 7)
            bh = max(4, int(abs(base) + abs(noise) + 5))
            clr = C["green"] if i % 3 != 0 else C["cyan"]
        elif _anim["speaking"]:
            base = math.sin(t * 7 + i * 0.4) * h * 0.34
            noise = random.randint(-5, 5)
            bh = max(4, int(abs(base) + abs(noise) + 4))
            clr = C["cyan_br"] if i % 2 == 0 else C["cyan"]
        elif _anim["processing"]:
            base = math.sin(t * 4 + i * 0.5) * h * 0.22
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

    interval = 40 if (_anim["listening"] or _anim["speaking"]) else (80 if _anim["processing"] else 120)
    root.after(interval, animate_waveform)


def animate_data_rain():
    rain_cv.delete("rain")
    w = rain_cv.winfo_width()
    h = rain_cv.winfo_height()

    if w < 10 or h < 10:
        root.after(200, animate_data_rain)
        return

    hex_chars = "0123456789ABCDEFΩλ§◈"
    for col in _anim["data_rain_cols"]:
        col["y"] += col["speed"] * 3
        if col["y"] > h + col["length"] * 14:
            col["y"] = random.randint(-180, -20)
            col["speed"] = random.uniform(0.8, 1.9)
            col["length"] = random.randint(6, 16)

        for ci in range(col["length"]):
            char_y = col["y"] + ci * 13
            if 0 <= char_y < h:
                if ci == 0: fc = C["cyan_br"] if not _anim["listening"] else C["green"]
                elif ci < 3: fc = C["cyan"] if not _anim["listening"] else C["green"]
                else:
                    fade = max(0.1, 1.0 - ci / col["length"])
                    fc = _lerp_color(C["panel"], C["cyan_dim"], fade)
                ch = random.choice(hex_chars) if random.random() < 0.15 else ""
                if ch:
                    rain_cv.create_text(col["x"], char_y, text=ch, font=(FN, 8), fill=fc, tags="rain")

    root.after(60, animate_data_rain)


def animate_particles():
    bg_cv.delete("particles")
    w = bg_cv.winfo_width()
    h = bg_cv.winfo_height()

    if w < 10:
        root.after(100, animate_particles)
        return

    for pt in _anim["particles"]:
        pt["x"] += pt["vx"]
        pt["y"] += pt["vy"]
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

    root.after(70, animate_particles)


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


def pulse_panel_borders():
    p = 0.5 + 0.5 * math.sin(_anim["pulse_phase"] * 0.8)
    if _anim["listening"]: bc = _lerp_color(C["border"], C["green"], p * 0.5)
    elif _anim["speaking"]: bc = _lerp_color(C["border"], C["cyan_br"], p * 0.5)
    elif _anim["processing"]: bc = _lerp_color(C["border"], C["amber"], p * 0.4)
    elif _anim["edit_mode"]: bc = _lerp_color(C["border_gl"], C["amber"], p * 0.6)
    else: bc = _lerp_color(C["border"], C["border_gl"], p * 0.3)

    for panel in (lp, cp, rp):
        panel.config(highlightbackground=bc)
    root.after(80, pulse_panel_borders)


def update_metrics():
    for key, ml in metric_labels.items():
        if key not in ("MIC", "TTS") and random.random() < 0.04:
            ml.config(text="SYNC", fg=C["amber"])
        elif key not in ("MIC", "TTS") and ml.cget("text") == "SYNC":
            ml.config(text="OK", fg=C["green"])

    if _anim["listening"]: metric_labels["MIC"].config(text="ACTIVE", fg=C["green"])
    elif _anim["processing"]: metric_labels["MIC"].config(text="PROC", fg=C["amber"])
    else: metric_labels["MIC"].config(text="READY", fg=C["cyan"])

    if _anim["speaking"]: metric_labels["TTS"].config(text="SPEAK", fg=C["cyan_br"])
    else: metric_labels["TTS"].config(text="READY", fg=C["cyan"])

    root.after(300, update_metrics)


# ── Cinematic Boot Sequence ──────────────────────────
BOOT_LINES = [
    ("Initializing holographic workstation core...", C["cyan_dim"]),
    ("Mounting neural microphone & speech array...", C["cyan_dim"]),
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
        tts_mode = hud_config.get("tts_engine", "sapi")
        if tts_mode == "elevenlabs":
            welcome_msg = "Adam ElevenLabs neural voice core online. All holographic workstation systems ready, sir."
        else:
            voices = get_available_voices()
            cur_idx = hud_config.get("voice_index", 0)
            vinfo = voices[cur_idx] if cur_idx < len(voices) else voices[0]
            welcome_msg = (
                "F.R.I.D.A.Y neural core online. All workstation systems ready, sir."
                if vinfo.get("is_female") else
                "J.A.R.V.I.S online. All holographic telemetry systems operational, sir."
            )
        terminal_feed_log("SYSTEM", welcome_msg)
        speak(welcome_msg)


# ── Initialize saved layout & animation loops ────────
if hud_config.get("theme") in THEMES:
    apply_theme(hud_config["theme"])

regrid_all_panels()
regrid_center_modules()

animate_reactor()
animate_waveform()
animate_data_rain()
animate_particles()
update_clock()
blink_dot()
pulse_panel_borders()
update_metrics()

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

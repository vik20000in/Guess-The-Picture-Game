"""
Generate simple sound effects for the Guess The Picture game using pydub and numpy
"""
import os
import numpy as np
from scipy.io import wavfile
from scipy import signal

# Create sounds directory if it doesn't exist
sounds_dir = 'sounds'
os.makedirs(sounds_dir, exist_ok=True)

def generate_tone(frequency, duration, sample_rate=44100, volume=0.3):
    """Generate a simple tone"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(frequency * 2 * np.pi * t)
    return (wave * volume * 32767).astype(np.int16)

def generate_beep(frequency=1000, duration=0.2, sample_rate=44100):
    """Generate a simple beep sound"""
    return generate_tone(frequency, duration, sample_rate)

def generate_rising_beep(start_freq=800, end_freq=1200, duration=0.3, sample_rate=44100):
    """Generate a rising pitch beep"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    frequency = np.linspace(start_freq, end_freq, len(t))
    wave = np.sin(frequency * 2 * np.pi * t / sample_rate)
    return (wave * 0.3 * 32767).astype(np.int16)

def generate_falling_beep(start_freq=1200, end_freq=600, duration=0.3, sample_rate=44100):
    """Generate a falling pitch beep"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    frequency = np.linspace(start_freq, end_freq, len(t))
    wave = np.sin(frequency * 2 * np.pi * t / sample_rate)
    return (wave * 0.3 * 32767).astype(np.int16)

def generate_success_sound(duration=0.5, sample_rate=44100):
    """Generate a success/correct answer sound - two ascending beeps"""
    sound1 = generate_tone(800, duration * 0.4, sample_rate, 0.4)
    sound2 = generate_tone(1200, duration * 0.4, sample_rate, 0.4)
    sound = np.concatenate([sound1, sound2])
    # Add fade out
    fade_len = int(0.1 * sample_rate)
    fade = np.linspace(1, 0, fade_len)
    sound[-fade_len:] = (sound[-fade_len:] * fade).astype(np.int16)
    return sound

def generate_background_music(duration=15, sample_rate=44100):
    """
    Generate soothing background music with gradually increasing beat.
    Creates a calm, flowing melody with tempo increasing over time.
    """
    sound = np.array([], dtype=np.int16)
    
    # Soothing note sequence (pentatonic scale - calming)
    base_notes = [
        (293, 0.4),   # D - root
        (349, 0.4),   # F - warm
        (392, 0.4),   # G - stable
        (349, 0.4),   # F - back down
    ]
    
    # Harmonic notes to play underneath (lower octave for richness)
    harmony_base = [146, 174, 196, 174]  # D, F, G, F (one octave lower)
    
    total_duration = 0
    time_phases = duration / 3  # Divide into 3 phases for tempo progression
    current_phase = 0
    
    while total_duration < duration:
        # Calculate current phase and tempo multiplier
        current_phase = total_duration / time_phases
        
        # Gradually speed up: start at 1.0x, end at 1.8x speed
        tempo_multiplier = 1.0 + (current_phase * 0.8)
        
        for i, (freq, base_duration) in enumerate(base_notes):
            if total_duration >= duration:
                break
            
            # Adjust note duration based on tempo
            adjusted_duration = base_duration / tempo_multiplier
            
            # Main melodic note
            t = np.linspace(0, adjusted_duration, int(sample_rate * adjusted_duration), False)
            
            # Create a smooth sine wave with slight envelope
            envelope = np.ones_like(t)
            # Fade in at the beginning
            fade_in_samples = int(0.02 * sample_rate)
            if fade_in_samples > 0:
                envelope[:fade_in_samples] = np.linspace(0, 1, fade_in_samples)
            # Fade out at the end
            fade_out_samples = int(adjusted_duration * sample_rate * 0.15)
            if fade_out_samples > 0:
                envelope[-fade_out_samples:] = np.linspace(1, 0, fade_out_samples)
            
            main_wave = np.sin(freq * 2 * np.pi * t) * envelope
            
            # Add harmony note (softer, lower)
            harmony_freq = harmony_base[i]
            harmony_wave = np.sin(harmony_freq * 2 * np.pi * t) * envelope * 0.5
            
            # Combine main and harmony
            combined = (main_wave + harmony_wave) * 0.25
            audio_data = (combined * 32767).astype(np.int16)
            
            sound = np.concatenate([sound, audio_data])
            total_duration += adjusted_duration
    
    return sound[:int(duration * sample_rate)]

# Generate all sound files
print("Generating sound effects...")

# 1. Background music
print("Generating background_music.mp3...")
bg_music = generate_background_music(15)
wavfile.write(os.path.join(sounds_dir, 'background_music.wav'), 44100, bg_music)

# 2. Reveal picture sound
print("Generating reveal_picture.mp3...")
reveal_pic = generate_rising_beep(600, 1000, 0.3)
wavfile.write(os.path.join(sounds_dir, 'reveal_picture.wav'), 44100, reveal_pic)

# 3. Reveal name sound
print("Generating reveal_name.mp3...")
reveal_name = generate_rising_beep(800, 1200, 0.4)
wavfile.write(os.path.join(sounds_dir, 'reveal_name.wav'), 44100, reveal_name)

# 4. Correct/success sound
print("Generating correct.mp3...")
correct = generate_success_sound(0.6)
wavfile.write(os.path.join(sounds_dir, 'correct.wav'), 44100, correct)

# 5. Timer end sound
print("Generating timer_end.mp3...")
timer_end = generate_falling_beep(1400, 400, 0.8)
wavfile.write(os.path.join(sounds_dir, 'timer_end.wav'), 44100, timer_end)

print("\n✓ All sound files generated successfully!")
print(f"Sound files are saved in the '{sounds_dir}' folder")
print("\nGenerated files:")
for filename in os.listdir(sounds_dir):
    filepath = os.path.join(sounds_dir, filename)
    filesize = os.path.getsize(filepath)
    print(f"  - {filename} ({filesize} bytes)")

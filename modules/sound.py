import math
import struct
import wave
import tempfile
import sys
import os
import time

try:
    import winsound  # only for Win32
except ImportError:
    pass


class Sound:
    def generate_beep_sound(self):
        """Generate alarm sound using only built-in Python libraries"""
        try:
            # Parameters for alarm sound
            sample_rate = 22050
            duration = 0.8
            frames = []
            
            for i in range(int(duration * sample_rate)):
                t = float(i) / sample_rate
                
                # Create alternating high-low beep pattern
                if t < 0.2:
                    freq = 1200  # High beep
                elif t < 0.4:
                    freq = 800   # Low beep
                elif t < 0.6:
                    freq = 1200  # High beep
                else:
                    freq = 0     # Silence
                
                if freq > 0:
                    wave_value = math.sin(freq * 2 * math.pi * t) * 0.7
                else:
                    wave_value = 0
                
                frames.append(struct.pack('<h', int(wave_value * 32767)))
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_file = f.name
            
            with wave.open(temp_file, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(b''.join(frames))
            
            return temp_file
            
        except Exception as e:
            print(f"Error generating sound: {e}")
            return None

    def play_beep_sound(self):
        """Generate and play the beep sound"""
        temp_file = self.generate_beep_sound()
        
        if temp_file:
            try:
                # Try to play the generated sound based on OS
                if sys.platform == "win32":
                    # Windows
                    try:
                        winsound.PlaySound(temp_file, winsound.SND_FILENAME)
                    except (ImportError, NameError):
                        # Fallback for Windows without winsound
                        os.system(f'start /min wmplayer "{temp_file}"')
                        time.sleep(1)  # Give time to play
                        
                elif sys.platform == "darwin":  # macOS
                    os.system(f'afplay "{temp_file}"')
                    
                else:  # Linux
                    # Try different players
                    players = ['aplay', 'paplay', 'play']
                    played = False
                    
                    for player in players:
                        if os.system(f'which {player} > /dev/null 2>&1') == 0:
                            os.system(f'{player} "{temp_file}" 2>/dev/null')
                            played = True
                            break
                    
                    if not played:
                        print("No audio player found on Linux")
                        print('\a' * 3)  # Fallback beep
                
                # Clean up temporary file
                time.sleep(1)  # Give time for sound to finish
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
            except Exception as e:
                print(f"Error playing sound: {e}")
                print('\a' * 3)  # Fallback terminal beep
        else:
            print('\a' * 3)  # Fallback if sound generation failed
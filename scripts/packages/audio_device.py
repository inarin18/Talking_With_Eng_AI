
import pyaudio

""" デバイス上でのオーディオ系の機器情報を表示する """
def look_for_audio_input():
    
    pa = pyaudio.PyAudio()

    for i in range(pa.get_device_count()):
        print(pa.get_device_info_by_index(i))
        print()

    pa.terminate()
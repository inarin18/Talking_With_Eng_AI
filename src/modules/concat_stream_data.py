
import pyaudio
import speech_recognition as sr

from .audio_parameter import (
    FORMAT             ,
    SAMPLE_RATE        ,
    CHANNELS           ,
    INPUT_DEVICE_INDEX ,
    CALL_BACK_FREQUENCY,
)


def generate_part_of_sentence(in_data):
    
    sprec = sr.Recognizer()
    
    try :
        audiodata  = sr.AudioData(in_data, SAMPLE_RATE, 2)
        sprec_text = sprec.recognize_google(audiodata, language='jp-JP')
        return sprec_text
        
    except sr.UnknownValueError as e:
        return ""
    
    except sr.RequestError as e:
        return ""


def concat_part_of_sentence(stream_data):
    
    user_sentence = ""
    for in_data in stream_data:
        user_sentence += generate_part_of_sentence(in_data)
        
    return user_sentence
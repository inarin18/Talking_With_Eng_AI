import pyaudio

# PyAudio に用いるパラメータ
FORMAT              = pyaudio.paInt16
SAMPLE_RATE         = 44100    # サンプリングレート
CHANNELS            = 1        # モノラルかバイラルか
INPUT_DEVICE_INDEX  = 0        # マイクのチャンネル
CALL_BACK_FREQUENCY = 3        # コールバック呼び出しの周期[sec]
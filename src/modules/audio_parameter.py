import os
import pyaudio

# PyAudio に用いるパラメータ

# os が macOS の際はバッファリングサイズが小さいと
# OSError: [Errno -9981] Input overflowed が発生するため
# バッファリングサイズを大きくしている
CHUNK               = 1024 if os.name == "nt" else 1024 * 4 

FORMAT              = pyaudio.paInt16
SAMPLE_RATE         = 44100    # サンプリングレート
CHANNELS            = 1        # モノラルかバイラルか
INPUT_DEVICE_INDEX  = 0        # マイクのチャンネル
CALL_BACK_FREQUENCY = 3        # コールバック呼び出しの周期[sec]
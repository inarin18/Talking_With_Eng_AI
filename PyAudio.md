# How To PyAudio

## non-blocking operation

> Reference : Details https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.Stream

You should use "callback function".

``` python 

def callback(in_data,       # input data if input=True; else None
             frame_count,   # number of frames
             time_info,     # dictionary
             status_flags   # PaCallbackFlags
            ): 
    """
    time_info is a dictionary with the following keys: 
    input_buffer_adc_time, current_time, and output_buffer_dac_time; 
    see the PortAudio documentation for their meanings. 
    status_flags is one of PortAutio Callback Flag.
    The callback must return a tuple: (out_data, flag)
    """
    return (in_data, pyaudio.paContinue)

# instantiate PyAudio
p = pyaudio.PyAudio()

stream = p.open(
    ...
    stream_callback = callback
)
```
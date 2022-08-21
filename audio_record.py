# import fs as fs
import pyaudio
import wave


def record_audio(filename, record_seconds):
    p = pyaudio.PyAudio()  # Создать интерфейс для PortAudio

    # for i in range(p.get_device_count()):
    #    print(i, p.get_device_info_by_index(i)['name'])

    CHANNELS = 1  # стерео
    RATE = 44100  # частота дискретизации
    CHUNK = 1024  # количество выборок
    FORMAT = pyaudio.paInt16  # 16 бит на выборку (битовая глубина)
    RECORD_SECONDS = record_seconds
    WAV_FILE_NAME = filename

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK)

    print("запись")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("конец записи")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAV_FILE_NAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return None


record_audio(input() + ".wav", 5)
# ху


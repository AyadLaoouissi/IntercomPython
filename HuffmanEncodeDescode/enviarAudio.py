from socket import socket
import pyaudio
import wave
import pywt as wt
from ctypes import c_int32
from pyaudio import paInt16
from pyaudio import PyAudio
import sys
import time
import audio_encoder

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "grabacion.wav"
VALORES = 32
ITERACIONESDWT = 9

#Graba audio 5 segundos y guarda audio.
def grabarAudio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
    print("* Grabando audio 5 segundos")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* Finalizado audio")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

#Envia archivo encoded con socket
def enviarDatos():
    s = socket()
    s.connect(("localhost", 6030))
    
    while True:
        f = open("grabacion.acod", "rb")
        content = f.read(1024)
        
        while content:
            # Enviar contenido.
            s.send(content)
            content = f.read(1024)
        
        break
    
    # Se utiliza el caracter de código 1 para indicar
    # al cliente que ya se ha enviado todo el contenido.
    try:
        s.send(chr(1))
    except TypeError:
        # Compatibilidad con Python 3.
        s.send(bytes(chr(1), "utf-8"))
    
    # Cerrar conexión y archivo.
    s.close()
    f.close()
    print("El archivo ha sido enviado correctamente.")

#utilizamos tres metodos: primero grabamos audio, despues utilizamos el encode de haffman con el archivo y enviamos el archivo con encode haffman
if __name__ == "__main__":
    grabarAudio()
    time.sleep(1)
    audio_encoder.encodeAudio(WAVE_OUTPUT_FILENAME)
    time.sleep(1)
    enviarDatos()
    input()
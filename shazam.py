import asyncio
from shazamio import Shazam
import subprocess
import os

# Функция для поиска всех аудиофайлов в текущей директории
def find_audio_files():
    audio_files = []
    allowed_extensions = ['.mp3', '.mp4', '.wav', '.ogg']
    for file in os.listdir('.'):
        if any(file.endswith(ext) for ext in allowed_extensions):
            audio_files.append(file)
    return audio_files

# Функция для конвертации аудиофайла в WAV
def convert_audio_to_wav(audio_file):
    subprocess.Popen(['ffmpeg', '-y', '-i', audio_file, '2.wav'])

# Функция для распознавания трека через Shazam
async def recognize_track():
    # Пауза в 2 секунды
    await asyncio.sleep(0.8)

    shazam = Shazam()
    out = await shazam.recognize('2.wav')  # rust version, use this!

    if 'track' in out and 'share' in out['track']:
        subject = out['track']['share']['subject']
        print(f"{subject}")
    else:
        print("")

    os.remove("2.wav")

# Получаем список аудиофайлов
audio_files = find_audio_files()

# Проверяем, найдены ли файлы
if audio_files:
    for audio_file in audio_files:
        # Конвертируем аудиофайл в WAV
        convert_audio_to_wav(audio_file)

        # Распознаем трек
        loop = asyncio.get_event_loop()
        loop.run_until_complete(recognize_track())

else:
    print("Аудиофайлы не найдены.")

# Ждем ввода от пользователя перед завершением программы
input("")

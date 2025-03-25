import os
import shutil
import logging

def save_subtitles_to_drive(imdb_code, hash_value, subtitle_path):
    """Salva as legendas no Google Drive montado."""
    drive_path = '/content/drive/MyDrive/GitHub/MakingOff/dist/cc'
    destination_path = os.path.join(drive_path, os.path.basename(subtitle_path))

    try:
        shutil.copy2(subtitle_path, destination_path)
        print(f"Legenda {os.path.basename(subtitle_path)} salva no Google Drive.")
    except (shutil.Error, OSError) as e:
        logging.error(f"Erro ao salvar legenda {os.path.basename(subtitle_path)}: {e}")

def upload_subtitles(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.srt', '.vtt')):
                subtitle_path = os.path.join(root, file)
                try:
                    movie_info = root.split('/')[-2]
                    if '-' not in movie_info:
                        logging.error(f"Formato inválido para movie_info: {movie_info}")
                        continue
                    imdb_code, hash_value = movie_info.split('-', 1)  # Obtém imdb_code e hash_value do nome da pasta
                    save_subtitles_to_drive(imdb_code, hash_value, subtitle_path)
                except ValueError:
                    logging.error(f"Erro ao processar legenda: {file}. Informação do filme: {movie_info}")
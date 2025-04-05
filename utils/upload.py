import os
import shutil
import logging
import requests

# Função para criar a pasta /content/filmes se não existir
def create_filmes_directory():
    filmes_path = '/content/filmes'
    if not os.path.exists(filmes_path):
        os.makedirs(filmes_path)
        print(f"Pasta {filmes_path} criada com sucesso.")
    else:
        print(f"Pasta {filmes_path} já existe.")

def save_subtitles_to_drive(imdb_code, hash_value, subtitle_path):
    """Salva as legendas no Google Drive montado."""
    drive_path = '/content/drive/MyDrive/GitHub/MakingOff.eu.org/dist/cc'
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

# Função para enviar arquivo para a API Hydrax
def send_to_hydrax(file_path):
    """
    Envia um arquivo para a API Hydrax.
    Retorna a resposta da API e o slug do arquivo no Hydrax, se o upload for bem-sucedido.
    """
    url = 'http://up.hydrax.net/276350a6150b6257eb928d9d3aba9fbf'
    file_name = os.path.basename(file_path)
    file_type = 'video/mp4'

    try:
        with open(file_path, 'rb') as file:
            files = {'file': (file_name, file, file_type)}
            response = requests.post(url, files=files)
            print(f'Resposta da API para {file_name}: {response.text}')
            if response.status_code == 200:
                hydrax_slug = response.json().get('slug', '')
                return response, hydrax_slug
            return response, None
    except requests.RequestException as e:
        print(f'Erro ao enviar o arquivo para a API: {e}')
        return None, None

def upload_files(directory):
    create_filmes_directory()  # Certifique-se de que a pasta /content/filmes existe

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.srt', '.vtt')):
                subtitle_path = os.path.join(root, file)
                try:
                    movie_info = root.split('/')[-2]
                    if '-' not in movie_info:
                        logging.error(f"Formato inválido para movie_info: {movie_info}")
                        continue
                    imdb_code, hash_value = movie_info.split('-', 1)
                    save_subtitles_to_drive(imdb_code, hash_value, subtitle_path)
                except ValueError:
                    logging.error(f"Erro ao processar legenda: {file}. Informação do filme: {movie_info}")
            elif file.endswith(('.mp4', '.mkv', '.avi', '.webm')):
                video_path = os.path.join(root, file)
                try:
                    # Upload para a API Hydrax
                    response, hydrax_slug = send_to_hydrax(video_path)
                    if hydrax_slug:
                        print(f'Arquivo {os.path.basename(video_path)} enviado com sucesso para Hydrax. Slug: {hydrax_slug}')
                    else:
                        logging.error(f"Erro ao enviar arquivo {os.path.basename(video_path)} para Hydrax. Resposta: {response.text}")
                    
                    # Copiar o arquivo de vídeo para o Google Drive
                    drive_path = '/content/drive/MyDrive/Projetos/Filmes'
                    destination_path = os.path.join(drive_path, os.path.basename(video_path))
                    shutil.copy2(video_path, destination_path)
                    print(f"Arquivo de vídeo {os.path.basename(video_path)} copiado para o Google Drive.")
                    
                except ValueError:
                    logging.error(f"Erro ao processar arquivo de vídeo: {file}.")
                except (shutil.Error, OSError) as e:
                    logging.error(f"Erro ao copiar arquivo de vídeo {os.path.basename(video_path)} para o Google Drive: {e}")
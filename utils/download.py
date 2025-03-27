import os
import subprocess
import logging
from utils.upload import upload_subtitles
from utils.utils import create_magnet_link

def download_and_process_torrent(torrent_info):
    imdb_code = torrent_info["imdb_code"].replace("tt", "", 1)  # Remover a primeira ocorrência de "tt"
    movie_id = torrent_info["id"]
    title_long = torrent_info["title_long"]
    quality = torrent_info["quality"]
    hash_value = torrent_info["hash"]
    download_base_dir = torrent_info["download_base_dir"]

    # Criar diretório específico para o filme
    movie_dir = f'{download_base_dir}/{movie_id}-{title_long}-{imdb_code}-{quality}'
    if not os.path.exists(movie_dir):
        os.makedirs(movie_dir)
        logging.info(f"Criado diretório: {movie_dir}")

    magnet_link = create_magnet_link(hash_value)
    logging.info(f"Iniciando o download do torrent com hash: {hash_value}")
    download_torrent(magnet_link, movie_dir, torrent_info)

def download_torrent(magnet_link, output_dir, movie_info):
    command = ['webtorrent', magnet_link, '--out', output_dir]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Exibir saídas em tempo real
        for line in process.stdout:
            print(line, end='')

        process.wait()
        if process.returncode != 0:
            logging.error(f"Erro ao baixar o torrent: {process.stderr.read()}")
        else:
            print(f"Download completo em {output_dir}!")
            rename_files(output_dir, movie_info)
            upload_subtitles(output_dir)  # Chama a função para upload das legendas
    except subprocess.TimeoutExpired:
        logging.error(f"Tempo esgotado ao baixar o torrent: {magnet_link}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar webtorrent: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado durante o download do torrent: {e}")

def rename_files(directory, movie_info):
    movie_id = movie_info['id']
    title_long = movie_info['title_long']
    imdb_code = movie_info['imdb_code'].replace("tt", "", 1)  # Remover a primeira ocorrência de "tt"
    quality = movie_info['quality']
    folder_name = f"{movie_id}-{title_long}-{imdb_code}-{quality}"

    for file in os.listdir(directory):
        if file.endswith(('.mp4', '.mkv', '.avi', '.webm')):
            old_file_path = os.path.join(directory, file)
            ext = os.path.splitext(file)[1]
            new_file_name = f"{folder_name}{ext}"
            new_file_path = os.path.join(directory, new_file_name)
            logging.info(f"Tentando renomear arquivo: {old_file_path} para {new_file_path}")
            try:
                os.rename(old_file_path, new_file_path)
                print(f"Arquivo renomeado para: {new_file_name}")
            except KeyError as e:
                logging.error(f"Erro ao renomear arquivo: {file}. Informações faltando: {e}")
            except OSError as e:
                logging.error(f"Erro ao renomear arquivo: {file}. Erro do sistema: {e}")
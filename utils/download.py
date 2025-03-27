import os
import subprocess
import logging
from utils.upload import upload_subtitles
from utils.utils import create_magnet_link
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Caminho para o arquivo de credenciais JSON
credential_path = '/content/drive/MyDrive/GitHub/DownTorr-CLI/client_secret_246697740043-brlhv8eaneapnht8frcinuo45qf5k6j8.apps.googleusercontent.com.json'

# Autenticar e criar o serviço da API do Google Drive
credentials = service_account.Credentials.from_service_account_file(credential_path)
service = build('drive', 'v3', credentials=credentials)

# Função para obter o ID do arquivo após o download
def obter_id_arquivo_apos_download(folder_id='1sASley-Ks5DOKkx61tcCsaTX5ErT-YYr'):
    """Obtém o ID do arquivo do Google Drive após o download do vídeo,
    pesquisando na pasta especificada e suas subpastas.

    Args:
        folder_id: O ID da pasta raiz onde iniciar a pesquisa.

    Returns:
        O ID do arquivo do Google Drive ou None se o arquivo não for encontrado.
    """
    # Criar um serviço Drive API.
    service = build('drive', 'v3', credentials=credentials)

    # Obter o nome do arquivo baixado automaticamente.
    lista_de_arquivos = os.listdir('.')
    lista_de_arquivos.sort(key=os.path.getmtime, reverse=True)
    nome_do_arquivo_de_video = lista_de_arquivos[0]

    # Função recursiva para pesquisar em todas as subpastas.
    def pesquisar_recursivamente(pasta_id):
        """Pesquisa o arquivo na pasta atual e chama a si mesma para subpastas."""
        results = service.files().list(
            q=f"name = '{nome_do_arquivo_de_video}' and '{pasta_id}' in parents",
            spaces='drive',
            fields='nextPageToken, files(id, name)'
        ).execute()
        items = results.get('files', [])
        if items:
            return items[0]['id']  # Encontrou o arquivo, retorna o ID

        # Se não encontrado na pasta atual, pesquisa nas subpastas
        results = service.files().list(
            q=f"'{pasta_id}' in parents and mimeType = 'application/vnd.google-apps.folder'",
            spaces='drive',
            fields='nextPageToken, files(id, name)'
        ).execute()
        subpastas = results.get('files', [])
        for subpasta in subpastas:
            arquivo_id = pesquisar_recursivamente(subpasta['id'])
            if arquivo_id:
                return arquivo_id  # Encontrou em uma subpasta, retorna o ID

        return None  # Não encontrado em nenhuma pasta

    # Iniciar a pesquisa a partir da pasta raiz.
    id_do_arquivo = pesquisar_recursivamente(folder_id)

    return id_do_arquivo

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

    # Obter o ID do arquivo do Google Drive após o download
    id_do_arquivo = obter_id_arquivo_apos_download()
    if id_do_arquivo:
        logging.info(f"ID do arquivo no Google Drive: {id_do_arquivo}")
    else:
        logging.error("Não foi possível obter o ID do arquivo no Google Drive.")

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
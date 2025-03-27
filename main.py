from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logging_config import configure_logging
from utils.download import download_and_process_torrent
from utils.utils import read_json_file
import requests
import os
import time
import json

# Configurar o logging
configure_logging()

# Criar diretório de downloads no Google Drive
download_base_dir = '/content/drive/MyDrive/Projetos/Filmes'
if not os.path.exists(download_base_dir):
    os.makedirs(download_base_dir)

def get_largest_non_3d_torrent(torrents):
    # Filtrar torrents que não são 3D
    non_3d_torrents = [t for t in torrents if t.get('quality') != '3D']
    # Ordenar torrents pelo tamanho (size_bytes) em ordem decrescente
    sorted_torrents = sorted(non_3d_torrents, key=lambda x: x.get('size_bytes', 0), reverse=True)
    # Retornar o maior torrent não 3D
    return sorted_torrents[0] if non_3d_torrents else None

def process_torrent(torrent_info):
    download_and_process_torrent(torrent_info)

def get_movie_details_by_imdb(imdb_code):
    response = requests.get(f"https://yts.mx/api/v2/movie_details.json?imdb_id={imdb_code}")
    return response.json().get('data', {}).get('movie', {})

def get_movie_details_by_movie_id(movie_id):
    response = requests.get(f"https://yts.mx/api/v2/movie_details.json?movie_id={movie_id}")
    return response.json().get('data', {}).get('movie', {})

def manual_processing():
    choice = input("Deseja processar manualmente algum filme específico? (Sim/Não): ").strip().lower()
    if choice != "sim":
        return False, None

    identifier = input("Qual filme deseja processar? (Digite o imdb_code, movie_id ou hash): ").strip()
    if identifier.startswith("tt"):
        movie = get_movie_details_by_imdb(identifier)
    elif identifier.isdigit():
        movie = get_movie_details_by_movie_id(identifier)
    else:
        hash_value = identifier
        imdb_code = input("Digite o imdb_code do filme: ").strip()
        movie = get_movie_details_by_imdb(imdb_code)
        if movie:
            torrents = movie.get('torrents', [])
            hash_torrent = next((t for t in torrents if t.get('hash') == hash_value), None)
            if hash_torrent:
                process_torrent({
                    "id": movie['id'],
                    "title_long": movie['title_long'],
                    "imdb_code": movie['imdb_code'],
                    "year": movie['year'],
                    "hash": hash_value,
                    "quality": hash_torrent.get('quality'),
                    "size_bytes": hash_torrent.get('size_bytes'),
                    "download_base_dir": download_base_dir
                })
                return True, None
            else:
                print("Hash não encontrado.")
                return False, None

    if movie:
        torrents = movie.get('torrents', [])
        print(f"Torrents encontrados para {movie['title_long']}:")
        for t in torrents:
            print(f"Hash: {t['hash']}, Quality: {t['quality']}, Size: {t['size_bytes']}")

        all_hashes = input("Deseja baixar todos os hashes? (Sim/Não): ").strip().lower()
        if all_hashes == "sim":
            for t in torrents:
                process_torrent({
                    "id": movie['id'],
                    "title_long": movie['title_long'],
                    "imdb_code": movie['imdb_code'],
                    "year": movie['year'],
                    "hash": t['hash'],
                    "quality": t['quality'],
                    "size_bytes": t['size_bytes'],
                    "download_base_dir": download_base_dir
                })
        else:
            specific_hash = input("Digite o hash que deseja processar: ").strip()
            hash_torrent = next((t for t in torrents if t.get('hash') == specific_hash), None)
            if hash_torrent:
                process_torrent({
                    "id": movie['id'],
                    "title_long": movie['title_long'],
                    "imdb_code": movie['imdb_code'],
                    "year": movie['year'],
                    "hash": specific_hash,
                    "quality": hash_torrent.get('quality'),
                    "size_bytes": hash_torrent.get('size_bytes'),
                    "download_base_dir": download_base_dir
                })
            else:
                print("Hash não encontrado.")
    else:
        print("Filme não encontrado.")
    
    return True, None

def main():
    manual, _ = manual_processing()
    if manual:
        return

    file_path = '/content/drive/MyDrive/GitHub/MakingOff/dist/filmes.json'
    
    while True:
        # Ler o arquivo JSON do Google Drive
        movies_data = read_json_file(file_path)
        
        # Filtrar filmes que já foram processados
        movies_to_process = [movie for movie in movies_data if not movie.get('processed', False)]
        
        if not movies_to_process:
            print("Todos os filmes foram processados.")
            break
        
        # Processar os torrents com um pool de threads
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for movie in movies_to_process:  # Processar um filme por vez
                imdb_code = movie.get('imdb_code')
                movie_id = movie.get('id')
                title_long = movie.get('title_long')
                largest_torrent = get_largest_non_3d_torrent(movie.get('torrents', []))
                if largest_torrent:
                    hash_value = largest_torrent.get('hash')
                    quality = largest_torrent.get('quality')
                    size_bytes = largest_torrent.get('size_bytes')
                    if hash_value:
                        torrent_info = {
                            "id": movie_id,
                            "title_long": title_long,
                            "imdb_code": imdb_code,
                            "year": movie['year'],
                            "hash": hash_value,
                            "quality": quality,
                            "size_bytes": size_bytes,
                            "download_base_dir": download_base_dir
                        }
                        futures.append(executor.submit(process_torrent, torrent_info))
                        movie['processed'] = True  # Marcar o filme como processado
                        break  # Processar apenas um torrent por filme
                        
            for future in as_completed(futures):
                future.result()  # Para capturar exceções, se houver
        
        # Salvar o estado atualizado de filmes no arquivo JSON
        with open(file_path, 'w') as f:
            json.dump(movies_data, f, indent=4)
    
        # Aguardar um pouco antes de processar o próximo lote
        time.sleep(5)

if __name__ == "__main__":
    main()

print("Todos os downloads foram concluídos.")
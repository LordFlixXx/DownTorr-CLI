# Projeto de Download e Processamento de Torrents

Este projeto automatiza o download de torrents, renomeia os arquivos, faz o upload dos vídeos para o Hydrax e salva as legendas no Google Drive. Ele é executado no Google Colab e utiliza várias bibliotecas para facilitar esse processo.

## Estrutura do Projeto

```
DownTorr-CLI/
├── main.py
├── requirements.txt
├── README.md
├── utils/
│   ├── __init__.py
│   ├── download.py
│   ├── upload.py
│   ├── ngrok_utils.py
│   └── logging_config.py
```

## Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`.

### Dependências Python

- pyngrok
- gspread
- requests
- google-colab

### Dependências npm

- webtorrent-cli

## Instruções de Instalação

### Instalando Dependências Python

Execute o seguinte comando para instalar as dependências Python:

```bash
pip install -r requirements.txt
```

### Instalando Dependências npm

Execute o seguinte comando para instalar o `webtorrent-cli`:

```bash
npm install -g webtorrent-cli
```

## Configuração do Ambiente

### Montagem do Google Drive

O Google Drive será montado automaticamente pelo Google Colab. Certifique-se de ter permissão para acessar o diretório especificado no código.

### Configuração do ngrok

Armazene o token de autenticação do ngrok em uma variável de ambiente:

```bash
export NGROK_AUTH_TOKEN="seu_token_ngrok"
```

## Execução do Projeto

### Passos para Executar

1. **Clone o repositório** e navegue até o diretório do projeto.
2. **Instale as dependências** conforme descrito acima.
3. **Carregue o notebook no Google Colab**.
4. **Execute o notebook** para iniciar o processo de download e processamento de torrents.

### Estrutura do Código

#### `main.py`

O arquivo principal que executa o processo de download e processamento de torrents.

- Monta o Google Drive.
- Inicia o ngrok.
- Processa os torrents com um pool de threads.

#### `utils/download.py`

Contém funções para download e processamento de torrents.

- `download_and_process_torrent`
- `download_torrent`
- `rename_files`

#### `utils/upload.py`

Contém funções para upload de vídeos e legendas.

- `upload_to_hydrax`
- `upload_videos_to_hydrax`
- `save_subtitles_to_drive`
- `upload_subtitles`

#### `utils/ngrok_utils.py`

Contém a função para iniciar o ngrok.

- `start_ngrok`

#### `utils/logging_config.py`

Configura o logging para registrar mensagens de erro.

- `configure_logging`

## Observações

- Certifique-se de que o arquivo JSON contendo os dados dos filmes está no local especificado.
- Verifique se o token do ngrok está corretamente configurado.
- Monitore o log (`app.log`) para mensagens de erro e informações sobre o processo.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorar este projeto.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
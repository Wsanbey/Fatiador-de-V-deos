programa "Fatiador de Vídeos":

# Imagem do sistema:

<div style="display: flex; justify-content: space-between;">
  <img src="https://github.com/user-attachments/assets/b2166a02-5d27-47cf-8d1b-228206b7b987" alt="image" width="45%" />
  <img src="https://github.com/user-attachments/assets/86793f40-c85d-40da-8f42-ec0dc0e414ee" alt="image" width="45%" />
</div>

<br />

<img src="https://github.com/user-attachments/assets/047bd77b-3d50-44d3-8822-6064b168eef9" alt="image" width="100%" />



---

# Fatiador de Vídeos

O **Fatiador de Vídeos** é uma ferramenta desenvolvida para dividir arquivos de vídeo em partes menores de acordo com a duração especificada pelo usuário. A interface gráfica foi construída utilizando `tkinter` e `customtkinter`, oferecendo uma maneira fácil e interativa de cortar vídeos. A aplicação também permite o ajuste do formato e da qualidade dos segmentos gerados.

## Funcionalidades

- **Seleção do vídeo**: Escolha o vídeo a ser fatiado diretamente do sistema de arquivos.
- **Definição de saída**: Especifique o diretório onde os vídeos fatiados serão salvos.
- **Ajuste de duração**: Defina a duração de cada segmento, podendo ser em segundos ou minutos.
- **Escolha de formato**: Selecione o formato de saída entre `mp4`, `avi`, `mov`, `mkv` e `webm`.
- **Qualidade configurável**: Opções de qualidade (`low`, `medium`, `high`) que ajustam o bitrate do vídeo.
- **Barra de progresso**: Visualize o andamento do processo de fatiamento em tempo real.
- **Redimensionamento com barras**: Redimensiona o vídeo mantendo a proporção original e adicionando barras para preencher o fundo.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python:
  - `tkinter`
  - `customtkinter`
  - `moviepy`
  - `concurrent.futures`

## Instalação

1. Clone este repositório:
    ```bash
    git clone https://github.com/seuusuario/fatiador-de-videos.git
    ```
2. Instale as dependências necessárias:
    ```bash
    pip install moviepy customtkinter
    ```

## Como Usar

1. **Executando a aplicação**:
   - Navegue até o diretório do projeto.
   - Execute o arquivo `front.py`:
     ```bash
     python front.py
     ```

2. **Interface**:
   - **Caminho do vídeo**: Use o botão "Buscar" para selecionar o arquivo de vídeo que deseja cortar.
   - **Caminho de saída**: Especifique o diretório onde os segmentos de vídeo serão salvos.
   - **Duração**: Insira a duração desejada para cada segmento, escolhendo entre segundos ou minutos.
   - **Formato e Qualidade**: Escolha o formato de saída e a qualidade do vídeo.
   - **Iniciar Corte**: Clique em "Iniciar Corte" para começar o processamento do vídeo.

3. **Processo de corte**:
   - O progresso será exibido na barra de progresso, e as informações de status serão atualizadas conforme o corte avança.
   - Após a conclusão, uma mensagem indicará que o processamento foi concluído.

## Estrutura do Projeto

```plaintext
Fatiador de Vídeos/
│
├── .venv                 # Fica a seu criterio criar um ambiente virtual
├── front.py              # Arquivo principal que inicia a interface gráfica
├── backend.py            # Funções backend responsáveis pelo processamento do vídeo
├── README.md             # Documentação do projeto
└── requirements.txt      # Lista de dependências para facilitar a instalação
```

## Contribuição

   - **Contribuições** são bem-vindas! Se você encontrar algum problema ou tiver sugestões para melhorar o projeto, sinta-se à vontade para abrir uma issue ou enviar um pull request.
---

## Contato

**Desenvolvido por @wellfulstack**  
Telegram: [https://t.me/wellfulstack](https://t.me/wellfulstack)

 

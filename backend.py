from moviepy.editor import VideoFileClip, ColorClip
from concurrent.futures import ThreadPoolExecutor
import os

def resize_with_bars(clip, target_width, target_height):
    """
    Redimensiona o vídeo mantendo a proporção original e adiciona barras para preencher o fundo.

    Args:
        clip (VideoFileClip): O vídeo a ser redimensionado.
        target_width (int): Largura alvo.
        target_height (int): Altura alvo.

    Returns:
        VideoFileClip: O vídeo redimensionado com barras.
    """
    original_width, original_height = clip.size
    scale = min(target_width / original_width, target_height / original_height)

    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    resized_clip = clip.resize(newsize=(new_width, new_height))

    # Criar um fundo com a resolução alvo (cor preta)
    background = ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=clip.duration)

    # Colocar o vídeo redimensionado sobre o fundo
    final_clip = background.set_duration(clip.duration).set_opacity(1).set_position(('center', 'center')).fx(lambda c: c.set_position('center')).set_audio(clip.audio)

    return final_clip

def get_bitrate(quality_choice):
    """
    Determina o bitrate com base na escolha de qualidade.

    Args:
        quality_choice (str): Qualidade do vídeo ("Baixa", "Média", "Alta").

    Returns:
        str: Bitrate correspondente.
    """
    bitrates = {
        "Baixa": "500k",
        "Média": "1000k",
        "Alta": "3000k"
    }
    return bitrates.get(quality_choice, "1000k")

def process_segment(segment_info):
    """
    Processa um segmento de vídeo: redimensiona e salva o arquivo.

    Args:
        segment_info (tuple): Informações do segmento (input_file, output_file, start_time, end_time, format_choice, quality_choice).
    """
    input_file, output_file, start_time, end_time, format_choice, quality_choice = segment_info
    video = VideoFileClip(input_file).subclip(start_time, end_time)
    final_clip = resize_with_bars(video, 1080, 1920)
    bitrate = get_bitrate(quality_choice)
    final_clip.write_videofile(output_file, codec="libx264", bitrate=bitrate, logger=None)

def process_video(input_file, output_dir, duration, format_choice, quality_choice, progress_callback):
    """
    Processa o vídeo dividindo-o em segmentos e redimensionando cada segmento mantendo a proporção original.

    Args:
        input_file (str): Caminho para o arquivo de vídeo de entrada.
        output_dir (str): Diretório onde os segmentos serão salvos.
        duration (float): Duração de cada segmento em segundos.
        format_choice (str): Formato de saída do vídeo (por exemplo, "mp4").
        quality_choice (str): Qualidade do vídeo ("Baixa", "Média", "Alta").
        progress_callback (function): Função de callback para monitorar o progresso.
    """
    try:
        video = VideoFileClip(input_file)
        video_duration = video.duration
        total_segments = int(video_duration // duration) + 1
        
        # Informar o número total de segmentos
        print(f"Total de vídeos a serem gerados: {total_segments}")

        segment_infos = [
            (
                input_file,
                os.path.join(output_dir, f"segmento_{i + 1}.{format_choice}"),
                i * duration,
                min((i + 1) * duration, video_duration),
                format_choice,
                quality_choice
            )
            for i in range(total_segments)
        ]

        def update_progress(future):
            """
            Atualiza o progresso com base no futuro do ThreadPoolExecutor.

            Args:
                future (Future): Objeto futuro do ThreadPoolExecutor.
            """
            completed = sum(f.done() for f in futures)
            progress = (completed / total_segments) * 100
            progress_callback(progress)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_segment, info) for info in segment_infos]
            for future in futures:
                future.add_done_callback(update_progress)

        progress_callback(100)

    except Exception as e:
        progress_callback(0)
        print(f"Erro ao processar o vídeo: {e}")

def get_video_info(filepath):
    """
    Obtém informações sobre o vídeo.

    Args:
        filepath (str): Caminho para o arquivo de vídeo.

    Returns:
        dict: Dicionário com informações sobre a duração, resolução e fps do vídeo.
    """
    try:
        video = VideoFileClip(filepath)
        info = {
            "duration": round(video.duration),
            "resolution": f"{video.w}x{video.h}",
            "fps": video.fps
        }
        return info

    except Exception as e:
        print(f"Erro ao obter informações do vídeo: {e}")
        return None

from emoji import emojize


def previsaoTempo(cidade=None, lat=None, lng=None):
    """
    Copyright (c) 2013 - Fernando B. Giannasi
    This work is free. You can redistribute it and/or modify it under the
    terms of the Do What The Fuck You Want To Public License, Version 2,
    as published by Sam Hocevar.
    Esta função obtem dados em XML do CPTEC/INPE (Centro de Previsão
    de Tempo e Estudos Climáticos do Instituto Nacional de Pesquisas Espaciais)
    para as cidades brasileiras.

    :param cidade: Nome da cidade que se deseja a previsão do tempo
    :param lat: Latitude do local
    :param lng: Logitude do local
    :return: Previsão do tempo para a cidade passada por parâmetro
    """
    import xml.etree.ElementTree
    from datetime import datetime
    from urllib.request import urlopen
    TEMPO = {'ec': 'Encoberto com Chuvas Isoladas :partly_sunny:',
             'ci': 'Chuvas Isoladas :umbrella:',
             'c': 'Chuva :umbrella:',
             'in': 'Instável :cloud:',
             'pp': 'Possibilidade de Pancadas de Chuva :umbrella:',
             'cm': 'Chuva pela Manhã :umbrella:',
             'cn': 'Chuva à Noite :umbrella:',
             'pt': 'Pancadas de Chuva à Tarde :partly_sunny:',
             'pm': 'Pancadas de Chuva pela Manhã :partly_sunny:',
             'np': 'Nublado e Pancadas de Chuva :umbrella:',
             'pc': 'Pancadas de Chuva :umbrella: :zap:',
             'pn': 'Parcialmente Nublado :partly_sunny:',
             'cv': 'Chuvisco:umbrella:',
             'ch': 'Chuvoso :umbrella: :zap:',
             't': 'Tempestade :umbrella: :zap:',
             'ps': 'Predomínio de Sol :sunny:',
             'e': 'Encoberto :partly_sunny:',
             'n': 'Nublado :partly_sunny:',
             'cl': 'Céu Claro :sunny:',
             'nv': 'Nevoeiro :snowflake:',
             'g': 'Geada :snowflake:',
             'ne': 'Neve :snowflake:',
             'nd': 'Não Definido',
             'pnt': 'Pancadas de Chuva à Noite :umbrella:',
             'psc': 'Possibilidade de Chuva :cloud:',
             'pcm': 'Possibilidade de Chuva pela Manhã :cloud:',
             'pct': 'Possibilidade de Chuva à Tarde :cloud:',
             'pcn': 'Possibilidade de Chuva à Noite :cloud:',
             'npt': 'Nublado com Pancadas à Tarde :partly_sunny:',
             'npn': 'Nublado com Pancadas à Noite :partly_sunny:',
             'ncn': 'Nublado com Possibilidade de Chuva à Noite :partly_sunny:',
             'nct': 'Nublado com Possibilidade de Chuva à Tarde :partly_sunny:',
             'ncm': 'Nublado com Possibilidade de Chuva pela Manhã :partly_sunny:',
             'npm': 'Nublado com Pancadas de Chuva pela Manhã :partly_sunny:',
             'npp': 'Nublado com Possibilidade de Chuva :partly_sunny:',
             'vn': 'Variação de Nebulosidade :cloud:',
             'ct': 'Chuva à Tarde :cloud:',
             'ppn': 'Possibilidade de Pancadas de Chuva à Noite :cloud:',
             'ppt': 'Possibilidade de Pancadas de Chuva à Tarde :cloud:',
             'ppm': 'Possibilidade de Pancadas de Chuva pela Manhã :cloud:'}

    busca = f'http://servicos.cptec.inpe.br/XML/cidade/7dias/{lat}/{lng}/previsaoLatLon.xml'

    if cidade:
        from unicodedata import normalize
        # Formata entrada, remove acentos e substitui os espaços por %20 para passar na url da requisição
        cidade = normalize('NFKD', cidade.lstrip()).encode('ascii', 'ignore').decode('ascii').lower().replace(' ', '%20')
        codigos = []

        with urlopen(f'http://servicos.cptec.inpe.br/XML/listaCidades?city={cidade}') as url:
            content = url.read().decode('iso-8859-1')
        root = xml.etree.ElementTree.fromstring(content)
        codigos.extend([elem.text for elem in root.findall('./cidade/id')])

        if len(codigos) == 0:
            return 'A busca não retornou nenhuma cidade! :confused:'

        cod = codigos[0]  # Pega a primeira cidade retornada
        busca = f'http://servicos.cptec.inpe.br/XML/cidade/{cod}/previsao.xml'

    # Obtém o XML das previsões
    with urlopen(busca) as url:
        content = url.read().decode('iso-8859-1')

    # Filtra os dados
    root = xml.etree.ElementTree.fromstring(content)
    dias = [elem.text for elem in root.findall('previsao/dia')]
    dias = [datetime.strptime(elem, '%Y-%m-%d').strftime('%d/%m/%Y') for elem in dias]
    clima = [elem.text for elem in root.findall('previsao/tempo')]
    temperaturas = [(ma, mi) for ma, mi in zip([elem.text for elem in root.findall('previsao/maxima')],
                                               [elem.text for elem in root.findall('previsao/minima')])]
    iuv = [elem.text for elem in root.findall('previsao/iuv')]

    # Retorna resultado
    text = f'\n:high_brightness: Previsão do tempo para *{root[0].text} - {root[1].text}*:'
    text += ('\n:repeat: (Atualizado em *{0}*)'.format(datetime.strptime(root[2].text, '%Y-%m-%d').strftime('%d/%m/%Y')))
    for i in range(len(dias)):
        text += f'\n\n:sunrise_over_mountains: Dia *{dias[i]}*:'
        text += f'\n:small_blue_diamond: Clima: *{TEMPO[clima[i]]}*'
        text += f'\n:small_red_triangle: Temperatura máxima: *{temperaturas[i][0]} °C*'
        text += f'\n:small_red_triangle_down: Temperatura mínima: *{temperaturas[i][1]} °C*'
        text += f'\n:small_orange_diamond: Índice UV: *{iuv[i]}*'
    return emojize(text, use_aliases=True)


def jokenpo(j):
    """
    Sorteia jogada do computador e compara com a jogada do jogador para definir quem venceu
    :param j: Jogada do jogador
    :return: None
    """
    from random import randint
    elem = ['Pedra :bomb:', 'Papel :page_with_curl:', 'Tesoura :scissors:']
    r = randint(1, 3)
    text = f'Eu joguei: {elem[r - 1]}\n'
    text += f'Você jogou: {elem[j - 1]}\n\n'

    if (r == 1 and j == 2) or (r == 2 and j == 3) or (r == 3 and j == 1):
        text += '*Você ganhou!* :tada:'
    elif (r == 1 and j == 3) or (r == 2 and j == 1) or (r == 3 and j == 2):
        text += '*Eu ganhei!* :stuck_out_tongue_winking_eye:'
    else:
        text += '*Empate!* :expressionless:'

    return emojize(text, use_aliases=True)


def __semana(w):
    """
    :param w: Inteiro referente ao dia da semana
    :return: Retorna nome do dia da semana
    """
    week = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    return week[w]


def __mes(m):
    """
    :param w: Inteiro referente ao mes
    :return: Retorna nome do mes
    """
    month = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    return month[m]


def regrasJokenpo():
    """
    :return: Envia as regras do jokenpô
    """
    return emojize('Digite:\n*1* ou :bomb: ou *pedra* para PEDRA\n*2* ou :page_with_curl: ou *papel* para PAPEL\n*3* ou :scissors: ou *tesoura* para TESOURA', use_aliases=True)


def boasVindas():
    """
    :return: Envia mensagem de boas vindas
    """
    # '*bold text*\n_italic text_\n[link](http://www.google.com)'
    return emojize('*Em que posso ajudar?* :grin:\n'
                   'Eis aqui a lista de alguns comandos que posso realizar\n'
                   ':white_check_mark: /hora para consultar a hora atual\n'
                   ':white_check_mark: /dia para consultar o dia\n'
                   ':white_check_mark: /falaTop seguido do que você quer que eu fale\n'
                   ':white_check_mark: /climaCruz seguido do nome da cidade, ou simplesmente envie-me sua localização\n'
                   ':white_check_mark: /random1a100 para sortear um número entre 1 e 100\n'
                   ':white_check_mark: /teste para resposta de teste\n'
                   ':white_check_mark: /jokenpo para jogar Jokenpô comigo\n'
                   ':white_check_mark: /video seguido do título para assistir ao video no Youtube\n'
                   ':white_check_mark: /baixar1 para baixar o mp3 de algum vídeo do Youtube anteriormente requisitado', use_aliases=True)


def fala(chatid, texto, slow=False):
    """
    :param chatid: ID do chat para salvar o arquivo.mp3
    :param texto: Texto que será convertido em voz
    :param slow: Decide a velocidade da fala, False por padrão
    :return: Salva o arquivo com o nome voz_{chatid} para ser enviado ao usuário posteriormente
    """
    from gtts import gTTS
    voz = gTTS(texto, lang='pt', slow=slow)
    voz.save(f'voz_{chatid}.mp3')


def dataHora(data):
    """
    :param data: Se True retorna a data, se False retorna a hora atual
    :return: Data ou Hora
    """
    from datetime import datetime
    d = datetime.now()
    if data:
        return emojize(f'Hoje é *{__semana(d.weekday())}* :sunny: dia *{d.day}* de *{__mes(d.month)}* de *{d.year}*', use_aliases=True)
    else:
        return emojize(f'Agora são :watch: *{d.hour:2}* hora(s) e *{d.minute:2}* minuto(s)', use_aliases=True)


def sorteaNum(n1, n2):
    """
    :param n1: Número Inferior
    :param n2: Número Superior
    :return: Número aleatório entre n1 e n2
    """
    from random import randint
    return emojize(f'O número aleatório gerado foi *{randint(n1, n2)}* :game_die:', use_aliases=True)


def pesquisa(pesquisa, site):
    """
    Pesquisa texto passado no site especificado e retorna 3 resultados referentes
    :param pesquisa: Texto que será pesquisado
    :param site: Site onde será feito a busca
    :return: None
    """
    from googlesearch import search
    return list(search(f'"{pesquisa}" {site}', stop=3))


def baixarMP3(url):
    """
    Baixa vídeo do Youtube com URL passada no parâmetro e o converte em áudio
    :param url: URL do vídeo à ser baixado
    :return: None
    """
    import youtube_dl
    op = {'format': 'bestaudio/best',
          'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
          'quiet': True, 'no-warnings': True}
    with youtube_dl.YoutubeDL(op) as ydl:
        ydl.download([url])


def pegaMP3():
    """
    :return: Retorna primeiro arquivo .mp3 que achar na pasta do script
    """
    from os import walk, getcwd
    for raiz, diretorios, arquivos in walk(getcwd()):
        for arquivo in arquivos:
            if arquivo.endswith('.mp3'):
                return arquivo

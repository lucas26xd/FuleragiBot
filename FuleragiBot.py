from telepot import Bot, glance
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize, demojize, emoji_count
from time import sleep
import Util, config

jogando = False
resultado = ['https://www.youtube.com/watch?v=QIEnH7cQNqs', 'https://www.youtube.com/watch?v=2m-vthh7s8U', 'https://www.youtube.com/watch?v=jgD16_umTqk']
bot = Bot(config.API_KEY_TelegramBot)


def naoEntendi(chatid, comando):
    return bot.sendMessage(chatid, emojize(f'Me desculpe, mas eu não entendi o comando: {comando} :disappointed_relieved:', use_aliases=True))


def jogaJokenpo(chatid, comando):
    bot.sendMessage(chatid, '_JO_', parse_mode='Markdown')
    sleep(0.3)
    bot.sendMessage(chatid, '_    KEN_', parse_mode='Markdown')
    sleep(0.3)
    bot.sendMessage(chatid, '_          PÔ!!!_', parse_mode='Markdown')
    comando = comando.replace('/', '')
    if demojize(comando) in ':bomb:1pedra':
        bot.sendMessage(chatid, Util.jokenpo(1), parse_mode='Markdown')  # pedra
    elif demojize(comando) in ':page_with_curl:2papel':
        bot.sendMessage(chatid, Util.jokenpo(2), parse_mode='Markdown')  # papel
    elif demojize(comando) in ':scissors::scissors:️3tesoura':  # nao sei pq mas o : do pc é diferente do cel
        bot.sendMessage(chatid, Util.jokenpo(3), parse_mode='Markdown')  # tesoura
    else:
        naoEntendi(chatid, comando)
        bot.sendMessage(chatid, Util.regrasJokenpo(), parse_mode='Markdown')
    bot.sendMessage(chatid, emojize('Jogue Novamente! :relieved:', use_aliases=True))


def Texto(chatid, nome, comando):
    global jogando, resultado
    if '/start' in comando:
        bot.sendMessage(chatid, emojize('Olá {}! :blush:', use_aliases=True).format(nome))
        bot.sendMessage(chatid, Util.boasVindas(), parse_mode='Markdown')
        Texto(chatid, None, f'/fala Olá {nome}. Tudo bem? Como posso ajudar?')  # Envia fala de boas vindas
    elif '/hora' in comando:
        bot.sendMessage(chatid, Util.dataHora(False), parse_mode='Markdown')
    elif '/dia' in comando:
        bot.sendMessage(chatid, Util.dataHora(True), parse_mode='Markdown')
    elif '/random' in comando:
        bot.sendMessage(chatid, Util.sorteaNum(int(comando[7:comando.rfind('a')]), int(comando[comando.rfind('a') + 1:])), parse_mode='Markdown')
    elif '/fala' in comando:
        bot.sendChatAction(chatid, 'record_audio')
        Util.fala(chatid, comando[5:])
        bot.sendVoice(chatid, open(f'voz_{chatid}.mp3', 'rb'))
        from os import remove
        remove(f'voz_{chatid}.mp3')
    elif '/clima' in comando:
        bot.sendMessage(chatid, Util.previsaoTempo(cidade=comando[6:]), parse_mode='Markdown')
    elif 'jokenpo' in comando:
        jogando = True
        bot.sendMessage(chatid, '*Bem-Vindo ao jogo do jokenpô:*', parse_mode='Markdown')
        bot.sendMessage(chatid, 'Você pode sair a qualquer momento digitando o comando /sair')
        bot.sendMessage(chatid, Util.regrasJokenpo(), parse_mode='Markdown')
    elif 'sair' in comando:
        if jogando:
            bot.sendMessage(chatid, 'Saindo...')
            jogando = False
            bot.sendMessage(chatid, 'Ok!')
        else:
            bot.sendMessage(chatid, 'Você não está jogando!')
    elif '/video' in comando or '/baixar' in comando:
        bot.sendMessage(chatid, emojize('Aguarde um instante enquanto realizo a busca... :hourglass:', use_aliases=True))
        resultado = Util.pesquisa(comando[6:], 'youtube')
        bot.sendMessage(chatid, 'Segue abaixo alguns vídeos relacionado à pequisa:')
        for i, res in enumerate(resultado):
            markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=emojize(':point_up: Baixar este MP3 :arrow_down:', use_aliases=True), callback_data=i)]])  # Botão com o índice do vídeo a ser baixado
            bot.sendMessage(chatid, emojize(res, use_aliases=True), reply_markup=markup)
    elif 'teste' in comando:
        bot.sendMessage(chatid, emojize('Tudo OK! :+1: :ok_hand: :wink:', use_aliases=True))
    else:
        if jogando:
            jogaJokenpo(chatid, comando)
        else:
            naoEntendi(chatid, comando)
    return comando


def onChatMessage(msg):
    nome = chatid = comando = ''
    try:
        # print(msg)
        nome = msg['from']['first_name']
        chatid = msg['chat']['id']
        keys = msg.keys()
        if 'text' in keys:  # Texto, Emoji, Edição ou Resposta
            comando = msg['text']
            if 'fala' not in comando:
                from unicodedata import normalize, combining
                comando = u"".join([c for c in normalize('NFKD', msg['text']) if not combining(c)])  # Remove acentos
            comando = comando.lower()

            if emoji_count(comando) > 0:  # Se for emoji recebido, responde com o mesmo emoji
                bot.sendMessage(chatid, comando)
                comando = f'Emoji: {demojize(comando)}.'
            else:
                comando = Texto(chatid, nome, comando)
                comando = f'Texto: {comando}.'
        elif 'sticker' in keys:  # Se for sticker recebido, responde com o mesmo sticker
            bot.sendSticker(chatid, msg['sticker']['file_id'])
            comando = f'Sticker. Nome: {msg["sticker"]["set_name"]}, Emoji: {demojize(msg["sticker"]["emoji"])}.'
        elif 'location' in keys:  # Responde ao usuário a previsão do tempo para aquela localização
            bot.sendMessage(chatid, Util.previsaoTempo(lat=msg['location']['latitude'], lng=msg['location']['longitude']), parse_mode='Markdown')
            comando = f'Localização. Lat:{msg["location"]["latitude"]}, Long:{msg["location"]["longitude"]}.'
        else:  # Comando/Tipo de mensagens que ainda não desenvolvi algo específico
            if 'audio' in keys:
                comando = f'Áudio. Nome: {msg["title"]}.'
            elif 'voice' in keys:
                comando = f'Mensagem de voz. Duração: {msg["voice"]["duration"]}s.'
            elif 'photo' in keys:
                comando = f'Foto. com Legenda: {msg["caption"]}.' if 'caption' in keys else 'Foto.'
            elif 'video' in keys:
                comando = f'Vídeo com Legenda: {msg["caption"]}.' if 'caption' in keys else 'Vídeo.'
            elif 'video_note' in keys:
                comando = f'Mensagem de vídeo. Duração: {msg["video_note"]["duration"]}s.'
            elif 'document' in keys:
                comando = f'Arquivo. Nome: {msg["document"]["file_name"]}, Tam: {int(msg["document"]["file_size"]) / 1024:.2f} KB.'
            elif 'reply_to_message' in keys:
                comando = f"Resposta à mensagem: '{msg['reply_to_message']['text']}' com o texto: '{msg['text']}.'"
            elif 'edit_date' in keys:
                comando = f"Mensagem Editada para : '{msg['text']}'"
            elif 'contact' in keys:
                comando = f'Contato. Nome: {msg["contact"]["first_name"]}, Número: {msg["contact"]["phone_number"]}.'
            else:
                comando = 'Comando desconhecido.'
            bot.sendMessage(chatid, emojize(f'Desculpe, ainda não entendo este tipo de mensagem: {comando} :disappointed_relieved:', use_aliases=True))
    except Exception as erro:
        bot.sendMessage(chatid, emojize(f'Desculpe, ocorreu um erro ainda não tratado: {erro} :cry:', use_aliases=True))
        print(f'\033[0;31mErro! {erro}.\033[m')
    finally:
        print(f'Nome: {nome:15} {comando}')


def onCallbackQuery(msg):  # Função de ação do botão de baixar
    queryID, chatid, queryData = glance(msg, flavor='callback_query')
    bot.answerCallbackQuery(queryID, text='Seu arquivo MP3 está sendo preparado')
    Util.baixarMP3(resultado[int(queryData)])
    bot.sendMessage(chatid, emojize('Sua música já está sendo enviada... :headphones:', use_aliases=True))
    bot.sendChatAction(chatid, 'upload_audio')
    arq = Util.pegaMP3()
    bot.sendAudio(chatid, open(arq, 'rb'), title=arq[:len(arq) - 16])  # manda a música com apenas seu nome original sem url
    sleep(5)
    from os import remove
    remove(arq)
    print(f'Baixar {arq[:len(arq) - 16]}')  # Nome do áudio baixado para o log


MessageLoop(bot, {'chat': onChatMessage, 'callback_query': onCallbackQuery}).run_as_thread()
print(bot.getMe())
print('Escutando ...')

while True:
    pass

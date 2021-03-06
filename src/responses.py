from pytz import timezone
from datetime import datetime
from libru import ru


weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta',
            'Sexta', 'Sábado', 'Domingo']

help = """Me manda um /quibe que eu te conto o que as tias do RU estão preparando hoje

Você também pode me enviar /subscribe e eu te enviarei \
o cardápio do RU todos os dias

Inspirado em https://voucomerno.ru/

Meu repositório: http://github.com/caiopo/quibe-bot

Feito por @caiopo"""

_cardapio = "*{weekday}, {day}/{month}*"

unknown_command = 'Não entendi'

subscribe = 'Inscrição feita!'

already_subscribed = 'Você já está inscrito!'

unsubscribe = 'Inscrição removida!'

not_subscribed = 'Você não está inscrito!'


def cardapio():
    menu = ru()

    dt = datetime.now(timezone('America/Sao_Paulo'))

    menu_lines = [
        _cardapio.format(
            weekday=weekdays[dt.weekday()],
            day=dt.day,
            month=str(dt.month).zfill(2)
        )
    ]

    if not any(menu):
        menu_lines.append('cardápio de hoje indisponível')
    else:
        menu_lines.append('hoje tem:')

        for item in menu:
            if item:
                menu_lines.append('\u2022 ' + item)

    return '\n'.join(menu_lines)


if __name__ == '__main__':
    import responses

    print(responses.cardapio())

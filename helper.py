from datetime import datetime


def money(text):
    text = text.__str__()
    return text.replace('.', ',')


def cep(text):
    text = text.__str__()
    return text[:5] + '-' + text[5:]


def telefone(text):
    text = text.__str__()
    return '(' + text[:2] + ') ' + text[2:7] + '-' + text[7:]


def show_date(text):
    text = text.__str__()
    return datetime.strptime(text, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
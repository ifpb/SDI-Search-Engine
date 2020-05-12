pure_dates_pattern = '(?:(?:\d{2}|\d{1})-(?:\d{2}|\d{1})-(?:\d{4}|\d{2})|(?:\d{2}|\d' \
                     '{1})\/(?:\d{2}|\d{1})\/(?:\d{4}|\d{2})|(?:\d{2}|\d{1})\/(?:jan' \
                     'eiro|jan(?:\.|)|fevereiro|fev(?:\.|)|março|mar(?:\.|)|abril|ab' \
                     'r(?:\.|)|maio|mai(?:\.|)|junho|jun(?:\.|)|julho|jul(?:\.|)|agost' \
                     'o|ago(?:\.|)|setembro|set(?:\.|)|outubro|out(?:\.|)|novembro|no' \
                     'v(?:\.|)|dezembro|dez(?:\.|))\/(?:\d{4}|\d{2})|(?:\d{2}|\d{1})-(' \
                     '?:janeiro|jan(?:\.|)|fevereiro|fev(?:\.|)|março|mar(?:\.|)|abril' \
                     '|abr(?:\.|)|maio|mai(?:\.|)|junho|jun(?:\.|)|julho|jul(?:\.|)|a' \
                     'gosto|ago(?:\.|)|setembro|set(?:\.|)|outubro|out(?:\.|)|novembro' \
                     '|nov(?:\.|)|dezembro|dez(?:\.|))-(?:\d{4}|\d{2})|\d{2}-\d{4}|\d{2}' \
                     '\/\d{4}|\d{4})'

month_pattern = '(?:janeiro|jan(?:\.|)|fevereiro|fev(?:\.|)|março|mar(' \
                '?:\.|)|abril|abr(?:\.|)|maio|mai(?:\.|)|junho|jun(?:\.|' \
                ')|julho|jul(?:\.|)|agosto|ago(?:\.|)|setembro|set(?:\.|)' \
                '|outubro|out(?:\.|)|novembro|nov(?:\.|)|dezembro|dez(?:\.|))'

full_dates_pattern = '(?:(?:[0-9]|[0-9][0-9]|(?:décimo segundo|décimo primero|último|p' \
                     'rimeiro|segundo|terceiro|quarto|quinto|sexto|sétimo|oitavo|nono|' \
                     'décimo))(?:º|)(?: de | do mês de |))(?:(?:janeiro|jan(?:\.|)|fev' \
                     'ereiro|fev(?:\.|)|março|mar(?:\.|)|abril|abr(?:\.|)|maio|mai(?:' \
                     '\.|)|junho|jun(?:\.|)|julho|jul(?:\.|)|agosto|ago(?:\.|)|setembr' \
                     'o|set(?:\.|)|outubro|out(?:\.|)|novembro|nov(?:\.|)|dezembro|dez' \
                     '(?:\.|))(?: de | do ano de | em | ))(?:\d{4}|\d{2})'

semester_and_others_pattern = '(?:[0-9](?:º|)|(?:décimo segundo|décimo primero|último' \
                              '|primeiro|segundo|terceiro|quarto|quinto|sexto|sétimo|' \
                              'oitavo|nono|décimo))(?: |)(?:(?:mês do ano de | mês do' \
                              ' ano | mês de )|(?:semestre|sem\.|sem)|(?:bimestre|bi' \
                              'm\.|bim)|(?:trimestre|trim\.|trim))(?: de |\/| em | do' \
                              ' ano de |)(?:\d{4}|\d{2})'

period = {
    'primeiro': 1,
    'segundo': 2,
    'terceiro': 3,
    'quarto': 4,
    'quinto': 5,
    'sexto': 6,
    'sétimo': 7,
    'setimo': 7,
    'nono': 9,
    'décimo': 10,
    'decimo': 10,
    'décimo primeiro': 11,
    'decimo primeiro': 11,
    'décimo segundo': 12,
    'decimo segundo': 12,
    'mês': 12,
    'mes': 12,
    'bimestre': 2,
    'trimestre': 3,
    'semestre': 6
}

day_one = '01'

months = {
    'janeiro': 1,
    'jan': 1,
    'jan.': 1,
    'fevereiro': 2,
    'fev': 2,
    'fev.': 2,
    'março': 3,
    'mar': 3,
    'mar.': 3,
    'abril': 4,
    'abr': 4,
    'abr.': 4,
    'maio': 5,
    'mai': 5,
    'mai.': 5,
    'junho': 6,
    'jun': 6,
    'jun.': 6,
    'julho': 7,
    'jul': 7,
    'jul.': 7,
    'agosto': 8,
    'ago': 8,
    'ago.': 8,
    'setembro': 9,
    'set': 9,
    'set.': 9,
    'outubro': 10,
    'out': 10,
    'out.': 10,
    'novembro': 11,
    'nov': 11,
    'nov.': 11,
    'dezembro': 12,
    'dez': 12,
    'dez.': 12,
}

end_dates = {
    'janeiro': 31,
    'fevereiro': 29,
    'março': 31,
    'abril': 30,
    'maio': 31,
    'junho': 30,
    'julho': 31,
    'agosto': 31,
    'setembro': 30,
    'outubro': 31,
    'novembro': 30,
    'dezembro': 31,
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    '01': 31,
    '02': 29,
    '03': 31,
    '04': 30,
    '05': 31,
    '06': 30,
    '07': 31,
    '08': 31,
    '09': 30,
    10: 31,
    11: 30,
    12: 31
}

min_year = 1900

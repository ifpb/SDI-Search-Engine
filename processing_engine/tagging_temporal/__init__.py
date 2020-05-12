from dateparser.search import search_dates
import re
from tagging_temporal.patterns import *
import datetime
import util

''' Log com as configurações padroes '''
log = util.get_logger()


def validate_years(start_year, end_year):
    current_year = int(datetime.datetime.today().date().strftime("%Y"))
    if current_year >= int(start_year) and \
            current_year >= int(end_year) and \
            min_year <= int(end_year):
        return True
    else:
        log.info('TAGGING - invalid date ' + str(start_year) + ' ' + str(end_year))
        return False


def lowest_and_highest_date(dates):
    start_dates = []
    end_dates_local = []
    for d in dates:
        start_dates.append(d['start_date'])
        end_dates_local.append(d['end_date'])
    orderedStartDates = [datetime.datetime.strptime(d, '%d/%m/%Y') for d in start_dates]
    orderedStartDates.sort()
    orderedEndDates = [datetime.datetime.strptime(d, '%d/%m/%Y') for d in end_dates_local]
    orderedEndDates.sort()
    start_date = orderedStartDates[0].date()
    end_date = orderedEndDates[len(orderedEndDates) - 1].date()
    if validate_years(start_date.strftime('%Y'), end_date.strftime('%Y')):
        return {
            'start_date': start_date.strftime('%d/%m/%Y'),
            'end_date': end_date.strftime('%d/%m/%Y')
        }
    return None


def remove_term(term, data):
    return data.replace(term, '')


def calculate_period(type_of_period, index):
    return {
        'start': ((index - 1) * type_of_period + 1),
        'end': ((index - 1) * type_of_period + 1) + (type_of_period - 1)
    }


def build_date(start_day, start_month, start_year,
               end_day=None, end_month=None, end_year=None):
    if end_day is None and end_month is None and end_year is None:
        end_day = start_day
        end_month = start_month
        end_year = start_year
    if validate_years(start_year, end_year):
        return {
            'start_date': f'{start_day}/{start_month}/{start_year}',
            'end_date': f'{end_day}/{end_month}/{end_year}'
        }
    return None


def validate_word(word, max_period):
    if word in period:
        two_months = period[word]
        if two_months <= max_period:
            return True
        else:
            return False


def validate_number(number, max_period):
    first_term = remove_term('º', number)
    if first_term.isnumeric():
        first_term = int(first_term)
        if first_term <= max_period:
            return True
        else:
            return False

# SEMESTER, TRIMEMSTER, BIMESTER AND MONTHS


def build_date_for_semester_others(date_result):
    if ' mês ' in date_result or ' mes ' in date_result:
        date_split = date_result.split(' ')
        year = str(date_split[len(date_split) - 1])
        first_term = date_split[0]
        if len(first_term) > 3:
            if validate_word(date_split[0], period['mes']):
                interval = calculate_period(1, period[date_split[0]])
                return build_date(day_one, interval['start'], year,
                                  end_dates[interval['end']], interval['end'], year)
            return False
        else:
            if validate_number(first_term, period['mes']):
                first_term = remove_term('º', first_term)
                first_term = int(first_term)
                interval = calculate_period(1, first_term)
                return build_date(day_one, interval['start'], year,
                                  end_dates[interval['end']], interval['end'], year)
            return None
    elif 'bimestre' in date_result or 'bim' in date_result:
        date_split = date_result.split(' ')
        year = str(date_split[len(date_split) - 1])
        first_term = date_split[0]
        if len(first_term) > 3:
            if validate_word(date_split[0], 6):
                interval = calculate_period(period['bimestre'], period[date_split[0]])
                return build_date(day_one, interval['start'], year,
                                  end_dates[interval['end']], interval['end'], year)
            return None
        else:
            if validate_number(first_term, 6):
                first_term = remove_term('º', first_term)
                first_term = int(first_term)
                interval = calculate_period(period['bimestre'], first_term)
                return build_date(day_one, interval['start'], year,
                                  end_dates[interval['end']], interval['end'], year)
            return None
    elif 'trimestre' in date_result or 'trim' in date_result:
        date_split = date_result.split(' ')
        year = str(date_split[len(date_split) - 1])
        first_term = date_split[0]
        if len(first_term) > 3:
            if validate_word(date_split[0], 4):
                interval = calculate_period(period['trimestre'], period[date_split[0]])
                return build_date(day_one, interval['start'], year,
                                  end_dates[interval['end']], interval['end'], year)
            return None
        else:
            if validate_number(first_term, 4):
                first_term = remove_term('º', first_term)
                first_term = int(first_term)
                interval = calculate_period(period['trimestre'], first_term)
                return build_date(day_one, interval['start'], year,
                                  end_dates[interval['end']], interval['end'], year)
            return None

    elif 'semestre' in date_result or 'sem' in date_result:
        date_split = date_result.split(' ')
        year = str(date_split[len(date_split) - 1])
        first_term = date_split[0]
        if len(first_term) > 3:
            if validate_word(date_split[0], period['semestre']):
                interval = calculate_period(period['semestre'], period[date_split[0]])
                return build_date(day_one, interval['start'], year,
                                  end_dates[interval['end']], interval['end'], year)
            return None
        else:
            if validate_number(first_term, period['semestre']):
                first_term = remove_term('º', first_term)
                first_term = int(first_term)
                interval = calculate_period(period['semestre'], first_term)
                return build_date(day_one, interval['start'], year,
                                  end_dates[interval['end']], interval['end'], year)
            return None


def check_contains_semester(date):
    log.info('check_contains_semester')
    pattern = semester_and_others_pattern
    match = re.findall(pattern, date, re.IGNORECASE)
    if len(match) == 1:
        return build_date_for_semester_others(match[0])
    elif len(match) > 1:
        dates = []
        for d in match:
            dt = build_date_for_semester_others(d)
            if dt is not None:
                dates.append(dt)
        return lowest_and_highest_date(dates)

# FULL DATES


def build_date_for_full_dates(date):
    local_month_pattern = month_pattern
    date_result = date
    date_result = date_result.split(' ')
    year = date_result[len(date_result) - 1]
    first_term = date_result[0]
    month_result = re.findall(local_month_pattern, date, re.IGNORECASE)
    if len(month_result) > 0:
        month = month_result[0].lower()
        month_number = months[month]
        if len(first_term) > 3:
            if first_term in period:
                return build_date(period[first_term], month_number, year)
            return None
        else:
            first_term = remove_term('º', first_term)
            if first_term.isnumeric():
                first_term = int(first_term)
                return build_date(first_term, month_number, year)


def check_contains_dates(date):
    log.info('check_contains_dates')
    pattern = full_dates_pattern
    match = re.findall(pattern, date, re.IGNORECASE)
    if len(match) == 1:
        return build_date_for_full_dates(match[0])
    elif len(match) > 1:
        dates = []
        for d in match:
            dt = build_date_for_full_dates(d)
            if dt is not None:
                dates.append(dt)
        return lowest_and_highest_date(dates)
    else:
        return None


# PURE DATES


def build_date_for_pure_dates(result):
    local_month_pattern = month_pattern
    month_result = re.findall(local_month_pattern, result, re.IGNORECASE)
    if len(month_result) > 0:
        date = result
        date = date.replace(month_result[0], str(months[month_result[0]]))
        return date
    else:
        date = result
        if len(date) == 4:
            return build_date(day_one, '01', date,
                              end_dates['dezembro'], '12', date)
        elif len(date) == 6 or len(date) == 7:
            if '/' in date:
                date_split = date.split('/')
                return build_date(day_one, date_split[0], date_split[1],
                                  end_dates[date_split[0]], date_split[0], date_split[1])
            else:
                date_split = date.split('-')
                return build_date(day_one, date_split[0], date_split[1],
                                  end_dates[date_split[0]], date_split[0], date_split[1])
        else:
            if '/' in date:
                date_split = date.split('/')
                return build_date(date_split[0], date_split[1], date_split[2])
            else:
                date_split = date.split('-')
                return build_date(date_split[0], date_split[1], date_split[2])


def check_pure_dates(date):
    log.info('check_pure_dates')
    pattern = pure_dates_pattern
    result = re.findall(pattern, date, re.IGNORECASE)
    if len(result) == 1:
        return build_date_for_pure_dates(result[0])
    elif len(result) > 1:
        dates = []
        for match in result:
            dt = build_date_for_pure_dates(match)
            if dt is not None:
                dates.append(dt)
        return lowest_and_highest_date(dates)
    else:
        return None


def find_date(text):
    result = check_contains_semester(text)
    if result is None:
        result = check_contains_dates(text)
    if result is None:
        result = check_pure_dates(text)
    return result


# if __name__ == '__main__':
#     # text1 = 'Precipitação anual média (06-1960 - -06-1990) 22/06/1990 e a data de 22/06/1899  '
#     # text1 = 'Precipitação anual média de 01 de janeiro de 2015 a 05 de março do ano de 2020 e a data de 03 de janeiro de 1899'
#     text1 = 'Precipitação anual média do 2º bimestre de 2014 ao terceiro trimestre do ano de 2017 e final do 4º mês de 1899'
#     print(find_date(text1))

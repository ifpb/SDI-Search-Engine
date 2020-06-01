import datetime
from dateutil import relativedelta
import data_access

end_of_month = {
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


def representation_start_day_of_month(date):
    quantity_days_month = end_of_month[date.month]
    return (quantity_days_month - (quantity_days_month - date.day)) / quantity_days_month


def representation_end_day_of_month(date):
    return date.day / end_of_month[date.month]


def calculate_total_month_same_year(start_date, end_date):
    if start_date.month != end_date.month:
        if start_date.day == 1:
            if end_date.day == end_of_month[end_date.month]:
                return end_date.month - (start_date.month - 1)
            else:
                return (end_date.month - start_date.month) + representation_end_day_of_month(end_date)
        elif start_date.day > 1:
            if end_date.day == end_of_month[end_date.month]:
                return (end_date.month - (start_date.month + 1)) + representation_start_day_of_month(start_date)
            else:
                return representation_start_day_of_month(start_date) + representation_end_day_of_month(end_date)
    else:
        start_day = 0 if start_date.day == 1 else start_date.day
        return (end_date.day - start_day) / end_of_month[start_date.month]


def calculate_total_month(start_date, end_date):
    if start_date.year == end_date.year:
        return calculate_total_month_same_year(start_date, end_date)
    else:
        if start_date.month <= end_date.month:
            return calculate_total_month_same_year(start_date, end_date) + (12 * (end_date.year - start_date.year))
        else:
            diference_month = (end_date.month + (start_date.month - end_date.month))
            fake_end_date = datetime.date(start_date.year, diference_month, 1) + relativedelta.relativedelta(day=31)
            result = calculate_total_month_same_year(start_date, fake_end_date) + (
                    12 * (end_date.year - start_date.year))
            result = result - (start_date.month - end_date.month)
            return result


def intersection(a_start_date, a_end_date, b_start_date, b_end_date):
    if b_start_date >= a_start_date and b_end_date <= a_end_date:
        return {'start_date': b_start_date, 'end_date': b_end_date}
    elif b_start_date < a_start_date and b_end_date >= a_start_date:
        if b_end_date <= a_end_date:
            return {'start_date': a_start_date, 'end_date': b_end_date}
        else:
            return {'start_date': a_start_date, 'end_date': a_end_date}
    elif b_start_date < a_end_date and b_end_date >= a_end_date:
        if b_start_date < a_start_date:
            return {'start_date': a_start_date, 'end_date': a_end_date}
        else:
            return {'start_date': b_start_date, 'end_date': a_end_date}
    else:
        return None


def difference(a_start_date, a_end_date, b_start_date, b_end_date):
    """ calculate the difference of b by a """
    if b_start_date >= a_start_date and b_end_date <= a_end_date:
        return 0
    elif b_start_date < a_start_date and b_end_date >= a_start_date:
        if b_end_date < a_end_date:
            return calculate_total_month(b_start_date, a_start_date)
        else:
            return calculate_total_month(b_start_date, a_start_date) + calculate_total_month(a_end_date, b_end_date)
    elif b_start_date < a_end_date and b_end_date >= a_end_date:
        if b_start_date < a_start_date:
            return calculate_total_month(b_start_date, a_start_date) + calculate_total_month(a_end_date, b_end_date)
        else:
            return calculate_total_month(a_end_date, b_end_date)
    else:
        print('não tem diferença')
        return None


def tversky(a_start_date, a_end_date, b_start_date, b_end_date):
    intersection_date = intersection(a_start_date, a_end_date, b_start_date, b_end_date)
    if intersection_date is not None:
        a_inter_b = calculate_total_month(intersection_date['start_date'], intersection_date['end_date'])
        a_difference_b = difference(b_start_date, b_end_date, a_start_date, a_end_date)
        b_difference_a = difference(a_start_date, a_end_date, b_start_date, b_end_date)
        return a_inter_b / (a_inter_b + (0.5 * a_difference_b) + (0.5 * b_difference_a))
    return None


def features_intersects_dates(data, data_dict):
    split = data['start_date'].split('-')
    start_date = datetime.date(int(split[0]), int(split[1]), int(split[2]))
    split = data['end_date'].split('-')
    end_date = datetime.date(int(split[0]), int(split[1]), int(split[2]))
    all_features = data_access.feature_type_id_dates()
    for feature in all_features:
        if feature['start_date'] is not None and feature['end_date'] is not None:
            if intersection(start_date, end_date, feature['start_date'], feature['end_date']) is not None:
                similarity = tversky(start_date, end_date, feature['start_date'], feature['end_date'])
                data_dict[feature['id']] = similarity


def services_intersects_dates(data, data_dict):
    split = data['start_date'].split('-')
    start_date = datetime.date(int(split[0]), int(split[1]), int(split[2]))
    split = data['end_date'].split('-')
    end_date = datetime.date(int(split[0]), int(split[1]), int(split[2]))
    all_services = data_access.service_id_dates()
    for service in all_services:
        if service['start_date'] is not None and service['end_date'] is not None:
            if intersection(start_date, end_date, service['start_date'], service['end_date']):
                similarity = tversky(start_date, end_date, service['start_date'], service['end_date'])
                data_dict[service['id']] = similarity

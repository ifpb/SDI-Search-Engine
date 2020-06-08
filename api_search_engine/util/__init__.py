import log

app_log = log.get_logger()


def filter_result_of_dict(list_of_dict):
    result = []
    if list_of_dict.__len__() > 1:
        FILTERS_LENGTH = list_of_dict.__len__()
        shortest_list = list_of_dict[0]
        # find shortest list
        for d in list_of_dict:
            if d.__len__() < shortest_list.__len__():
                shortest_list = d

        # find common ids
        for i in shortest_list:
            count = 0
            sum_similarity = 0
            for d in list_of_dict:
                if d.__contains__(f'{i}'):
                    count += 1
                    sum_similarity += d[i]
            if count == FILTERS_LENGTH:
                app_log.info('Common resources: ' + i)
                similarity = sum_similarity / FILTERS_LENGTH
                result.append(build_item_result(i, similarity))
    else:
        dict = list_of_dict[0]
        for i in dict:
            result.append(build_item_result(i, dict[i]))
    return result


def build_item_result(id, similarity):
    return {
        'id': id,
        'similarity': similarity
    }
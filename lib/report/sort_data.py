from collections import OrderedDict


def sort_data(data, key):
    if key == 'event_translation':
        return _event_translation_sort(data)
    return data


def _event_translation_sort(data):
    rtn = []
    for event in data:
        new_event = OrderedDict()
        for key, val in sorted(event.iteritems(), cmp=_event_translation_sorter):
            new_event[key] = val
        rtn.append(new_event)
    return rtn


def _event_translation_sorter(val1, val2):
    val1_parts = val1[0].split('_')
    val2_parts = val2[0].split('_')
    if val1_parts[0] == val2_parts[0] and len(val1_parts) == 2 and len(val1_parts) == 2:
        return -1 * cmp(val1_parts[1], val2_parts[1])
    else:
        return cmp(val1, val2)

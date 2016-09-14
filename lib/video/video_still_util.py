def convert_min_sec_to_sec(time_str):
    parts = time_str.split(':')

    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 60 * 60 + int(parts[1]) * 60 + int(parts[2])


def convert_seconds_to_parts(seconds):
    seconds = int(seconds)
    if type(seconds) == str:
        seconds = int(seconds)
    m, s = divmod(seconds, 60)
    m_digit_2, m_digit_1 = divmod(m, 10)
    s_digit_2, s_digit_1 = divmod(s, 10)

    if m_digit_2 == 0:
        return m_digit_1, s_digit_2, s_digit_1
    else:
        return m_digit_2, m_digit_1, s_digit_2, s_digit_1


def convert_parts_to_seconds(parts):
    if len(parts) == 3:
        return parts[0] * 60 + parts[1] * 10 + parts[2]
    elif len(parts) == 4:
        return parts[0] * 60 * 10 + parts[1] * 60 + parts[2] * 10 + parts[3]
    else:
        return None


def convert_parts_to_string(parts):
    if len(parts) == 3:
        return str(parts[0]) + ":" + str(parts[1]) + str(parts[2])
    elif len(parts) == 4:
        return str(parts[0]) + str(parts[1]) + ":" + str(parts[2]) + str(parts[3])
    else:
        return None


def seconds_to_string(seconds):
    if seconds is None:
        return ""
    return convert_parts_to_string(convert_seconds_to_parts(int(seconds)))

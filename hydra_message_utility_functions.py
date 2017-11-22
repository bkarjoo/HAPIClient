def get_len_str(msg):
    l = len(msg)
    if l < 10:
        return '00' + str(l)
    elif l < 100:
        return '0' + str(l)
    else:
        return str(l)


def add_length(msg):
    return msg[:10] + get_len_str(msg) + msg[13:]
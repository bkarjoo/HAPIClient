def update_quote(q, tokens):
    if tokens[2] == 'A':
        q.set_ask(tokens[5])
        q.set_ask_size(tokens[6])
        q.set_tick_val(tokens[7])
    elif tokens[2] == 'B':
        q.set_bid(tokens[5])
        q.set_bid_size(tokens[6])
        q.set_tick_val(tokens[7])
    elif tokens[2] == 'J':
        q.set_last(tokens[5])
        q.set_last_size(tokens[6])
    elif tokens[2] == 'C':
        q.set_bid(tokens[5])
        q.set_bid_size(tokens[6])
        q.set_ask(tokens[7])
        q.set_ask_size(tokens[8])
        q.set_tick_val(tokens[9])
    elif tokens[2] == 'D':
        q.set_high(tokens[5])
    elif tokens[2] == 'K':
        q.set_low(tokens[5])
    elif tokens[2] == 'F':
        q.set_open(tokens[5])
    elif tokens[2] == 'G':
        q.set_previous_close(tokens[5])
    elif tokens[2] == 'H':
        q.set_volume(tokens[5])
    elif tokens[2] == 'V':
        q.set_vwap(tokens[5])
        q.set_vwap_exchange(tokens[6])
        q.set_vwap_10(tokens[7])
    elif tokens[2] == 'N':
        q.set_unofficial_close(tokens[5])
    elif tokens[2] == '1':
        # level 1 data
        if len(tokens) < 19: return
        print tokens
        q.set_last(tokens[5])
        q.set_bid(tokens[6])
        q.set_bid_size(tokens[7])
        q.set_ask(tokens[8])
        q.set_ask_size(tokens[9])
        q.set_high(tokens[10])
        q.set_low(tokens[11])
        q.set_volume(tokens[12])
        q.set_open(tokens[13])
        q.set_previous_close(tokens[14])
        q.set_tick_val(tokens[15])
        q.set_news(tokens[16])
        q.set_vwap(tokens[17])
        q.set_vwap_10(tokens[18])
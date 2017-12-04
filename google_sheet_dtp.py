from google_api import *

class GoogleSheetDailyTradingProcedure(object):
    def process_row(self, row, i = 0):
        if (len(row) >= 9):
            strategy = str(row[0]).upper().strip()
            account = str(row[1]).upper().strip()
            symbol = str(row[2]).split(' ')[0].upper().strip()
            side = str(row[3]).upper().strip()
            shares = str(row[4]).strip()
            dollar_value = str(row[5]).strip()
            order_type = str(row[6]).upper().strip()
            limit_price = str(row[7])
            order_date = str(row[8])
            exit_strategy = ''
            if (len(row)) >= 11:
                exit_strategy = str(row[10])

            print '{}. strat:{} acct:{} symb:{} side:{} shrs:{} ${} {}k type:{} dd:{} exit:{}'.format(
                i, strategy, account, symbol, side, shares, limit_price[1:], dollar_value, order_type, order_date,
                exit_strategy
            )


            if strategy == 'SENTIMENT':
                # place opening orders
                try:
                    qty = int(shares)
                    if side == 'SHORT' or side == 'SELL':
                        qty *= -1
                    limit_price = float(limit_price[1:])
                    o = generate_opg_limit_order(qty, symbol, limit_price, account)
                    message = add_length(o.craft_message())
                    if confirm:
                        action = 'buy' if qty > 0 else 'sell'
                        user_input = raw_input('Should I {0} {1} {2} {3} LOO (y/n)?'.format(
                            action, abs(qty), symbol, limit_price))
                        if user_input == 'y':
                            send_message_to_es(message)
                        else:
                            print 'Did not submit: {}'.format(message)
                    else:
                        send_message_to_es(message)
                    pass
                except:
                    print 'Error placing order for {0} from row {1}.'.format(symbol, i)
            elif strategy == 'SECONDARY':
                # place opening orders
                try:
                    if note.strip() == 'Exit (MOC)':
                        prompt = 'How many shares of {0} do you have in {1}?'.format(
                            symbol, account
                        )
                        qty = raw_input(prompt)
                        qty = int(qty) * -1
                        o = generate_moc_market_order(qty, symbol, account)
                        prompt = 'Should I {0} {1} {2} moc (y/n)?'.format('sell', abs(qty), symbol)
                        user_input = raw_input(prompt)
                        if user_input == 'y':
                            hydra_order_message = o.craft_message()
                            hydra_order_message = add_length(hydra_order_message)
                            es_sock.sendall(hydra_order_message)
                            # print hydra_order_message
                        else:
                            pass
                    elif note.strip() == 'Enter (MOO)':
                        prompt = 'How many shares of {0} do you have in {1}?'.format(
                            symbol, account
                        )
                        qty = raw_input(prompt)
                        qty = int(qty)
                        o = generate_opg_market_order(qty, symbol, account)
                        prompt = 'Should I {0} {1} {2} moo (y/n)?'.format('buy', abs(qty), symbol)
                        user_input = raw_input(prompt)
                        if user_input == 'y':
                            hydra_order_message = o.craft_message()
                            hydra_order_message = add_length(hydra_order_message)
                            es_sock.sendall(hydra_order_message)
                            # print hydra_order_message
                        else:
                            pass
                except:
                    print 'Error placing order for {0} from row {1}.'.format(symbol, i)
            elif strategy == 'INDEX MOME':
                pass
            elif strategy == 'CLE':
                pass
            elif strategy == 'INDEX ARB':
                pass
            elif strategy == 'LOCK-UP':
                pass
            elif strategy == 'IPO':
                pass
            elif strategy == 'RSI':
                pass
            elif strategy == 'BUYBACK':
                pass
            elif strategy == 'JAP CROSS':
                pass
            elif strategy == 'CORP ACTION':
                pass
            elif strategy == 'Tax':
                pass

    def process_sheet(self, confirm = True):
        sheet = get_sheet()
        i = 1
        for row in sheet:
            i += 1
            self.process_row(row, i)

    def get_row(self, row_number):
        sheet = get_sheet()
        try:
            return sheet[row_number+1]
        except:
            return None

    def print_row(self, row_number):
        row = get_row(row_number)
        print row

from order import *
from order_id_generator import OrderIdGenerator

class OrderFactory(object):

    def __init__(self):
        self.id_generator = OrderIdGenerator()

    def generate_limit_order(self, qty, symbol, price, acct):
        if type(qty) != int:
            qty = int(qty)
        o = Order()
        o.account = acct
        o.quantity = abs(qty)
        o.symbol = symbol
        o.order_price = price
        o.tif = tif_type.day
        o.type = order_type.limit
        o.parent_id = self.id_generator.generate_order_id()
        o.display = 'Y'
        o.algo_fields = '4A,,,,,'
        o.security_type = '8'
        o.security_id = symbol
        o.reserve_size = ''
        if qty > 0:
            o.side = side_type.buy
        elif qty < 0:
            o.side = side_type.sell
        return o

    def generate_opg_market_order(self, qty, symbol, acct):
        if type(qty) != int:
            qty = int(qty)
        o = Order()
        o.account = acct
        o.quantity = abs(qty)
        o.symbol = symbol
        o.tif = tif_type.opg
        o.type = order_type.market
        o.parent_id = self.id_generator.generate_order_id()
        o.display = 'Y'
        o.algo_fields = '9,,,,,'
        o.security_type = '8'
        o.security_id = symbol
        o.reserve_size = 100
        if qty > 0:
            o.side = side_type.buy
        elif qty < 0:
            o.side = side_type.sell
        return o

    def generate_moc_market_order(self, qty, symbol, acct):
        if type(qty) != int:
            qty = int(qty)
        o = Order()
        o.account = acct
        o.quantity = abs(qty)
        o.symbol = symbol
        o.tif = tif_type.day
        o.type = order_type.moc
        o.parent_id = self.id_generator.generate_order_id()
        o.display = 'Y'
        o.algo_fields = '9,,,,,'
        o.security_type = '8'
        o.security_id = symbol
        o.reserve_size = ''
        if qty > 0:
            o.side = side_type.buy
        elif qty < 0:
            o.side = side_type.sell
        return o

    def generate_opg_limit_order(self, qty, symbol, price, acct):
        if type(qty) != int:
            qty = int(qty)
        o = Order()
        o.account = acct
        o.quantity = abs(qty)
        o.symbol = symbol
        o.tif = tif_type.opg
        o.type = order_type.limit
        o.parent_id = self.id_generator.generate_order_id()
        o.display = 'Y'
        o.algo_fields = '9,,,,,'
        o.security_type = '8'
        o.security_id = symbol
        o.reserve_size = ''
        o.order_price = price
        if qty > 0:
            o.side = side_type.buy
        elif qty < 0:
            o.side = side_type.sell
        return o

    def generate_loc_limit_order(self, qty, symbol, price, acct):
        if type(qty) != int:
            qty = int(qty)
        o = Order()
        o.account = acct
        o.quantity = abs(qty)
        o.symbol = symbol
        o.tif = tif_type.day
        o.type = order_type.loc
        o.parent_id = self.id_generator.generate_order_id()
        o.display = 'Y'
        o.algo_fields = '9,,,,,'
        o.security_type = '8'
        o.security_id = symbol
        o.reserve_size = ''
        o.order_price = price
        if qty > 0:
            o.side = side_type.buy
        elif qty < 0:
            o.side = side_type.sell
        return o

    def generate_nite_vwap_order(self, qty, symbol, start_time, end_time, stop_price, acct):
        if type(qty) != int:
            qty = int(qty)
        o = Order()
        o.account = acct
        o.quantity = abs(qty)
        o.symbol = symbol
        o.tif = tif_type.day
        o.type = order_type.market
        o.parent_id = self.id_generator.generate_order_id()
        o.display = 'Y'
        o.set_nite_vwap(start_time, end_time, stop_price)
        o.security_type = '8'
        o.security_id = symbol
        o.reserve_size = ''
        o.channel_of_execution = 'NITE'
        if qty > 0:
            o.side = side_type.buy
        elif qty < 0:
            o.side = side_type.sell
        return o

    def generate_stop_limit_order(self, qty, symbol, stop_price, stop_limit, acct):
        if type(qty) != int:
            qty = int(qty)
        o = Order()
        o.account = acct
        o.quantity = abs(qty)
        o.symbol = symbol
        o.order_price = stop_price
        o.stop_limit_price = stop_limit
        o.tif = tif_type.day
        o.type = order_type.stop
        o.parent_id = self.id_generator.generate_order_id()
        o.display = 'Y'
        o.algo_fields = '9,,,,,'
        o.security_type = '8'
        o.security_id = symbol
        o.reserve_size = ''
        if qty > 0:
            o.side = side_type.buy
        elif qty < 0:
            o.side = side_type.sell
        return o

    def generate_stop_market_order(self, qty, symbol, stop_price, acct):
        if type(qty) != int:
            qty = int(qty)
        o = Order()
        o.account = acct
        o.quantity = abs(qty)
        o.symbol = symbol
        o.order_price = stop_price
        o.tif = tif_type.day
        o.type = order_type.stop
        o.parent_id = self.id_generator.generate_order_id()
        o.display = 'Y'
        o.algo_fields = '9,,,,,'
        o.security_type = '8'
        o.security_id = symbol
        o.reserve_size = ''
        if qty > 0:
            o.side = side_type.buy
        elif qty < 0:
            o.side = side_type.sell
        return o

    def sell(self, command):
        try:
            """sell 100 XYZ 23.50 day ALGOPAIR"""
            """sell 100 XYZ 23.50 loo ALGOSYND"""
            """sell 100 XYZ moo ALGOGROUP"""
            """sell 100 XYZ vwap 23.5 stop ALGOSYND"""
            """sell 100 XYZ vwap 23.5 * 0.99 stop ALGOGROUP"""
            values = command.split(' ')
            qty = int(values[1])
            # -qty means sell
            qty = qty * -1
            o = Order()
            acct = 'ALGOGROUP'
            if values[3].upper() == 'MOO':
                if len(values) == 5:
                    acct = values[4]
                o = self.generate_opg_market_order(qty, values[2], acct)
            elif values[3].upper() == 'MOC':
                if len(values) == 5:
                    acct = values[4]
                o = self.generate_moc_market_order(qty, values[2], acct)
            elif values[3].upper() == 'VWAP':
                if values[5] == '*':
                    price = float(values[4])
                    multiplier = float(values[6])
                    price = round(price * multiplier, 2)
                    if len(values) == 9:
                        acct = values[8]
                    o = self.generate_nite_vwap_order(qty, values[2], '09-45-00', '13-00-00', price, acct)
                else:
                    if len(values) == 7:
                        acct = values[6]
                    o = self.generate_nite_vwap_order(qty, values[2], '09-45-00', '13-00-00', values[4], acct)
            elif values[4].upper() == 'LOO':
                if len(values) == 6:
                    acct = values[5]
                o = self.generate_opg_limit_order(qty, values[2], values[3], acct)
            elif values[4].upper() == 'LOC':
                if len(values) == 6:
                    acct = values[5]
                o = self.generate_loc_limit_order(qty, values[2], values[3], acct)
            elif values[4].upper() == 'DAY':
                if len(values) == 6:
                    acct = values[5]
                o = self.generate_limit_order(qty, values[2], values[3], acct)
            elif values[4].upper() == 'STOP':
                if len(values) == 8:
                    acct = values[7]
                o = self.generate_stop_limit_order(qty, values[2], values[3], values[5], acct)

            return o
        except Exception as e:
            print e

    def buy(self, command):
        try:
            """buy 100 XYZ 23.50 day (ALGOPAI)"""
            """buy 100 XYZ 23.50 loo (ALGOSYND)"""
            """buy 100 XYZ moo (ALGOGROUP)"""
            """buy 100 XYZ 23.5 stop 23.75 limit (ALGOGROUP)"""
            """buy 100 XYZ VWAP 23.5 stop (ALGOGROUP)"""
            """buy 100 XYZ VWAP 23.5 * 1.01 stop (ALGOGROUP)"""
            values = command.split(' ')

            o = Order()
            acct = 'ALGOGROUP'
            if len(values) == 4: values.append(acct)
            if values[3].upper() == 'MOO':
                if len(values) == 5:
                    acct = values[4]
                o = self.generate_opg_market_order(values[1], values[2], acct)
            elif values[3].upper() == 'MOC':
                if len(values) == 5:
                    acct = values[4]
                o = self.generate_moc_market_order(values[1], values[2], acct)
            elif values[3].upper() == 'VWAP':
                if values[5] == '*':
                    price = float(values[4])
                    multiplier = float(values[6])
                    price = round(price * multiplier, 2)
                    if len(values) == 9:
                        acct = values[8]
                    o = self.generate_nite_vwap_order(values[1], values[2], '09-45-00', '13-00-00', price, acct)
                else:
                    if len(values) == 7:
                        acct = values[6]
                    o = self.generate_nite_vwap_order(values[1], values[2], '09-45-00', '13-00-00', values[4], acct)
            elif values[4].upper() == 'LOO':
                if len(values) == 6:
                    acct = values[5]
                o = self.generate_opg_limit_order(values[1], values[2], values[3], acct)
            elif values[4].upper() == 'LOC':
                if len(values) == 6:
                    acct = values[5]
                o = self.generate_loc_limit_order(values[1], values[2], values[3], acct)
            elif values[4].upper() == 'DAY':
                if len(values) == 6:
                    acct = values[5]
                o = self.generate_limit_order(values[1], values[2], values[3], acct)
            elif values[4].upper() == 'STOP':
                if len(values) == 8:
                    acct = values[7]
                o = self.generate_stop_limit_order(values[1], values[2], values[3], values[5], acct)


            return o
        except Exception as e:
            print 'error encountered in buy function:\n{}'.format(e)

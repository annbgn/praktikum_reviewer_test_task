import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            # трудно читать, когда в конструкции if not <condition> все элементы находятся на разных строках. можно прогнать black, чтобы стало красиво
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # с заглавной буквы пишутся названия классов, а здесь переменная, и ее надо именовать с маленькой буквы. подробнее про нейминг https://www.python.org/dev/peps/pep-0008/#naming-conventions
        for Record in self.records:
            #  обычно если в теле цикла содержится один if и никакой другой логики, то сокращают через list comprehension, например так: sum([record for record in self.record if record > date == dt.datetime.now().date()])
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                #  можно сократить до 0 <=(today - record.date).days < 7
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # название метода достаточно выразительно, чтобы комментарий стал излишним :)
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # бэкслеш не обязателен
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        #  этот else можно опустить, потому что перед ним if + return
        else:
            # скобки можно убрать
            return('Хватит есть!')


class CashCalculator(Calculator):
    # можно не переводить int во float, а задать константу изначально вещественной 60. Комментарии так же не нужны, потому что константы хорошо названы
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                # в методах класса всегда можно обратиться к его атрибутам через self.<name>, поэтому передавать константы как аргументы не обязательно
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # можно не заводить новую переменную, а пользоваться только currency, это сделает код чище
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # == возвращает булево значение, а = присваивает значение переменной
            cash_remained == 1.00
            currency_type = 'руб'
        # возможно стоит обрабатывать случай, если currency пришла не usd, eur или rub, а какая-то неизвестная
        # хочется видеть пустую строку перед новым блоком, это как разделение на абзацы в тексте
        if cash_remained > 0:
            return (
                # в некоторых случаях возвращаются f-строки, а в некоторых обычные. лучше придерживаться одного формата
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # elif можно заменить на else, потому что перед ним проверяются условия cash_remained>0 и cash_remained==0, поэтому в этой ветке cash_remained ничего не остается как быть отрицательным
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # здесь формально переопределяется метод, а де факто он работает так же, как и метод родительского класса, так что переопределение теряет смысл
    def get_week_stats(self):
        super().get_week_stats()

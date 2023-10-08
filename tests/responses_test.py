from handlers._responses import RESPONSES


def current_balance_test():
    expected = (
            'Изменить баланс на ЧИСЛО - /balance ЧИСЛО. '
            'Поддерживаются целые числа, а так же выражения с ними. '
            'Например: "100 + 200", или "100 '
            '\n'
            '* все что ты напишешь с новой строки строки будет '
            'расцениваться как комментарий и будет сохранен в историю'
            '\n\n'
            'Твой баланс: 100 AMD'
        )
    msg = RESPONSES['current_balance'].format(balance=100, currency='AMD')

    assert expected == msg


def write_expence_test():
    expected = (
            "Впиши свой расход для 'test item'. "
            'Поддерживаются целые числа, а так же выражения с ними. '
            'Например: "100 + 200", или "100 '
            '\n'
            '* все что ты напишешь с новой строки строки будет '
            'расцениваться как комментарий и будет сохранен в историю'
            '\n\n'
        )
    msg = RESPONSES['current_balance'].format(item='test item')

    assert expected == msg

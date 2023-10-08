_custom_eval_msg = (
        'Поддерживаются целые числа, а так же '
        'выражения с ними. Например: "100 + 200", или "100 -200".'
        '\n'
        '* все что ты напишешь с новой строки строки будет расцениваться как '
        'комментарий и будет сохранен в историю'
    )


RESPONSES = {
        'write_expence': 'Впиши свой расход для {item!r}. ' + _custom_eval_msg,
        'new_record': (
            'Пользователь {first_name} добавил новую запись для категории '
            '{item_name!r} на сумму {text} {currency}'
        ),
        'new_item': 'Расход {text!r} доступен в общем списке',
        'choose': 'Выбирай',
        'select_new_type': 'Выбери тип расхода',
        'write_new_type_name': 'Напиши название для нового типа расходов',
        'custom_date': 'Введи дату в формате YYYY-MM-DD для получения отчета',
        'current_balance': (
            'Изменить баланс на ЧИСЛО - /balance ЧИСЛО. ' + _custom_eval_msg +
            '\n\n'
            'Твой баланс: {balance!r} {currency}'
        ),
        'new_replanishment': 'Новое пополнение на {value} {currency}',
        'new_expence': 'Новый расход на сумму {value} {currency}',
        'wrong_value_argument': 'Неправильный аргумент: {value!r}',
    }

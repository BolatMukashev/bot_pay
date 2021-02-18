def you_promo_code_registered_message(promo_code):
    html = f"""
        <html>
        <head>
        </head>
        <body>
        <h1>Поздравляю!</h1>
        <p>Твой промокод <b>{promo_code}</b> зарегистрирован!</p>
        </body>
        </html>
    """

    return html
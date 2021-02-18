def hello_auto_school_message(secret_key):
    html = f"""
        <html>
        <head>
        </head>
        <body>
        <p>{secret_key}</p>
        <p><img src="https://avatarko.ru/img/kartinka/33/multfilm_lyagushka_32117.jpg" alt="Письма мастера дзен"></p>
        </body>
        </html>
    """
    return html

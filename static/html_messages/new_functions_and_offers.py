def new_func_and_offers_message(message):
    html = ["""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Обновление</title>
                <style type="text/css">
                    /*Псевдо-Обнуление*/
                    *,
                    *:before,
                    *:after {
                        -moz-box-sizing: border-box;
                        -webkit-box-sizing: border-box;
                        box-sizing: border-box;
                    }
        
                    :focus,
                    :active {
                        outline: none;
                    }
        
                    a:focus,
                    a:active {
                        outline: none;
                    }
        
                    nav,
                    footer,
                    header,
                    aside {
                        display: block;
                    }
        
                    input,
                    button,
                    textarea {
                        font-family: inherit;
                    }
        
                    input::-ms-clear {
                        display: none;
                    }
        
                    button {
                        cursor: pointer;
                    }
        
                    button::-moz-focus-inner {
                        padding: 0;
                        border: 0;
                    }
        
                    a,
                    a:visited {
                        text-decoration: none;
                    }
        
                    a:hover {
                        text-decoration: none;
                    }
        
                    ul li {
                        list-style: none;
                    }
        
                    img {
                        vertical-align: top;
                    }
        
                    input::-webkit-outer-spin-button,
                    input::-webkit-inner-spin-button {
                        -webkit-appearance: none;
                    }
        
                    /*--------------------*/
                    .main__block {
                        width: 100%;
                        height: 100%;
                        text-align: center;
                    }
        
                    h1 {
                        font-family: Verdana, Arial, Helvetica, sans-serif;
                        font-size: 1.5em;
                        color: #333366;
                    }
        
                    h2 {
                        font-family: Verdana, Arial, Helvetica, sans-serif;
                        font-size: 1.2em;
                        color: #333366;
                    }
        
                    p {
                        font-family: Verdana, Arial, Helvetica, sans-serif;
                        font-size: 1em;
                        color: rgb(29, 24, 24);
                    }
        
                    .button {
                        width: 280px;
                        height: 60px;
                        background-color: darkblue;
                        color: white;
                        font-size: 16px;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        letter-spacing: 1.5px;
                        font-weight: 800;
                        border: 2px solid white;
                        border-radius: 30px;
                    }
                </style>
            </head>
            """,
            f"""
            <body>
                <div class="main__block">
                    {message}
                    <div><a href="http://pddgoodbot.ru"><button class="button">Открыть сайт</button></a></div>
                </div>
            </body>
            """]
    html_message = ''.join(html)
    return html_message

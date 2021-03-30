var telegram_id = $('script[src*="pay_script.js"]').data('telegram_id');
var secret_key = $('script[src*="pay_script.js"]').data('secret_key');

var price = $('script[src*="pay_script.js"]').data('price_on_page');
var priceInt = Number(price)

var user_language = $('script[src*="pay_script.js"]').data('language_on_page');
if (user_language === 'KZ') {
    lang = 'kk-KZ';
    description_message = 'Telegram мессенджері негізінде білім беру платформасына кіру ақысы';
} else {
    var lang = 'ru-RU';
    var description_message = 'Плата за доступ к образовательной платформе на базе мессенджера Telegram';
};

var user_country = $('script[src*="pay_script.js"]').data('country_on_page');
if (user_country === 'KZ') {
    user_currency = 'KZT';
} else {
    user_currency = 'RUB';
};

let url = `/accept?telegram_id=${telegram_id}&secret_key=${secret_key}`;

this.pay = function () {
    var widget = new cp.CloudPayments({ language: lang });
    widget.pay('charge', // или 'auth' - двухстадийная, возврат в течении 7 дней
        { //options
            publicId: 'pk_9754c753b1482165aa85d1e17a1f3', //id из личного кабинета
            description: description_message, //назначение
            amount: priceInt, //сумма
            currency: user_currency, //валюта
            invoiceId: '', //номер заказа  (необязательно)
            accountId: '', //идентификатор плательщика (необязательно)
            skin: "modern", //дизайн виджета (необязательно)
            data: {
                myProp: 'myProp value'
            }
        },
        {
            onSuccess: function (options) { // success
                //действие при успешной оплате
                var zap = new XMLHttpRequest();
                zap.open("GET", url, true);
                zap.onload = function () { console.log(zap.responseText); }
                zap.send();
                document.location.href = `/pay_registered/${user_language}`;
            },

            onFail: function (reason, options) { // fail
                //действие при неуспешной оплате
            },

            onComplete: function (paymentResult, options) { //Вызывается как только виджет получает от api.cloudpayments
                // ответ с результатом транзакции. Положительный или отрицательный - неважно
                //например вызов вашей аналитики Facebook Pixel
            }
        }
    )
};

$('#pay_button_on').click(pay);
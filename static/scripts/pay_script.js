var price = $('script[src*="pay_script.js"]').data('price_on_page');
var priceInt = Number(price)

var language = $('script[src*="pay_script.js"]').data('language_on_page');
var lang = 'ru-RU';
var description_message = 'Плата за доступ к образовательной платформе на базе мессенджера Telegram';

if (language === 'KZ') {
    lang = 'kk-KZ';
    description_message = 'Telegram мессенджері негізінде білім беру платформасына кіру ақысы';
};


this.pay = function () {
 var widget = new cp.CloudPayments({language: lang});
    widget.pay('charge', // или 'auth' - двухстадийная, возврат в течении 7 дней
        { //options
            publicId: 'test_api_00000000000000000000001', //id из личного кабинета
            description: description_message, //назначение
            amount: priceInt, //сумма
            currency: 'KZT', //валюта
            invoiceId: '', //номер заказа  (необязательно)
            accountId: 'user@example.com', //идентификатор плательщика (необязательно)
            skin: "modern", //дизайн виджета (необязательно)
            data: {
                myProp: 'myProp value'
            }
        },
        {
            onSuccess: function (options) { // success
                //действие при успешной оплате
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


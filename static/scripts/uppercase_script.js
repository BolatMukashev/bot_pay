var loader__block = document.getElementById("loader__block");
var secret_key = document.getElementById("secret_key");
var promo_code = document.getElementById("promo_code");

loader__block.style.display = 'none';

// показать картинку загрузки при нажатии на кнопку, если поля promo_code и secret_key не пустые
button.onclick = function() {
    if (secret_key.value && promo_code.value) {
        loader__block.style.display = 'flex';
    }
}

// uppercase всех символов в поле promo_code при потере фокуса
$(function() {
    $('promo_code').focusout(function() {
        this.value = this.value.toLocaleUpperCase();
    });
});

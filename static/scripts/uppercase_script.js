$(function() {
    $('input').focusout(function() {
        // Uppercase-ize contents
        this.value = this.value.toLocaleUpperCase();
    });
});
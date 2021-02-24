var windowWidth = document.documentElement.clientWidth;

var title2 = document.getElementById("title2");
var title3 = document.getElementById("title3");
var title4 = document.getElementById("title4");
var title5 = document.getElementById("title5");
var text2 = document.getElementById("text2");
var text3 = document.getElementById("text3");
var text4 = document.getElementById("text4");
var text5 = document.getElementById("text5");
var macbook = document.getElementById("macbook");
var ipad = document.getElementById("ipad");
var instructor = document.getElementById("instructor");
var student = document.getElementById("student");
var telegram500 = document.getElementById("telegram500");
var telegram_chat = document.getElementById("telegram_chat");
var win = document.getElementById("win");
var button = document.getElementById("button");

if (windowWidth > 1024){
    macbook.style.visibility = 'hidden';
    ipad.style.visibility = 'hidden';
    instructor.style.visibility = 'hidden';
    student.style.visibility = 'hidden';
    telegram500.style.visibility = 'hidden';
    telegram_chat.style.visibility = 'hidden';
    win.style.visibility = 'hidden';

    $(function() {
        $(window).on('load resize scroll', function() {
        addClassToElementInViewport(macbook, 'animate__backInRight');
        addClassToElementInViewport(ipad, 'animate__backInLeft');
        addClassToElementInViewport(instructor, 'animate__backInLeft');
        addClassToElementInViewport(student, 'animate__backInRight');
        addClassToElementInViewport(telegram500, 'animate__backInLeft');
        addClassToElementInViewport(telegram_chat, 'animate__backInRight');
        addClassToElementInViewport(win, 'animate__fadeInUp');
        // 👏 repeat as needed ...
        });

        function addClassToElementInViewport(element, newClass) {
        if (inViewport(element)) {
            element.style.visibility = 'visible';
            element.classList.add('animate__animated');
            element.classList.add(newClass);
            }
        }

        function inViewport(element) {
        if (typeof jQuery === "function" && element instanceof jQuery) {
            element = element[0];
        }

        var elementBounds = element.getBoundingClientRect();
        return (
            elementBounds.top >= 0 &&
            elementBounds.left >= 0 &&
            elementBounds.bottom <= $(window).height() &&
            elementBounds.right <= $(window).width()
            );
        }
    });
}


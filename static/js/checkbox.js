(function () {
    'use strict';
    var cn = 'CheckBoxes', set = {}, cook = cookies(cn) || {};
    cookies.expires = 10 * 24 * 3600;

    function saveChecked() {
        cook[this.id] = this.checked;
        set[cn] = cook;

    // Записываем в кукис текущее значение checked
        cookies(set);
    };

    document.querySelectorAll('input[type=checkbox]').forEach(function(i) {
        i.onchange = saveChecked;
    // Устанавливаем значение из кукиса
        i.checked = !!cook[i.id];
    })

    })
    ();

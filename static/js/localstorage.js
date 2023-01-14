var form121 = document.getElementById('form12');
var formFields = form121.elements;
console.log(formFields);

function changeHandler() {
    if (this.type === 'checkbox') {
        localStorage.setItem(this.id, this.checked);
        console.log(this.id, this.checked);

    }
}

function checkStorage() {
    for (let i = 0; i < formFields.length; i++) {
        if (formFields[i].type === 'checkbox') {
            formFields[i].checked = localStorage.getItem(formFields[i].id);

        }
    }
    attachEvents()
}

function attachEvents() {
    for (let i = 0; i < formFields.length; i++) {
        formFields[i].addEventListener('change', changeHandler);
    }
}

window.onbeforeunload = function (e) {

    window.localStorage.unloadTime = JSON.stringify(new Date());

};

window.onload = function () {

    let loadTime = new Date();
    let unloadTime = new Date(JSON.parse(window.localStorage.unloadTime));
    let refreshTime = loadTime.getTime() - unloadTime.getTime();

    if (refreshTime > 100)//3000 milliseconds
    {
        window.localStorage.clear();
    }

};

checkStorage()
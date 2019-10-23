const App = {
    startUp: (sessionLimit, timeLogged, redirectUrl) => {
        let loggedSince = timeLogged;
        let minutesLimit = sessionLimit;

        let counterEl = document.querySelector('#time-counter');
        if (loggedSince > 0 && counterEl != null) {
            setInterval(() => {
                let now = new Date().getTime() / 1000;
                let diffSeconds = Math.floor(now - loggedSince);
                let diffMinutes = Math.floor(diffSeconds / 60);
                diffSeconds = diffSeconds % 60;
                let diffHours = Math.floor(diffMinutes / 60);
                diffMinutes = diffMinutes % 60;
                let diffDays = Math.floor(diffHours / 24);
                diffHours = diffHours % 24;
                let clock = "";
                clock += (diffHours > 9) ? diffHours : "0" + diffHours;
                clock += ":";
                clock += (diffMinutes > 9) ? diffMinutes : "0" + diffMinutes;
                clock += ":";
                clock += (diffSeconds > 9) ? diffSeconds : "0" + diffSeconds;
                counterEl.innerText = clock;
                if (diffMinutes >= minutesLimit) {
                    window.location = redirectUrl;
                }
            }, 1000);
        }
        App.addFormListener();
        App.addDeleteListener();
    },
    addFormListener: () => {
        let form = document.querySelector("form");
        if (form != null) {
            form.addEventListener("submit", (ev) => {
                ev.preventDefault();
                let method = form.getAttribute("method");
                let action = form.getAttribute("action");
                let formData = new FormData(form);
                fetch(action, {
                    method: method,
                    body: formData
                }).then((response) => {
                    App.responseHandler(response);
                })
            });
        }
    },
    addDeleteListener: () => {
        let del = document.querySelectorAll("[data-delete]");
        if (del.length > 0) {
            for (let i = 0; i < del.length; i++) {
                let d = del[i];
                d.addEventListener("click", (ev) => {
                    if (confirm("Tem certeza que dejesa remover?")) {
                        let url = d.getAttribute("data-delete");
                        fetch(url, {
                            method: 'delete'
                        }).then((response) => {
                            App.responseHandler(response);
                        });
                    }
                });
            }
        }
    },
    responseHandler: (response) => {
        if (response.status === 200 || response.status === 201) {
            response.json().then((jsonResponse) => App.onFormSuccess(jsonResponse));
        } else if (response.status === 401) {
            App.onNotAuth();
        } else if (response.status === 403) {
            App.onForbidden();
        } else if (response.status === 500) {
            App.onServerError();
        } else {
            response.json().then((jsonResponse) => App.onFormError(jsonResponse));
        }
    },
    onFormError: (response) => {
        alert(response.message);
    },
    onNotAuth: () => {
        alert('não logado');
    },
    onForbidden: () => {
        alert('não autorizado');
    },
    onServerError: () => {
        alert('erro no servidor, tente mais tarde');
    },
    onFormSuccess: (response) => {
        console.log(response);
        alert(response.message);
        if (response.redirect && response.redirect.length > 0) {
            setTimeout(() => {
                window.location.href = response.redirect;
            },300);
        }
    },
};

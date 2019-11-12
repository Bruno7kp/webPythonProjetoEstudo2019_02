const App = {
    startUp: (minutesLimit, loggedSince, redirectUrl) => {
        App.addSessionCounter(minutesLimit, loggedSince, redirectUrl);
        App.addFormListener();
        App.addDeleteListener();
        App.addClientSelectorListener();
        App.addProductListener();
        App.addMasks();
    },
    addMasks: () => {
        let money = document.querySelectorAll('.mask-money');
        for (let i = 0; i < money.length; i++) {
            IMask(money[i], {
                 mask: Number,
                  scale: 2,
                  signed: false,
                  thousandsSeparator: '',
                  padFractionalZeros: false,
                  normalizeZeros: true,
                  radix: ',',
                  mapToRadix: ['.'],
                  min: 0,
                  max: 9999999999.99
            });
        }
        let cep = document.querySelectorAll('.mask-cep');
        for (let i = 0; i < cep.length; i++) {
            IMask(cep[i], {
                 mask: '00000-000',
            });
        }

        let phone = document.querySelectorAll('.mask-phone');
        for (let i = 0; i < phone.length; i++) {
            IMask(phone[i], {
                 mask: '(00) 00000-0000',
            });
        }

    },
    addSessionCounter: (minutesLimit, loggedSince, redirectUrl) => {
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
    addClientSelectorListener: () => {
        let select = document.querySelector("#cliente");
        if (select != null) {
            select.addEventListener("change", () => {
                if (parseInt(select.value) > 0) {
                    App.searchClientData(select.value);
                } else {
                    App.cleanClientData();
                }
            });
            // Ao carregar página
            if (parseInt(select.value) > 0) {
                App.searchClientData(select.value);
            }
        }
    },
    searchClientData: (id) => {
        fetch("/cliente/busca/" +  id).then(response => {
            if (response.status === 200) {
                response.json().then(jsonResponse => {
                    let cliente = jsonResponse.data[0];
                    App.fillClientData(cliente);
                });
            } else {
               App.cleanClientData();
            }
        });
    },
    fillClientData: (cliente) => {
        document.querySelector("#code").value = cliente.id_cliente;
        document.querySelector("#tel").value = cliente.telefone;
        document.querySelector("#endereco").value = cliente.endereco;
        document.querySelector("#numero").value = cliente.numero;
        document.querySelector("#bairro").value = cliente.bairro;
        document.querySelector("#cep").value = cliente.cep;
        document.querySelector("#cidade").value = cliente.cidade;
    },
    cleanClientData: () => {
        document.querySelector("#code").value = "";
        document.querySelector("#tel").value = "";
        document.querySelector("#endereco").value = "";
        document.querySelector("#numero").value = "";
        document.querySelector("#bairro").value = "";
        document.querySelector("#cep").value = "";
        document.querySelector("#cidade").value = "";
    },
    addProductListener: () => {
        let add = document.querySelector("#addproduto");
        let template = document.querySelector(".product-row");
        if (add != null) {
            add.addEventListener("click", () => {
                let temp = document.createElement('div');
                temp.innerHTML = template.outerHTML;
                let newRow = temp.firstChild;
                newRow.querySelector("[name='produto[][id_produto]']").value = "";
                newRow.querySelector("[name='produto[][quantidade]']").value = "";
                newRow.querySelector("[name='produto[][total]']").value = "";
                newRow.querySelector("[name='produto[][observacao]']").value = "";
                App.cleanProductData(newRow);
                add.parentElement.parentElement.before(newRow);
                App.addProductRowListener(newRow);
            });
        }
        // Ao carregar página
        let produtos = document.querySelectorAll(".product-row");
        for (let i = 0; i < produtos.length; i++) {
            App.addProductRowListener(produtos[i]);
        }
        App.updateOverallTotal();
    },
    addProductRowListener: (row) => {
        let select = row.querySelector("select");
        let quantity = row.querySelector("[name='produto[][quantidade]']");
        let remove = row.querySelector(".btn-remove");

        select.addEventListener("change", () => {
            if (parseInt(select.value) > 0) {
                App.searchProductData(row, select.value);
            } else {
                App.cleanProductData(row);
                App.updateTotal(row);
            }
        });

        quantity.addEventListener("change", () => {
            App.updateTotal(row);
        });

        remove.addEventListener("click", () => {
            if (confirm("Tem certeza que deseja remover este produto?")) {
                row.parentElement.removeChild(row);
            }
        });
    },
    searchProductData: (row, id) => {
          fetch("/produto/busca/" + id).then(response => {
           if (response.status === 200) {
               response.json().then(jsonResponse => {
                   let produto = jsonResponse.data[0];
                   App.fillProductData(row, produto);
                   App.updateTotal(row);
               });
           } else {
               App.cleanProductData(row);
               App.updateTotal(row);
           }
        });
    },
    fillProductData: (row, product) => {
        row.querySelector("[name='produto[][preco]']").value = product.valor.toString().replace(".", ",");
    },
    updateTotal: (row) => {
        let price = row.querySelector("[name='produto[][preco]']").value;
        let quantity = row.querySelector("[name='produto[][quantidade]']").value;
        let priceValue = 0;
        let quantityValue = 0;
        if (price.length > 0) {
            priceValue = parseFloat(price.replace(",", "."));
        }
        if (quantity.length > 0) {
            quantityValue = parseInt(quantity)
        }
        let total = (priceValue * quantityValue).toFixed(2);
        row.querySelector("[name='produto[][total]']").value = total.toString().replace(".", ",");
        App.updateOverallTotal();
    },
    updateOverallTotal: () => {
        let totalEl = document.querySelector("#total");
        let totals = document.querySelectorAll("[name='produto[][total]']");
        let sum = 0;
        for (let i = 0; i < totals.length; i++) {
            sum = sum + parseFloat(totals[i].value.replace(",", "."));
        }
        if (totalEl != null) {
            totalEl.innerHTML = "R$ " + sum.toFixed(2).toString().replace(".", ",");
        }
     },
    cleanProductData: (row) => {
        row.querySelector("[name='produto[][preco]']").value = ""
    },
    responseHandler: (response) => {
        if (response.status === 200 || response.status === 201) {
            response.json().then((jsonResponse) => App.onFormSuccess(jsonResponse));
        } else if (response.status === 401) {
            App.onNotAuth();
        } else if (response.status === 403) {
            response.json().then((jsonResponse) => App.onForbidden(jsonResponse));
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
    onForbidden: (response) => {
        alert(response.message);
    },
    onServerError: () => {
        alert('erro no servidor, tente mais tarde');
    },
    onFormSuccess: (response) => {
        alert(response.message);
        if (response.redirect && response.redirect.length > 0) {
            setTimeout(() => {
                window.location.href = response.redirect;
            },300);
        }
    },
};

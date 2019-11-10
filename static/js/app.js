const App = {
    startUp: (minutesLimit, loggedSince, redirectUrl) => {
        App.addSessionCounter(minutesLimit, loggedSince, redirectUrl);
        App.addFormListener();
        App.addDeleteListener();
        App.addClientSelectorListener();
        App.addProductListener();
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
                    fetch("/cliente/busca/" + select.value).then(response => {
                       if (response.status === 200) {
                           response.json().then(jsonResponse => {
                               let cliente = jsonResponse.data[0];
                               App.fillClientData(cliente);
                           });
                       } else {
                           App.cleanClientData();
                       }
                    });
                } else {
                    App.cleanClientData();
                }
            });
        }
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
        let template = `
            <div class="product-row">
                <hr>
                <div class="row">
                    <div class="col col-6">
                        <div class="form-group">
                            <label>Produto</label>
                            <select name="id_produto[]" id="id_produto[]" class="form-control">
                                <option value="0">Selecione o produto</option>
                                {% for produto in produtos %}
                                <option value="{{ produto.id_produto }}">{{ produto.descricao }}</option>
                                {% endfor %}
                            </select>
                        </div>
                    </div>
                    <div class="col col-3">
                        <div class="form-group">
                            <label>Preço</label>
                            <input pattern="\\d{1,8}(?:[,]\\d{1,2})?" name="preco[]" type="text" class="form-control" disabled="disabled">
                        </div>
                    </div>
                    <div class="col col-3">
                        <div class="form-group">
                            <label>&nbsp;</label>
                            <button type="button" class="btn btn-danger btn-sm d-block mt-1 btn-remove"><i class="fa fa-trash"></i> REMOVER PRODUTO</button>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col col-2">
                        <div class="form-group">
                            <label for="quantidade">Quantidade</label>
                            <input name="quantidade[]" type="number" min="1" class="form-control">
                        </div>
                    </div>
                    <div class="col col-3">
                        <div class="form-group">
                            <label for="total">Total R$</label>
                            <input pattern="\\d{1,8}(?:[,]\\d{1,2})?" name="total[]" type="text" class="form-control">
                        </div>
                    </div>
                    <div class="col col-4">
                        <div class="form-group">
                            <label>Observações</label>
                            <textarea name="observacoes[]" rows="1" class="form-control"></textarea>
                        </div>
                    </div>
                </div>
            </div>`;
        App.addProductRowListener(template);
        add.addEventListener("click", () => {
            let temp = document.createElement('div');
            temp.innerHTML = template;
            let newRow = temp.firstChild;
            add.parentElement.parentElement.before(newRow);
            App.addProductRowListener(newRow);
        });
    },
    addProductRowListener: (row) => {
        let select = row.querySelector("select");
        let quantity = row.querySelector("[name='quantidade[]']");
        let remove = row.querySelector(".btn-remove");

        select.addEventListener("change", () => {
            if (parseInt(select.value) > 0) {
                    fetch("/produto/busca/" + select.value).then(response => {
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
    fillProductData: (row, product) => {
        row.querySelector("[name='preco[]']").value = product.valor.toString().replace(".", ",");
    },
    updateTotal: (row) => {
        let price = row.querySelector("[name='preco[]']").value;
        let quantity = row.querySelector("[name='quantidade[]']").value;
        let priceValue = 0;
        let quantityValue = 0;
        if (price.length > 0) {
            priceValue = parseFloat(price.replace(",", "."));
        }
        if (quantity.length > 0) {
            quantityValue = parseInt(quantity)
        }
        let total = (priceValue * quantityValue).toFixed(2);
        row.querySelector("[name='total[]']").value = total.toString().replace(".", ",");
    },
    cleanProductData: (row) => {
        row.querySelector("[name='preco[]']").value = ""
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
        alert(response.message);
        if (response.redirect && response.redirect.length > 0) {
            setTimeout(() => {
                window.location.href = response.redirect;
            },300);
        }
    },
};

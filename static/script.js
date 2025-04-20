let tokenAtual = null;
let mensagensAntigas = new Set();

function gerarTudo() {
    fetch("/gerar", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("usuario").value = data.usuario;
            document.getElementById("senha").value = data.senha;
            document.getElementById("email").value = data.email;
            tokenAtual = data.token;
            mensagensAntigas.clear();
            iniciarMonitoramento();
        });
}

function iniciarMonitoramento() {
    setInterval(() => {
        if (!tokenAtual) return;
        fetch(`/mensagens/${tokenAtual}`)
            .then(res => res.json())
            .then(data => {
                if (data.expirado) {
                    document.getElementById("mensagens").innerText = "☠️ A caixa expirou.";
                    return;
                }
                const container = document.getElementById("mensagens");
                container.innerHTML = "";
                data.mensagens.forEach(msg => {
                    const div = document.createElement("div");
                    div.className = "notification is-light";
                    div.innerHTML = `<strong>De:</strong> ${msg.de}<br>
                                     <strong>Assunto:</strong> ${msg.assunto}<br>
                                     <pre>${msg.corpo}</pre>`;
                    container.appendChild(div);
                });
            });
    }, 10000);
}

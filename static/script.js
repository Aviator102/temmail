let tokenAtual = null;

function gerarTudo() {
  fetch("/api/gerar") // ← agora é GET, compatível com Vercel
    .then(res => res.json())
    .then(data => {
      if (data.erro) {
        alert("Erro ao gerar email: " + data.erro);
        return;
      }

      document.getElementById("usuario").value = data.usuario;
      document.getElementById("senha").value = data.senha;
      document.getElementById("email").value = data.email;
      tokenAtual = data.token;

      document.getElementById("mensagens").innerHTML = "<em>Monitorando mensagens...</em>";
    })
    .catch(err => alert("Erro ao chamar API: " + err));
}

setInterval(() => {
  if (!tokenAtual) return;

  fetch(`/api/mensagens?token=${tokenAtual}`)
    .then(res => res.json())
    .then(data => {
      const box = document.getElementById("mensagens");
      box.innerHTML = "";

      if (data.expirado) {
        box.innerHTML = "<strong>☠️ A caixa expirou.</strong>";
        return;
      }

      if (data.mensagens.length === 0) {
        box.innerHTML = "<em>📭 Nenhuma mensagem ainda.</em>";
        return;
      }

      data.mensagens.forEach(msg => {
        const div = document.createElement("div");
        div.className = "notification is-light";
        div.innerHTML = `
          <strong>De:</strong> ${msg.de}<br>
          <strong>Assunto:</strong> ${msg.assunto}<br>
          <pre>${msg.corpo}</pre>
        `;
        box.appendChild(div);
      });
    });
}, 10000);

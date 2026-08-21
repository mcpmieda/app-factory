import http from "node:http";
const html = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Página controlada Focus Lens</title><style>body{font-family:system-ui;max-width:760px;margin:60px auto;padding:20px;background:#f4f1e9}article{padding:20px;margin:16px 0;background:white;border-radius:14px}</style></head><body><h1>Prioridades da oficina</h1><p>Use a extensão para destacar os itens acionáveis.</p><article data-focus-item><h2>Revisar pauta</h2><p>Validar os três tópicos antes da reunião.</p></article><article><h2>Informativo</h2><p>Este bloco não é acionável.</p></article><article data-focus-item><h2>Enviar convite</h2><p>Compartilhar o horário com participantes.</p></article></body></html>`;
http
  .createServer((request, response) => {
    response.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    response.end(html);
  })
  .listen(4174, "127.0.0.1", () => console.log("fixture ready"));

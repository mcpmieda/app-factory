# Inspection Environment

## Objetivo

Dar ao usuário um endereço simples e estável para abrir qualquer sistema criado pela App Factory, escondendo detalhes de GitHub Pages, Vercel, previews e infraestrutura.

## Padrão de projeto

Software real novo criado pela Factory deve ir, por padrão, para:

```text
projects/<slug-do-projeto>/
```

Exemplo:

```text
projects/bancodenotas/
```

As demais pastas têm papéis diferentes:

- `examples/`: pilotos e exemplos da própria Factory;
- `audits/`: projetos/evidências de auditoria;
- `starters/`: moldes reutilizáveis;
- `projects/`: sistemas reais do usuário.

## URL canônica

O endereço apresentado ao usuário deve preferir:

```text
https://escolaieda.com/<slug>
```

Exemplos:

```text
https://escolaieda.com/bancodenotas
https://escolaieda.com/patrimonio
https://escolaieda.com/emprestimos
```

O slug público deve ser curto, minúsculo, sem acentos, espaços ou pontuação quando isso não causar ambiguidade. Exemplo: `Banco de Notas` → `bancodenotas`.

## Hospedagem por trás do link

A URL pública não deve obrigar uma única tecnologia de hospedagem.

### Conteúdo estático

Pode ser servido diretamente pelo site escolar, mantendo o caminho canônico sob `escolaieda.com`.

### Aplicação com runtime/backend

Pode usar Vercel ou outro backend adequado. O domínio principal deve fazer rewrite/proxy de `/<slug>` para o backend, preservando a URL visível no navegador.

Exemplo conceitual:

```text
escolaieda.com/bancodenotas
        ↓ rewrite/proxy
bancodenotas.vercel.app
```

O usuário continua vendo `escolaieda.com/bancodenotas`.

## Preview

Branches/PRs podem usar URLs temporárias de preview para testes técnicos. Essas URLs não são o endereço principal entregue ao usuário.

Fluxo desejado:

```text
alteração
→ preview temporário
→ testes/CI
→ aprovação/merge
→ endereço canônico existente atualizado
```

## Infraestrutura atual

O `escolaieda.com` atual usa conteúdo estático no repositório `mcpmieda/escolaieda` com `CNAME`. Isso permite caminhos estáticos diretamente, mas não fornece sozinho reverse proxy para aplicações hospedadas em outro backend.

Para preservar `escolaieda.com/<slug>` também em aplicações complexas, a implantação futura deve adicionar uma camada de roteamento que suporte rewrites/proxy. Vercel é o caminho preferido por simplicidade e por já suportar rewrites para destinos externos mantendo a URL original.

Essa mudança de domínio/roteamento é uma implantação controlada e não deve ser feita implicitamente durante a criação de um projeto comum.

## Regra de experiência

O usuário não deve precisar escolher hospedagem, configurar link de preview ou memorizar URL técnica. A Factory decide o backend, automatiza a publicação quando a infraestrutura estiver disponível e entrega principalmente o endereço canônico simples.

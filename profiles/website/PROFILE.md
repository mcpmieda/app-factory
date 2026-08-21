# Website Profile

Status: `validated`

## Quando usar

Sites institucionais, editoriais, documentação e presença pública em que conteúdo, navegação, SEO e desempenho predominam sobre estado transacional.

## Defaults comprovados

- saída estática/content-first quando o conteúdo é igual para visitantes;
- HTML semântico, metadata/canonical, foco visível, skip link e responsividade;
- framework cliente ausente até existir interação que o justifique;
- teste do build de produção em desktop, mobile e teclado.

Astro é uma opção comprovada, não obrigatória. Escolher o gerador estático/CMS conforme conteúdo e publicação.

## Condicionais e anti-defaults

Ativar ilhas, CMS, busca ou formulários com backend somente por requisito. Não instalar auth, banco, estado global, Next.js, shell administrativo ou design system por reflexo.

## Living UI e gates

Motion Profile `ambient` cabe em hero/superfícies amplas; leitura longa atenua para `subtle`. Exigir reduced motion, sem overflow, CTA/rotas reais, build, audit e browser sem erros. Conteúdo real requer aprovação, privacidade e ownership editorial; publicação deve permitir rollback.

Evidence: `examples/website-pilot/` and `research/V0.9_UNIVERSAL_VALIDATION.md`.

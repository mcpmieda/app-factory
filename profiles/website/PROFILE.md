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

## Independent Verification

Site estático simples normalmente permanece `baseline` ou `independent`; não instalar mutation testing/DAST apenas por cerimônia.

Quando `core/INDEPENDENT_VERIFICATION.md` elevar a matriz:

- Trivy/Semgrep podem verificar dependências/configuração quando aplicáveis;
- axe-core + Playwright é especialmente útil para páginas/estados relevantes;
- Lighthouse CI pode se tornar gate após existir baseline estável de performance/qualidade;
- OWASP ZAP entra somente se houver superfície dinâmica/backend que justifique DAST;
- GitHub CI/runner equivalente é preferido para execução reproduzível.

A camada permanece `free-only` e não substitui aprovação de conteúdo, UX ou revisão semântica.

## Living UI e gates

Motion Profile `ambient` cabe em hero/superfícies amplas; leitura longa atenua para `subtle`. Exigir reduced motion, sem overflow, CTA/rotas reais, build, audit e browser sem erros. Conteúdo real requer aprovação, privacidade e ownership editorial; publicação deve permitir rollback.

Checks independentes `required` selecionados pela Factory também precisam passar; checks não aplicáveis permanecem fora do projeto.

Evidence: `examples/website-pilot/` and `research/V0.9_UNIVERSAL_VALIDATION.md`.

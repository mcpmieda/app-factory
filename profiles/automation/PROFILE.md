# Automation Profile

Status: `validated`

## Quando usar

Processos repetitivos de ingestão, normalização, regras e saída que possam ser executados por script, job ou integração recuperável.

## Defaults comprovados

- transformação pura separada de adapters de entrada/saída;
- validação global e erro parcial por registro;
- resultado determinístico e execução idempotente;
- `--dry-run` antes de escrita e substituição atômica local;
- logs claros sem dados sensíveis; testes unitários e de processo.

Python stdlib é uma opção comprovada para arquivos locais, não runtime universal.

## Condicionais e anti-defaults

SaaS, filas, scheduler, banco, SDK e credenciais entram somente pelo ambiente real. Não escolher Power Automate/Graph/Google/API externa antes do requisito; nunca tornar conector destrutivo por padrão.

Quando uma API externa, webhook, evento ou contrato entre sistemas for parte material da automação, aplicar `core/API_ENGINEERING.md`/`api-engineering` proporcionalmente. Uma chamada pontual controlada pode ficar `lightweight`; integrações compartilhadas/produção podem exigir `contract`/`governed`.

Não criar OpenAPI para script que apenas consome uma API externa sem expor contrato próprio. Nesse caso, a Factory deve registrar o contrato/dependência do provedor, scopes, timeout/retry/rate limit, validação de resposta, idempotência/checkpoint e recovery necessários.

## Independent Verification

Use `core/INDEPENDENT_VERIFICATION.md` proporcionalmente:

- automação local simples pode permanecer `baseline`;
- escrita em dados compartilhados, dependências externas, secrets/credenciais ou impacto institucional podem elevar para `independent`/`adversarial`;
- Trivy/Semgrep são candidatos naturais quando aplicáveis;
- mutmut pode verificar força dos testes Python em módulos críticos, de forma seletiva;
- Schemathesis entra somente quando existir contrato API compatível e API Engineering selecionar o gate;
- ZAP/axe/Lighthouse não são adicionados a automação sem superfície web.

A matriz permanece `free-only`; scanners não substituem dry-run, idempotência, testes de processo ou validação real do conector.

## Gates e recovery

Exigir format/lint/compile/test, dry-run sem escrita, repetição byte/semanticamente idêntica e falha sem corrupção. Conectores reais adicionam least privilege, timeout, retry limitado, checkpoint/idempotency key e rollback. Webhooks adicionam autenticidade, replay/duplicidade e idempotência quando aplicáveis. Contratos formais adicionam os gates de `core/API_ENGINEERING.md` sem substituir os testes de processo da automação.

Quando Independent Verification ficar acima de `baseline`, executar checks `required` em CI/runner equivalente, com secrets protegidos e dados fictícios quando possível. Ferramenta não executada não vira `pass`.

Living UI não se aplica a automação sem UI; logs são o feedback de estado.

Evidence: `examples/automation-pilot/` and `research/V0.9_UNIVERSAL_VALIDATION.md`.

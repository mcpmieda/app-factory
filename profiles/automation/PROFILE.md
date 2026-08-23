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

## Gates e recovery

Exigir format/lint/compile/test, dry-run sem escrita, repetição byte/semanticamente idêntica e falha sem corrupção. Conectores reais adicionam least privilege, timeout, retry limitado, checkpoint/idempotency key e rollback. Webhooks adicionam autenticidade, replay/duplicidade e idempotência quando aplicáveis. Contratos formais adicionam os gates de `core/API_ENGINEERING.md` sem substituir os testes de processo da automação.

Living UI não se aplica a automação sem UI; logs são o feedback de estado.

Evidence: `examples/automation-pilot/` and `research/V0.9_UNIVERSAL_VALIDATION.md`.

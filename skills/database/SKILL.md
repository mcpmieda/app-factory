---
name: database
description: Planeja e modifica dados, schemas e migrations com contratos explícitos, integridade, idempotência, backup/rollback proporcional e testes de comportamento.
---

# Database

## Projeto novo

- modele dados a partir das regras de negócio;
- defina chaves, unicidade e relações explicitamente;
- evite schema excessivamente abstrato antes de existir necessidade;
- use migrations versionadas.

## Mudança em sistema existente

1. confirme schema/versão atual;
2. avalie compatibilidade e volume de dados;
3. defina migration e recuperação;
4. valide em ambiente controlado quando possível;
5. aplique;
6. releia/inspecione resultado;
7. teste os fluxos afetados.

## Regras

- não alterar banco diretamente quando existe mecanismo de migration estabelecido;
- não copiar IDs específicos entre ambientes;
- operações administrativas devem ser idempotentes quando possível;
- dados críticos exigem estratégia explícita de backup/rollback proporcional ao risco.
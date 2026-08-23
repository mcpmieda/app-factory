# SEMANTICS

## Decisões de domínio deste field test

- **Hospedagem ≠ compartilhamento:** estar publicado no Vercel não transforma persistência local em banco compartilhado.
- **Matrícula é identidade de negócio local:** comparação ignora espaços laterais e diferença entre maiúsculas/minúsculas.
- **Migração preserva conhecimento:** campos que não existiam no v1 permanecem explicitamente desconhecidos; turno vira `not_informed`.
- **Status não remove histórico:** arquivar/transferir altera o status do mesmo registro. Exclusão é uma ação separada e confirmada.
- **Backup é substitutivo:** restauração de um backup válido substitui a coleção local inteira somente depois de confirmação.
- **CSV não é backup:** CSV serve para saída tabular; o JSON v2 é o contrato de restauração.

Essas decisões complementam `specs/semantic-assurance.json`; não duplicam schema Zod nem regras gerais da App Factory.

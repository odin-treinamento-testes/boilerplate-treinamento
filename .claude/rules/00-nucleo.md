# Regras — Base do Núcleo

> Regras gerais que valem para todo projeto do NDados. (Idealmente vêm do plugin core-plugin; mantidas aqui como fallback/base.)

- Antes de implementar, apresente o plano e aguarde aprovação explícita.
- Não altere arquivos fora do escopo da tarefa recebida.
- Toda decisão técnica relevante vira um arquivo em `context/<etapa>/` no padrão decision-record.
- Dados de cliente nunca saem para learnings/KB sem anonimização.
- Nunca commite segredo (token, credencial, .env).

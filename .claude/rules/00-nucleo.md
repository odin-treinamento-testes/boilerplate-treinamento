# Regras — Base do Núcleo

> Regras gerais que valem para todo projeto do NDados. (Idealmente vêm do plugin core-plugin; mantidas aqui como fallback/base.)

- Antes de implementar, apresente o plano e aguarde aprovação explícita.
- Não altere arquivos fora do escopo da tarefa recebida.
- Toda decisão técnica relevante vira um arquivo em `context/<etapa>/` no padrão decision-record.
- Todo arquivo novo em `context/` entra numa etapa que o membro indica (pergunte antes de gravar),
  com até 8KB; o `project-context.md` é a exceção. Detalhe em `context/README.md`.
- Dados de cliente nunca saem para learnings/KB sem anonimização.
- Nunca commite segredo (token, credencial, .env).

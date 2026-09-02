# Projeto Descontinuado / Consolidado: Este bot foi integrado à Central de Automações RPA. O desenvolvimento ativo continua por lá.

#  Hospital Diet Automation — Playwright & Gemini LLM

Automação inteligente de processos (RPA) com integração a LLM para extração, padronização e inserção automatizada de prescrições dietéticas em sistema hospitalar legado.

##  Problema de Negócio
A transcrição diária de relatórios impressos de nutrição para o sistema hospitalar era manual, lenta e suscetível a erros de digitação em dietas com restrições severas. O desafio envolvia lidar com dados não estruturados gerados via OCR móvel (Google Lens) com ruídos e quebras de linha.

##  Solução
* **Parsing com IA Generativa**: Utilização do `gemini-3.6-flash` com saída estruturada em JSON (`response_mime_type="application/json"`) para filtrar cabeçalhos, corrigir ruídos e padronizar nomenclaturas clínicas.
* **Automação Web com Playwright**: Script resiliente que autentica, navega pela árvore de menus do sistema interno e cadastra cada dieta preenchendo categorias, grupos e status ativo.

##  Tecnologias
* **Python 3.11+**
* **Google GenAI SDK** (`gemini-3.6-flash`)
* **Playwright** (Sync API)

## Fluxo da Aplicação
```text
Foto/Relatório ➔ Google Lens (OCR) ➔ Gemini LLM (Limpeza/JSON) ➔ Playwright (Cadastro Web)

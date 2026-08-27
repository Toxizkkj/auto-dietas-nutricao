# 🏥 Hospital Diet Automation — Playwright & Gemini LLM

Automação inteligente de processos (RPA) integrada a modelos de linguagem (LLMs) para extração, estruturação e cadastro automático de dietas hospitalares em sistemas legados.

---

## 📌 Contexto & Problema de Negócio
No setor de nutrição hospitalar, a transcrição de relatórios impressos/OCR para o sistema de gestão hospitalar consumia horas diárias de trabalho manual, gerando gargalos operacionais e risco de erro humano na alimentação de prescrições dietéticas críticas.

## 💡 Solução Desenvolvida
Pipeline automatizado ponta a ponta que:
1. **Ingere texto bruto via OCR** (Google Lens) contendo ruídos, quebras de linha e desformatação.
2. **Processa e Estrutura via IA Generativa**: Utiliza o modelo `gemini-3.6-flash` com saída forçada em JSON (`application/json`) para filtrar dados irrelevantes e padronizar as nomenclaturas.
3. **Executa RPA com Playwright**: Navega pelo sistema interno autenticado, preenche os formulários de cadastro e persiste os dados de forma assíncrona e resiliente.

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem**: Python 3.11+
* **Automação Web**: Playwright (Sync API)
* **IA & LLM**: Google GenAI SDK (`gemini-3.6-flash`)
* **Gestão de Ambiente**: Python Virtualenv / Dotenv

---

## ⚙️ Arquitetura do Fluxo

```text
[ Documento Físico / Foto ]
           │
           ▼
[ Google Lens / OCR Bruto ]
           │
           ▼
[ Gemini 3.6 Flash ] ──> (Limpeza, Deduplicação & JSON Estruturado)
           │
           ▼
[ Playwright Worker ] ──> (Login ➔ Navegação ➔ Preenchimento Form ➔ Persistência)

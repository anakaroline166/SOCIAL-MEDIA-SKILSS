---
name: notion-brief
description: >
  Cria um brief completo de conteúdo direto na Central de Conteúdo do Notion,
  a partir de uma intenção descrita em uma frase.
  Ativa quando a pessoa disser /notion-brief, quiser criar um conteúdo, pedir
  um card na Central de Conteúdo, ou descrever uma intenção de conteúdo.
---

# Skill — Notion Brief

Você vai transformar uma intenção em um brief completo, direto na Central de Conteúdo do Notion. Lê o DNA da marca, identifica o pilar, e cria o card com tudo pronto para produzir.

---

## PASSO 1 — Coletar a intenção

Se a pessoa ainda não informou a intenção do conteúdo:

> **Qual conteúdo você quer criar?**
>
> Descreva em uma frase — pode ser simples:
> *"quero falar sobre procrastinação"* ou *"quero um carrossel sobre os erros mais comuns de quem começa a usar IA"*.

Se a pessoa já informou a intenção na mesma mensagem que ativou a skill, pular essa pergunta e seguir direto para o Passo 2.

---

## PASSO 2 — Ler o DNA da Marca no Notion

Antes de criar qualquer coisa, usar o MCP do Notion para:
1. Buscar a página "DNA da Marca" no workspace
2. Ler o conteúdo completo: posicionamento, público, tom de voz, pilares, diferencial

**Se não encontrar a página DNA da Marca**, avisar:

> "Não encontrei a página DNA da Marca no seu Notion. Para criar um brief alinhado com a sua marca, você precisa ter o DNA preenchido. Quer que eu rode o `/notion-studio-builder` primeiro para criar o sistema completo?"

**Se encontrar**, continuar sem avisar — processar silenciosamente e seguir para o Passo 3.

---

## PASSO 3 — Identificar o pilar

Com base no DNA lido e na intenção informada, identificar automaticamente qual pilar de conteúdo melhor se encaixa. Usar o nome exato do pilar como aparece no DNA da Marca.

---

## PASSO 4 — Criar o card na Central de Conteúdo

Criar um novo registro na database "Central de Conteúdo" com os seguintes campos.

**Campos sempre preenchidos:**

| Campo | Instrução |
|-------|-----------|
| **Título** | Título direto com gancho embutido — máx. 10 palavras. Não usar "como fazer" genérico. |
| **Pilar** | O pilar identificado no Passo 3 |
| **Status** | `💡 Ideia` |
| **Formato** | Inferir com base na intenção. Se não especificado, sugerir o mais adequado. Opções: Reels, Carrossel, Post Estático, Story, Newsletter, Thread. |
| **Gancho** | 3 opções numeradas, estilos diferentes: (1) pergunta que provoca, (2) afirmação ousada ou contraintuitiva, (3) dado ou problema concreto |
| **Legenda** | Legenda completa e pronta para publicar, com tom de voz do DNA. Quebras de linha naturais. Até 8 linhas para feed. |
| **CTA** | Escolher a opção mais alinhada com o objetivo do conteúdo: `💾 Salva`, `🔁 Compartilha`, `💬 Comenta`, `🔗 Link na bio` ou `📩 DM` |

**Campos preenchidos conforme o formato:**

| Formato | Campo a preencher | O que gerar |
|---------|-------------------|-------------|
| **Reels** | `Roteiro / Copy` | Roteiro completo estruturado: gancho (0–3s) → desenvolvimento em 3 blocos (3–50s) → CTA (50–60s). Tom conforme DNA. |
| **Post Estático** | `Roteiro / Copy` | Texto completo do post (body copy): o que aparece no design ou na sobreposição de texto. Direto, impactante, máx. 15 palavras. |
| **Story** | `Roteiro / Copy` | Copy da sequência de stories: o que dizer em cada frame, de forma conversacional e com CTA no final. |
| **Carrossel** | `Copy dos Slides` | Copy slide a slide, numerada. Slide 1 = capa com gancho. Slides do meio = desenvolvimento. Último slide = CTA. Máx. 15 palavras por slide principal + texto de apoio opcional (máx. 30 palavras). |
| **Newsletter / Thread** | `Roteiro / Copy` | Texto completo estruturado: abertura, desenvolvimento, fechamento com CTA. Tom conforme DNA. |

---

## PASSO 5 — Confirmar criação

Após criar o card, enviar o resumo mostrando o que foi gerado:

> **✅ Card criado na Central de Conteúdo.**
>
> **[Título do conteúdo]**
> Pilar: [nome] | Formato: [formato] | Status: 💡 Ideia
>
> **3 opções de gancho:**
> 1. [Gancho 1]
> 2. [Gancho 2]
> 3. [Gancho 3]
>
> **[Se Reels] Roteiro:**
> [roteiro completo]
>
> **[Se Carrossel] Copy dos slides:**
> [copy slide a slide]
>
> **[Se Post/Story/Newsletter] Copy:**
> [copy do conteúdo]
>
> **Legenda pronta:**
> [legenda completa]
>
> **CTA:** [opção escolhida]
>
> Quer ajustar algum campo, mudar o formato, ou criar outro conteúdo?

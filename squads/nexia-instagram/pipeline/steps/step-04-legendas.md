---
execution: subagent
agent: redatora
format: instagram-feed
inputFile: squads/nexia-instagram/output/calendario-semanal.md
outputFile: squads/nexia-instagram/output/legendas.md
model_tier: powerful
---

# Step 04: Legendas e textos

## Context Loading

Load these files before executing:
- `squads/nexia-instagram/output/calendario-semanal.md` — calendário aprovado pela Karolzinha
- `_opensquad/_memory/company.md` — perfil, dados confirmados e tom de voz da marca
- `squads/nexia-instagram/pipeline/data/tone-of-voice.md` — os 6 tons; usar o tom definido no calendário
- `squads/nexia-instagram/pipeline/data/quality-criteria.md` — critérios e bloqueios automáticos
- `squads/nexia-instagram/pipeline/data/output-examples.md` — referência de qualidade
- `squads/nexia-instagram/pipeline/data/anti-patterns.md` — erros a evitar
- `squads/nexia-instagram/output/revisao.md` — parecer da revisora, se esta for uma rodada de correção
- `_opensquad/core/best-practices/instagram-reels.md` — ler apenas se houver reels no calendário

## Instructions

### Process
1. Ler o calendário e, se existir, o parecer da revisora; aplicar todas as correções obrigatórias.
2. Para cada post, escrever o gancho a partir da cena da rotina indicada.
3. Carrossel: texto de cada slide (40 a 80 palavras), com título forte e texto de apoio. Estático: frase da arte (até 20 palavras). Reels: roteiro de 20 a 40 segundos com cena, solução e chamada.
4. Escrever a legenda completa, com chamada para ação única (sem preço) e de 5 a 10 hashtags.
5. Conferir: voz em "nós", português correto, pontuação completa, números só de `company.md`.
6. Marcar "a confirmar" em qualquer dado ou prazo sem fonte.
7. Salvar tudo no formato abaixo.

## Output Format

The output MUST follow this exact structure:
```
# Legendas e Textos — Semana de {data}

## Post {n} — {formato} — {público}
**Tom:** {tom}
**Gancho:** {frase}

### Texto da arte
{slides numerados, frase da arte ou roteiro por cena}

### Legenda
{legenda completa}

### Hashtags
{hashtags}

### A confirmar
{itens ou "nenhum"}
```

## Output Example

```
# Legendas e Textos — Semana de 13/10/2026

## Post 3 — Estático — Pessoa física/família
**Tom:** Acolhedor
**Gancho:** Um plano. Quatro pessoas cuidadas.

### Texto da arte
Um plano. Quatro pessoas cuidadas.

### Legenda
Um plano. Quatro pessoas cuidadas.

Titular e até três dependentes com telemedicina 24 horas, psicologia, nutrição e mais de 12 especialidades médicas.

Cuidado para a família inteira, no mesmo plano e no horário que couber na rotina.

Conheça o plano individual e familiar. Link na bio.

### Hashtags
#telemedicina #saudedafamilia #planodesaude #cuidado #nexiasaude

### A confirmar
nenhum

## Post 2 — Reels — Empresário/gestor
**Tom:** Narrativo
**Gancho:** Terça, 9h. A cadeira vazia pela terceira vez no mês.

### Texto da arte
Cena 1 (0-5s): gestor olha a cadeira vazia. Tela: "Terça, 9h. Terceira falta do mês."
Cena 2 (5-15s): mensagem do colaborador. Tela: "Uma consulta, uma manhã perdida."
Cena 3 (15-25s): consulta por vídeo na mesa. Tela: "Com telemedicina, são minutos."
Cena 4 (25-30s): logo. Tela: "Nexia Saúde. Menos espera. Mais saúde."

### Legenda
A ausência não é descuido. É tempo que o atendimento tradicional toma do seu time. Fale com nosso time e conheça o plano para a sua empresa.

### Hashtags
#telemedicina #gestaodepessoas #saudecorporativa

### A confirmar
nenhum
```

## Veto Conditions

Reject and redo if ANY of these are true:
1. Há "eu" na voz da marca, promessa de saúde, "o melhor", "garantido" ou preço.
2. Algum post tem dois públicos, dois chamados para ação ou erro de português visível.
3. Há número ou prazo sem estar em `company.md` e sem constar em "A confirmar".

## Quality Criteria

- [ ] Todos os 4 posts do calendário têm texto, legenda e hashtags.
- [ ] O tom segue o definido no calendário.
- [ ] Cada post abre com cena ou dado.
- [ ] Limites de formato respeitados.
- [ ] Pontuação completa em todos os fechamentos.

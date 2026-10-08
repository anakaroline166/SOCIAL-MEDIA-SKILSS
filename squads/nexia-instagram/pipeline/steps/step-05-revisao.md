---
execution: subagent
agent: revisora
inputFile: squads/nexia-instagram/output/legendas.md
outputFile: squads/nexia-instagram/output/revisao.md
on_reject: step-04-legendas
model_tier: powerful
---

# Step 05: Revisão

## Context Loading

Load these files before executing:
- `squads/nexia-instagram/output/legendas.md` — textos escritos pela redatora
- `squads/nexia-instagram/pipeline/data/quality-criteria.md` — critérios, notas e bloqueios automáticos
- `squads/nexia-instagram/pipeline/data/anti-patterns.md` — erros comuns da marca
- `squads/nexia-instagram/pipeline/data/tone-of-voice.md` — tom e vocabulário
- `_opensquad/_memory/company.md` — fonte de todos os dados e do perfil
- `squads/nexia-instagram/output/calendario-semanal.md` — para conferir público, formato e tom planejados

## Instructions

### Process
1. Ler `legendas.md` inteiro antes de pontuar.
2. Para cada post, verificar os bloqueios automáticos: promessa de saúde, "melhor", preço, dado sem fonte, "eu", erro no título ou na chamada, dois públicos, NR-1 sem confirmação.
3. Pontuar os 10 critérios de 1 a 10, com justificativa de uma ou duas frases.
4. Para toda nota abaixo de 10, citar o trecho e dar a correção sugerida.
5. Calcular a média por post e conferir se há nota abaixo de 7.
6. Declarar o veredito por post e o veredito da semana.
7. Listar as pendências "a confirmar" para a Karolzinha, separadas das correções.

## Output Format

The output MUST follow this exact structure:
```
# Revisão — Semana de {data}

**Veredito da semana:** APROVADO | REPROVADO
**Ciclo de revisão:** {n} de 3

## Post {n} — {formato}
**Veredito:** APROVADO | REPROVADO | média {x}
| Critério | Nota | Justificativa |
|----------|------|---------------|

**Bloqueios:** {lista ou "nenhum"}
**Correções obrigatórias:**
1. Trecho: "..." → Correção sugerida: "..."
**Sugestões opcionais:** {lista ou "nenhuma"}

## Pendências para a Karolzinha
- {item}
```

## Output Example

```
# Revisão — Semana de 13/10/2026

**Veredito da semana:** REPROVADO
**Ciclo de revisão:** 1 de 3

## Post 2 — Reels
**Veredito:** REPROVADO | média 7,2
| Critério | Nota | Justificativa |
|----------|------|---------------|
| Público único | 9 | Fala só com o gestor, desde a cena inicial. |
| Português | 6 | Fechamento sem pontuação e com anglicismo. |
| Tom de voz | 7 | Voz de pessoa ("eu acredito") no lugar de "nós". |
| Precisão dos dados | 5 | "em até 7 dias" não está em company.md. |
| Chamada para ação | 9 | Única, sem preço. |

**Bloqueios:** dado numérico sem fonte.
**Correções obrigatórias:**
1. Trecho: "Nexia Saúde Transformamos horas perdidas em performance" → Correção sugerida: "Nexia Saúde. Transformamos horas perdidas em resultado."
2. Trecho: "eu acredito na Nexia" → Correção sugerida: "nós acreditamos".
3. Trecho: "em até 7 dias" → remover ou marcar "a confirmar".
**Sugestões opcionais:** trocar "time" por "equipe" na legenda.

## Post 3 — Estático
**Veredito:** APROVADO | média 8,9
**Bloqueios:** nenhum
**Correções obrigatórias:** nenhuma
**Sugestões opcionais:** nenhuma

## Pendências para a Karolzinha
- Confirmar texto e prazos da NR-1 usados no post 1.
```

## Veto Conditions

Reject and redo if ANY of these are true:
1. Algum critério ficou sem nota ou sem justificativa.
2. Alguma nota abaixo de 10 não traz o trecho e a correção sugerida.
3. Existe bloqueio automático e o veredito do post não é REPROVADO.

## Quality Criteria

- [ ] Os 4 posts foram revisados do início ao fim.
- [ ] O veredito da semana está na primeira linha do arquivo.
- [ ] Correções obrigatórias e sugestões opcionais estão separadas.
- [ ] As pendências para a Karolzinha estão listadas.
- [ ] O ciclo de revisão está registrado e não passa de 3.

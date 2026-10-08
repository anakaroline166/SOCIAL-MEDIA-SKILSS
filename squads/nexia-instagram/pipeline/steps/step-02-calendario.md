---
execution: subagent
agent: estrategista
inputFile: squads/nexia-instagram/output/foco-da-semana.md
outputFile: squads/nexia-instagram/output/calendario-semanal.md
model_tier: powerful
---

# Step 02: Calendário semanal

## Context Loading

Load these files before executing:
- `squads/nexia-instagram/output/foco-da-semana.md` — tema e itens especiais definidos pela Karolzinha
- `_opensquad/_memory/company.md` — perfil da Nexia, públicos, argumentos e dados confirmados
- `squads/nexia-instagram/pipeline/data/domain-framework.md` — pilares, distribuição, formatos e horários
- `squads/nexia-instagram/pipeline/data/tone-of-voice.md` — os 6 tons e as regras de escolha
- `squads/nexia-instagram/pipeline/data/anti-patterns.md` — erros a evitar
- `squads/nexia-instagram/_memory/memories.md` — preferências aprendidas nas rodadas anteriores

## Instructions

### Process
1. Ler o foco da semana e identificar tema, parceiro (se houver) e restrições.
2. Distribuir 4 posts: 3 para empresário/gestor e 1 para pessoa física/família, sem repetir pilar em posts seguidos.
3. Definir o formato de cada post (ao menos um carrossel, um estático e um reels na semana).
4. Para cada post, escrever público, pilar, formato, tom, gancho, cena da rotina, chamada para ação, dia e horário.
5. Escrever uma justificativa de uma linha por post.
6. Listar tudo o que precisa de confirmação (dados, prazos da NR-1, logo de parceiro).
7. Salvar o calendário no formato abaixo.

## Output Format

The output MUST follow this exact structure:
```
# Calendário Semanal — Nexia Saúde

**Semana de:** {data}
**Foco:** {tema}

## Visão geral
| # | Dia e hora | Público | Pilar | Formato | Tom | Gancho |
|---|------------|---------|-------|---------|-----|--------|

## Detalhe por post
### Post {n}
- Público:
- Pilar:
- Formato:
- Tom:
- Gancho:
- Cena da rotina:
- Chamada para ação:
- Justificativa:

## A confirmar
- {item}
```

## Output Example

```
# Calendário Semanal — Nexia Saúde

**Semana de:** 13/10/2026
**Foco:** NR-1 e produtividade

## Visão geral
| # | Dia e hora | Público | Pilar | Formato | Tom | Gancho |
|---|------------|---------|-------|---------|-----|--------|
| 1 | Terça, 10h | Empresário/gestor | NR-1 | Carrossel (8 slides) | Educativo | A NR-1 mudou. Sua empresa já olha para a saúde mental do time? |
| 2 | Quarta, 19h | Empresário/gestor | Produtividade | Reels (30s) | Narrativo | Terça, 9h. A cadeira vazia pela terceira vez no mês. |
| 3 | Quinta, 10h | Pessoa física/família | Plano individual | Estático | Acolhedor | Um plano. Quatro pessoas cuidadas. |
| 4 | Sexta, 10h | Empresário/gestor | Prova social | Estático | Institucional | Quem cuida do time valoriza cada processo bem conduzido. |

## Detalhe por post
### Post 1
- Público: empresário/gestor
- Pilar: NR-1
- Formato: carrossel de 8 slides
- Tom: Educativo
- Gancho: A NR-1 mudou. Sua empresa já olha para a saúde mental do time?
- Cena da rotina: o gestor que descobre o assunto numa reunião de RH e não sabe por onde começar
- Chamada para ação: Fale com nosso time e conheça o plano para a sua empresa.
- Justificativa: abre a semana com a obrigação, que é o argumento mais forte.

## A confirmar
- Texto e prazos da NR-1 usados no post 1.
- Logo do parceiro do post 4.
```

## Veto Conditions

Reject and redo if ANY of these are true:
1. O calendário não tem exatamente 4 posts, ou a proporção não é 3 empresário/gestor e 1 pessoa física/família.
2. Dois posts seguidos têm o mesmo pilar, ou algum post tem dois públicos.
3. Algum número ou prazo aparece sem estar em `company.md` e sem constar em "A confirmar".

## Quality Criteria

- [ ] Todos os campos estão preenchidos em todos os posts.
- [ ] Há ao menos um carrossel, um estático e um reels.
- [ ] NR-1 ou produtividade aparece pelo menos uma vez.
- [ ] Cada post tem justificativa de uma linha.
- [ ] A lista "A confirmar" existe, mesmo que vazia.

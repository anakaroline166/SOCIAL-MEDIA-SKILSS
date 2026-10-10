---
execution: subagent
agent: designer
format: instagram-feed
inputFile: squads/nexia-instagram/output/legendas.md
outputFile: squads/nexia-instagram/output/artes.md
model_tier: powerful
---

# Step 07: Artes no Canva

## Context Loading

Load these files before executing:
- `squads/nexia-instagram/output/legendas.md` — textos aprovados pela Karolzinha (não alterar)
- `_opensquad/_memory/company.md` — identidade visual: a Nexia já tem kit de marca e modelos no Canva
- `squads/nexia-instagram/pipeline/data/quality-criteria.md` — critério 10, consistência visual
- `squads/nexia-instagram/pipeline/data/anti-patterns.md` — erros a evitar
- `squads/nexia-instagram/_memory/memories.md` — preferências visuais aprendidas
- `skills/canva/SKILL.md` — instruções de uso do Canva

## Instructions

### Process
1. Abrir o Canva (a primeira vez pede login da Karolzinha) e localizar o kit de marca e os modelos da Nexia.
2. Para cada post de `legendas.md`, escolher o modelo conforme formato e público: carrossel, estático ou capa de reels.
3. Preencher textos e imagens com o texto aprovado, sem alterá-lo. Se não couber, não cortar: registrar aviso.
4. Conferir cores, fontes, logo, legibilidade e se o texto bate com o aprovado.
5. Exportar cada peça (PNG; 1080x1350 px para carrossel e estático, 1080x1920 px para capa de reels).
6. Para reels, entregar a capa e o roteiro de cenas; o vídeo é montado manualmente.
7. Registrar links dos designs, arquivos exportados e pendências no formato abaixo.

## Output Format

The output MUST follow this exact structure:
```
# Artes — Semana de {data}

| # | Peça | Modelo usado | Link do Canva | Arquivo exportado | Observação |
|---|------|--------------|---------------|-------------------|------------|

## Avisos
- {texto que não coube, logo pendente, etc. ou "nenhum"}

## Resumo
{uma frase}
```

## Output Example

```
# Artes — Semana de 13/10/2026

| # | Peça | Modelo usado | Link do Canva | Arquivo exportado | Observação |
|---|------|--------------|---------------|-------------------|------------|
| 1 | Carrossel NR-1 (8 slides) | Carrossel claro Nexia | link do design | 8 PNG, 1080x1350 | Capa com 11 palavras |
| 2 | Capa de reels "Cadeira vazia" | Capa reels Nexia | link do design | 1 PNG, 1080x1920 | Vídeo a montar |
| 3 | Estático "Um plano. Quatro pessoas cuidadas." | Estático família | link do design | 1 PNG, 1080x1350 | Sem alteração |
| 4 | Estático de parceiro | Estático institucional | link do design | 1 PNG, 1080x1350 | Logo do parceiro pendente |

## Avisos
- Post 4: aguardando o logo do parceiro, enviado pela Karolzinha.
- Post 1, slide 5: texto longo; leitura confortável pede dividir em dois slides. Decisão da Karolzinha.

## Resumo
4 peças criadas com o kit de marca da Nexia, sem alteração nos textos aprovados.
```

## Veto Conditions

Reject and redo if ANY of these are true:
1. O texto de alguma arte difere do texto aprovado em `legendas.md`.
2. Alguma peça usa cor, fonte ou logo fora do kit de marca da Nexia.
3. Alguma peça não tem link do Canva ou arquivo exportado registrado.

## Quality Criteria

- [ ] Todas as peças do calendário têm arte.
- [ ] A capa do carrossel é legível em um segundo, com no máximo 12 palavras.
- [ ] Os formatos de exportação estão corretos.
- [ ] Avisos de texto que não coube ou de itens pendentes estão registrados.
- [ ] Nenhum rosto de paciente real aparece nas artes.

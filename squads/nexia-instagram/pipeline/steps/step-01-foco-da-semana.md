---
type: checkpoint
outputFile: squads/nexia-instagram/output/foco-da-semana.md
---

# Step 01: Foco da semana

Pergunte à Karolzinha, com `AskUserQuestion`, o que ela quer para a semana. Use perguntas com 2 a 4 opções (a opção "Other" permite texto livre):

1. **Tema principal da semana**
   - NR-1 e obrigação da empresa
   - Produtividade, presenteísmo e absenteísmo
   - Deixar a estrategista escolher (semana livre)
2. **Algo especial para entrar na semana?**
   - Anúncio de empresa parceira (a Karolzinha informa o nome e o que foi contratado)
   - Data comemorativa ou campanha de saúde do mês
   - Nada especial

Depois de coletar as respostas, salve em `output/foco-da-semana.md` neste formato:

```
# Foco da Semana

**Tema principal:** {resposta}
**Item especial:** {resposta, com nome do parceiro se houver}
**Observações da Karolzinha:** {texto livre, se houver}
**Data:** {AAAA-MM-DD}
```

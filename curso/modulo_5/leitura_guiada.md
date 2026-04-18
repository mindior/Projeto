# Módulo 5 — Avaliação, Confiabilidade e Robustez em Large Language Models

---

## 1. Objetivos

No final deste módulo, o estudante deverá ser capaz de:

- compreender os principais problemas de confiabilidade em LLM  
- identificar e analisar alucinações  
- aplicar métricas de avaliação de respostas  
- compreender conceitos de robustez e segurança  
- avaliar criticamente sistemas baseados em LLM  

---

## 2. Enquadramento do módulo

Nos módulos anteriores, foram explorados os mecanismos de funcionamento dos Large Language Models (LLM), bem como estratégias para o seu controlo e integração em sistemas.

No entanto, a utilização destes modelos em contextos reais levanta uma questão central:

> até que ponto podemos confiar nas respostas geradas?

Este módulo aborda a avaliação e a confiabilidade como elementos fundamentais no desenvolvimento de sistemas baseados em LLM, sendo particularmente relevantes em contextos de apoio à decisão.

[![Avaliação, Confiabilidade e Robustez em Large Language Models](https://img.youtube.com/vi/TrYNkCdYq_M/0.jpg)](https://www.youtube.com/watch?v=TrYNkCdYq_M)

---

## 3. O problema da confiabilidade

Apesar do seu elevado desempenho, os LLM não garantem:

- veracidade factual  
- consistência nas respostas  
- previsibilidade do comportamento  

Por exemplo, um modelo pode fornecer respostas diferentes para perguntas semelhantes ou apresentar informação incorreta de forma convincente.

Estas limitações tornam-se críticas em contextos como:

- sistemas de apoio à decisão  
- aplicações em saúde  
- sistemas financeiros  
- ambientes organizacionais  

---

## 4. Alucinações em LLM

### 4.1 Definição

Uma alucinação ocorre quando o modelo gera informação que parece plausível, mas que é incorreta.

Por exemplo, um LLM pode inventar uma referência bibliográfica ou apresentar dados inexistentes.

---

### 4.2 Tipos de alucinação

As alucinações podem assumir diferentes formas:

- **factual** — informação incorreta ou inventada  
- **lógica** — raciocínio inválido ou inconsistente  
- **contextual** — uso incorreto do contexto disponível  

---

### 4.3 Causas

As principais causas incluem:

- otimização para fluência linguística, em vez de veracidade  
- ausência de ligação ao mundo real (*grounding*)  
- limitações dos dados de treino  

---

## 5. Métricas de avaliação

A avaliação de respostas geradas por LLM pode ser realizada de diferentes formas.

---

### 5.1 Avaliação automática

Inclui métricas como:

- BLEU  
- ROUGE  
- similaridade semântica  

Estas métricas são úteis para comparar textos, mas apresentam limitações importantes:

> não avaliam diretamente a veracidade factual.

---

### 5.2 Avaliação humana

A avaliação humana continua a ser fundamental.

As principais dimensões incluem:

- correção factual  
- relevância  
- clareza  
- utilidade  

Por exemplo, um especialista pode avaliar se uma resposta é adequada a um contexto específico.

---

### 5.3 Avaliação assistida por LLM

Os próprios LLM podem ser utilizados para avaliar respostas.

Exemplos:

- comparação entre respostas  
- atribuição de pontuações  
- identificação de erros  

No entanto, esta abordagem levanta questões sobre confiabilidade e viés.

---

## 6. Confiabilidade em sistemas baseados em LLM

### 6.1 Dimensões da confiabilidade

A confiabilidade pode ser analisada segundo várias dimensões:

- **factualidade** — a resposta está correta?  
- **consistência** — o modelo responde de forma estável?  
- **robustez** — o comportamento é estável face a variações?  
- **transparência** — é possível compreender a resposta?  

---

### 6.2 Fundamentação no contexto (*groundedness*)

Em sistemas baseados em RAG, é importante avaliar se a resposta:

> está fundamentada nos documentos fornecidos.

Uma resposta bem fundamentada tende a ser mais confiável.

---

## 7. Robustez

A robustez refere-se à capacidade do modelo de manter um comportamento estável perante variações no input.

Por exemplo, um sistema robusto deverá:

- produzir respostas semelhantes para perguntas equivalentes  
- resistir a pequenas alterações no prompt  
- evitar respostas incoerentes  

A falta de robustez pode comprometer a utilização em sistemas reais.

---

## 8. Segurança

### 8.1 Riscos

Os LLM apresentam vários riscos:

- geração de conteúdo incorreto ou enganador  
- manipulação através de prompts adversariais  
- utilização indevida ou maliciosa  

---

### 8.2 Estratégias de mitigação

Para reduzir estes riscos, podem ser utilizadas várias abordagens:

- validação das respostas  
- filtragem de conteúdo  
- melhoria do design de prompts  
- utilização de RAG para introduzir contexto  

No entanto, nenhuma destas estratégias elimina totalmente os riscos.

---

## 9. Avaliação como componente de sistema

A avaliação não deve ser vista como uma etapa final, mas como parte integrante do sistema.

Isto implica:

- avaliação contínua  
- monitorização do desempenho  
- melhoria iterativa  

Por exemplo, um sistema de apoio à decisão deve incluir mecanismos de validação das respostas.

---

## 10. Ligação com explicabilidade (XAI)

A explicabilidade desempenha um papel fundamental na confiabilidade.

Permite:

- compreender as decisões do modelo  
- identificar erros  
- justificar resultados  

Em sistemas reais, a combinação de avaliação e explicabilidade é essencial para aumentar a confiança dos utilizadores.

---

## 11. Leituras obrigatórias

- Kamath et al. (2024)  
  - Cap. 6 — Evaluation of LLM  

---

## 12. Questões de reflexão

1. Podemos confiar em LLM em contextos críticos?  
2. Qual o papel da avaliação humana na validação de respostas?  
3. O RAG elimina completamente as alucinações?  
4. Como medir a confiabilidade de um sistema baseado em LLM?  

---

## 13. Síntese

Neste módulo foram abordados os principais desafios associados à avaliação e confiabilidade dos Large Language Models.

Foram explorados:

- o fenómeno das alucinações  
- diferentes métodos de avaliação  
- conceitos de robustez e segurança  
- a importância da avaliação contínua  

Estes conceitos são fundamentais para o desenvolvimento de sistemas de IA responsáveis e serão articulados com técnicas de explicabilidade nos módulos seguintes.
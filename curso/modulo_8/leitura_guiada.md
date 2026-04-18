# Módulo 8 — Integração de Large Language Models em Sistemas de Apoio à Decisão

---

## 1. Objetivos

No final deste módulo, o estudante deverá ser capaz de:

- compreender o papel dos Large Language Models (LLM) como interfaces em sistemas complexos  
- analisar a integração de LLM em sistemas de apoio à decisão (Decision Support Systems — DSS)  
- compreender a interação humano–IA  
- identificar desafios de integração, confiabilidade e usabilidade  
- projetar sistemas baseados em LLM para contextos reais  

---

## 2. Enquadramento do módulo

Ao longo desta unidade curricular, foram estudados os fundamentos dos LLM, os mecanismos de controlo (engenharia de prompts), a integração de conhecimento (RAG), a avaliação e a explicabilidade.

Neste módulo final, estes elementos são integrados numa perspetiva sistémica.

A questão central passa a ser:

> como integrar LLM em sistemas reais de forma confiável e útil para a tomada de decisão?

[![Integração de Large Language Models em Sistemas de Apoio à Decisão](https://img.youtube.com/vi/PBJ7FTpVv3Y/0.jpg)](https://www.youtube.com/watch?v=PBJ7FTpVv3Y)
---

## 3. LLM como interface

Tradicionalmente, os sistemas de informação utilizam interfaces como:

- interfaces gráficas  
- dashboards  
- formulários estruturados  

Com a introdução dos LLM, surge um novo paradigma:

→ **interface conversacional baseada em linguagem natural**

---

### 3.1 Características

As interfaces baseadas em LLM apresentam várias vantagens:

- interação em linguagem natural  
- maior flexibilidade  
- redução de barreiras técnicas para o utilizador  

Por exemplo, um utilizador pode consultar um sistema de apoio à decisão através de perguntas em linguagem natural, sem necessidade de conhecer a estrutura dos dados.

---

### 3.2 Limitações

Apesar das vantagens, existem limitações importantes:

- ambiguidade na interpretação das perguntas  
- falta de precisão nas respostas  
- necessidade de validação  

Estas limitações reforçam a necessidade de mecanismos de avaliação e explicabilidade.

---

## 4. Sistemas de apoio à decisão (DSS)

### 4.1 Definição

Os sistemas de apoio à decisão (DSS) são sistemas que suportam:

- análise de dados  
- avaliação de cenários  
- tomada de decisão  

São amplamente utilizados em contextos organizacionais.

---

### 4.2 Componentes

Um DSS típico inclui:

- **dados** — fontes de informação  
- **modelos** — algoritmos de análise ou previsão  
- **interface** — meio de interação com o utilizador  
- **utilizador** — decisor humano  

---

## 5. Integração de LLM em DSS

Os LLM podem ser integrados em DSS com diferentes funções:

- interface de consulta  
- explicador de resultados  
- assistente de decisão  

---

### 5.1 Arquitetura típica

Um sistema integrado pode ser representado como:

dados → modelo → explicação → LLM → utilizador  

Neste fluxo:

- o modelo gera resultados  
- técnicas de explicabilidade ajudam a interpretar esses resultados  
- o LLM traduz e comunica a informação ao utilizador  

---

### 5.2 Exemplo aplicado

Considere um sistema de gestão da cadeia de abastecimento:

- um modelo prevê a procura  
- uma técnica de explicabilidade identifica os fatores relevantes  
- o LLM apresenta uma explicação em linguagem natural  
- o utilizador interage com o sistema para explorar cenários  

Este tipo de integração aproxima a IA do processo de decisão.

---

## 6. Interação humano–IA

### 6.1 Dimensões da interação

A interação entre humanos e sistemas de IA envolve várias dimensões:

- **usabilidade** — facilidade de utilização  
- **confiança** — perceção de fiabilidade  
- **compreensão** — capacidade de interpretar resultados  

---

### 6.2 Papel do utilizador

O utilizador desempenha um papel central:

- interpreta os outputs do sistema  
- valida as decisões  
- interage com o sistema para obter informação adicional  

Assim, os sistemas devem ser concebidos para apoiar, e não substituir, o decisor humano.

---

## 7. Desafios de integração

A integração de LLM em sistemas reais apresenta vários desafios.

---

### 7.1 Desafios técnicos

- integração de múltiplos componentes  
- latência e tempo de resposta  
- escalabilidade  

---

### 7.2 Desafios cognitivos

- compreensão das respostas  
- interpretação de explicações  
- construção de confiança  

---

### 7.3 Desafios organizacionais

- aceitação por parte dos utilizadores  
- integração em processos existentes  
- impacto na tomada de decisão  

---

## 8. Confiabilidade em sistemas integrados

A confiabilidade de um sistema baseado em LLM depende de múltiplos fatores:

- qualidade do modelo  
- qualidade do contexto (por exemplo, em sistemas RAG)  
- presença de mecanismos de explicabilidade  
- interação adequada com o utilizador  

A ausência de qualquer destes elementos pode comprometer o sistema.

---

## 9. LLM como mediador da explicabilidade

Os LLM podem desempenhar um papel importante na explicabilidade:

- traduzindo outputs técnicos em linguagem natural  
- facilitando a compreensão por utilizadores não técnicos  

Por exemplo, um LLM pode transformar uma explicação baseada em variáveis num texto acessível ao utilizador.

---

## 10. Limitações

Apesar do seu potencial, a utilização de LLM como interface apresenta limitações:

- risco de simplificação excessiva das explicações  
- possibilidade de geração de explicações incorretas  
- dependência do prompt utilizado  

Estas limitações exigem uma utilização cuidadosa e validada.

---

## 11. Integração com explicabilidade (XAI)

Sistemas avançados combinam diferentes componentes:

- modelos preditivos  
- técnicas de explicabilidade  
- mecanismos de recuperação (RAG)  
- interfaces conversacionais  

Esta integração permite construir sistemas mais completos e confiáveis.

---

## 12. Leituras sugeridas

- Kamath et al. (2024), 
  - Cap. 8 - LLMs in Production
  - Cap. 6 - LLM Challenges and Solutions
  - Cap. 10 - LLMs: Evolution and New Frontiers
- Kamath & Liu (2021)  
  - Cap. 8 - XAI: Challenges and Future

---

## 13. Questões de reflexão

1. Os LLM podem substituir interfaces tradicionais?  
2. Como garantir confiança em sistemas de apoio à decisão baseados em LLM?  
3. O utilizador deve confiar nas respostas do sistema? Em que condições?  
4. Qual o papel da explicabilidade na interação humano–IA?  

---

## 14. Síntese

Neste módulo foi analisada a integração de Large Language Models em sistemas de apoio à decisão.

Foram abordados:

- o papel dos LLM como interfaces  
- a estrutura dos sistemas DSS  
- os desafios técnicos, cognitivos e organizacionais  
- a importância da confiabilidade e da explicabilidade  

Este módulo conclui a unidade curricular, integrando os conceitos abordados e preparando o estudante para o desenvolvimento de sistemas reais baseados em LLM.
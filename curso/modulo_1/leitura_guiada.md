# Módulo 1 — Fundamentos dos Large Language Models e o Problema da Confiabilidade

---

## 1. Objetivos de aprendizagem

No final deste módulo, o estudante deverá ser capaz de:

- explicar a evolução dos modelos de linguagem até aos LLM  
- compreender os princípios fundamentais que distinguem os LLM de abordagens anteriores  
- analisar criticamente as capacidades emergentes dos LLM  
- identificar limitações estruturais dos LLM  
- relacionar essas limitações com a necessidade de explicabilidade (XAI)  

---

## 2. Enquadramento do módulo

Nos últimos anos, os Large Language Models (LLM) transformaram profundamente a forma como interagimos com sistemas de inteligência artificial. Aplicações como assistentes conversacionais, sistemas de apoio à decisão e ferramentas de geração de texto tornaram-se cada vez mais comuns.

No entanto, apesar do seu elevado desempenho, estes modelos apresentam limitações importantes que levantam questões sobre a sua utilização em contextos reais.

Este módulo tem como objetivo introduzir os fundamentos dos LLM, analisando simultaneamente as suas capacidades e limitações. Em particular, será dada especial atenção ao problema da confiabilidade, que será um tema central ao longo da unidade curricular.

[![Fundamentos dos Large Language Models e o Problema da Confiabilidade](https://img.youtube.com/vi/aT9UPG6yIg4/0.jpg)](https://www.youtube.com/watch?v=aT9UPG6yIg4)

---

## 3. Evolução dos modelos de linguagem

Para compreender os LLM, é importante perceber como os modelos de linguagem evoluíram ao longo do tempo.

### 3.1 Da linguística simbólica aos modelos estatísticos

Os primeiros sistemas de processamento de linguagem natural baseavam-se em regras explícitas e gramáticas formais. Estes sistemas tentavam descrever a linguagem de forma estruturada, mas enfrentavam dificuldades em lidar com a ambiguidade e diversidade da linguagem natural.

Posteriormente, surgiram os modelos estatísticos, que passaram a utilizar grandes conjuntos de dados (corpora) para aprender padrões linguísticos. Estes modelos permitiram:

- modelar probabilidades de sequências de palavras  
- utilizar dados reais em vez de regras fixas  
- capturar padrões linguísticos de forma mais flexível  

No entanto, apresentavam limitações importantes, como a dependência de características manuais (features) e a dificuldade em capturar contextos longos.

---

### 3.2 A introdução das representações densas

Com o desenvolvimento das redes neuronais, surgiram representações contínuas da linguagem, conhecidas como embeddings.

Modelos como Word2Vec e GloVe permitiram representar palavras como vetores numéricos, capturando relações semânticas. Por exemplo, palavras com significados semelhantes apresentam representações próximas no espaço vetorial.

Esta abordagem introduziu:

- generalização semântica  
- capacidade de capturar similaridades contextuais  
- melhoria significativa em várias tarefas de NLP  

---

### 3.3 A revolução dos transformers

Um dos avanços mais importantes foi a introdução da arquitetura transformer, baseada no mecanismo de **self-attention**.

Este mecanismo permite ao modelo:

- identificar relações entre palavras numa sequência  
- capturar dependências de longo alcance  
- processar informação de forma paralela  

Por exemplo, numa frase longa, o modelo consegue relacionar palavras distantes, algo que era difícil em abordagens anteriores.

Os transformers constituem a base dos modelos modernos, incluindo os Large Language Models.

---

### 3.4 Escala como fator crítico

Uma característica distintiva dos LLM é a sua escala:

- milhões ou milhares de milhões de parâmetros  
- grandes volumes de dados de treino  
- elevada capacidade computacional  

Esta escala permite que os modelos desenvolvam capacidades que não foram explicitamente programadas, conhecidas como **capacidades emergentes**.

---

## 4. O que são Large Language Models

### 4.1 Definição operacional

Um Large Language Model pode ser entendido como um modelo que prevê a próxima unidade linguística (token) com base no contexto anterior.

Formalmente:

P(w_t | w_1, ..., w_{t-1})

Apesar desta definição simples, os LLM são capazes de realizar tarefas complexas, como responder a perguntas, resumir textos ou gerar código.

---

### 4.2 Capacidades emergentes

Uma das características mais surpreendentes dos LLM é o surgimento de capacidades emergentes, tais como:

- raciocínio aproximado  
- adaptação a tarefas não vistas durante o treino  
- compreensão contextual avançada  

Por exemplo, um modelo pode responder a uma questão sobre supply chain mesmo sem ter sido explicitamente treinado para essa tarefa.

---

### 4.3 Paradigma de utilização

Os LLM são utilizados principalmente através de linguagem natural, o que representa uma mudança significativa no paradigma de interação com sistemas de IA.

As principais abordagens incluem:

- prompting (instruções em linguagem natural)  
- fine-tuning (ajuste do modelo a tarefas específicas)  
- retrieval-augmented generation (integração com conhecimento externo)  

---

## 5. Limitações fundamentais dos LLM

Apesar do seu desempenho, os LLM apresentam limitações estruturais que devem ser cuidadosamente consideradas.

### 5.1 Alucinações

Os modelos podem gerar respostas plausíveis mas incorretas.

Por exemplo, um LLM pode inventar uma referência bibliográfica ou apresentar dados incorretos de forma convincente.

Isto acontece porque o modelo é otimizado para gerar texto plausível, e não necessariamente verdadeiro.

---

### 5.2 Falta de grounding

Os LLM não têm acesso direto à realidade. Em vez disso, baseiam-se em padrões aprendidos durante o treino.

Isto significa que:

- não verificam factos  
- não têm consciência do mundo real  
- podem gerar respostas descontextualizadas  

A indústria vem tentando diminuir esse problema dando aos modelos acesso em tempo real à internet e buscadores bem como criando modelos LLM multimodais, que conseguem, por exemplo, analisar imagens. Essas tentativas visam ancorar as respostas dos modelos em realidade lógica e factual.

---

### 5.3 Sensibilidade ao prompt

Pequenas alterações no input podem produzir respostas muito diferentes.

Por exemplo, reformular uma pergunta pode levar a resultados distintos, o que levanta questões sobre consistência e reprodutibilidade.

---

### 5.4 Opacidade (black-box)

Os LLM são modelos complexos, dificultando a compreensão de como produzem as suas respostas.

Isto levanta desafios em termos de:

- interpretação  
- validação  
- confiança  

---

## 6. O problema da explicabilidade

As limitações dos LLM tornam evidente a necessidade de explicabilidade.

A explicabilidade permite:

- compreender decisões  
- identificar erros  
- aumentar a confiança dos utilizadores  

Em contextos como saúde, finanças ou supply chain, a capacidade de justificar decisões é essencial.

---

### 6.1 Tipos de explicação

As explicações podem ser:

- globais — descrevem o comportamento geral do modelo  
- locais — explicam uma decisão específica  

---

### 6.2 Explicabilidade em sistemas reais

Em aplicações reais, a explicabilidade é frequentemente um requisito.

Por exemplo:

- justificar decisões de um sistema de recomendação  
- explicar previsões de um modelo de procura  
- suportar decisões estratégicas  

---

## 7. Integração conceptual

Um ponto central deste módulo é que:

> Os LLM são poderosos, mas não são confiáveis por defeito.

Assim, a utilização destes modelos em sistemas reais exige a integração de mecanismos adicionais, nomeadamente:

- avaliação  
- validação  
- explicabilidade  

---

## 8. Leituras obrigatórias

- Kamath et al. (2024), 
  - Cap. 1 - Introduction to LLM  
  - Cap. 2 - Language Models Pre-training
  - Cap. 6 - LLMChallenges and Solutions
- Kamath & Liu (2021), 
  - Cap. 1 — Introduction to Explainable AI  
- Alammar, J., & Grootendorst, M. (2024). 
  - Cap. 1 - Introduction to Large Language Models
- Munn, M., & Pitman, D. (2022), 
  - Cap. 1 - Introduction
  - Cap. 2 - An Overview of Explainability
---

## 9. Questões de reflexão

1. Por que razão os LLM apresentam capacidades emergentes?  
2. Qual a diferença entre plausibilidade e veracidade em LLM?  
3. Em que contextos a falta de explicabilidade é crítica?  
4. É possível confiar em LLM sem mecanismos adicionais? Justifique.  

---

## 10. Síntese final

Neste módulo foram apresentados os fundamentos dos Large Language Models, incluindo:

- a evolução dos modelos de linguagem  
- o funcionamento e capacidades dos LLM  
- as suas limitações estruturais  
- a importância da explicabilidade  

Estes conceitos constituem a base para os módulos seguintes, onde serão exploradas técnicas para controlo, avaliação e integração de LLM em sistemas reais.
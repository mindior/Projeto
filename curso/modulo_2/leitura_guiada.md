# Módulo 2 — Engenharia de Prompts e Geração Aumentada por Recuperação (RAG)

---

## 1. Objetivos

No final deste módulo, o estudante deverá ser capaz de:

- compreender o papel da engenharia de prompts (*prompt engineering*) na interação com LLM  
- projetar prompts eficazes para diferentes tarefas  
- analisar a sensibilidade dos LLM ao input  
- compreender a arquitetura de sistemas de geração aumentada por recuperação (RAG)  
- implementar e avaliar pipelines de recuperação de informação e geração  

---

## 2. Enquadramento do módulo

Após compreender os fundamentos dos Large Language Models (LLM), torna-se essencial perceber como interagir eficazmente com estes sistemas e como ultrapassar algumas das suas limitações.

Neste módulo são abordados dois conceitos centrais:

- **engenharia de prompts**, que permite controlar o comportamento dos modelos através de linguagem natural  
- **geração aumentada por recuperação (Retrieval-Augmented Generation — RAG)**, que permite integrar conhecimento externo no processo de geração  

Estes dois mecanismos são fundamentais para o desenvolvimento de sistemas reais baseados em LLM.

[![Engenharia de Prompts e Geração Aumentada por Recuperação (RAG)](https://img.youtube.com/vi/6n6Dc3z8DGI/0.jpg)](https://www.youtube.com/watch?v=6n6Dc3z8DGI)

---

## 3. Engenharia de prompts

### 3.1 LLM como sistemas condicionais

Os LLM não executam instruções de forma determinística. Em vez disso, geram respostas com base em probabilidades condicionadas ao input.

Isto significa que:

> o comportamento do modelo depende diretamente do prompt fornecido.

Por exemplo, as seguintes instruções:

- "Explique o conceito de otimização da cadeia de abastecimento"
- "Explique o conceito de otimização da cadeia de abastecimento com exemplos simples"

podem originar respostas significativamente diferentes, tanto em detalhe como em estrutura.

---

### 3.2 Tipos de prompting

#### Zero-shot

O modelo recebe apenas a instrução, sem exemplos adicionais.

Exemplo:  
> "Explique o que é previsão da procura."

Esta abordagem é simples, mas pode produzir respostas inconsistentes.

---

#### Few-shot

Inclui exemplos no prompt, ajudando o modelo a compreender melhor a tarefa.

Exemplo:

Pergunta: O que é gestão de inventário?  
Resposta: É o processo de equilibrar níveis de stock e procura.

Pergunta: O que é previsão da procura?  
Resposta: É o processo de estimar quanto de um produto ou serviço os clientes irão querer no futuro.

Esta abordagem tende a melhorar a consistência das respostas.

---

#### Prompt baseado em instrução

Define explicitamente o que se pretende do modelo.

Exemplo:  
> "Apresente uma explicação estruturada sobre otimização da cadeia de abastecimento, incluindo definição, vantagens e limitações."

---

### 3.3 Estratégias avançadas de prompting

#### Cadeia de raciocínio (*chain-of-thought*)

Incentiva o modelo a explicar o raciocínio passo a passo.

Exemplo:  
> "Explique passo a passo como reduzir custos numa cadeia de abastecimento."

---

#### Definição de papel (*role prompting*)

Atribui um papel ao modelo.

Exemplo:  
> "Assuma o papel de um especialista em logística e explique como reduzir custos de transporte."

---

#### Estruturação da resposta

Define o formato da resposta.

Exemplo:  
> "Responda em tópicos e inclua vantagens e riscos."

---

Estas estratégias permitem:

- melhorar a qualidade das respostas  
- aumentar a consistência  
- controlar o comportamento do modelo  

---

### 3.4 Sensibilidade ao prompt

Os LLM são altamente sensíveis à forma como o input é formulado.

Pequenas variações no prompt podem:

- alterar significativamente a resposta  
- introduzir inconsistências  
- afetar a confiabilidade  

Este fenómeno levanta desafios importantes em termos de:

- reprodutibilidade  
- avaliação  
- utilização em sistemas reais  

---

## 4. Limitações da engenharia de prompts

Apesar da sua importância, a engenharia de prompts não resolve todos os problemas dos LLM.

Em particular, não resolve:

- a falta de conhecimento atualizado  
- erros factuais  
- ausência de ligação ao mundo real (*grounding*)  

Por exemplo, um modelo pode produzir uma resposta bem estruturada, mas incorreta do ponto de vista factual.

---

## 5. Geração aumentada por recuperação (RAG)

### 5.1 Motivação

A geração aumentada por recuperação (RAG) surge como uma abordagem para ultrapassar algumas das limitações dos LLM.

Em vez de depender apenas do conhecimento interno do modelo, o RAG permite:

- aceder a informação externa  
- integrar contexto relevante  
- melhorar a qualidade das respostas  

Por exemplo, num sistema de apoio à decisão, o modelo pode utilizar dados reais da organização.

---

### 5.2 Arquitetura RAG

Um sistema RAG típico inclui os seguintes passos:

1. os documentos são convertidos em representações vetoriais (*embeddings*)  
2. estas representações são armazenadas numa base vetorial  
3. a pergunta do utilizador é convertida em embedding  
4. são recuperados os documentos mais relevantes  
5. o contexto é fornecido ao modelo  
6. o modelo gera a resposta  

---

### 5.3 Componentes principais

Um sistema RAG inclui:

- **codificador de embeddings** — transforma texto em vetores  
- **base de dados vetorial** — armazena os embeddings  
- **mecanismo de recuperação (retriever)** — identifica documentos relevantes  
- **modelo gerador (LLM)** — produz a resposta  

---

### 5.4 Impacto do contexto

A introdução de contexto pode:

- aumentar a precisão  
- reduzir alucinações  
- melhorar a relevância  

No entanto, também pode introduzir problemas:

- contexto irrelevante  
- excesso de informação  
- perda de coerência  

Assim, a seleção de contexto é um elemento crítico no desempenho do sistema.

---

## 6. Avaliação de sistemas RAG

A avaliação deve considerar várias dimensões:

- **relevância** — a resposta responde à questão?  
- **factualidade** — a informação está correta?  
- **fundamentação no contexto (groundedness)** — a resposta baseia-se nos documentos?  
- **robustez** — o sistema é consistente?  

---

## 7. Limitações do RAG

Apesar das suas vantagens, o RAG apresenta limitações:

- depende da qualidade dos dados  
- a recuperação pode ser imperfeita  
- a integração com o modelo pode introduzir erros  

Por exemplo, se forem recuperados documentos irrelevantes, a resposta poderá ser incorreta.

---

## 8. Ligação com explicabilidade (XAI)

O RAG introduz um elemento de transparência, uma vez que permite identificar as fontes utilizadas.

Isto facilita:

- validação  
- auditoria  
- aumento da confiança  

No entanto, o RAG não substitui técnicas de explicabilidade, sendo apenas um mecanismo complementar.

---

## 9. Leituras obrigatórias

- Kamath et al. (2024)  
  - Cap. 3 — Prompting  
  - Cap. 7 — Retrieval-Augmented Generation  
- Alammar, J., & Grootendorst, M. (2024)
  - Cap. 6 - Prompt Engineering
---

## 10. Questões de reflexão

1. A engenharia de prompts é suficiente para controlar um LLM?  
2. Em que situações o RAG melhora significativamente o desempenho?  
3. O RAG resolve o problema da explicabilidade?  
4. Quais são os riscos de sistemas baseados em RAG?  

---

## 11. Síntese

Neste módulo foram abordados dois elementos fundamentais para o uso de LLM em sistemas reais:

- a engenharia de prompts, como mecanismo de controlo  
- o RAG, como mecanismo de integração de conhecimento externo  

Estes conceitos são essenciais para o desenvolvimento de sistemas mais confiáveis e serão aprofundados nos módulos seguintes.
# Módulo 4 — Geração Aumentada por Recuperação (RAG) e Sistemas Baseados em LLM

---

## 1. Objetivos

No final deste módulo, o estudante deverá ser capaz de:

- compreender o problema da recuperação de informação em sistemas de IA  
- explicar o funcionamento de sistemas de geração aumentada por recuperação (RAG)  
- projetar pipelines de recuperação e geração  
- analisar o impacto da recuperação na qualidade das respostas  
- compreender limitações e desafios de sistemas RAG  

---

## 2. Enquadramento do módulo

Nos módulos anteriores, foram explorados os fundamentos dos Large Language Models (LLM) e os mecanismos de controlo baseados em engenharia de prompts.

No entanto, mesmo com prompts bem estruturados, os LLM apresentam limitações importantes, nomeadamente ao nível do conhecimento e da confiabilidade.

Este módulo introduz a **geração aumentada por recuperação (Retrieval-Augmented Generation — RAG)** como uma abordagem para integrar conhecimento externo e melhorar o desempenho dos sistemas baseados em LLM.

[![Geração Aumentada por Recuperação (RAG) e Sistemas Baseados em LLM](https://img.youtube.com/vi/JTCrJxb23kA/0.jpg)](https://www.youtube.com/watch?v=JTCrJxb23kA)

---

## 3. O problema da recuperação de informação

Os LLM apresentam limitações estruturais relacionadas com o conhecimento:

- conhecimento desatualizado  
- ausência de informação específica de domínio  
- geração de respostas incorretas (alucinações)  

Estas limitações resultam do facto de:

> o conhecimento estar incorporado nos parâmetros do modelo, adquiridos durante o treino.

Por exemplo, um LLM pode não ter acesso a dados recentes de uma organização ou a informação específica de um contexto empresarial.

Assim, torna-se necessário integrar mecanismos de recuperação de informação.

---

## 4. Geração aumentada por recuperação (RAG)

### 4.1 Definição

A geração aumentada por recuperação (RAG) combina dois processos:

- recuperação de informação (*retrieval*)  
- geração de linguagem (*generation*)  

O objetivo é permitir que o modelo utilize conhecimento externo no momento da geração da resposta.

---

### 4.2 Arquitetura geral

Um sistema RAG segue tipicamente o seguinte pipeline:

1. os documentos são convertidos em representações vetoriais (*embeddings*)  
2. estas representações são armazenadas numa base vetorial  
3. a pergunta do utilizador é convertida em embedding  
4. são recuperados os documentos mais relevantes  
5. o contexto é construído a partir desses documentos  
6. o LLM gera a resposta com base nesse contexto  

Este processo permite combinar recuperação de informação com geração de linguagem.

---

## 5. Representação vetorial

### 5.1 Embeddings

Os embeddings são representações numéricas densas de texto.

Estas representações permitem:

- capturar significado semântico  
- comparar textos  
- identificar documentos relevantes  

Por exemplo, duas frases com significado semelhante terão embeddings próximos no espaço vetorial.

---

### 5.2 Similaridade

A recuperação de informação baseia-se na comparação entre embeddings.

As métricas mais comuns incluem:

- similaridade do cosseno (*cosine similarity*)  
- distância euclidiana  

Estas métricas permitem identificar os documentos mais relevantes para uma determinada questão.

---

## 6. Bases de dados vetoriais

### 6.1 Conceito

Uma base de dados vetorial permite:

- armazenar embeddings  
- realizar pesquisas eficientes por similaridade  

Este tipo de base de dados é essencial para o funcionamento de sistemas RAG.

---

### 6.2 Exemplos

Algumas soluções utilizadas incluem:

- FAISS  
- Chroma  
- Weaviate  

---

### 6.3 Indexação

A indexação dos embeddings é fundamental para:

- melhorar a eficiência da pesquisa  
- garantir escalabilidade  
- reduzir o tempo de resposta  

---

## 7. Recuperação de informação

### 7.1 Recuperação top-k

Um dos métodos mais comuns consiste em selecionar os **k documentos mais relevantes** para uma dada questão.

Este valor (k) deve ser cuidadosamente escolhido.

---

### 7.2 Trade-offs

A escolha de k envolve um compromisso:

- k pequeno → menor contexto, possível perda de informação  
- k grande → mais contexto, mas maior risco de ruído  

Por exemplo, recuperar demasiados documentos pode introduzir informação irrelevante, afetando a qualidade da resposta.

---

## 8. Construção de contexto

O contexto fornecido ao modelo deve ser:

- relevante  
- conciso  
- não redundante  

A qualidade do contexto influencia diretamente a qualidade da resposta.

Por exemplo, incluir informação irrelevante pode levar o modelo a produzir respostas incorretas ou confusas.

---

## 9. Integração com LLM

O contexto recuperado é incluído no prompt enviado ao modelo.

Assim, o LLM passa a gerar respostas condicionadas não apenas pelo prompt, mas também pelo conhecimento externo.

Este mecanismo permite:

- melhorar a precisão  
- reduzir alucinações  
- aumentar a relevância  

---

## 10. Avaliação de sistemas RAG

A avaliação de sistemas RAG deve considerar várias dimensões:

- **factualidade** — a resposta está correta?  
- **relevância** — responde à questão?  
- **fundamentação no contexto (groundedness)** — utiliza os documentos recuperados?  
- **consistência** — produz resultados estáveis?  

A avaliação é essencial para garantir a qualidade do sistema.

---

## 11. Limitações dos sistemas RAG

Apesar das suas vantagens, os sistemas RAG apresentam limitações:

- recuperação imperfeita de documentos  
- dependência da qualidade dos dados  
- integração complexa entre componentes  

Por exemplo, se o sistema recuperar documentos incorretos, a resposta final será afetada.

---

## 12. RAG como sistema de engenharia

É importante compreender que o RAG não é apenas uma técnica isolada, mas sim uma arquitetura de sistema.

Um sistema RAG inclui:

- ingestão de dados  
- processamento  
- armazenamento  
- recuperação  
- geração  
- avaliação  

Isto implica decisões de engenharia que influenciam o desempenho do sistema.

---

## 13. Ligação com explicabilidade (XAI)

O RAG introduz um elemento de transparência, uma vez que permite identificar os documentos utilizados na resposta.

Isto facilita:

- validação das respostas  
- auditoria do sistema  
- aumento da confiança  

No entanto, o RAG não resolve completamente o problema da interpretabilidade interna dos modelos.

---

## 14. Leituras obrigatórias

- Kamath et al. (2024)  
  - Cap. 7 — Retrieval-Augmented Generation  
- Alammar, J., & Grootendorst, M. (2024). 
  - Cap. 8 - Semantic Search and Retrieval-Augmented Generation
---

## 15. Questões de reflexão

1. O RAG elimina completamente as alucinações?  
2. Como avaliar a qualidade da recuperação de informação?  
3. Qual o impacto do contexto na resposta gerada?  
4. O RAG é suficiente para garantir confiabilidade?  

---

## 16. Síntese

Neste módulo foi introduzida a geração aumentada por recuperação (RAG) como uma abordagem central para a construção de sistemas baseados em LLM.

Foram abordados:

- o problema da recuperação de informação  
- a arquitetura dos sistemas RAG  
- os seus componentes principais  
- os desafios de implementação e avaliação  

O RAG constitui um elemento fundamental na construção de sistemas mais confiáveis e será articulado com técnicas de avaliação e explicabilidade nos módulos seguintes.
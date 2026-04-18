# Módulo 7 — Técnicas de Explicabilidade em Sistemas de Inteligência Artificial

---

## 1. Objetivos

No final deste módulo, o estudante deverá ser capaz de:

- compreender técnicas de explicabilidade aplicadas a modelos de machine learning  
- distinguir explicações locais e globais  
- aplicar métodos como importância de variáveis, LIME e SHAP  
- interpretar resultados de explicabilidade  
- analisar limitações das técnicas de explicabilidade (XAI)  

---

## 2. Enquadramento do módulo

No módulo anterior, foi introduzido o conceito de explicabilidade em inteligência artificial (XAI) e a sua importância em sistemas reais.

Neste módulo, são abordadas técnicas concretas que permitem explicar o comportamento de modelos complexos, nomeadamente modelos de machine learning e sistemas híbridos.

Estas técnicas são fundamentais para:

- compreender decisões  
- validar resultados  
- aumentar a confiança nos sistemas  

[![Técnicas de Explicabilidade em Sistemas de Inteligência Artificial](https://img.youtube.com/vi/PE4uw7UCN4Q/0.jpg)](https://www.youtube.com/watch?v=PE4uw7UCN4Q)

---

## 3. Explicabilidade em modelos complexos

Os modelos modernos, como redes neuronais e métodos de ensemble, apresentam elevada capacidade preditiva, mas baixa interpretabilidade.

Isto significa que:

- produzem resultados precisos  
- mas não são facilmente compreendidos  

As técnicas de explicabilidade permitem:

- extrair explicações após o treino (pós-hoc)  
- analisar decisões individuais  
- compreender padrões de comportamento do modelo  

---

## 4. Importância de variáveis (*feature importance*)

### 4.1 Definição

A importância de variáveis mede o contributo de cada variável para a previsão do modelo.

Por exemplo, num modelo de previsão de procura, pode indicar quais os fatores mais relevantes, como preço, sazonalidade ou promoções.

---

### 4.2 Tipos de importância

Existem diferentes formas de calcular a importância:

- **baseada no modelo** — comum em modelos como árvores de decisão  
- **por permutação** — avalia o impacto de alterar uma variável  
- **baseada em explicadores** — como SHAP  

---

### 4.3 Limitações

Apesar da sua utilidade, apresenta limitações:

- pode ser instável  
- depende do tipo de modelo  
- pode não captar interações complexas entre variáveis  

---

## 5. Explicações locais vs globais

### 5.1 Explicações globais

Descrevem o comportamento geral do modelo.

Permitem compreender:

- padrões gerais  
- variáveis mais relevantes  
- lógica global do modelo  

---

### 5.2 Explicações locais

Explicam uma decisão específica.

Por exemplo:

- por que razão um cliente foi classificado como de alto risco  
- quais fatores influenciaram uma previsão  

---

### 5.3 Trade-offs

Existe um compromisso entre os dois tipos:

- explicações globais → visão geral do modelo  
- explicações locais → maior detalhe e contexto  

Ambos são necessários para uma compreensão completa.

---

## 6. LIME (Local Interpretable Model-agnostic Explanations)

### 6.1 Conceito

O LIME é uma técnica que aproxima o comportamento do modelo numa região local através de um modelo simples e interpretável.

---

### 6.2 Processo

O funcionamento do LIME envolve:

1. gerar variações (perturbações) da instância original  
2. observar as respostas do modelo  
3. ajustar um modelo simples que aproxima o comportamento local  

---

### 6.3 Vantagens

- aplicável a diferentes tipos de modelos  
- fornece explicações locais intuitivas  
- relativamente simples de implementar  

---

### 6.4 Limitações

- pode ser instável  
- depende da forma como as perturbações são geradas  
- sensível a parâmetros  

---

## 7. SHAP (SHapley Additive exPlanations)

### 7.1 Conceito

O SHAP baseia-se na teoria dos jogos, utilizando valores de Shapley para atribuir contributos às variáveis.

---

### 7.2 Propriedades

O método apresenta propriedades importantes:

- **consistência** — contribuições coerentes com o modelo  
- **aditividade** — soma das contribuições corresponde à previsão  

---

### 7.3 Vantagens

- explicações teoricamente fundamentadas  
- interpretação consistente  
- aplicável a diferentes modelos  

---

### 7.4 Limitações

- elevado custo computacional  
- maior complexidade de implementação  
- dificuldade de aplicação em larga escala  

---

## 8. Explicabilidade em sistemas complexos

### 8.1 Sistemas híbridos

Em sistemas reais, é comum a integração de múltiplos componentes, por exemplo:

- modelos preditivos  
- sistemas RAG  
- Large Language Models  

---

### 8.2 Desafios

Nestes sistemas, surgem desafios adicionais:

- múltiplas fontes de decisão  
- interação entre componentes  
- necessidade de explicações integradas  

Por exemplo, uma decisão pode resultar da combinação de um modelo preditivo com um LLM, dificultando a explicação.

---

## 9. Explicabilidade em LLM

A aplicação de técnicas tradicionais de explicabilidade a LLM apresenta desafios específicos:

- ausência de variáveis explícitas  
- natureza gerativa dos outputs  
- elevada complexidade do modelo  

Por exemplo, ao contrário de modelos tabulares, não é evidente quais “variáveis” influenciam diretamente a resposta.

Isto motiva o desenvolvimento de novas abordagens de explicabilidade.

---

## 10. Avaliação de explicações

A qualidade das explicações pode ser avaliada segundo diferentes critérios:

- **fidelidade** — a explicação reflete o comportamento real do modelo?  
- **estabilidade** — a explicação é consistente?  
- **interpretabilidade** — é compreensível para o utilizador?  
- **utilidade** — ajuda na tomada de decisão?  

A avaliação das explicações é essencial para garantir a sua eficácia.

---

## 11. Leituras obrigatórias

- Kamath & Liu (2021)  
  - Cap. 5 — Métodos pós-hoc de explicabilidade  
  - Cap. 6 -  Explainable Deep Learning
- Munn, M., & Pitman, D. (2022), 
  - Cap. 3 - Explainability for Tabular Data
---

## 12. Questões de reflexão

1. Qual a diferença entre SHAP e LIME?  
2. As explicações locais são suficientes para compreender um modelo?  
3. Como avaliar a qualidade de uma explicação?  
4. É possível aplicar estas técnicas diretamente a LLM?  

---

## 13. Síntese

Neste módulo foram apresentadas técnicas de explicabilidade aplicadas a modelos de inteligência artificial.

Foram abordados:

- importância de variáveis  
- explicações locais e globais  
- métodos como LIME e SHAP  
- desafios em sistemas complexos e LLM  

Estas técnicas são essenciais para tornar modelos complexos mais transparentes, embora apresentem limitações que devem ser consideradas na sua aplicação.
# Módulo 6 — Introdução à Explicabilidade em Inteligência Artificial

---

## 1. Objetivos

No final deste módulo, o estudante deverá ser capaz de:

- distinguir interpretabilidade e explicabilidade  
- compreender a importância da explicabilidade em sistemas reais  
- identificar diferentes tipos de explicações  
- analisar o papel da explicabilidade na confiança e tomada de decisão  
- relacionar explicabilidade com sistemas baseados em LLM  

---

## 2. Enquadramento do módulo

Nos módulos anteriores, foram analisados os Large Language Models (LLM), bem como os mecanismos de controlo, recuperação de informação e avaliação.

No entanto, uma questão central permanece:

> como compreender e justificar as decisões produzidas por sistemas de IA?

Este módulo introduz o conceito de **explicabilidade em inteligência artificial (Explainable AI — XAI)**, que visa tornar os modelos mais transparentes e compreensíveis, especialmente em contextos onde a confiança e a validação são essenciais.

[![Introdução à Explicabilidade em Inteligência Artificial](https://img.youtube.com/vi/GxQVcRw954U/0.jpg)](https://www.youtube.com/watch?v=GxQVcRw954U)
---

## 3. O problema da opacidade em IA

Os modelos modernos de inteligência artificial, incluindo redes neuronais profundas e LLM, são frequentemente descritos como modelos de “caixa negra” (*black-box models*).

Isto significa que:

- não é possível compreender diretamente como produzem os outputs  
- o processo de decisão não é transparente para o utilizador  

Por exemplo, um modelo pode prever um valor ou gerar uma resposta sem fornecer uma justificação clara para essa decisão.

Esta opacidade levanta desafios importantes, sobretudo em aplicações críticas.

---

## 4. Interpretabilidade vs Explicabilidade

É fundamental distinguir dois conceitos frequentemente confundidos.

---

### 4.1 Interpretabilidade

A interpretabilidade refere-se à capacidade de compreender diretamente o funcionamento de um modelo.

Exemplos incluem:

- regressão linear  
- árvores de decisão  

Estes modelos apresentam:

- estrutura simples  
- transparência intrínseca  
- facilidade de interpretação  

---

### 4.2 Explicabilidade

A explicabilidade refere-se à capacidade de explicar o comportamento de modelos complexos.

Exemplos incluem:

- redes neuronais  
- modelos de ensemble  
- Large Language Models  

Nestes casos, as explicações são:

- externas ao modelo  
- obtidas através de técnicas específicas (pós-hoc)  

---

### 4.3 Diferença essencial

A diferença pode ser resumida da seguinte forma:

- interpretabilidade → o modelo é diretamente compreensível  
- explicabilidade → o modelo não é transparente, mas pode ser explicado  

---

## 5. Tipos de explicações

As explicações podem assumir diferentes formas, dependendo do objetivo e do contexto.

---

### 5.1 Explicações globais

Descrevem o comportamento geral do modelo.

Por exemplo:

- quais variáveis são mais importantes  
- como o modelo toma decisões em termos gerais  

---

### 5.2 Explicações locais

Explicam uma decisão específica.

Por exemplo:

- por que razão uma determinada previsão foi feita  
- quais fatores influenciaram uma resposta concreta  

---

### 5.3 Formas de explicação

As explicações podem basear-se em:

- variáveis (*features*)  
- exemplos  
- regras  
- linguagem natural  

A escolha depende do tipo de modelo e da aplicação.

---

## 6. Importância da explicabilidade

A explicabilidade desempenha um papel fundamental em sistemas de IA aplicados.

---

### 6.1 Confiança

Os utilizadores precisam de:

- compreender as decisões  
- validar os resultados  
- confiar no sistema  

Sem explicação, a aceitação do sistema pode ser reduzida.

---

### 6.2 Regulamentação

Em muitos contextos, existem requisitos legais e normativos.

Por exemplo:

- decisões automatizadas devem ser justificadas  
- sistemas devem ser auditáveis  

A explicabilidade torna-se, assim, um requisito obrigatório.

---

### 6.3 Tomada de decisão

A explicabilidade é particularmente importante em domínios como:

- saúde  
- finanças  
- cadeia de abastecimento (supply chain)  

Nestes contextos, as decisões têm impacto significativo e devem ser justificadas.

---

## 7. Explicabilidade em sistemas com LLM

A aplicação de explicabilidade a LLM apresenta desafios específicos:

- outputs não determinísticos  
- ausência de estrutura explícita  
- dificuldade em rastrear o processo de geração  

Por exemplo, um LLM pode gerar uma resposta plausível sem indicar claramente a sua origem ou justificação.

---

## 8. Explicabilidade como componente de sistema

A explicabilidade não deve ser considerada um elemento adicional, introduzido no final do desenvolvimento.

Pelo contrário:

> deve ser integrada desde a conceção do sistema.

Isto implica:

- considerar explicabilidade no design  
- definir mecanismos de interpretação  
- garantir transparência ao longo do processo  

---

## 9. Limitações da explicabilidade

Apesar da sua importância, a explicabilidade apresenta limitações:

- as explicações podem ser incompletas  
- existe risco de interpretações incorretas  
- pode haver compromisso entre explicabilidade e desempenho  

Por exemplo, modelos mais simples são mais interpretáveis, mas podem apresentar menor precisão.

---

## 10. Ligação com avaliação

A explicabilidade está diretamente relacionada com a avaliação de sistemas.

Permite:

- validar resultados  
- identificar erros  
- compreender o comportamento do modelo  

Assim, explicabilidade e avaliação devem ser consideradas de forma integrada.

---

## 11. Leituras obrigatórias

- Kamath & Liu (2021)  
  - Cap. 1 — Introduction to Explainable AI  
  - Cap. 2 - Pre-modelInterpretabilityandExplainability
  - Cap. 3 - ModelVisualizationTechniquesandTraditionalInterpretable
Algorithms
  - Cap. 4 - Model Interpretability: Advances in Interpretable Machine Learning
---

## 12. Questões de reflexão

1. Todos os modelos de IA devem ser explicáveis?  
2. A explicabilidade garante confiança nos sistemas?  
3. Qual o papel da explicação na tomada de decisão?  
4. Como é possível explicar o comportamento de um LLM?  

---

## 13. Síntese

Neste módulo foi introduzido o conceito de explicabilidade em inteligência artificial, abordando:

- o problema da opacidade dos modelos  
- a distinção entre interpretabilidade e explicabilidade  
- diferentes tipos de explicações  
- a importância da explicabilidade em sistemas reais  

A explicabilidade constitui um elemento fundamental para o desenvolvimento de sistemas de IA responsáveis e será aprofundada nos módulos seguintes.
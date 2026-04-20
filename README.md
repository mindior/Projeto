# 📚 Large Language Models e Inteligência Artificial Confiável

## 📌 Visão Geral

Este repositório apresenta a proposta científico-pedagógica de uma unidade curricular de mestrado, bem como o desenvolvimento de dois protótipos funcionais complementares:

- uma aplicação de **Learning Analytics pedagógico**
- um **tutor inteligente baseado em Retrieval-Augmented Generation (RAG)**

O projeto integra:

- ensino avançado em Large Language Models (LLM)
- princípios de Inteligência Artificial Confiável (XAI)
- desenvolvimento de sistemas interativos de apoio à aprendizagem

A proposta articula investigação recente em explicabilidade e avaliação de sistemas de IA com um modelo pedagógico centrado no estudante, alinhado com o modelo pedagógico da Universidade Aberta (2026), baseado em aprendizagem ativa, autorregulação e interação em ambientes digitais.

---

## 🧱 Estrutura do Repositório

O repositório está organizado em duas componentes principais:

```
├── curso/
└── app/
```

---

### 📁 `curso/`

Contém todos os materiais pedagógicos da unidade curricular, incluindo:

- programa detalhado da disciplina
- módulos estruturados de aprendizagem
- leituras guiadas
- atividades formativas
- projeto final
- materiais de apoio (notebooks, exercícios, etc.)

A unidade curricular foi concebida com base num modelo de aprendizagem **centrado no estudante e orientado por atividades**, promovendo:

- construção ativa do conhecimento  
- desenvolvimento progressivo de competências  
- reflexão crítica e aprendizagem autónoma  

Os materiais seguem princípios de ensino aberto, a distância e em rede, e foram desenvolvidos com o apoio de ferramentas de IA generativa, posteriormente avaliados, validados e estruturados pedagogicamente.

---

### 📁 `app/`

Contém um protótipo integrado composto por:

#### 📊 Aplicação de Learning Analytics

Sistema interativo que permite:

- acompanhamento do progresso do estudante  
- visualização de métricas de aprendizagem  
- avaliação formativa com feedback imediato  
- gamificação (pontos, badges, ranking)  
- apoio à tomada de decisão pedagógica pelo docente  

#### 🤖 Tutor Inteligente (RAG)

Sistema baseado em LLM que permite:

- responder a perguntas com base nos materiais da disciplina  
- fornecer explicações contextualizadas  
- apoiar o estudo autónomo  
- reforçar a autorregulação da aprendizagem  

---

## 🔐 Acesso à Aplicação

A aplicação encontra-se protegida por autenticação simples (para fins de demonstração). As credenciais encontram-se no CV e no projeto pedagógico do candidato.

---

## 🤖 Aplicação RAG

### 🎯 Objetivo

O tutor RAG foi desenvolvido como suporte pedagógico, permitindo:

- exploração interativa dos conteúdos  
- reforço da aprendizagem autónoma  
- apoio à autorregulação  
- compreensão prática de sistemas baseados em LLM  

---

### ⚙️ Funcionamento

O sistema segue uma arquitetura RAG composta por:

1. **Indexação dos materiais**
   - extração de conteúdo dos livros base  
   - segmentação em excertos  
   - criação de embeddings vetoriais  

2. **Recuperação de informação**
   - pesquisa semântica (FAISS)  
   - seleção de excertos relevantes  

3. **Geração de resposta**
   - utilização de LLM  
   - resposta condicionada ao contexto recuperado  

---

### 🧠 Características principais

- respostas fundamentadas em evidência (*grounded*)  
- redução de alucinações  
- identificação explícita das fontes  
- adaptação pedagógica das respostas  
- integração com o percurso de aprendizagem do estudante  

---

### ⚠️ Natureza do Protótipo

Tanto a aplicação de analytics como o tutor RAG são **protótipos funcionais**, desenvolvidos com objetivos pedagógicos e de demonstração.

O tutor RAG utiliza atualmente:

- **Google Gemini API**

No entanto, a arquitetura foi concebida para ser **agnóstica ao modelo**, podendo ser adaptada para:

- modelos open source (ex: Llama, Mistral, Mixtral)  
- execução local ou em infraestrutura institucional  
- integração com serviços próprios da Universidade Aberta  

Esta flexibilidade é fundamental para:

- garantir soberania tecnológica  
- reduzir dependência de serviços externos  
- controlar custos e privacidade  

---

## 🌐 Demonstração

A aplicação encontra-se disponível online:

👉 https://mindioruab.streamlit.app/

> ⚠️ Nota: A aplicação pode demorar alguns segundos a iniciar caso esteja em modo de repouso.

---

## 🎓 Proposta Pedagógica

A unidade curricular segue um modelo de **activity-based learning**, onde a aprendizagem é estruturada em atividades progressivas.

O curso promove competências como:

- pensamento crítico  
- criatividade e inovação  
- colaboração  
- comunicação  

A abordagem integra:

- conteúdos teóricos estruturados  
- atividades práticas orientadas  
- avaliação contínua  
- feedback formativo  

A aplicação de analytics e o tutor RAG funcionam como **instrumentos de mediação pedagógica**, apoiando:

- a aprendizagem autónoma  
- a reflexão  
- a tomada de decisão  

---

## 📊 Avaliação e Feedback

O modelo inclui:

- microavaliações (miniquizzes)  
- feedback imediato  
- avaliação contínua  
- reflexão estruturada  

Os dados recolhidos permitem:

- acompanhar o progresso  
- identificar dificuldades  
- apoiar intervenções pedagógicas  

---

## 🔬 Ligação à Investigação

O projeto está alinhado com investigação nas áreas de:

- Explainable Artificial Intelligence (XAI)  
- interação humano-IA  
- sistemas de apoio à decisão  
- avaliação de explicações  

O sistema RAG reflete preocupações centrais como:

- confiabilidade  
- controlo de comportamento  
- explicabilidade  
- transparência  

---

## 🚀 Tecnologias Utilizadas

- Python  
- Streamlit  
- FAISS (vector search)  
- Sentence Transformers  
- Google Gemini API  
- arquitetura RAG  

---

## 📌 Considerações Finais

Este projeto demonstra:

- integração entre ensino, investigação e prática  
- aplicação de IA confiável em contexto educativo  
- desenvolvimento de sistemas reais baseados em LLM  
- utilização de IA como suporte à aprendizagem  

O repositório evidencia não apenas a proposta pedagógica, mas também a sua **implementação concreta**, alinhada com modelos contemporâneos de educação digital centrada no estudante.
# Plataforma de Inteligência Operacional — VendaMais

## Descrição do Projeto

Este projeto tem como objetivo o desenvolvimento de uma Plataforma de Inteligência Operacional para a empresa VendaMais Distribuidora Ltda.

A solução visa automatizar a coleta, processamento e visualização de dados provenientes do sistema ERP da empresa, permitindo que áreas como Comercial, Estoque, Financeiro e Logística tenham acesso a indicadores atualizados com defasagem máxima de 24 horas.

---

## Integrantes

Jorge  
https://github.com/Dutra04  

Nicolas  
https://github.com/nicolaskmb  

Thales  
https://github.com/thalesnap  

Vladimir  
https://github.com/vladimirlima  

---

## Estrutura do Repositório

```text
docs/
├── c4/
│ ├── 01-context.png # Diagrama C4 Nível 1 (Contexto)
│ ├── 02-container.png # Diagrama C4 Nível 2 (Containers)
│
├── adr/
│ ├── ADR-001.md # Decisão: Estratégia de ingestão
│ ├── ADR-002.md # Decisão: Estratégia de armazenamento
│
README.md
```

---

## Navegação da Documentação

### Diagramas C4

C4 Nível 1 — Contexto  
Representa a interação entre o sistema, usuários e sistemas externos.  
Caminho: docs/c4/01-context.png

C4 Nível 2 — Containers  
Detalha os componentes internos da solução e suas responsabilidades.  
Caminho: docs/c4/02-container.png

---

### Architecture Decision Records (ADR)

ADR-001 — Estratégia de Ingestão  
Define o uso de Azure Functions no modelo serverless para extração de dados.  
Caminho: docs/adr/ADR-001.md

ADR-002 — Estratégia de Armazenamento  
Define o uso de Azure SQL Database como base estruturada e Blob Storage para dados brutos.  
Caminho: docs/adr/ADR-002.md


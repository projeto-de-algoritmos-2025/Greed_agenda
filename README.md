# Greed_agenda

# Agenda Inteligente

Aplicativo de agenda com interface gráfica em Python (Tkinter), que permite cadastrar, visualizar e **otimizar tarefas automaticamente** com base no algoritmo de _Interval Scheduling_.

## Funcionalidades

- Adicionar tarefas com:
  - Título
  - Horário de início e término
  - Prioridade (1 a 5)
- Visualizar todas as tarefas cadastradas
- Otimizar automaticamente as tarefas (selecionar o maior número de tarefas não sobrepostas)
- Excluir tarefas
- Persistência local de dados (`tasks.json`)

## Algoritmo de Otimização

O botão **"Otimizar Agenda"** aplica o algoritmo **Interval Scheduling**, que seleciona o maior subconjunto de tarefas compatíveis entre si (sem sobreposição), maximizando o aproveitamento do tempo.





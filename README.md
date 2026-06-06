## Monitoramento de Sistemas Energéticos

Sistema de monitoramento energético de missão espacial desenvolvido em Python, sem dependências externas.

## Funcionalidades

- Coleta de dados dos sensores da missão: temperatura dos painéis, geração de energia solar, sinal de comunicação e nível de bateria
- Classificação automática de cada sensor em **NORMAL**, **ATENÇÃO** ou **CRÍTICO**
- Geração de alertas com respostas automatizadas para cada situação crítica detectada
- **Índice de saúde da missão**: score geral de 0 a 100 calculado com pesos por relevância energética, classificando a missão como ESTÁVEL, EM RISCO ou CRÍTICA
- **Análise preditiva**: a partir da segunda medição, o sistema identifica tendências de queda ou alta nos sensores e projeta o valor esperado na próxima leitura, permitindo agir antes que uma situação crítica ocorra
- Sugestões de sustentabilidade energética baseadas nos dados inseridos
- Relatório geral da sessão com médias, saúde média da missão e histórico de alertas

## Navegação

| Opção | Descrição |
|-------|-----------|
| [1] Registrar monitoramento | Insere dados e exibe análise completa |
| [2] Relatório geral | Resume todas as medições da sessão |
| [0] Encerrar | Finaliza o programa |

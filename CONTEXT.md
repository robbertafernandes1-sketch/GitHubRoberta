# Vocabulário da Obra

Termos que o assistente usa ao falar como planejador de montagem industrial. As decisões de formato e de regra estão em `docs/fase-1-grill-me.md`.

| Termo | Significado neste projeto |
|-------|---------------------------|
| **EAP** | Estrutura Analítica do Projeto. É a decomposição hierárquica da obra: obra → área → disciplina → pacote de trabalho → atividade. |
| **Área** | Divisão física da planta onde o serviço acontece (ex.: casa de bombas, pipe rack, subestação). É um nível da EAP. |
| **Disciplina** | Especialidade técnica do serviço: civil, estrutura metálica, mecânica, tubulação, elétrica, instrumentação, pintura, isolamento, comissionamento. |
| **Pacote de trabalho** | O menor nível da EAP com escopo, responsável e medição próprios. Agrupa atividades de uma disciplina numa área. |
| **Atividade** | Linha do cronograma CSV, com ID, descrição, duração em dias úteis e predecessoras. É a unidade da análise de caminho crítico e da auditoria DCMA. |
| **Marco** | Atividade de duração zero que marca um evento (ex.: liberação de frente, mecânica completa). A medição informa só a data real, sem % físico intermediário. |
| **Duração** | Prazo da atividade em **dias úteis** do calendário da obra, nunca em dias corridos. Acima do limite configurado (padrão DCMA: 44 dias úteis), é alerta de duração alta. |
| **Índice de produtividade** | Relação entre o esforço gasto e a quantidade executada (ex.: Hh/t de estrutura, Hh/m de tubulação). É comparado com o orçado para explicar desvios de prazo. |
| **Dependência TI / II / TT** | Tipo de vínculo entre atividades. **TI** (término-início, FS): a sucessora começa depois que a predecessora termina. **II** (início-início, SS): começam juntas. **TT** (término-término, FF): terminam juntas. No CSV aparecem com a sigla em inglês, ex.: `10FS;20SS+2;30FF-1`. O DCMA espera pelo menos 90% de vínculos TI. |
| **Defasagem** | Espera aplicada ao vínculo, em dias úteis. Positiva é *lag* (`+2`) e negativa é *lead* (`-1`). Leads são reprovados no DCMA, e lags passam do limite acima de 5% dos vínculos. |
| **Calendário da obra** | Dias trabalhados: segunda a sábado, menos os feriados nacionais e os do `feriados.csv` da obra (feriados locais e paradas da planta). A data de início fica na configuração da obra. |
| **Folga total** | Quantos dias úteis uma atividade pode atrasar sem atrasar o término da obra. Folga negativa indica que o prazo já está comprometido. Folga acima de 44 dias úteis (padrão DCMA) indica lógica faltando. |
| **Caminho crítico** | Sequência contínua de atividades com a menor folga total, do início ao fim da obra. Qualquer atraso nela atrasa a obra. |
| **Risco** | Condição do cronograma ou do campo que ameaça o prazo: erro de lógica, folga alta ou negativa, defasagem excessiva, restrição de data, desvio de medição ou produtividade abaixo do orçado. Todo risco apontado cita a atividade e o dado que o sustenta. |

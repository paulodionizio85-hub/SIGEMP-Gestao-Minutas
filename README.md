**Título: 🏢 SIGEMP - Sistema Interno de Gestão de Minutas**

**O que é**: Uma breve explicação (copie o Item 2 do seu trabalho).

**Tecnologias**: Liste Python, MySQL, HTML e CSS.

**🌟 Destaque**: **Privacidade desde a Concepção (Privacy by Design) e LGPD**

O grande diferencial do SIGEMP é a aplicação prática da Lei Geral de Proteção de Dados (LGPD) no dia a dia do Tribunal, garantindo a segurança dos dados dos jurisdicionados sem perder a agilidade do fluxo de trabalho da equipe.

Para resolver o risco de exposição desnecessária de dados sensíveis na tela do sistema (onde atuam diariamente assessores e estagiários), o projeto utiliza a técnica de Pseudonimização com Separação de Bases:

**🔒 Zona Segura (Dados Reais)**: Os nomes verdadeiros, CPFs e dados médicos das partes ficam isolados em uma tabela de banco de dados estritamente restrita (tb_processo_real), protegida e acessível apenas por usuários com permissão máxima (Magistrado).

**✅ Zona Operacional (GAB-ID)**: No painel visual de tarefas (Kanban), a interface não recebe os dados reais. O servidor processa a regra de negócio e envia para a tela apenas um código identificador fictício gerado automaticamente (Ex: GAB-101/26).

**🎯 O Resultado**: A equipe consegue triar, redigir e revisar as minutas operando unicamente com o GAB-ID. O nome real do cidadão nunca transita ou fica exposto na tela de gestão diária do gabinete, mitigando drasticamente o risco de vazamentos acidentais dentro da Circunscrição Judiciária.

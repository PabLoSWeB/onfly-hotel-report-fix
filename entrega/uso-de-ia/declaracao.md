# Declaração de uso de IA

**Ferramenta e modelo:** Claude (Anthropic), Claude Sonnet 5.5, via claude.ai (chat).

## O que a IA fez

- Converteu o projeto Python do desafio para Java/Spring Boot, mantendo os defeitos originais, porque eu não domino Python.
- Depois, converteu de volta para Python a minha versão em Java com as correções, aplicando as correções no código Python original.
- Identificou que o limite de 200 registros na leitura do CSV continuava presente.
- Escreveu os testes adicionais (`tests/test_extra_regressions.py`) e o rascunho do `README-ENTREGA.md`.
- Executou testes e conferências (pytest, ruff, validação contra a amostra do README e um cálculo independente do dataset completo).



**Ferramenta: Leo AI (Brave) Modelo: Qwen 3.6 35B**

[
1. Investigação de Erros de Lógica e Cálculo
A IA Leo me ajudou a interpretar erros específicos e a correlacioná-los com o código-fonte.

- Erro Non-terminating decimal expansion: A IA explicou que esse erro no Java BigDecimal ocorre apenas em divisões sem escala definida, orientando-me a usar divide(divisor, escala, RoundingMode) e a verificar onde a divisão estava sendo feita indevidamente.
- Valores Inflados e Negativos: Ao analisar meus logs, a IA identificou padrões (valores negativos em noites, diferenças exatas de 300.00 BRL) que apontaram para bugs específicos:
- Identificou que CurrencyConverter estava usando divide() em vez de multiply() para conversão de câmbio.

2. Correção de Regras de Negócio
- Ordenação: A IA identificou que Comparator.reverseOrder() estava sendo declarado como uma linha sem efeito.

3. Diagnóstico e Debug
- A IA me orientou sobre como estruturar logs de debug para isolar variáveis, permitindo que eu verificasse se o erro vinha do parser, da conversão ou da agregação. Também me ajudou a configurar os argumentos de execução no VS Code e Maven para validar a amostra de entrada (exemplo-validacao.csv).]

## O que eu fiz

- [Explicado no `README-ENTREGA.md`].

## Sessão

A exportação da conversa está em `sessao.md` (ou `sessao-01.md`, `sessao-02.md`...) nesta pasta.

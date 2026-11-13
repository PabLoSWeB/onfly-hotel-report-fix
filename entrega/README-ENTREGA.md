# Relatório de investigação


## Defeitos corrigidos

1. Conversão de câmbio usava `float` e dividia pela taxa (`services/currency_converter.py`).
2. Cálculo de noites usava a diferença do dia do mês, quebrando na virada de mês (`services/stay_calculator.py`).
3. `NO_SHOW` era tratado como faturável; só `CONFIRMED` deveria ser (`services/status_policy.py`).
4. Ranking `top_hotels` estava em ordem crescente de valor (`services/report_builder.py`).
5. A leitura do CSV de reservas parava em 200 registros, descartando 100 das 300 reservas do dataset (`repositories/csv_reservation_repository.py`).

## Causa raiz

1. `float(amount) / float(rate)`: operação invertida (a regra é `amount * rate`) e uso de `float` em dinheiro, o que perde exatidão.
2. `checkout.day - checkin.day` ignora mês e ano; o correto é `(checkout - checkin).days`.
3. `status != "CANCELLED"` é uma lista de exclusão incompleta; a regra correta é `status == "CONFIRMED"`.
4. `sorted` com chave `(amount, hotel_id)` ordena do menor para o maior valor; a chave correta é `(-amount, hotel_id)`.
5. Um `break` quando `len(rows) == 200` interrompia a leitura do arquivo antes do fim.

## Investigação e abordagem

- Rodei `pytest -q` no código original: 5 testes falhavam (câmbio, noites, status, ranking e regressão da amostra), o que apontou os defeitos 1 a 4.
- O defeito 5 não é detectado por nenhum teste fornecido. Percebi comparando o total de reservas do relatório com o número de linhas do `data/reservas_hoteis.csv` (300 linhas, mas o relatório contava no máximo 200).
- Cada correção foi validada contra as regras do README do desafio e contra a amostra de validação.
- Conferi o relatório do dataset completo com um cálculo independente (script separado, só com `csv` e `Decimal`), e os números bateram.
- Adicionei `tests/test_extra_regressions.py` (testes novos, sem alterar os fornecidos), incluindo um teste para o limite de 200 registros.

[Contexto: O teste técnico foi entregue em Python. No entanto, minha stack principal de desenvolvimento é Java Spring Boot. Para garantir que eu compreendesse profundamente a lógica de negócio pedi que a IA convertesse o código Python em Java Spring Boot, ela utilizou uma abordagem de "Rubber Duck Debugging" via Tradução:
1. Tradução Reversa: A IA Claude a lógica central do projeto Python para Java Spring Boot. A partir do readme pude observar onde a implementação divergia das regras de negócio (ex: uso de float vs Decimal, lógica de datas, conversão cambial).
2. Isolamento de Bugs: Corrigi os defeitos críticos na versão Java, validando-os contra a amostra de dados (exemplo-validacao.csv) até obter precisão nos cálculos de noites, valores BRL e ordenação.
3. Aplicação no Original: Com a lógica validada e os bugs mapeados na tradução, A IA aplicou as mesmas correções lógicas no código Python original, garantindo que a entrega final atenda aos requisitos técnicos (Python 3).]

## Como validar

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

pytest -q

PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json
```

Esperado na amostra: 12 reservas, 9 confirmadas, 2 canceladas, 1 no-show, 28 noites, total `7566.00`, média `270.21`.

## Resultado dos testes

- Antes das correções: `5 failed` (testes fornecidos).
- Depois das correções: `9 passed` (5 fornecidos, inalterados, + 4 adicionais). `ruff check` sem apontamentos.
- Dataset completo (`data/reservas_hoteis.csv`): 300 reservas, 235 confirmadas, 1347 noites, total `396170.00`, média `294.11`.
- Amostra de validação: summary, `by_month` e `top_hotels` idênticos ao esperado no README.
- Observação: a soma dos `total_brl` mensais pode diferir em centavos do total geral, pois o arredondamento é feito só na serialização, conforme o README.



**Documentação original em escrita em Java**
## Defeitos corrigidos
- [1. StayCalculator.calculateRoomNights()]
- [2. CurrencyConverter.convertToBrl()]
- [3. StatusPolicy.isBillable()]
- [4. ReportBuilder.build() ordenação do top_hotels]


## Causa raiz
- [1. Usava getDayOfMonth() (só dia do mês) em vez de ChronoUnit.DAYS.between() para calcular a diferença real de datas entre check-in e check-out(isso em Java).]
- [2. Estava dividindo ao invés de multiplicar para converter moeda estrangeira para BRL, lógica errada para conversão.]
- [3. A lógica não incluia o status NO_SHOW (!CANCELLED && "!NO_SHOW") e era uma lógica negativa. permitia que status inesperados fossem tratados como faturáveis, modifiquei a lógica e coloquei apenas equals("CONFIRMED").]
- [3. Comparator.reverseOrder() era uma linha sem efeito pois precisava ser passado como segundo argumento de comparing(), resultando em ordenação crescente quando o readme exigia decrescente.]

## Investigação e abordagem
- [Todas as mudanças foram pensadas e identificadas por meio da consulta do Readme enviado no teste. Segui as regras de negócio e o que cada parte dizia. Por exemplo: nesta parte de Cambio que diz "Câmbio
- amount está na moeda de currency.
- Converta com **amount * rate_to_brl**, usando a tabela data/taxas\_cambio.csv.
- Todas as moedas do dataset têm taxa.
" e em outra parte: "Use **Decimal, nunca float**, no dinheiro." A partir dessas informaçõe foi possível perceber no código orinal os erros: A conversão retornava a **divisão(ao invés da multiplicação)** do dinheiro(amount) sendo **float(ao invés de Decimal)**. A linha de raciocínio foi essa em geral, **verificando cada exigência** da Regra de Servico no Readme e **comparando** com o código original.]

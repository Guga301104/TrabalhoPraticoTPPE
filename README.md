# Trabalho Prático — Curadoria de Dados Científicos

Deduplicação de nomes de autores em repositórios de informações científicas,
desenvolvida com **TDD**.

## Integrantes do grupo

| Nome | Matrícula |
|------|-----------|
| Gustavo Gontijo Lima | 231011426 |
| Mylena Trindade de Mendonça | 231035769 |
| João Pedro Ferreira Moraes | 231028989 |
| Pedro Henrique Fernandino da Silva | 221031354 |

## Linguagem e framework

- **Linguagem Orientada a Objetos:** Python 3 (testado em 3.14.2)
- **Framework de testes unitários:** pytest **9.0.3**

O pytest atende a todos os recursos exigidos no enunciado:

| Recurso exigido | Como é usado |
|-----------------|--------------|
| Suítes de testes | Cada caso tem uma classe `Test...` agrupando seus testes |
| Categorias de testes | Markers `@pytest.mark.caso1..caso5`, `excecao`, `parametrizado` (em `pytest.ini`) |
| Testes parametrizados | `@pytest.mark.parametrize` com ≥ 2 conjuntos de dados por caso |
| Testes de exceção | `pytest.raises(ValueError)` em cada caso |

## Estrutura

```
curadoria-tdd/
├── curadoria/
│   ├── __init__.py
│   ├── normalizacao.py   # normalizacao e equivalencia de nomes
│   └── casos.py          # as 5 unidades de deduplicacao
├── tests/
│   ├── test_caso1_tipografia.py
│   ├── test_caso2_sobrenome_iniciais.py
│   ├── test_caso3_particulas.py
│   ├── test_caso4_iniciais_agrupadas.py
│   └── test_caso5_ids.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Os cinco casos (unidades)

| Caso | Unidade (`curadoria/casos.py`) | O que resolve |
|------|--------------------------------|----------------|
| 1 | `unificar_grafia(variantes)` | Acentuacao, apostrofo/crase, cedilha → grafia correta |
| 2 | `unificar_abreviacao_sobrenome(completo, abreviado)` | `Seabra A M` → `Ana de Mattos Seabra` |
| 3 | `unificar_particulas(variantes)` | Omissao de `de`/`da` e ponto opcional |
| 4 | `unificar_iniciais_agrupadas(completo, agrupado)` | `SH Guaraldi` → `Sérgio Henrique Guaraldi` |
| 5 | `unificar_ids(registros)` | Mapeia todos os ids do mesmo autor para o **menor** |

## Como executar os testes

Requer Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate  

python3 -m pip install -r requirements.txt

python3 -m pytest
```

**Resultado esperado:** `33 passed`.

Rodar uma categoria específica (por marker):

```bash
python3 -m pytest -m caso1        # só o caso 1
python3 -m pytest -m excecao      # só os testes de excecao
```

Markers disponíveis: `caso1`..`caso5`, `excecao`, `parametrizado`.

### Sobre condição de corrida

Todas as unidades são **funções puras**,
portanto os testes podem ser executados em qualquer ordem ou em paralelo sem
condição de corrida.

Isso foi verificado executando a suíte em paralelo com o `pytest-xdist` e em
ordem aleatória com o `pytest-randomly`, sempre com `33 passed`. Os dois 
são ferramentas de verificação e não fazem parte das dependências do
projeto (não estão no `requirements.txt`). Para reproduzir:

```bash
python3 -m pip install pytest-xdist pytest-randomly
python3 -m pytest -n auto         # em paralelo (pytest-xdist)
python3 -m pytest                 # ordem aleatória (pytest-randomly)
```

## Etapa 2 — Refatoração

Sobre o código da Etapa 1 foram aplicadas três operações de refatoração, cada
uma em seu próprio commit:

| Operação | Alvo | Resultado |
|----------|------|-----------|
| Extrair Método | `_classificar()` | função `_classificar_token()` |
| Substituir Método por Objeto-Método | `equivalentes()` | classe `_ComparadorEquivalencia` |
| Extrair Classe | módulo `normalizacao` | classe `Nome` |

Os testes não foram alterados e continuam passando (`33 passed`), comprovando
que o comportamento foi preservado.

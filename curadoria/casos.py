from .normalizacao import (
    Nome,
    equivalentes,
    forma_canonica,
    normalizar_apostrofo,
    remover_acentos,
)


def _chave_tipografica(nome: str) -> str:
    return remover_acentos(normalizar_apostrofo(nome)).lower().strip()


# 1: diferencas de grafia

def unificar_grafia(variantes) -> str:
    variantes = [v for v in variantes if v and v.strip()]
    if not variantes:
        raise ValueError("Lista de variantes vazia.")

    chaves = {_chave_tipografica(v) for v in variantes}
    if len(chaves) != 1:
        raise ValueError(
            "As variantes não diferem apenas por grafia (use o caso adequado)."
        )

    return normalizar_apostrofo(max(variantes, key=lambda v: Nome(v).pontuacao())).strip()


# 2: sobrenome + iniciais dos nomes

def unificar_abreviacao_sobrenome(completo: str, abreviado: str) -> str:
    if not equivalentes(completo, abreviado):
        raise ValueError("Os nomes não representam o mesmo autor.")
    return forma_canonica([completo, abreviado])


# 3: 'de' e ponto opcional

def unificar_particulas(variantes) -> str:
    return forma_canonica(variantes)


# 4: iniciais dos nomes agrupadas + sobrenome

def unificar_iniciais_agrupadas(completo: str, agrupado: str) -> str:
    if not Nome(agrupado).tem_grupo_iniciais():
        raise ValueError("A versão informada não possui iniciais agrupadas.")
    if not equivalentes(completo, agrupado):
        raise ValueError("Os nomes não representam o mesmo autor.")
    return forma_canonica([completo, agrupado])

# 5: ids diferentes

def unificar_ids(registros):
    if not registros:
        raise ValueError("Nenhum registro fornecido.")

    ids = []
    for registro in registros:
        rid = registro[0]
        if isinstance(rid, bool) or not isinstance(rid, int) or rid <= 0:
            raise ValueError(f"ID inválido: {rid!r}")
        ids.append(rid)

    menor = min(ids)
    return [(menor, nome) for (_id, nome) in registros]

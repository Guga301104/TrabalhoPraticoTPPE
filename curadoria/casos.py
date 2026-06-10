from .normalizacao import (
    equivalentes,
    forma_canonica,
    normalizar_apostrofo,
    remover_acentos,
    tem_grupo_iniciais,
    _pontuacao,
)


def _chave_tipografica(nome: str) -> str:
    return remover_acentos(normalizar_apostrofo(nome)).lower().strip()


# 1: diferencas de grafia

def unificar_grafia(variantes) -> str:
    variantes = [v for v in variantes if v and v.strip()]
    if not variantes:
        raise ValueError("lista de variantes vazia")

    chaves = {_chave_tipografica(v) for v in variantes}
    if len(chaves) != 1:
        raise ValueError(
            "as variantes nao diferem apenas por grafia"
        )

    return normalizar_apostrofo(max(variantes, key=_pontuacao)).strip()


# 2: sobrenome + iniciais dos nomes 

def unificar_abreviacao_sobrenome(completo: str, abreviado: str) -> str:
    if not equivalentes(completo, abreviado):
        raise ValueError("os nomes sao do mesmo autor")
    return forma_canonica([completo, abreviado])


# 3: 'de' e ponto opcional

def unificar_particulas(variantes) -> str:
    return forma_canonica(variantes)


# 4: iniciais dos nomes agrupadas + sobrenome

def unificar_iniciais_agrupadas(completo: str, agrupado: str) -> str:
    if not tem_grupo_iniciais(agrupado):
        raise ValueError("essa versao nao possui iniciais agrupadas")
    if not equivalentes(completo, agrupado):
        raise ValueError("os nomes nao sao do mesmo autor")
    return forma_canonica([completo, agrupado])


# 5: ids diferentes

def unificar_ids(registros):
    if not registros:
        raise ValueError("nenhum registro fornecido")

    ids = []
    for registro in registros:
        rid = registro[0]
        if isinstance(rid, bool) or not isinstance(rid, int) or rid <= 0:
            raise ValueError(f"id invalido: {rid!r}")
        ids.append(rid)

    menor = min(ids)
    return [(menor, nome) for (_id, nome) in registros]

import unicodedata
from collections import Counter

PARTICULAS = {"de", "da", "do", "dos", "das", "e", "di", "du"}
_APOSTROFOS = ["`", "´", "’", "‘", "'"]


def remover_acentos(texto: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalizar_apostrofo(texto: str) -> str:
    for ch in _APOSTROFOS:
        texto = texto.replace(ch, "'")
    return texto


def _reordenar_virgula(nome: str) -> str:
    if "," in nome:
        antes, depois = nome.split(",", 1)
        return f"{depois.strip()} {antes.strip()}".strip()
    return nome


# --- MÉTODO EXTRAÍDO de `_classificar` ---
def _classificar_token(bruto: str):
    limpo = bruto.strip(".,")
    if not limpo:
        return ("vazio", None)

    base = remover_acentos(limpo).lower()

    if limpo.isupper() and len(limpo) >= 2 and base not in PARTICULAS:
        return ("grupo_iniciais", [c.lower() for c in limpo if c.isalpha()])
    if base in PARTICULAS:
        return ("particula", base)
    if len(limpo) == 1:
        return ("inicial", base)
    return ("cheio", base)


def _classificar(nome: str):
    nome = _reordenar_virgula(normalizar_apostrofo(nome))

    cheios, iniciais, particulas = [], [], []
    for bruto in nome.split():
        categoria, valor = _classificar_token(bruto)
        if categoria == "grupo_iniciais":
            iniciais.extend(valor)
        elif categoria == "inicial":
            iniciais.append(valor)
        elif categoria == "particula":
            particulas.append(valor)
        elif categoria == "cheio":
            cheios.append(valor)

    return cheios, iniciais, particulas


def equivalentes(nome_a: str, nome_b: str) -> bool:
    cheios_a, ini_a, _ = _classificar(nome_a)
    cheios_b, ini_b, _ = _classificar(nome_b)

    if len(cheios_a) + len(ini_a) != len(cheios_b) + len(ini_b):
        return False

    cnt_a, cnt_b = Counter(cheios_a), Counter(cheios_b)
    comuns = cnt_a & cnt_b
    resto_a = list((cnt_a - comuns).elements())
    resto_b = list((cnt_b - comuns).elements())

    ini_a, ini_b = Counter(ini_a), Counter(ini_b)

    for palavra in resto_a:
        if ini_b[palavra[0]] > 0:
            ini_b[palavra[0]] -= 1
        else:
            return False
    for palavra in resto_b:
        if ini_a[palavra[0]] > 0:
            ini_a[palavra[0]] -= 1
        else:
            return False

    return +ini_a == +ini_b


def _pontuacao(nome: str):
    cheios, _iniciais, particulas = _classificar(nome)
    n_acentos = sum(1 for ch in nome if ch.isalpha() and remover_acentos(ch) != ch)
    return (len(cheios), len(particulas), n_acentos, len(nome))


def forma_canonica(variantes) -> str:
    variantes = [v for v in variantes if v and v.strip()]
    if not variantes:
        raise ValueError("Lista de variantes vazia.")

    referencia = variantes[0]
    for v in variantes[1:]:
        if not equivalentes(referencia, v):
            raise ValueError(f"'{v}' não é equivalente a '{referencia}'.")

    melhor = max(variantes, key=_pontuacao)
    return normalizar_apostrofo(melhor).strip()


def tem_grupo_iniciais(nome: str) -> bool:
    for bruto in normalizar_apostrofo(nome).split():
        if _classificar_token(bruto)[0] == "grupo_iniciais":
            return True
    return False

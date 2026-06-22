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


# --- Refatoração 1: Extrair Método (extraído de `_classificar`) ---
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


# --- Refatoração 3: Extrair Classe (extraída do módulo `normalizacao`) ---
class Nome:
    def __init__(self, bruto: str):
        self.bruto = bruto
        self.cheios, self.iniciais, self.particulas = _classificar(bruto)

    def total_componentes(self) -> int:
        return len(self.cheios) + len(self.iniciais)

    def pontuacao(self):
        n_acentos = sum(
            1 for ch in self.bruto if ch.isalpha() and remover_acentos(ch) != ch
        )
        return (len(self.cheios), len(self.particulas), n_acentos, len(self.bruto))

    def tem_grupo_iniciais(self) -> bool:
        tokens = normalizar_apostrofo(self.bruto).split()
        return any(_classificar_token(t)[0] == "grupo_iniciais" for t in tokens)


# --- Refatoração 2: Substituir Método por Objeto-Método (de `equivalentes`) ---
class _ComparadorEquivalencia:

    def __init__(self, nome_a: str, nome_b: str):
        self.a = Nome(nome_a)
        self.b = Nome(nome_b)

    def calcular(self) -> bool:
        if self.a.total_componentes() != self.b.total_componentes():
            return False

        self._separar_comuns()
        if not self._casar_extensos(self.resto_a, self.ini_b):
            return False
        if not self._casar_extensos(self.resto_b, self.ini_a):
            return False

        return +self.ini_a == +self.ini_b

    def _separar_comuns(self):
        cnt_a, cnt_b = Counter(self.a.cheios), Counter(self.b.cheios)
        comuns = cnt_a & cnt_b
        self.resto_a = list((cnt_a - comuns).elements())
        self.resto_b = list((cnt_b - comuns).elements())
        self.ini_a = Counter(self.a.iniciais)
        self.ini_b = Counter(self.b.iniciais)

    @staticmethod
    def _casar_extensos(restos, iniciais) -> bool:
        for palavra in restos:
            if iniciais[palavra[0]] > 0:
                iniciais[palavra[0]] -= 1
            else:
                return False
        return True


def equivalentes(nome_a: str, nome_b: str) -> bool:
    return _ComparadorEquivalencia(nome_a, nome_b).calcular()


def forma_canonica(variantes) -> str:
    variantes = [v for v in variantes if v and v.strip()]
    if not variantes:
        raise ValueError("Lista de variantes vazia.")

    referencia = variantes[0]
    for v in variantes[1:]:
        if not equivalentes(referencia, v):
            raise ValueError(f"'{v}' não é equivalente a '{referencia}'.")

    melhor = max(variantes, key=lambda v: Nome(v).pontuacao())
    return normalizar_apostrofo(melhor).strip()

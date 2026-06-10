import pytest

from curadoria import unificar_particulas


@pytest.mark.caso3
class TestUnificarParticulas:

    @pytest.mark.parametrizado
    @pytest.mark.parametrize(
        "variantes, esperado",
        [
            # 1: sem 'de' e ponto opcional
            (
                ["Luiz de Oliveira de Souza", "Luiz Oliveira Souza",
                 "Luiz de O. de Souza"],
                "Luiz de Oliveira de Souza",
            ),
            # 2: apenas duas variantes
            (
                ["Veronica de Oliveira Moreira", "V de O Moreira"],
                "Veronica de Oliveira Moreira",
            ),
            # 3: forma com virgula e 'de'
            (
                ["Souza, Luiz de Oliveira", "Luiz de Oliveira de Souza"],
                "Luiz de Oliveira de Souza",
            ),
        ],
    )
    def test_prefere_forma_completa_com_particulas(self, variantes, esperado):
        assert unificar_particulas(variantes) == esperado

    def test_uma_variante(self):
        assert unificar_particulas(["Luiz de Oliveira de Souza"]) == \
            "Luiz de Oliveira de Souza"

    @pytest.mark.excecao
    def test_lista_vazia_levanta_excecao(self):
        with pytest.raises(ValueError):
            unificar_particulas([])

    @pytest.mark.excecao
    def test_autores_diferentes_levantam_excecao(self):
        with pytest.raises(ValueError):
            unificar_particulas(["Luiz de Oliveira de Souza", "Cassius de Souza"])

import pytest

from curadoria import unificar_grafia


@pytest.mark.caso1
class TestUnificarGrafia:

    @pytest.mark.parametrizado
    @pytest.mark.parametrize(
        "variantes, esperado",
        [
            # 1: apostrofo/crase e acentuacao
            (
                ["Monica Hirata Sant`anna", "Mônica Hirata Sant’anna",
                 "Mônica Hirata Sant'anna"],
                "Mônica Hirata Sant'anna",
            ),
            # 2: acentuacao ausente
            (
                ["Sergio Henrique Guaraldi", "Sérgio Henrique Guaraldi"],
                "Sérgio Henrique Guaraldi",
            ),
            # 3: cedilha + acento
            (
                ["Raphael Goncalves Viana", "Raphael Gonçalves Viana"],
                "Raphael Gonçalves Viana",
            ),
            # 4: veronica com acento
            (
                ["Veronica de Oliveira Moreira", "Verônica de Oliveira Moreira"],
                "Verônica de Oliveira Moreira",
            ),
        ],
    )
    def test_unifica_para_grafia_correta(self, variantes, esperado):
        assert unificar_grafia(variantes) == esperado

    def test_variante_unica_e_idempotente(self):
        assert unificar_grafia(["Mônica Hirata Sant'anna"]) == \
            "Mônica Hirata Sant'anna"

    @pytest.mark.excecao
    def test_lista_vazia_levanta_excecao(self):
        with pytest.raises(ValueError):
            unificar_grafia([])

    @pytest.mark.excecao
    def test_nomes_estruturalmente_diferentes_levantam_excecao(self):
        with pytest.raises(ValueError):
            unificar_grafia(["Ana de Mattos Seabra", "Seabra A M"])

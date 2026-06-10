import pytest

from curadoria import unificar_iniciais_agrupadas


@pytest.mark.caso4
class TestUnificarIniciaisAgrupadas:

    @pytest.mark.parametrizado
    @pytest.mark.parametrize(
        "completo, agrupado, esperado",
        [
            # 1: VC Junior
            ("Vanilda Cristina Junior", "VC Junior", "Vanilda Cristina Junior"),
            # 2: SH Guaraldi
            ("Sérgio Henrique Guaraldi", "SH Guaraldi", "Sérgio Henrique Guaraldi"),
            # 3: AM Seabra
            ("Ana de Mattos Seabra", "AM Seabra", "Ana de Mattos Seabra"),
        ],
    )
    def test_unifica_para_versao_completa(self, completo, agrupado, esperado):
        assert unificar_iniciais_agrupadas(completo, agrupado) == esperado

    @pytest.mark.excecao
    def test_sem_iniciais_agrupadas_levanta_excecao(self):
        with pytest.raises(ValueError):
            unificar_iniciais_agrupadas("Cassius de Souza", "Souza C.")

    @pytest.mark.excecao
    def test_autores_diferentes_levantam_excecao(self):
        with pytest.raises(ValueError):
            unificar_iniciais_agrupadas("Vanilda Cristina Junior", "SH Guaraldi")

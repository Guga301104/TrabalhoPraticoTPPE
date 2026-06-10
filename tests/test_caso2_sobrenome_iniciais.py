import pytest

from curadoria import unificar_abreviacao_sobrenome


@pytest.mark.caso2
class TestUnificarAbreviacaoSobrenome:

    @pytest.mark.parametrizado
    @pytest.mark.parametrize(
        "completo, abreviado, esperado",
        [
            # 1: iniciais sem ponto
            ("Ana de Mattos Seabra", "Seabra A M", "Ana de Mattos Seabra"),
            # 2: iniciais com ponto
            ("Cassius de Souza", "Souza C.", "Cassius de Souza"),
            # 3: inicial antes do sobrenome
            ("Cassius de Souza", "C. Souza", "Cassius de Souza"),
            # 4: forma com virgula
            ("Ana de Mattos Seabra", "Seabra, A. M.", "Ana de Mattos Seabra"),
        ],
    )
    def test_unifica_para_versao_completa(self, completo, abreviado, esperado):
        assert unificar_abreviacao_sobrenome(completo, abreviado) == esperado

    def test_ordem_dos_argumentos_nao_importa(self):
        assert unificar_abreviacao_sobrenome("Seabra A M", "Ana de Mattos Seabra") \
            == "Ana de Mattos Seabra"

    @pytest.mark.excecao
    @pytest.mark.parametrize(
        "completo, abreviado",
        [
            ("Ana de Mattos Seabra", "Cassius de Souza"), 
            ("Cassius de Souza", "Souza D."),             
        ],
    )
    def test_autores_diferentes_levantam_excecao(self, completo, abreviado):
        with pytest.raises(ValueError):
            unificar_abreviacao_sobrenome(completo, abreviado)

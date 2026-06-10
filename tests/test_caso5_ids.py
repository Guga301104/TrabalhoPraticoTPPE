import pytest

from curadoria import unificar_ids


@pytest.mark.caso5
class TestUnificarIds:

    @pytest.mark.parametrizado
    @pytest.mark.parametrize(
        "registros, id_esperado",
        [
            # 1: Raphael Gonçalves Viana . menor id = 31298
            (
                [
                    (31298, "Raphael Goncalves Viana"),
                    (433094, "Raphael Gonçalves Viana"),
                    (549243, "Raphael Gonçalves Viana"),
                    (608297, "Raphael Gonçalves Viana"),
                    (746938, "Raphael Gonçalves Viana"),
                ],
                31298,
            ),
            # 2: Lílian Luíza Viana Vieira . menor id = 243351
            (
                [
                    (899639, "Lilian Luíza Viana Vieira"),
                    (243351, "Lílian Luíza Viana Vieira"),
                    (663795, "Lílian Luíza Viana Vieira"),
                ],
                243351,
            ),
        ],
    )
    def test_todos_mapeados_para_o_menor_id(self, registros, id_esperado):
        resultado = unificar_ids(registros)
        assert all(rid == id_esperado for rid, _nome in resultado)
        assert [nome for _id, nome in resultado] == \
            [nome for _id, nome in registros]

    def test_registro_unico(self):
        assert unificar_ids([(713897, "Yuri Vieira Faria")]) == \
            [(713897, "Yuri Vieira Faria")]

    @pytest.mark.excecao
    def test_lista_vazia_levanta_excecao(self):
        with pytest.raises(ValueError):
            unificar_ids([])

    @pytest.mark.excecao
    @pytest.mark.parametrize("id_invalido", [0, -5, "31298", None])
    def test_id_invalido_levanta_excecao(self, id_invalido):
        with pytest.raises(ValueError):
            unificar_ids([(id_invalido, "Fulano de Tal")])

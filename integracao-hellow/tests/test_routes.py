import unittest

from starlette.routing import Match

from routes.v1.canais import router


def http_scope(path: str, method: str) -> dict:
    return {
        "type": "http",
        "path": path,
        "method": method,
        "root_path": "",
        "scheme": "http",
        "query_string": b"",
        "headers": [],
        "server": ("test", 8001),
    }


class RouteMatchingTests(unittest.TestCase):
    def test_caminho_nao_uuid_nao_corresponde_a_rota_de_canal(self):
        matches = [
            route.matches(
                http_scope("/relacionamento/v1/consumidor", "POST")
            )[0]
            for route in router.routes
        ]

        self.assertTrue(all(match is Match.NONE for match in matches))

    def test_uuid_corresponde_a_rota_de_consulta(self):
        matches = [
            (route.path, route.matches(
                http_scope(
                    "/relacionamento/v1/canais/00000000-0000-0000-0000-000000000000",
                    "GET",
                )
            )[0])
            for route in router.routes
        ]

        self.assertIn(
            ("/relacionamento/v1/canais/{canal_id:uuid}", Match.FULL),
            matches,
        )


if __name__ == "__main__":
    unittest.main()

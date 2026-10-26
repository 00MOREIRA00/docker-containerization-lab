"""Popula o banco local com canais de exemplo."""

from uuid import NAMESPACE_URL, uuid5

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.canais import CanalCreate
from models.canais_db import Canal
from provider.database import SessionLocal


CANAIS = (
    ("pedidos-dev", "Pedidos de exemplo", "loja", "erp", "ativo", "dev"),
    ("estoque-dev", "Estoque de exemplo", "erp", "loja", "ativo", "dev"),
    ("clientes-dev", "Clientes de exemplo", "crm", "erp", "inativo", "dev"),
    ("pagamentos-staging", "Pagamentos de exemplo", "checkout", "financeiro", "ativo", "staging"),
    ("notas-staging", "Notas fiscais de exemplo", "erp", "fiscal", "inativo", "staging"),
    ("entregas-prod", "Entregas de exemplo", "logistica", "loja", "ativo", "prod"),
)


def popular_canais(session: Session) -> tuple[int, int]:
    """Insere exemplos ausentes sem alterar registros existentes."""
    exemplos = []
    for chave, nome, origem, destino, status, ambiente in CANAIS:
        dados = CanalCreate(
            nome=nome,
            sistema_origem=origem,
            sistema_destino=destino,
            status=status,
            ambiente=ambiente,
        )
        canal_id = uuid5(NAMESPACE_URL, f"dockerfile-trainer/seed/canais/{chave}")
        exemplos.append((canal_id, dados))

    ids = [canal_id for canal_id, _ in exemplos]
    existentes = set(session.scalars(select(Canal.id).where(Canal.id.in_(ids))))
    inseridos = 0

    for canal_id, dados in exemplos:
        if canal_id not in existentes:
            session.add(Canal(id=canal_id, **dados.model_dump(mode="json")))
            inseridos += 1

    return inseridos, len(existentes)


def main() -> None:
    with SessionLocal.begin() as session:
        inseridos, existentes = popular_canais(session)

    print(f"Seed concluído: {inseridos} canais inseridos, {existentes} já existentes.")


if __name__ == "__main__":
    main()

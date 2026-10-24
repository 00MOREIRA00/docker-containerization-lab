from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from provider.database import Base


class Canal(Base):
    __tablename__ = "canais"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )

    nome: Mapped[str] = mapped_column(String(100))
    sistema_origem: Mapped[str] = mapped_column(String)
    sistema_destino: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String(20))
    ambiente: Mapped[str] = mapped_column(String(20))

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

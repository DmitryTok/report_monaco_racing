from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.team_model import Team


class Driver(Base):
    __tablename__ = 'drivers'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(length=64))
    abbr: Mapped[str] = mapped_column(String(length=64), unique=True)

    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id', ondelete='CASCADE'))
    team: Mapped['Team'] = relationship()

    def __str__(self):
        return f'{self.id}: {self.name}'

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.driver_model import Driver
from app.db.models.race_model import Race
from app.db.models.stage_model import Stage


class Result(Base):
    __tablename__ = 'reports'

    id: Mapped[int] = mapped_column(primary_key=True)

    position: Mapped[int] = mapped_column(nullable=True)
    result: Mapped[str] = mapped_column()
    start_time: Mapped[datetime] = mapped_column()
    end_time: Mapped[datetime] = mapped_column()

    driver_id: Mapped[int] = mapped_column(
        ForeignKey('drivers.id', ondelete='CASCADE'), nullable=True)
    driver: Mapped['Driver'] = relationship()

    stage_id: Mapped[int] = mapped_column(
        ForeignKey('stages.id', ondelete='CASCADE'), nullable=True)
    stage: Mapped['Stage'] = relationship()

    race_id: Mapped[int] = mapped_column(
        ForeignKey('races.id', ondelete='CASCADE'), nullable=True)
    race: Mapped['Race'] = relationship()

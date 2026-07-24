from sqlalchemy.orm import Mapped, mapped_column 
from uuid import UUID,uuid4

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id : Mapped[UUID] = mapped_column(primary_key=True,default=uuid4)
    username: Mapped[str] = mapped_column(unique=True,nullable=False)
    email : Mapped[str] = mapped_column(unique=True,nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fullname: Mapped[str] = mapped_column(nullable=False)
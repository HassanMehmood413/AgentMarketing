from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, func
from .database  import Base


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    logs: Mapped[list["Log"]] = relationship(
        "Log", back_populates="user", cascade="all, delete-orphan"
    )

class Log(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profiles.id", ondelete="CASCADE"), index=True)
    agent: Mapped[str] = mapped_column(String, index=True)      # "research" | "writer"
    stage: Mapped[str] = mapped_column(String, index=True)      # e.g. "writer_delta", "compile_html"
    message: Mapped[str] = mapped_column(Text)                  # free text / JSON
    timestamp: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped[Profile] = relationship("Profile", back_populates="logs")
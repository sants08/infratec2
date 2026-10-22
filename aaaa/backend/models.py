from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome_sistema = Column(String(100), nullable=False, default="Infratec - Segurança no Trabalho")
    email = Column(String(150), unique=True, nullable=False, index=True)
    senha = Column(String(255), nullable=False)

    funcionarios = relationship("Funcionario", back_populates="usuario")


class EPI(Base):
    __tablename__ = "epi"

    id_epi = Column(Integer, primary_key=True, index=True)
    matricula = Column(Integer, ForeignKey("funcionario.matricula", ondelete="CASCADE"), nullable=False)
    epi_nome = Column(String(100), nullable=True)
    data_entrega_epi = Column(Date, nullable=False)
    validade_epi = Column(Date, nullable=False)
    status_epi = Column(String(20), nullable=False)

    funcionario = relationship("Funcionario", back_populates="epis")


class TipoInspecao(Base):
    __tablename__ = "tipo_inspecao"

    id_tipo_inspecao = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(100), nullable=False)

    inspecoes = relationship("Inspecao", back_populates="tipo_inspecao")


class Especialidade(Base):
    __tablename__ = "especialidade"

    id_especialidade = Column(Integer, primary_key=True, index=True)
    nome_especialidade = Column(String(100), unique=True, nullable=False)

    profissionais = relationship("Profissional", back_populates="especialidade")


class Curso(Base):
    __tablename__ = "curso"

    id_curso = Column(Integer, primary_key=True, index=True)
    nome_curso = Column(String(150), unique=True, nullable=False)

    treinamentos = relationship("Treinamento", back_populates="curso")


class Profissional(Base):
    __tablename__ = "profissional"

    id_profissional = Column(Integer, primary_key=True, index=True)
    nome_profissional = Column(String(100), nullable=False)
    id_especialidade = Column(Integer, ForeignKey("especialidade.id_especialidade", ondelete="RESTRICT"), nullable=False)

    especialidade = relationship("Especialidade", back_populates="profissionais")
    treinamentos = relationship("Treinamento", back_populates="profissional")


class Funcionario(Base):
    __tablename__ = "funcionario"

    matricula = Column(Integer, primary_key=True, index=True)
    nome_funcionario = Column(String(100), nullable=False)
    setor = Column(String(50), nullable=False)
    cargo = Column(String(50), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="SET NULL"), nullable=True)

    usuario = relationship("Usuario", back_populates="funcionarios")
    epis = relationship("EPI", back_populates="funcionario")
    inspecoes = relationship("Inspecao", back_populates="responsavel")
    ocorrencias = relationship("Ocorrencia", back_populates="funcionario")
    treinamentos = relationship("Treinamento", back_populates="funcionario")


class Inspecao(Base):
    __tablename__ = "inspecao"

    id_inspecao = Column(Integer, primary_key=True, index=True)
    id_tipo_inspecao = Column(Integer, ForeignKey("tipo_inspecao.id_tipo_inspecao", ondelete="CASCADE"), nullable=False)
    matricula_responsavel = Column(Integer, ForeignKey("funcionario.matricula", ondelete="CASCADE"), nullable=False)
    data_inspecao = Column(DateTime, nullable=False)
    resultado_inspecao = Column(String(255), nullable=False)

    tipo_inspecao = relationship("TipoInspecao", back_populates="inspecoes")
    responsavel = relationship("Funcionario", back_populates="inspecoes")
    ocorrencias = relationship("Ocorrencia", back_populates="inspecao")


class Ocorrencia(Base):
    __tablename__ = "ocorrencia"

    id_ocorrencia = Column(Integer, primary_key=True, index=True)
    matricula = Column(Integer, ForeignKey("funcionario.matricula", ondelete="CASCADE"), nullable=False)
    id_inspecao = Column(Integer, ForeignKey("inspecao.id_inspecao", ondelete="SET NULL"), nullable=True)
    tipo_ocorrencias = Column(String(50), nullable=False)
    gravidade = Column(String(10), nullable=False)
    data_ocorrencia = Column(Date, nullable=False)

    funcionario = relationship("Funcionario", back_populates="ocorrencias")
    inspecao = relationship("Inspecao", back_populates="ocorrencias")


class Treinamento(Base):
    __tablename__ = "treinamento"

    id_treinamentos = Column(Integer, primary_key=True, index=True)
    matricula = Column(Integer, ForeignKey("funcionario.matricula", ondelete="CASCADE"), nullable=False)
    id_curso = Column(Integer, ForeignKey("curso.id_curso", ondelete="SET NULL"), nullable=True)
    id_profissional = Column(Integer, ForeignKey("profissional.id_profissional", ondelete="SET NULL"), nullable=True)
    data_treinamento = Column(Date, nullable=False)
    situacao_treinamento = Column(String(20), nullable=False)
    aviso_treinamento = Column(String(150), nullable=True)

    funcionario = relationship("Funcionario", back_populates="treinamentos")
    curso = relationship("Curso", back_populates="treinamentos")
    profissional = relationship("Profissional", back_populates="treinamentos")
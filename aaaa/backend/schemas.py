from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import date, datetime

# Base Config para Pydantic v2
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# 1. Usuário
class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str
    nome_sistema: Optional[str] = "Infratec - Segurança no Trabalho"

class UsuarioResponse(BaseSchema):
    id_usuario: int
    email: str
    nome_sistema: str

# 2. Funcionário
class FuncionarioCreate(BaseModel):
    matricula: int
    nome_funcionario: str
    setor: str
    cargo: str
    id_usuario: Optional[int] = None

class FuncionarioResponse(BaseSchema):
    matricula: int
    nome_funcionario: str
    setor: str
    cargo: str
    id_usuario: Optional[int] = None

# 3. Tipo de Inspeção
class TipoInspecaoCreate(BaseModel):
    descricao: str

class TipoInspecaoResponse(BaseSchema):
    id_tipo_inspecao: int
    descricao: str

# 4. EPI
class EPICreate(BaseModel):
    matricula: int
    epi_nome: Optional[str] = None
    data_entrega_epi: date
    validade_epi: date
    status_epi: str

class EPIResponse(BaseSchema):
    id_epi: int
    matricula: int
    epi_nome: Optional[str] = None
    data_entrega_epi: date
    validade_epi: date
    status_epi: str

# 5. Especialidade
class EspecialidadeCreate(BaseModel):
    nome_especialidade: str

class EspecialidadeResponse(BaseSchema):
    id_especialidade: int
    nome_especialidade: str

# 6. Curso
class CursoCreate(BaseModel):
    nome_curso: str

class CursoResponse(BaseSchema):
    id_curso: int
    nome_curso: str

# 7. Profissional
class ProfissionalCreate(BaseModel):
    nome_profissional: str
    id_especialidade: int

class ProfissionalResponse(BaseSchema):
    id_profissional: int
    nome_profissional: str
    id_especialidade: int

# 8. Inspeção
class InspecaoCreate(BaseModel):
    id_tipo_inspecao: int
    matricula_responsavel: int
    data_inspecao: datetime
    resultado_inspecao: str

class InspecaoResponse(BaseSchema):
    id_inspecao: int
    id_tipo_inspecao: int
    matricula_responsavel: int
    data_inspecao: datetime
    resultado_inspecao: str

# 9. Ocorrência
class OcorrenciaCreate(BaseModel):
    matricula: int
    id_inspecao: Optional[int] = None
    tipo_ocorrencias: str
    gravidade: str
    data_ocorrencia: date

class OcorrenciaResponse(BaseSchema):
    id_ocorrencia: int
    matricula: int
    id_inspecao: Optional[int] = None
    tipo_ocorrencias: str
    gravidade: str
    data_ocorrencia: date

# 10. Treinamento
class TreinamentoCreate(BaseModel):
    matricula: int
    id_curso: Optional[int] = None
    id_profissional: Optional[int] = None
    data_treinamento: date
    situacao_treinamento: str
    aviso_treinamento: Optional[str] = None

class TreinamentoResponse(BaseSchema):
    id_treinamentos: int
    matricula: int
    id_curso: Optional[int] = None
    id_profissional: Optional[int] = None
    data_treinamento: date
    situacao_treinamento: str
    aviso_treinamento: Optional[str] = None
from fastapi import FastAPI, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Infratec - Segurança no Trabalho API")

# ---------------------------------------------------------
# 1. Funcionários
# ---------------------------------------------------------
@app.get("/api/funcionarios", response_model=List[schemas.FuncionarioResponse])
def listar_funcionarios(db: Session = Depends(get_db)):
    return db.query(models.Funcionario).all()

@app.post("/api/funcionarios", response_model=schemas.FuncionarioResponse, status_code=status.HTTP_201_CREATED)
def criar_funcionario(funcionario: schemas.FuncionarioCreate, db: Session = Depends(get_db)):
    novo_funcionario = models.Funcionario(**funcionario.model_dump())
    db.add(novo_funcionario)
    db.commit()
    db.refresh(novo_funcionario)
    return novo_funcionario

# ---------------------------------------------------------
# 2. Usuários
# ---------------------------------------------------------
@app.get("/api/usuarios", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

@app.post("/api/usuarios", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    novo_usuario = models.Usuario(**usuario.model_dump())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

# ---------------------------------------------------------
# 3. Equipamentos de Segurança (EPI)
# ---------------------------------------------------------
@app.get("/api/epis", response_model=List[schemas.EPIResponse])
def listar_epis(db: Session = Depends(get_db)):
    return db.query(models.EPI).all()

@app.post("/api/epis", response_model=schemas.EPIResponse, status_code=status.HTTP_201_CREATED)
def registrar_epi(epi: schemas.EPICreate, db: Session = Depends(get_db)):
    # 1. Verifica se o funcionário (matricula) existe no banco de dados
    funcionario = db.query(models.Funcionario).filter(models.Funcionario.matricula == epi.matricula).first()
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Funcionário com a matrícula {epi.matricula} não encontrado."
        )

    # 2. Cria o registo do EPI
    novo_epi = models.EPI(**epi.model_dump())
    db.add(novo_epi)
    db.commit()
    db.refresh(novo_epi)
    return novo_epi
# ---------------------------------------------------------
# 4. Tipos de Inspeção
# ---------------------------------------------------------
@app.get("/api/tipos-inspecao", response_model=List[schemas.TipoInspecaoResponse])
def listar_tipos_inspecao(db: Session = Depends(get_db)):
    return db.query(models.TipoInspecao).all()

@app.post("/api/tipos-inspecao", response_model=schemas.TipoInspecaoResponse, status_code=status.HTTP_201_CREATED)
def criar_tipo_inspecao(tipo: schemas.TipoInspecaoCreate, db: Session = Depends(get_db)):
    novo_tipo = models.TipoInspecao(**tipo.model_dump())
    db.add(novo_tipo)
    db.commit()
    db.refresh(novo_tipo)
    return novo_tipo

# ---------------------------------------------------------
# 5. Especialidades
# ---------------------------------------------------------
@app.get("/api/especialidades", response_model=List[schemas.EspecialidadeResponse])
def listar_especialidades(db: Session = Depends(get_db)):
    return db.query(models.Especialidade).all()

@app.post("/api/especialidades", response_model=schemas.EspecialidadeResponse, status_code=status.HTTP_201_CREATED)
def criar_especialidade(especialidade: schemas.EspecialidadeCreate, db: Session = Depends(get_db)):
    nova_especialidade = models.Especialidade(**especialidade.model_dump())
    db.add(nova_especialidade)
    db.commit()
    db.refresh(nova_especialidade)
    return nova_especialidade

# ---------------------------------------------------------
# 6. Cursos
# ---------------------------------------------------------
@app.get("/api/cursos", response_model=List[schemas.CursoResponse])
def listar_cursos(db: Session = Depends(get_db)):
    return db.query(models.Curso).all()

@app.post("/api/cursos", response_model=schemas.CursoResponse, status_code=status.HTTP_201_CREATED)
def criar_curso(curso: schemas.CursoCreate, db: Session = Depends(get_db)):
    novo_curso = models.Curso(**curso.model_dump())
    db.add(novo_curso)
    db.commit()
    db.refresh(novo_curso)
    return novo_curso

# ---------------------------------------------------------
# 7. Profissionais
# ---------------------------------------------------------
@app.get("/api/profissionais", response_model=List[schemas.ProfissionalResponse])
def listar_profissionais(db: Session = Depends(get_db)):
    return db.query(models.Profissional).all()

@app.post("/api/profissionais", response_model=schemas.ProfissionalResponse, status_code=status.HTTP_201_CREATED)
def criar_profissional(profissional: schemas.ProfissionalCreate, db: Session = Depends(get_db)):
    novo_profissional = models.Profissional(**profissional.model_dump())
    db.add(novo_profissional)
    db.commit()
    db.refresh(novo_profissional)
    return novo_profissional

# ---------------------------------------------------------
# 8. Inspeções
# ---------------------------------------------------------
@app.get("/api/inspecoes", response_model=List[schemas.InspecaoResponse])
def listar_inspecoes(db: Session = Depends(get_db)):
    return db.query(models.Inspecao).all()

@app.post("/api/inspecoes", response_model=schemas.InspecaoResponse, status_code=status.HTTP_201_CREATED)
def criar_inspecao(inspecao: schemas.InspecaoCreate, db: Session = Depends(get_db)):
    nova_inspecao = models.Inspecao(**inspecao.model_dump())
    db.add(nova_inspecao)
    db.commit()
    db.refresh(nova_inspecao)
    return nova_inspecao

# ---------------------------------------------------------
# 9. Ocorrências
# ---------------------------------------------------------
@app.get("/api/ocorrencias", response_model=List[schemas.OcorrenciaResponse])
def listar_ocorrencias(db: Session = Depends(get_db)):
    return db.query(models.Ocorrencia).all()

@app.post("/api/ocorrencias", response_model=schemas.OcorrenciaResponse, status_code=status.HTTP_201_CREATED)
def registrar_ocorrencia(ocorrencia: schemas.OcorrenciaCreate, db: Session = Depends(get_db)):
    nova_ocorrencia = models.Ocorrencia(**ocorrencia.model_dump())
    db.add(nova_ocorrencia)
    db.commit()
    db.refresh(nova_ocorrencia)
    return nova_ocorrencia

# ---------------------------------------------------------
# 10. Treinamentos
# ---------------------------------------------------------
@app.get("/api/treinamentos", response_model=List[schemas.TreinamentoResponse])
def listar_treinamentos(db: Session = Depends(get_db)):
    return db.query(models.Treinamento).all()

@app.post("/api/treinamentos", response_model=schemas.TreinamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_treinamento(treinamento: schemas.TreinamentoCreate, db: Session = Depends(get_db)):
    novo_treinamento = models.Treinamento(**treinamento.model_dump())
    db.add(novo_treinamento)
    db.commit()
    db.refresh(novo_treinamento)
    return novo_treinamento
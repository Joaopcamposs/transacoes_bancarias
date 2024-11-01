from dataclasses import dataclass

from fastapi import HTTPException, status


@dataclass
class TransacaoBancariaNaoEncontrado(HTTPException):
    detail: str = "numero da TransacaoBancaria não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class TransacaoBancariaJaCadastrado(HTTPException):
    detail: str = "numero da TransacaoBancaria já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class ErroAoCadastrarTransacaoBancaria(HTTPException):
    detail: str = "Erro ao cadastrar transacao bancaria."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoAtualizarTransacaoBancaria(HTTPException):
    detail: str = "Erro ao atualizar transacao bancaria."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoDeletarTransacaoBancaria(HTTPException):
    detail: str = "Erro ao deletar transacao bancaria."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ValorDaTransacaoNegativo(HTTPException):
    detail: str = "O valor da transação não pode ser negativo."
    status_code: int = status.HTTP_400_BAD_REQUEST

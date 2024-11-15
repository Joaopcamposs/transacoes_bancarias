from dataclasses import dataclass, field

from fastapi import status, HTTPException


@dataclass
class ClienteNaoEncontrado(HTTPException):
    detail: str = "Cliente não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class ClienteJaCadastrado(HTTPException):
    detail: str = "Email de Cliente já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class ErroAoCadastrarCliente(HTTPException):
    detail: str = "Erro ao cadastrar cliente."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoAtualizarCliente(HTTPException):
    detail: str = "Erro ao atualizar cliente."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoDeletarCliente(HTTPException):
    detail: str = "Erro ao deletar cliente."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ContaBancariaNaoEncontrado(HTTPException):
    detail: str = "numero da ContaBancaria não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class ContaBancariaJaCadastrado(HTTPException):
    detail: str = "numero da ContaBancaria já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class ErroAoCadastrarContaBancaria(HTTPException):
    detail: str = "Erro ao cadastrar conta bancaria."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoAtualizarContaBancaria(HTTPException):
    detail: str = "Erro ao atualizar conta bancaria."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoDeletarContaBancaria(HTTPException):
    detail: str = "Erro ao deletar conta bancaria."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class SaldoInsuficienteParaRealizarTransacao(HTTPException):
    detail: str = "Saldo insuficiente para realizar a transação."
    status_code: int = status.HTTP_400_BAD_REQUEST


@dataclass
class UsuarioNaoEncontrado(HTTPException):
    detail: str = "Usuario não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class UsuarioJaCadastrado(HTTPException):
    detail: str = "Email de Usuario já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class PermissaoFaltando(HTTPException):
    detail: str = "Esse usuário não tem permissão para executar essa ação."
    status_code: int = status.HTTP_403_FORBIDDEN


@dataclass
class ErroAoCadastrarUsuario(HTTPException):
    detail: str = "Erro ao deletar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoAtualizarUsuario(HTTPException):
    detail: str = "Erro ao deletar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


@dataclass
class ErroAoDeletarUsuario(HTTPException):
    detail: str = "Erro ao deletar usuário."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


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


@dataclass
class ErroAoGerarToken(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Erro ao gerar token."


@dataclass
class NaoFoiPossivelValidarAsCredenciais(HTTPException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Não foi possível validar as credenciais"
    headers: dict = field(default_factory=dict)


@dataclass
class CredenciaisIncorretas(HTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Email ou senha incorretos"

import sympy
from sympy import *


class No(object):
    """description of class"""
    filhos = []
    pai = None
    expressao = None

    def __init__(self, expressao, pai):
        self.expressao = expressao
        self.pai = pai


class Transformacao_Realizada(object):

    expressoes = []
    funcao_consolidadora = function()

    def __init__(self, expressoes, funcao_consolidadora):
        self.expressoes = expressoes
        self.funcao_consolidadora = funcao_consolidadora


class Transformacao(object):
    """description of class"""
    
    """Retorna verdadeiro se a expressão é do tipo tratado pela transformação """
    funcao_reconhecimento = None
    """Devolve a lista de expressões nas quais a expressão é transformada. Cada expressão deve ser passar pela integração (se não for o resultado final)"""
    funcao_transformacao = None
    """funcao consolidacao: uma expressão pode ser transformada em várias, que, depois de integradas, devem ser consolidadas em uma expressão. Esta função faz esta consolidação"""
    funcao_consolidacão = None
    """Nome da transformação para referência"""
    nome = ""

    def __init__(self, funcao_reconhecimento, funcao_transformacao, funcao_consolidacao, nome):
        self.funcao_reconhecimento = funcao_reconhecimento
        self.funcao_transformacao = funcao_transformacao
        self.funcao_consolidacão = funcao_consolidacao
        self.nome = nome
        
class Transformacoes(object):
    """description of class"""
    transformacoes = list()
    transformacoes_realizadas = list()

    def Transforma( self, expressao ):
        for transformacao in self.transformacoes:
            if transformacao.funcao_reconhecimento(expressao):
                transformacoes_realizadas.append(Transformacao_Realizada(transformacao.funcao_transformacao(expressao),transformacao.funcao_consolidadora))

        return transformacoes_realizadas
        

class Transformacoes_Finais(Transformacoes):
    def __init__(self):
        
        def reconhece_x_elevado_n(expressao):
            expressao_eh_potencia = isinstance(expressao,sympy.Pow)
            base_eh_x = isinstance(expressao.args[0],sympy.Symbol)
            expoente_eh_real = isinstance(expressao.args[1],sympy.numbers.Number)
            return expressao_eh_potencia and base_eh_x and expoente_eh_real
                
        def calcula_x_elevado_n(expressao):
            expoente = expressao.args[1]
            return [(x**(expoente + 1)) / (expoente + 1)] 

        def funcao_identidade(lista_expressoes):
            return lista_expressoes[0]

        self.transformacoes.append(Transformacao(reconhece_x_elevado_n, calcula_x_elevado_n,funcao_identidade,"x elevado a constante"))

class Transformacoes_Certeiras(Transformacoes):
    def __init__(self):
        
        def reconhece_soma(expressao):
            expressao_eh_soma = isinstance(expressao,sympy.Add)
            return expressao_eh_soma
                
        def separa_parcelas_soma(expressao):
            return (list(expressao.args))
        
        def soma_parcelas(lista_expressoes):
            return(sum(lista_expressoes))

        self.transformacoes.append(Transformacao(reconhece_soma, separa_parcelas_soma, soma_parcelas, "integral da soma é a soma das integrais"))



class Transformacoes_Heuristicas(Transformacoes):
    def __init__(self):
        
        """Ainda não tem nada"""
        def reconhece_soma(expressao):
            expressao_eh_soma = isinstance(expressao,sympy.Add)
            return expressao_eh_soma
                
        def separa_parcelas_soma(expressao):
            return (list(expressao.args))
        
        def soma_parcelas(lista_expressoes):
            return(sum(lista_expressoes))

        self.transformacoes.append(Transformacao(reconhece_soma, separa_parcelas_soma, soma_parcelas, "integral da soma é a soma das integrais"))




    



x = symbols('x')
expressao = x**2
no = No(expressao, None)
print(No)

transformacoes_finais = Transformacoes_Finais()
expressao = x**2
resultado = transformacoes_finais.Transforma(expressao)
print(resultado)

















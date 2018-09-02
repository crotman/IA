import sympy
from sympy import *
from enum import Enum
from queue import *


class Ramificacao(Enum):
    AND = 1
    OR = 2  
    
class Transformacao_Realizada(object):

    expressoes = []
    funcao_consolidadora = None

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
    funcao_consolidadora = None
    """Nome da transformação para referência"""
    nome = ""

    def __init__(self, funcao_reconhecimento, funcao_transformacao, funcao_consolidadora, nome):
        self.funcao_reconhecimento = funcao_reconhecimento
        self.funcao_transformacao = funcao_transformacao
        self.funcao_consolidadora = funcao_consolidadora
        self.nome = nome
        
class Transformacoes(object):
    """description of class"""
    transformacoes = list()
    transformacoes_realizadas = list()

    def Transforma( self, expressao ):
        for transformacao in self.transformacoes:
            if transformacao.funcao_reconhecimento(expressao):
                self.transformacoes_realizadas.append(Transformacao_Realizada(transformacao.funcao_transformacao(expressao),transformacao.funcao_consolidadora))

        return self.transformacoes_realizadas
        
class Transformacoes_Finais(Transformacoes):
    def __init__(self):


        """As transformações finais sempre devolvem uma só transformação com uma só expressão de resultado"""

        
        def reconhece_x_elevado_n(expressao):
            expressao_eh_potencia = isinstance(expressao,sympy.Pow)
            base_eh_x = isinstance(expressao.args[0],sympy.Symbol)
            expoente_eh_real = isinstance(expressao.args[1],sympy.numbers.Number)
            return expressao_eh_potencia and base_eh_x and expoente_eh_real
                
        def calcula_x_elevado_n(expressao):
            expoente = expressao.args[1]
            return [(x**(expoente + 1)) / (expoente + 1)] 

        def funcao_identidade(expressao_base,lista_expressoes_resultado):
            return lista_expressoes_resultado[0]

        self.transformacoes.append(Transformacao(reconhece_x_elevado_n, calcula_x_elevado_n,funcao_identidade,"x elevado a constante"))

class Transformacoes_Certeiras(Transformacoes):
    def __init__(self):

        """As transformações finais sempre devolvem uma só transformação, que pode trazer n expressões para serem resolvidas. Todas precisam ser resolvidas (AND)"""

        
        def reconhece_soma(expressao):
            expressao_eh_soma = isinstance(expressao,sympy.Add)
            return expressao_eh_soma
                
        def separa_parcelas_soma(expressao):
            return (list(expressao.args))
        
        def soma_parcelas(expressao_base,lista_expressoes_resultado):
            return(sum(lista_expressoes))

        self.transformacoes.append(Transformacao(reconhece_soma, separa_parcelas_soma, soma_parcelas, "integral da soma é a soma das integrais"))

        def reconhece_constante_multiplicando_funcao_com_simbolo(expressao):
            expressao_eh_produto = isinstance(expressao,sympy.Mul)
            primeiro_fator_eh_numero = isinstance(expressao.args[0],sympy.numbers.Number)
            return (expressao_eh_produto and primeiro_fator_eh_numero)
                
        def retira_constante_multiplicada(expressao):
            return [(expressao/expressao.args[0])]
        
        def multiplica_constante_de_volta(expressao_base,lista_expressoes_resultado):
            return (expressao_base.args[0] * lista_expressoes_resultado[0] )

        self.transformacoes.append(Transformacao(reconhece_constante_multiplicando_funcao_com_simbolo, retira_constante_multiplicada, multiplica_constante_de_volta, "integral(cx) = c integral(x)"))

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


transformacoes_finais = Transformacoes_Finais()
transformacoes_certeiras = Transformacoes_Certeiras()
transformacoes_heuristicas = Transformacoes_Heuristicas()


class No(object):
    """description of class"""
    filhos = []
    filhos_construidos = False
    funcao_consolidadora_filhos = None
    tipo_de_ramificacao_filhos = Ramificacao()
    pai = None
    expressao_a_solucionar = None
    solucionado = False
    solucao = None
    resultados_filhos = []


    def __init__(self, expressao, pai):
        self.expressao = expressao
        self.pai = pai

    def constroi_filhos(self):
        """retirar. Usada para intellisense"""
        solucoes_finais = [Transformacao_Realizada(None,None)]
        solucoes_finais = transformacoes_finais.Transforma(expressao_a_solucionar)
        if len(solucoes_finais) > 0:
            solucao = solucoes_finais[0].expressoes[0]
            solucionado = True
        else:
            solucoes_finais = transformacoes_certeiras.Transforma(expressao_a_solucionar)
            if len(solucoes_finais) > 0:
                for expressao in solucoes_finais[0].expressoes:
                    self.filhos.append(No(expressao,self))
                self.funcao_consolidadora = solucoes_finais[0].funcao_consolidadora
                self.solucionado = False
                self.tipo_de_ramificacao_filhos = Ramificacao.AND
            else:
                solucoes_finais = transformacoes_heuristicas.Transforma(expressao_a_solucionar)
                for solucao in solucoes_finais:
                    self.filhos.append(No(solucao.expressoes[0],self))
                    self.solucionado = False
                    self.tipo_de_ramificacao_filhos = Ramificacao.OR
    
    def  __str__(self, nivel = 0):
        """imprime a situação atual da árvore, em nível"""
        ret = "\t"*nivel+repr(self.value)+"\n"
        for filho in self.filhos:
            ret += filho.__str__(nivel + 1)
            


    def resolve(self):
        if not self.filhos_construidos:
            self.constroi_filhos()
        if self.solucionado:
            return self.solucao
        else:
            if self.tipo_de_ramificacao_filhos == Ramificacao.AND:
                for filho in self.filhos:
                    self.resultados_filhos.append(filho.resolve())



        


    
         


x = symbols('x')



expressao = x**2
no = No(expressao, None)
print(No)

expressao = x**2
resultado = transformacoes_finais.Transforma(expressao)
print(resultado)

















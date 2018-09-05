import sympy
from sympy import *
from enum import Enum
from queue import *

def ifNone(str):
    if str == None:
        return "X"
    else:
        return str



class Ramificacao(Enum):
    AND = "AND"
    OR = "OR"

class Transformacao_Realizada(object):

    expressoes = []
    funcao_consolidadora = None
    nome = ""

    def __init__(self, expressoes, funcao_consolidadora, nome):
        self.expressoes = expressoes
        self.funcao_consolidadora = funcao_consolidadora
        self.nome = nome
        i = 0

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

    def __init__(self):
        a = 0

    def Transforma( self, expressao ):
        self.transformacoes_realizadas = list()
        for transformacao in self.transformacoes:
            if transformacao.funcao_reconhecimento(expressao):
                self.transformacoes_realizadas.append(Transformacao_Realizada(transformacao.funcao_transformacao(expressao),transformacao.funcao_consolidadora, transformacao.nome))

        return self.transformacoes_realizadas

class Transformacoes_Finais(Transformacoes):

    transformacoes = list()
    transformacoes_realizadas = list()


    def __init__(self):


        """As transformações finais sempre devolvem uma só transformação com uma só expressão de resultado"""


        def reconhece_x_elevado_n(expressao):
            try:
                expressao_eh_potencia = isinstance(expressao,sympy.Pow)
                base_eh_x = isinstance(expressao.args[0],sympy.Symbol)
                expoente_eh_real = isinstance(expressao.args[1],sympy.numbers.Number)
            except:
                return False
            return expressao_eh_potencia and base_eh_x and expoente_eh_real

        def calcula_x_elevado_n(expressao):
            expoente = expressao.args[1]
            return [(x**(expoente + 1)) / (expoente + 1)]

        def funcao_identidade(expressao_base,lista_expressoes_resultado):
            return lista_expressoes_resultado[0]

        self.transformacoes.append(Transformacao(reconhece_x_elevado_n, calcula_x_elevado_n,funcao_identidade,"x elevado a constante"))

        def reconhece_constante(expressao):
            expressao_eh_constante = isinstance(expressao,sympy.numbers.Number) or type(expressao) == int
            return expressao_eh_constante

        def calcula_constante(expressao):
            return [expressao*x]

        self.transformacoes.append(Transformacao(reconhece_constante, calcula_constante, funcao_identidade, "constante"))

        def reconhece_exponencial(expressao):
            try:
                expressao_eh_exponencial = expressao.func == exp
                expoente_eh_x = isinstance(expressao.args[0],sympy.Symbol)
                return expressao_eh_exponencial and expoente_eh_x
            except:
                return False

        def calcula_exponencial(expressao):
            return [expressao]

        self.transformacoes.append(Transformacao(reconhece_exponencial, calcula_exponencial, funcao_identidade,"exponencial"))

        def reconhece_x(expressao):
            return isinstance(expressao,sympy.Symbol)

        def calcula_x(expressao):
            return [x**2/2]

        self.transformacoes.append(Transformacao(reconhece_x, calcula_x, funcao_identidade, "x"))




class Transformacoes_Certeiras(Transformacoes):

    transformacoes = list()
    transformacoes_realizadas = list()


    def __init__(self):

        """As transformações finais sempre devolvem uma só transformação, que pode trazer n expressões para serem resolvidas. Todas precisam ser resolvidas (AND)"""


        def reconhece_soma(expressao):
            expressao_eh_soma = isinstance(expressao,sympy.Add)
            return expressao_eh_soma

        def separa_parcelas_soma(expressao):
            return (list(expressao.args))

        def soma_parcelas(expressao_base,lista_expressoes_resultado):
            return(sum(lista_expressoes_resultado))

        self.transformacoes.append(Transformacao(reconhece_soma, separa_parcelas_soma, soma_parcelas, "integral da soma"))

        def reconhece_constante_multiplicando_funcao_com_simbolo(expressao):
            try:
                expressao_eh_produto = isinstance(expressao,sympy.Mul)
                primeiro_fator_eh_numero = isinstance(expressao.args[0],sympy.numbers.Number)
                return (expressao_eh_produto and primeiro_fator_eh_numero)
            except:
                return False

        def retira_constante_multiplicada(expressao):
            return [(expressao/expressao.args[0])]

        def multiplica_constante_de_volta(expressao_base,lista_expressoes_resultado):
            return (expressao_base.args[0] * lista_expressoes_resultado[0] )

        self.transformacoes.append(Transformacao(reconhece_constante_multiplicando_funcao_com_simbolo, retira_constante_multiplicada, multiplica_constante_de_volta, "integral(cx) = c integral(x)"))


        def reconhece_divisao_polinomios(expressao):
            try:
                eh_mult = expressao.func == sympy.Mul
                op1_eh_polinomio = expressao.args[0].is_polynomial()
                op2_eh_potencia = expressao.args[1].func == sympy.Pow
                op2_eh_denominador = expressao.args[1].args[1] == -1
                op2_eh_polinomio = expressao.args[1].args[0].is_polynomial()
                return eh_mult and op1_eh_polinomio and op2_eh_potencia and op2_eh_denominador and op2_eh_polinomio
            except:
                return False

        def divide_polinomio(expressao):
            p1 = expressao.args[0]
            p2 = expressao.args[1].args[0]
            q,r = div(p1,p2)
            saida = q + r/p2
            return [saida]

        def funcao_identidade(expressao_base,lista_expressoes_resultado):
            return lista_expressoes_resultado[0]


        self.transformacoes.append(Transformacao(reconhece_divisao_polinomios, divide_polinomio, funcao_identidade, "divide polinômio"))




class Transformacoes_Heuristicas(Transformacoes):

    transformacoes = list()
    transformacoes_realizadas = list()


    def __init__(self):


        def operador_eh_sen_expoente_positivo_ou_cos_expoente_negativo(operador):
            expressao_eh_potenciacao = isinstance(operador,sympy.Pow)
            if (operador.args[0].func == cos):
                eh_simbolo = isinstance(operador.args[0].args[0], sympy.Symbol)
                expoente_correto = isinstance(operador.args[1],sympy.numbers.Number) and operador.args[1] < 0
            else:
                if (operador.args[0].func == sin):
                    eh_simbolo = isinstance(operador.args[0].args[0], sympy.Symbol)
                    expoente_correto = isinstance(operador.args[1],sympy.numbers.Number) and operador.args[1] > 0
                else:
                    return false
            return expressao_eh_potenciacao and eh_simbolo and expoente_correto

        def reconhece_sin_sobre_cos(expressao):
            try:
                expressao_eh_multiplicacao = isinstance(expressao,sympy.Mul)
                operador1_eh_ok = operador_eh_sen_expoente_positivo_ou_cos_expoente_negativo(expressao.args[0])
                operador2_eh_ok = operador_eh_sen_expoente_positivo_ou_cos_expoente_negativo(expressao.args[1])
                n_operadores_eh_2 = len(expressao.args) == 2
                expoentes_iguais = abs(expressao.args[0].args[1]) == abs(expressao.args[1].args[1])
                return expressao_eh_multiplicacao and operador1_eh_ok and operador2_eh_ok and n_operadores_eh_2 and expoentes_iguais
            except:
                return false

        def transforma_em_tangente(expressao):
            expoente = abs(expressao.args[0].args[1])
            simbolo = expressao.args[0].args[0].args[0]
            return [(tan(simbolo)**expoente)]

        def funcao_identidade(expressao_base,lista_expressoes_resultado):
            return lista_expressoes_resultado[0]

        self.transformacoes.append(Transformacao(reconhece_sin_sobre_cos, transforma_em_tangente, funcao_identidade, "sen/cos vira tan"))

        def transforma_em_cotangente(expressao):
            expoente = abs(expressao.args[0].args[1])
            simbolo = expressao.args[0].args[0].args[0]
            return [(cot(simbolo)**-expoente)]

        self.transformacoes.append(Transformacao(reconhece_sin_sobre_cos, transforma_em_cotangente, funcao_identidade, "sen/cos vira cot"))


        def reconhece_um_menos_x_quadrado(expressao):
            try:
                eh_soma = expressao.func == sympy.Add
                operador1_eh_1 = expressao.args[0] == 1
                operador2 = expressao.args[1]
                operador2_eh_multiplicacao = operador2.func == sympy.Mul
                operador1_do_operador2_eh_menos_1 = operador2.args[0] == -1
                operador2_do_operador2_eh_potencia = operador2.args[1].func == sympy.Pow
                operador1_do_operador2_do_operador2_eh_simbolo = isinstance(operador2.args[1].args[0], sympy.Symbol)
                operador2_do_operador2_do_operador2_eh_dois = operador2.args[1].args[1] == 2
                return  eh_soma and operador1_eh_1  and operador2_eh_multiplicacao and operador1_do_operador2_eh_menos_1 and operador2_do_operador2_eh_potencia and operador1_do_operador2_do_operador2_eh_simbolo and operador2_do_operador2_do_operador2_eh_dois

            except:
                return false

        def reconhece_algum_um_menos_x_ao_quadrado(expressao):
            achou = False
            for subexp in preorder_traversal(expressao):
                if reconhece_um_menos_x_quadrado(subexp):
                    achou = True
                    break
            return achou

        def substitui_x_senx(expresso):
            saida = expressao.subs(x,sin(x)) * cos(x)
            saida = saida.subs(-sin(x)**2 + 1, cos(x)**2)
            saida = powdenest(saida, force = True)
            saida = saida.subs(Abs(cos(x)),cos(x))
            return [saida]

        def volta_subs_x_senx(expressao_base, lista_expressoes_resultado):
            return lista_expressoes_resultado[0].subs(x,asin(x))

        self.transformacoes.append(Transformacao(reconhece_algum_um_menos_x_ao_quadrado, substitui_x_senx, volta_subs_x_senx, "em (1-x**2) x vira sin(x)"))

        def reconhece_tg_4(expressao):
            try:
                eh_potencia = expressao.func == sympy.Pow
                op1_eh_tan = expressao.args[0].func == tan
                op1_de_op1_eh_simbolo = isinstance(expressao.args[0].args[0] , sympy.Symbol)
                op2_de_op1_eh_4 = expressao.args[1] == 4
                return eh_potencia and op1_eh_tan and op1_de_op1_eh_simbolo and op2_de_op1_eh_4
            except:
                return False

        def substitui_tg4(expressao):
            return[x**4 / (1 + x**2)]

        def volta_subs_tan_4(expressao_base, lista_expressoes_resultado):
            return lista_expressoes_resultado[0].subs(x,atan(x))

        self.transformacoes.append(Transformacao(reconhece_tg_4, substitui_tg4, volta_subs_tan_4, "substitui tan**4"))

        
        def reconhece_1_sobre_1_mais_x_quadrado(expressao):
            return expressao == 1/(1+x**2)

        def calcula_1_sobre_1_mais_x_quadrado(expressao):
            return [1]

        def volta_substitui_atan(expressao_base, lista_expressoes_resultado):
            return lista_expressoes_resultado[0].subs(x,tan(x))

        self.transformacoes.append(Transformacao(reconhece_1_sobre_1_mais_x_quadrado, calcula_1_sobre_1_mais_x_quadrado, volta_substitui_atan, "substitui arctan"))



transformacoes_finais = Transformacoes_Finais()
transformacoes_certeiras = Transformacoes_Certeiras()
transformacoes_heuristicas = Transformacoes_Heuristicas()


class No(object):
    """description of class"""
    filhos = []
    funcoes_filhos_or = []
    filhos_construidos = False
    funcao_consolidadora_filhos = None
    tipo_de_ramificacao_filhos = Ramificacao.AND
    pai = None
    solucionado = False
    solucao = None
    resultados_filhos = []
    transformacao = ""
    ultimo_no = 0
    id


    def __init__(self, expressao, pai, transformacao):
        self.expressao = expressao
        self.pai = pai
        self.filhos = []
        self.funcoes_filhos_or = []
        self.transformacao = transformacao
        No.ultimo_no = No.ultimo_no + 1
        self.id = No.ultimo_no

    def constroi_filhos(self):
        solucoes_finais = transformacoes_finais.Transforma(self.expressao)
        if len(solucoes_finais) > 0:
            self.solucao = solucoes_finais[0].funcao_consolidadora(self.expressao,solucoes_finais[0].expressoes)
            self.solucionado = True
        else:
            solucoes_finais = transformacoes_certeiras.Transforma(self.expressao)
            if len(solucoes_finais) > 0:
                for expressao in solucoes_finais[0].expressoes:
                    self.filhos.append(No(expressao,self, solucoes_finais[0].nome))
                self.funcao_consolidadora_filhos = solucoes_finais[0].funcao_consolidadora
                self.solucionado = False
                self.tipo_de_ramificacao_filhos = Ramificacao.AND
            else:
                solucoes_finais = transformacoes_heuristicas.Transforma(self.expressao)
                for solucao in solucoes_finais:
                    self.filhos.append(No(solucao.expressoes[0],self,solucao.nome))
                    self.funcoes_filhos_or.append(solucao.funcao_consolidadora)
                    self.solucionado = False
                    self.tipo_de_ramificacao_filhos = Ramificacao.OR


    def to_dot(self, nivel = 0):
        """retorna a situação atual da árvore, em nível"""
        n = nivel
        if self.tipo_de_ramificacao_filhos == Ramificacao.AND :
            ramificacao = "AND"
        else:
            ramificacao = "OR"
        if self.solucao:
            ret = ['\tn%s [ label = "%s: %s -> %s. Filhos: %s" ];' % (self.id, self.transformacao, self.expressao, self.solucao, ramificacao)]
        else:
            ret = ['\tn%s [ label = "%s: %s -> NADA. Filhos: %s" ];' % (self.id, self.transformacao, self.expressao, ramificacao)]

        # ret = "\t"*nivel+repr(self.expressao)+"->"+  str(self.solucao)  +" \n"
        for i, filho in enumerate(self.filhos):
            nivel += 1
            ret.append(filho.to_dot(nivel))
            ret.append('\tn%s -> n%s' % (self.id, filho.id))

        return "\n".join(ret)


    def  __str__(self):
        return self.to_dot(0)


    def resolve_depth(self):

        lista_filhos = []

        if not self.filhos_construidos:
            self.constroi_filhos()

        if self.solucionado:
            return self.solucao
        else:
            if len(self.filhos) == 0:
                return None

            if self.tipo_de_ramificacao_filhos == Ramificacao.AND:
                for filho in self.filhos:
                    expressao = filho.resolve_depth()
                    if expressao == None:
                        return None
                    else:
                        lista_filhos.append(expressao)
                self.solucao = self.funcao_consolidadora_filhos(self.expressao,lista_filhos)
                self.solucionado = True
                return(self.solucao)
            else:
               if self.tipo_de_ramificacao_filhos == Ramificacao.OR:
                   i = 0
                   for filho in self.filhos:
                       expressao = filho.resolve_depth()
                       if expressao != None:
                           self.solucao = self.funcoes_filhos_or[i](self.expressao,[expressao])
                           self.solucionado = True
                           return (self.solucao)
                       i = i+1
                   return None




def pede_expressao_pro_usuario():
    global x, y, z, expressao

    x, y, z = sympy.symbols('x y z')
    entrada = input("Informe a expressão [ex: x**4 / ((1-x**2)**(5/2))]: ")

    try:
        print("sympy.srepr(%s)" % entrada)
        expressao = eval("%s" % entrada)
        return expressao
    except Exception as e:
        print("Expressão inválida. " +  e)
        exit()


def main():
    global x, y, z, expressao

    # expressao = x**4 / ((1-x**2)**(5/2))
    expressao = pede_expressao_pro_usuario()

    no = No(expressao, None, "Raiz")
    expressao = no.resolve_depth()

    print("")
    print("Resultado: %s" % expressao)
    print("")
    print("Árvore: ")
    print("")
    print("digraph G {")
    print(no)
    print("}")


if __name__ == '__main__':
    main()
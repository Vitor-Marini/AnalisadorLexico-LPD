import pandas as pd

#Dicionario de tokens
TOKENS = {
    "program": "sprogram",
    "begin": "sbegin",
    "end": "send",
    "procedure": "sprocedure",
    "function": "sfunction",
    "if": "sif",
    "then": "sthen",
    "else": "selse",
    "while": "swhile",
    "do": "sdo",
    "repeat": "srepeat",
    "until": "suntil",
    ":=": "satribuição",
    "writec": "swritec",
    "writed": "swrited",
    "readc": "sreadc",
    "readd": "sreadd",
    "var": "svar",
    "int": "sint",
    "char": "schar",
    "and": "sand",
    "or": "sor",
    "not": "snot",
    ">": "smaior",
    "<": "smenor",
    "=": "sigual",
    "<>": "sdiferente",
    ">=": "smaior_igual",
    "<=": "smenor_igual",
    "+": "smais",
    "-": "smenos",
    "*": "svezes",
    "div": "sdiv",
    ".": "sponto",
    ";": "sponto_vírgula",
    ",": "svírgula",
    "(": "sabre_parênteses",
    ")": "sfecha_parênteses",
    "[": "sabre_colchete",
    "]": "sfecha_colchete",
}

OPERADORES_E_SIMBOLOS = [":", "+", "-", "*", "/", "=", "<", ">", ";", ",", ".", "(", ")", "[", "]"]


#Classe que representa um token
class Token:
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

    def __repr__(self):
        return f'Token({self.tipo}, {self.valor}, linha {self.linha})'


def analisar_lexico(arquivo):
    tokens_list = []
    linha_atual = 1

    with open(arquivo, 'r') as codigo_fonte:
        conteudo = codigo_fonte.read()
        i = 0
        while i < len(conteudo):
            char = conteudo[i]

            # Ignorar espaços em branco e contar linhas
            if char.isspace():
                if char == '\n':
                    linha_atual += 1
                i += 1
                continue

            # Tratar comentários
            if char == '{':
                while i < len(conteudo) and conteudo[i] != '}':
                    if conteudo[i] == '\n':
                        linha_atual += 1
                    i += 1
                i += 1  # Ignorar o '}' final
                continue

            # Tratar números
            if char.isdigit():
                inicio = i
                while i < len(conteudo) and conteudo[i].isdigit():
                    i += 1
                numero = conteudo[inicio:i]
                tokens_list.append(Token("snúmero", numero, linha_atual))
                continue

            # Tratar identificadores e palavras reservadas
            if char.isalpha():
                inicio = i
                while i < len(conteudo) and (conteudo[i].isalnum() or conteudo[i] == '_'):
                    i += 1
                palavra = conteudo[inicio:i].lower()  # Case-insensitive
                tipo = TOKENS.get(palavra, "sidentificador")
                tokens_list.append(Token(tipo, palavra, linha_atual))
                continue
             

            # Tratar operadores e símbolos
            if char in OPERADORES_E_SIMBOLOS:
                if char == ':' and i + 1 < len(conteudo) and conteudo[i + 1] == '=':
                    tokens_list.append(Token("satribuição", ":=", linha_atual))
                    i += 2
                else:
                    token_tipo = TOKENS.get(char, "desconhecido")
                    tokens_list.append(Token(token_tipo, char, linha_atual))
                    i += 1
                continue

            # Se não for reconhecido
            i += 1 

    return tokens_list

# Função que cria tabela exibindo os resultados
from tabulate import tabulate

def gerar_tabela(tokens_list):
    data = {'Token': [token.valor for token in tokens],
            'Classificação': [token.tipo for token in tokens],
            'Linha': [token.linha for token in tokens]}
    df = pd.DataFrame(data)
    
    # Imprime o DataFrame sem o índice
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))


arquivo = 'input.txt'  
tokens = analisar_lexico(arquivo)
gerar_tabela(tokens)
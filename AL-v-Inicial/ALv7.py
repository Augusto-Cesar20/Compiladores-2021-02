arquivo = open('testeArquivo.txt', 'r')
palavra = []
char = []
i = 0   
for linha in arquivo:
    palavra.append(linha)
    for caractere in palavra[i]:
        char.append(caractere) 
    i = i + 1
arquivo.close()
char.append('$')

tamanho = len(char)
posicao = 0
linha = 1
coluna = 1

letras = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
digitos = list("0123456789")
outros = list(",;:.!?\*+-/(){}[]<>='\"") 



tabela =    [
                ["inicio", "inicio", "inicio"],
                ["varinicio", "varinicio", "varinicio"],
                ["varfim", "varfim", "varfim"],
                ["escreva", "escreva", "escreva"],
                ["leia", "leia", "leia"],
                ["se", "se", "se"],
                ["entao", "entao", "entao"],
                ["fimse", "fimse", "fimse"],
                ["fim", "fim", "fim"],
                ["inteiro", "inteiro", "inteiro"],
                ["literal", "literal", "literal"],
                ["real", "real", "real"],
            ]



class Token:
    def __init__ (self): 
        self.vet = []
        self.classe = None
        self.lexema = None
        self.tipo = None


    def se_letra (self, c):
        if (c in letras):
            return True
        return False

    def se_digito (self, c):
        if (c in digitos):
            return True
        return False

    def se_outro (self, c):
        if (c in outros):
            return True
        return False

    def se_alfabeto (self, c):
        if(self.se_outro(c) or self.se_digito(c) or self.se_letra(c)):
            return True
        return False


    def atualiza_posicao(self):
        global posicao
        global coluna
        posicao = posicao + 1
        coluna = coluna + 1

    def retorna_char(self, p):
        return char[p]


    def resp(self):
        return ''.join(self.vet)

    def Scanner(self):
        self.q0()
        if(self.lexema is not None and self.classe != "Comentario"):
            return Token
        else:
            return -1

    def aceita(self, estado):
        self.lexema = self.resp()
        self.tipo = "Nulo"

        if(estado in [0, 2, 4, 5]):
            self.classe = "ERRO"

        if(estado in [1, 3, 6]):
            self.classe = "Num"
            if(estado == 1):
                self.tipo = "inteiro"
            else:
                self.tipo = "real"

        if(estado in [7, 8]):
            tb_bool = False
            for tb_i in tabela:
                if(tb_i[1] == self.lexema):
                    tb_bool = True
                    tk_id = tb_i
            if (tb_bool == True):
                self.classe = tk_id[0]
                self.lexema = tk_id[1]
                self.tipo = tk_id[2]
            else:
                self.classe = 'id'
                tabela.append([self.classe, self.lexema, self.tipo])

        if(estado == 9):
            self.classe = 'EOF'
            self.lexema = 'EOF'

        if(estado == 10):
            self.classe = "ERRO"

        if(estado == 11):
            self.classe = 'Lit'
            self.tipo = 'literal'

        if(estado in [12, 13]):
            self.classe = 'Comentario'

        if(estado in [14, 15, 16, 18, 19, 20]):
            self.classe = 'OPR'

        if(estado == 17):
            self.classe = 'ATR'

        if(estado == 21):
            self.classe = 'OPA'

        if(estado == 22):
            self.classe = 'AB_P'

        if(estado == 23):
            self.classe = 'FC_P'

        if(estado == 24):
            self.classe = 'PT_V'

        if(estado == 25):
            self.classe = 'VIR'

        if(self.classe == "ERRO"):
            print('Classe:', self.classe,  ', Lexema:', self.lexema, ', Tipo:', self.tipo)
            if(estado in [2, 4, 5]):
                print("ERRO LEXICO - Palavra inválida, linha", linha, ", coluna", coluna)
            if(estado == 0):
                print("ERRO LEXICO - Caractere inválido na linguagem, linha", linha, ", coluna", coluna)
            if(estado == 10):
                print("ERRO LEXICO -  Palavra inválida na linguagem (EOF enquanto lendo um literal), linha", linha, ", coluna", coluna)


    def q0(self):
        c = self.retorna_char(posicao)
        alpha = self.se_alfabeto(c)
        if(alpha):
            if(self.se_digito(c)):
                self.q1()
            else:
                if(self.se_letra(c)):
                    self.q7()
                else:
                    if(c == '"'):
                        self.q10()
                    else:
                        if(c == '{'):
                            self.q12()
                        else:
                            if(c == '<'):
                                self.q14()
                            else:
                                if(c == '='):
                                    self.q18()
                                else:
                                    if(c == '>'):
                                        self.q19()
                                    else:
                                        if(c in ['+', '-', '*', '/']):
                                            self.q21()
                                        else:
                                            if(c == '('):
                                                self.q22()
                                            else:
                                                if(c == ')'):
                                                    self.q23()
                                                else:
                                                    if(c == ';'):
                                                        self.q24()
                                                    else:
                                                        if(c == ','):
                                                            self.q25()
                                                        else:
                                                            self.atualiza_posicao()
        else:
            if(c == ' ' or c == '\n'):
                if(c == '\n'):
                    global linha
                    global coluna
                    linha = linha + 1
                    coluna = 0
                self.atualiza_posicao()
            else:
                if(c == '$' and tamanho-1 == posicao):
                    self.q9()
                else:
                    self.vet.append(c)
                    self.aceita(0)
                    self.atualiza_posicao()


    def q1(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 1

        if(self.se_digito(prox) or prox == '.' or prox == 'E' or prox == 'e'):
            if(self.se_digito(prox)):          
                self.q1()
            else:
                if(prox == '.'):
                    self.q2()
                if(prox == 'E' or prox == 'e'):
                    self.q4()
        else:
            self.aceita(estado)
    
    def q2(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 2

        if(self.se_digito(prox)):
            self.q3()
        else:
            self.aceita(estado)

    def q3(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 3

        if(self.se_digito(prox)):
            self.q3()
        else:
            if(prox == 'E' or prox == 'e'):
                self.q4()
            else:
                self.aceita(estado)
                
    def q4(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 4

        if(self.se_digito(prox)):
            self.q6()
        else:
            if(prox == '+' or prox == '-'):
                self.q5()
            else:
                self.aceita(estado)

    def q5(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 5

        if(self.se_digito(prox)):
            self.q6()
        else:
            self.aceita(estado)

    def q6(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 6

        if(self.se_digito(prox)):
            self.q6()
        else:
            self.aceita(estado)


    def q7(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 7

        if(self.se_letra(prox) or self.se_digito(prox) or prox == '_'):
            self.q8()
        else:
            self.aceita(estado)

    def q8(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 8

        if(self.se_letra(prox) or self.se_digito(prox) or prox == '_'):
            self.q8()
        else:
            self.aceita(estado)

    
    def q9(self):
        self.atualiza_posicao()
        estado = 9

        self.aceita(estado)


    def q10(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        if(c != '\n'):
            self.vet.append(c)

        estado = 10

        if(prox == '"'):
            self.q11()
        else:
            if(prox == '$' and tamanho-1 == posicao):
                self.aceita(estado)
            else:
                self.q10()

    def q11(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 11

        self.aceita(estado)

    
    def q12(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 12

        if(prox == "}"):
            self.q13()
        else:
            if(prox == '$' and tamanho-1 == posicao):
                self.aceita(estado)
            else:    
                self.q12()

    def q13(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 13

        self.aceita(estado)


    def q14(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 14

        if(prox in ['=', '>', '-']):
            if(prox == '='):
                self.q15()
            if(prox == '>'):
                self.q16()
            if(prox == '-'):
                self.q17()
        else:
            self.aceita(estado)

    def q15(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 15

        self.aceita(estado)

    def q16(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 16

        self.aceita(estado)

    def q17(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 17

        self.aceita(estado)


    def q18(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 18

        self.aceita(estado)


    def q19(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        prox = self.retorna_char(posicao)
        self.vet.append(c)
        estado = 19

        if(prox == '='):
            self.q20()
        else:
            self.aceita(estado)
    
    def q20(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 20

        self.aceita(estado)


    def q21(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 21

        self.aceita(estado)


    def q22(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 22

        self.aceita(estado)
        

    def q23(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 23

        self.aceita(estado)
    

    def q24(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 24

        self.aceita(estado)


    def q25(self):
        c = self.retorna_char(posicao)
        self.atualiza_posicao()
        self.vet.append(c)
        estado = 25

        self.aceita(estado)



if __name__ == '__main__':

    teste = True
    while (teste):
        tk = Token()
        sc = tk.Scanner()
        if(tk.classe != "ERRO" and sc != -1):
            print('Classe:', tk.classe,  ', Lexema:', tk.lexema, ', Tipo:', tk.tipo)
        if(tamanho == posicao):
            teste = False
        
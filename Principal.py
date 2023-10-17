import numpy as np
import math
import random
import matplotlib.pyplot as plt

def x(theta):
    return (1 - math.cos(theta))/2  

def pontos():
    pontos = []
    for i in range(0, 500):
        theta = random.uniform(0, math.pi)
        valor = x(theta)
        pontos.append(valor)
    return pontos
    
def SplineNatural(x, a):
    h = []
    
    n = len(x)
    
    for i in range(1, n):
        h.append(x[i] - x[i-1])
    
    alpha = [0]
    for j in range(1, n-1):
        alpha.append((3/h[j])* (a[j+1] - a[j]) - (3/h[j-1])*(a[j] - a[j - 1]))
        
    b, c, d, l, mi, z = n*[0], n*[0], n*[0], n*[0], n*[0], n*[0]
    l[0] = 1
    mi[0] = 0
    z[0] = 0
    
    for i in range(1, n-1):
        l[i] = 2*(x[i+1] - x[i-1]) - h[i-1]*mi[i-1]
        mi[i] = h[i]/l[i]
        z[i] = (alpha[i] - h[i-1]*z[i-1])/l[i]
    
    l[-1] = 1
    z[-1] = 0
    c[-1] = 0
    
    for k in range(n - 2, -1, -1):
        c[k] = z[k] - mi[k]*c[k+1]
        b[k] = (a[k+1] - a[k])/h[k] - (h[k]*(c[k+1]+2*c[k]))/3
        d[k] = (c[k+1] - c[k])/(3*h[k])

    # Certifique-se de que a, b, c e d tenham o mesmo tamanho que x
    a = a[:-1]  # Remove o último elemento de a
    b = b[:-1]  # Remove o último elemento de b
    c = c[:-1]  # Remove o último elemento de c
    d = d[:-1]  # Remove o último elemento de d
    
    return a, b, c, d

def EspessuraMaxima(x, fxCima, fxBaixo):
    espessura_max = 0
    ponto_espessura_max = 0
    
    for i in range(len(x)):
        espessura = abs(fxCima[i] - fxBaixo[i])
        if espessura > espessura_max:
            espessura_max = espessura
            ponto_espessura_max = x[i]
            
    return ponto_espessura_max, espessura_max
        

def Main():
    opcao = input('Digite a Spline que deseja ver: \n 1 - ah79100b.txt \n 2 - goe122.txt \n 3 - fx05h126.txt\n')
    
    arq = ""
    
    if opcao == '1':
        arq = "ah79100b.txt"
    
    elif opcao == '2':
        arq = "goe122.txt"
    
    elif opcao == '3':
        arq = "fx05h126.txt"
    
    xCima = []  # Lista para x de cima
    fxCima = []  # Lista para fx de cima
    xBaixo = []  # Lista para x de baixo
    fxBaixo = []  # Lista para fx de baixo
    lendo_cima = True  # Indica se estamos lendo os pontos de cima
    
    with open(arq,'r') as arquivo:
        linhas = arquivo.readlines()
        
        # Comece a ler após a terceira linha
        linhas = linhas[3:]
        
        for linha in linhas:
            valores = linha.split()
            
            # Verifique se a linha está vazia, o que indica um separador entre os blocos
            if not valores:
                lendo_cima = not lendo_cima  # Alterne entre os blocos de cima e de baixo
            else:
                valor1 = float(valores[0])
                valor2 = float(valores[1])
                
                # Adicione os pontos à lista apropriada
                if lendo_cima:
                    xCima.append(valor1)
                    fxCima.append(valor2)
                else:
                    xBaixo.append(valor1)
                    fxBaixo.append(valor2)
    
    # Agora você tem 'xCima', 'fxCima', 'xBaixo' e 'fxBaixo' com os pontos separados
    # Calcule as splines cúbicas para cada parte da asa
    a1, b1, c1, d1 = SplineNatural(xCima, fxCima)
    a2, b2, c2, d2 = SplineNatural(xBaixo, fxBaixo)
    
    valores_x = pontos()
    
    # Use a função SplineNatural para calcular os valores correspondentes de fx_grafico
    fx_grafico_cima = []
    for xi in valores_x:
        i = 0
        while i < len(xCima) - 1 and xi > xCima[i + 1]:
            i += 1
        dx = xi - xCima[i]
        fx = a1[i] + b1[i] * dx + c1[i] * dx**2 + d1[i] * dx**3
        fx_grafico_cima.append(fx)
        
    fx_grafico_baixo = []
    for xi in valores_x:
        i = 0
        while i < len(xBaixo) - 1 and xi > xBaixo[i + 1]:
            i += 1
        dx = xi - xBaixo[i]
        fx = a2[i] + b2[i] * dx + c2[i] * dx**2 + d2[i] * dx**3
        fx_grafico_baixo.append(fx)
    
    ponto_espessura_max, espessura_max = EspessuraMaxima(valores_x, fx_grafico_cima, fx_grafico_baixo)
    
    print(f'Ponto de espessura máxima: {ponto_espessura_max} \nEspessura máxima: {espessura_max}')
    
    plt.scatter(valores_x, fx_grafico_cima, color = 'k', s = 5)
    plt.scatter(valores_x, fx_grafico_baixo, color = 'k', s = 5)
    
    plt.axis([0, 1, -0.3, 0.3])
    plt.xticks(np.linspace(0.0, 1.0, num=11))
    plt.xlabel(f"Ponto de espessura máxima = {ponto_espessura_max} \n Espessura máxima = {espessura_max}")
    plt.grid()
    plt.legend()
    plt.gca().set_aspect("equal")
    plt.show()
    
Main()
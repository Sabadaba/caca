import numpy as np
import cv2 as cv
import heapq


def code(frame):
    
    diccionario ={} 
    zigzag_completo = [] 
    #Cuatificacion y dct
    Q = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
              [12, 12, 14, 19, 26, 58, 60, 55],
              [14, 13, 16, 24, 40, 57, 69, 56],
              [14, 17, 22, 29, 51, 87, 80, 62],
              [18, 22, 37, 56, 68, 109, 103, 77],
              [24, 35, 55, 64, 81, 104, 113, 92],
              [49, 64, 78, 87, 103, 121, 120, 101],
              [72, 92, 95, 98, 112, 100, 103, 99]]) 
    
    percent = 97  
    dct_quant = np.zeros_like(frame, dtype=np.float32)
    Q = dynamic_Q_matrix(percent)
    for i in range(0, frame.shape[0], 8):
        for j in range(0, frame.shape[1], 8):
            sub_dct = cv.dct(frame[i:(i+8),j:(j+8)].astype('float32'))
            dct_quant[i:(i+8),j:(j+8)] = np.round(sub_dct/Q)
            zigzag_matrix=zigzag2(dct_quant[i:(i+8),j:(j+8)])
            zigzag_completo.append(zigzag_matrix)
            diccionario = run_length_encoding(zigzag_matrix,diccionario)  
       
    
#Codificacion de huffmann
    # Construir dendograma con las probabilidades ordenadas
    dendograma = [[frequencia/64, [simbolo, ""]] for simbolo, frequencia in diccionario.items()]
    heapq.heapify(dendograma)
    while len(dendograma) > 1:
        lo = heapq.heappop(dendograma)
        hi = heapq.heappop(dendograma)
        for codigo in lo[1:]:
            codigo[1] = '0' + codigo[1]
        for codigo in hi[1:]:
            codigo[1] = '1' + codigo[1]
        heapq.heappush(dendograma, [lo[0] + hi[0]] + lo[1:] + hi[1:])    
    dendograma = sorted(heapq.heappop(dendograma)[1:])
    dendograma = {simbolo : codigo for simbolo, codigo in dendograma}  
    

    #Generar texto en una tira binaria
    texto_codificado = ""
    for letra in zigzag_completo:   
        for j in letra:
            texto_codificado += dendograma[j] 
    
    #Se envia el texto codificado y el dendograma

    palabra = texto_codificado+"-" + str(dendograma)
    
    return palabra

def decode(message):
    #Transformo el mensaje en string y le quito los caracteres que no me sirven
    message = str(message)
    a = ""
    for i in message:
        if i != '"' and i!='b':
            a = a + i
    message=a
    #Luego guardo en palabra el texto codificado y en dendo el dendograma como string
    palabra = ''
    dendo = ""
    i = 0
    while message[i] !='-':
        palabra = palabra + message[i]
        i=i+1
    i=i+1
    while i<len(message):
        dendo = dendo + message[i]
        i=i+1
    #Transformo el dendograma en un diccionario
    dendograma = eval(dendo)

    #Se decodifica el mensaje y se guarda en variable total para obtener el array de array que seria el zig zag.
    dendo_invers = {codigo: simbolo for simbolo, codigo in dendograma.items()}
    codigo = ""
    texto = []
    total = []   
    for i in range(len(palabra)):
        codigo += palabra[i]
        if codigo in dendo_invers:
            texto.append(dendo_invers[codigo])
            codigo = ""
            if (len(texto)==64):
                total.append(texto)
                texto=[]         
    total_invertido = []
    for i in total:
        total_invertido.append(zigzaginv2(i))  
    
    total_invertido = np.array(total_invertido)
    b = np.reshape(total_invertido,(1080,1920))
    #Descuantizacion
    im_recon = np.zeros_like(b)
    Q = dynamic_Q_matrix(97)
    for i in range(0, b.shape[0], 8):
        for j in range(0, b.shape[1], 8):
            sub_matrix = b[i:(i+8),j:(j+8)]
            im_recon[i:(i+8),j:(j+8)] = cv.dct(sub_matrix*Q, flags=cv.DCT_INVERSE).astype('uint8')
    
    
    
    return im_recon.astype('uint8')

def denoise(frame):
    return frame

#Funcion rle
def run_length_encoding(array,count_dict):
    for i in array:
        if (i in count_dict):
            count_dict[i] += 1
        else:
            count_dict[i] = 1
    return count_dict


#zigzag recuperado y modificado, https://es.acervolima.com/matriz-de-impresion-en-zig-zag/
def zigzag2(matrix):
    rows=8
    columns=8
    solution=[[] for i in range(rows+columns-1)]
    for i in range(rows):
        for j in range(columns):
            sum=i+j
            if(sum%2 ==0):
                #add at beginning
                solution[sum].insert(0,matrix[i][j])
            else:
                #add at end of the list
                solution[sum].append(matrix[i][j])
    solution2=[]
    for i in solution:
        for j in i:
            solution2.append(j) 
    return solution2

#ZigZag Inverso.
def zigzaginv2(matriz):
    Index= [0, 1, 8, 16, 9, 2, 3, 10, 17, 24, 32, 25, 18, 11, 4, 5, 12, 19, 26, 33, 40, 48, 41, 34, 27, 20, 13, 6, 7, 14, 21, 28, 35, 42, 49, 56, 57, 50, 43, 36, 29, 22, 15, 23, 30, 37, 44, 51, 58, 59, 52, 45, 38, 31, 39, 46, 53, 60, 61, 54, 47, 55, 62, 63]    
    matrix = []
    for i in range(64):
            if Index[i] != i:
                for k in range(64):
                    if Index[k] == i:
                        matrix.append(matriz[k])
            else:
                matrix.append(matriz[i])
    return matrix

#Funcion percent dynamic q matrix
def dynamic_Q_matrix(percent):
    Q = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
              [12, 12, 14, 19, 26, 58, 60, 55],
              [14, 13, 16, 24, 40, 57, 69, 56],
              [14, 17, 22, 29, 51, 87, 80, 62],
              [18, 22, 37, 56, 68, 109, 103, 77],
              [24, 35, 55, 64, 81, 104, 113, 92],
              [49, 64, 78, 87, 103, 121, 120, 101],
              [72, 92, 95, 98, 112, 100, 103, 99]])
    if (percent < 50):
        S = 5000/percent
    else:
        S = 200 - 2*percent 
    Q_dyn = np.floor((S*Q + 50) / 100);
    Q_dyn[Q_dyn == 0] = 1
    return Q_dyn

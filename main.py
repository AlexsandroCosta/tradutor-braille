from processamento_imagem import ProcessadorImagem
import cv2

if __name__ == "__main__":
 
    for i in range(1, 12):
        processador = ProcessadorImagem(f'{i}.jpg')

        processador.mostrar_resultados()

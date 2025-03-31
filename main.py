from processamento_imagem import ProcessadorImagem
import cv2

if __name__ == "__main__":
    imagens = ['1.jpg', '3.png', '5.webp', '6.jpg']

    for imagem in imagens:
        processador = ProcessadorImagem(imagem)

        processador.mostrar_resultados()
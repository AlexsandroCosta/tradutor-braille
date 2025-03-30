from processamento_imagem import ProcessadorImagem
import cv2

if __name__ == "__main__":
    processador = ProcessadorImagem("1.jpg")

    processador.mostrar_resultados()
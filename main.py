from processamento_imagem import ProcessadorImagem
import cv2

if __name__ == "__main__":
    processador = ProcessadorImagem("L1ZzA.jpg")

    cv2.imshow("Original", processador.imagem_original)
    cv2.imshow("Processada", processador.imagem_processada)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
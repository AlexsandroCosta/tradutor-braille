from processamento_imagem import ProcessadorImagem
from tradutor_texto import TradutoTexto
import cv2

if __name__ == "__main__":
 
    # for i in range(1, 12):
    #     processador = ProcessadorImagem(f'{i}.jpg')

    #     processador.mostrar_resultados()

    trautor_texto = TradutoTexto('imagens_texto/download.png')
    print(trautor_texto.traduzir_para_braille())

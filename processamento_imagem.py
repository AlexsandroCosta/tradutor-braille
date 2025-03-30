import cv2
import numpy
from typing import Optional

class ProcessadorImagem:
    def __init__(self, caminho_imagem: str, params: Optional[dict] = None):
        self.params = {
            'median_blur_kernel': 3,
            'adaptive_block_size': 21,
            'adaptive_c': 6,
            'morph_kernel_size': 3
        }
        if params:
            self.params.update(params)

        # Carregar imagem
        self.imagem_original = self._carregar_imagem(caminho_imagem)
        if self.imagem_original is None:
            raise IOError(f'Não foi possível abrir a imagem: {caminho_imagem}')
        
        self.imagem_processada = self.processar_imagem()

    def _carregar_imagem(self, caminho: str) -> numpy.ndarray:
        imagem = cv2.imread(caminho)
        if imagem is None:
            raise IOError(f'Não foi possível abrir a imagem: {caminho}')
        
        return imagem

    def processar_imagem(self) -> numpy.ndarray:
        imagem_cinza = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2GRAY)

        # Aplicação do CLAHE (Equalização Adaptativa de Histograma) para melhorar o contraste local da imagem.
        # O 'clipLimit' controla o limite de contraste e o 'tileGridSize' define o tamanho dos blocos para a equalização.
        clahe = cv2.createCLAHE(
            clipLimit=2,
            tileGridSize=(8, 8)
        )
        imagem_cinza = clahe.apply(imagem_cinza)

        # Redução de ruídos
        imagem_suavizada = cv2.medianBlur(
            imagem_cinza,
            self.params['median_blur_kernel']
        )

        imagem_binaria = cv2.adaptiveThreshold(
            imagem_suavizada, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            self.params['adaptive_block_size'],
            self.params['adaptive_c']
        )

        kernel = numpy.ones(
            (self.params['morph_kernel_size'],)*2,
            numpy.uint8
        )

        # Aplicar a Abertura (Opening) - Remove pequenos ruídos brancos
        imagem_sem_ruido = cv2.morphologyEx(imagem_binaria, cv2.MORPH_OPEN, kernel)

        # Aplicar o Fechamento (Closing) - Fecha pequenos buracos pretos
        imagem_processada = cv2.morphologyEx(imagem_sem_ruido, cv2.MORPH_CLOSE, kernel)

        return imagem_processada


# # Detectar e destacar contornos
# contours, _ = cv2.findContours(imagem_sem_buracos, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# resultado = cv2.cvtColor(grayimage, cv2.COLOR_GRAY2BGR)  # Imagem colorida para destaque
# cv2.drawContours(resultado, contours, -1, (0, 255, 0), 1)


# cv2.imshow("grayimage", grayimage)
# cv2.imshow("thresholdimage", thresholdimage)
# cv2.imshow("imagem_sem_buracos", imagem_sem_buracos)
# cv2.imshow("resultado", resultado)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
import cv2
import numpy
import math

class ProcessadorImagem:
    def __init__(self, caminho_imagem: str):
        # Carregar imagem
        self.imagem_original = self._carregar_imagem(caminho_imagem)
        self.imagem_processada = self.processar_imagem()

    def _carregar_imagem(self, caminho: str) -> numpy.ndarray:
        imagem = cv2.imread(caminho)
        if imagem is None:
            raise IOError(f'Não foi possível abrir a imagem: {caminho}')
        
        return imagem

    def processar_imagem(self) -> numpy.ndarray:
        # Conversão para escala de cinza
        imagem_cinza = cv2.cvtColor(self.imagem_original, cv2.COLOR_BGR2GRAY)

        # Correção de gamma (ajuste de brilho/contraste)
        imagem_cinza = self._correcao_gamma(imagem_cinza)

        # Aplicação do CLAHE (Equalização Adaptativa de Histograma) para melhorar o contraste local da imagem.
        # O 'clipLimit' controla o limite de contraste e o 'tileGridSize' define o tamanho dos blocos para a equalização.
        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )
        imagem_cinza = clahe.apply(imagem_cinza)

        # Redução de ruídos
        imagem_suavizada = cv2.medianBlur(imagem_cinza, 3)
        imagem_suavizada = cv2.GaussianBlur(imagem_suavizada, (5, 5), 0)

        # Limiarização adaptativa (para destacar pontos)
        imagem_binaria = cv2.adaptiveThreshold(
            imagem_suavizada, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 4
        )

        # Operações morfológicas: erosão para separar pontos conectados e dilatação para recuperar forma
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        imagem_erodida = cv2.erode(imagem_binaria, kernel, iterations=1)
        imagem_processada = cv2.dilate(imagem_erodida, kernel, iterations=1)

        # imagem_sem_ruido = cv2.morphologyEx(imagem_binaria, cv2.MORPH_OPEN, kernel)
        # imagem_processada = cv2.morphologyEx(imagem_sem_ruido, cv2.MORPH_CLOSE, kernel)

        imagem_processada = self._remover_ruido(imagem_processada)

        return imagem_processada

    def _correcao_gamma(self, imagem: numpy.ndarray) -> numpy.ndarray:
        gamma = self._calcular_gamma(imagem)
        
        inversor_gamma = 1.0/gamma
        tabela = numpy.array([((i/255.0)**inversor_gamma) * 255 for i in numpy.arange(0, 256)]).astype('uint8')
        
        return cv2.LUT(imagem, tabela)
    
    def _calcular_gamma(self, imagem:numpy.ndarray) -> float:
        brilho_medio = numpy.mean(imagem)
        gamma = math.log(0.5) / math.log(brilho_medio/255) if brilho_medio > 0 else 1

        return max(0.5, min(gamma, 3.0))
    
    def _remover_ruido(self, imagem:numpy.ndarray) -> numpy.ndarray:
        # Inverter a imagem para connectedComponents funcionar corretamente
        imagem_invertida = cv2.bitwise_not(imagem)

        # Encontrar componentes conectados
        n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            imagem_invertida, 
            connectivity=8
        )

        mascara = numpy.zeros(imagem.shape, dtype=numpy.uint8)

        for i in range(1, n_labels):  # Ignorar o fundo (componente 0)
            area = stats[i, cv2.CC_STAT_AREA]
            width = stats[i, cv2.CC_STAT_WIDTH]
            height = stats[i, cv2.CC_STAT_HEIGHT]

            # Filtro baseado na área e proporção
            if 5 < area < 150 and 0.7 < (width/height) < 1.3:  # Mantém apenas elementos aproximadamente quadrados/circulares
                # Manter componentes válidos
                mascara[labels == i] = 255
        
        # Reaplicar máscara mantendo a orientação original
        resultado = cv2.bitwise_and(imagem, imagem, mask=cv2.bitwise_not(mascara))
        return resultado
    
    def mostrar_resultados(self):
        cv2.imshow('Processada', self.imagem_processada)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
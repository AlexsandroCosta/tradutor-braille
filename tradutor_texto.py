import pytesseract
import numpy
import cv2
import mimetypes
import fitz
from mapa_braille import mapa_braille

class TradutoTexto:
    def __init__(self, caminho_arquivo: str):
        self.texto_extraido = self._extrair_texto(caminho_arquivo)

    def _carregar_arquivo(self, caminho_arquivo: str) -> tuple[str, numpy.ndarray | fitz.Document]:
        tipo, _ = mimetypes.guess_type(caminho_arquivo)

        if tipo:
            if tipo.startswith('image'):
                tipo_arquivo = 'imagem'
                arquivo = cv2.imread(caminho_arquivo)
            elif tipo == 'application/pdf':
                tipo_arquivo = 'pdf'
                arquivo = fitz.open(caminho_arquivo)

        return tipo_arquivo, arquivo
    
    def _extrair_texto_imagem(self, imagem: numpy.ndarray) -> str:
        return pytesseract.image_to_string(imagem)

    def _extrair_texto_pdf(self, pdf: fitz.Document) -> str:
        texto = ''

        for pagina in pdf:
            texto += pagina.get_textpage().extractText()
        
        return texto

    def _extrair_texto(self, caminho_arquivo: str) -> str:
        tipo_arquivo, arquivo = self._carregar_arquivo(caminho_arquivo)

        if tipo_arquivo == 'imagem':
            texto_extraido = self._extrair_texto_imagem(arquivo)
        else:
            texto_extraido = self._extrair_texto_pdf(arquivo)

        return texto_extraido
    
    def traduzir_para_braille(self) -> str:
        traducao = ''

        for linha in self.texto_extraido.lower():
            for letra in linha:
                if letra in mapa_braille:
                    traducao += mapa_braille[letra]

        return traducao
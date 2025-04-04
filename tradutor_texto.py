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
        """Carrega o arquivo e retorna seu tipo e conteúdo."""
        tipo, _ = mimetypes.guess_type(caminho_arquivo)

        try:
            if tipo:
                if tipo.startswith('image'):
                    tipo_arquivo = 'imagem'
                    arquivo = cv2.imread(caminho_arquivo)
                
                elif tipo == 'application/pdf':
                    tipo_arquivo = 'pdf'
                    arquivo = fitz.open(caminho_arquivo)
                
                else:
                    raise ValueError('Tipo de arquivo não suportado')
        except Exception as e:
            raise ValueError(f'Erro ao carregar arquivo: {str(e)}')

        return tipo_arquivo, arquivo
    
    def _extrair_texto_imagem(self, imagem: numpy.ndarray) -> str:
        """Extrai texto de uma imagem usando OCR."""
        try:
            return pytesseract.image_to_string(imagem)
        except Exception as e:
            raise RuntimeError(f"Erro ao extrair texto da imagem: {str(e)}")

    def _extrair_texto_pdf(self, pdf: fitz.Document) -> str:
        """Extrai texto de um arquivo PDF."""
        try:
            texto = []

            for pagina in pdf:
                texto.append(pagina.get_textpage().extractText())
            
            return ''.join(texto)
        except Exception as e:
            raise RuntimeError(f"Erro ao extrair texto do PDF: {str(e)}")
        finally:
            pdf.close()

    def _extrair_texto(self, caminho_arquivo: str) -> str:
        tipo_arquivo, arquivo = self._carregar_arquivo(caminho_arquivo)

        if tipo_arquivo == 'imagem':
            return self._extrair_texto_imagem(arquivo)
        else:
            return self._extrair_texto_pdf(arquivo)

    def traduzir_para_braille(self) -> str:
        """Traduz o texto extraído para Braille."""
        traducao = []

        try:
            for linha in self.texto_extraido.lower():
                for letra in linha:
                        traducao.append(mapa_braille.get(letra, ''))

            return ''.join(traducao)
        except Exception as e:
            raise RuntimeError(f"Erro durante a tradução: {str(e)}")
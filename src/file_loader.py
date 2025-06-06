import PyPDF2
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class FileLoader:
    """Handles loading and processing of resume and personal info files"""

    @staticmethod
    def load_pdf_content(file_path: str) -> str:
        """
        Extract text content from PDF resume

        Args:
            file_path: Path to the PDF file

        Returns:
            Extracted text content
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                content = ""

                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            content += page_text + "\n"
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num}: {str(e)}")
                        continue

                if not content.strip():
                    raise ValueError("No text content extracted from PDF")

                return content.strip()

        except FileNotFoundError:
            error_msg = f"PDF file not found: {file_path}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Error loading PDF: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"

    @staticmethod
    def load_txt_content(file_path: str) -> str:
        """
        Load personal information from text file

        Args:
            file_path: Path to the text file

        Returns:
            Text content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()

                if not content:
                    raise ValueError("Text file is empty")

                return content

        except FileNotFoundError:
            error_msg = f"Text file not found: {file_path}"
            logger.error(error_msg)
            return f"Error: {error_msg}"
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read().strip()
                    return content
            except Exception as e:
                error_msg = f"Error reading text file with encoding: {str(e)}"
                logger.error(error_msg)
                return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Error loading text file: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"

    @staticmethod
    def validate_content(pdf_content: str, txt_content: str) -> bool:
        """
        Validate that loaded content is usable

        Args:
            pdf_content: Content from PDF
            txt_content: Content from text file

        Returns:
            True if content is valid
        """
        if pdf_content.startswith("Error:"):
            logger.error(f"PDF content invalid: {pdf_content}")
            return False

        if txt_content.startswith("Error:"):
            logger.error(f"Text content invalid: {txt_content}")
            return False

        if len(pdf_content.strip()) < 100:
            logger.warning("PDF content seems too short")
            return False

        if len(txt_content.strip()) < 10:
            logger.warning("Text content seems too short")
            return False

        return True
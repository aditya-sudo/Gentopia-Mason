from typing import Any, Optional, Type
from pydantic import BaseModel, Field
from PyPDF2 import PdfReader
from googlesearch import search
from gentopia.tools.basetool import *
import requests
import os


class PDFReaderArgs(BaseModel):
    file_path_or_url: str = Field(
        ..., description="Path to the PDF file or URL of the PDF file"
    )


class PDFReader(BaseTool):
    """Tool that adds the capability to read and extract text from a PDF file."""

    name = "pdf_reader"
    description = (
        "A tool that extracts text from a given PDF file or URL. "
        "Input should be the path or URL to the PDF file."
    )

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, file_path_or_url: str) -> str:
        try:
            # Check if the input is a URL
            if file_path_or_url.startswith(("http://", "https://")):
                response = requests.get(file_path_or_url)
                if response.status_code == 200:
                    # Save the downloaded PDF to a temporary file
                    temp_file_path = "temp.pdf"
                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(response.content)
                    file_path = temp_file_path
                else:
                    return "Failed to download the PDF from the provided URL."
            else:
                file_path = file_path_or_url

            # Open and read the PDF file
            reader = PdfReader(file_path)
            extracted_text = []
            for index, page in enumerate(reader.pages):
                text = page.extract_text()
                extracted_text.append(f"Page {index + 1}:\n{text}\n")

            # Remove the temporary file if it was created
            if file_path == "temp.pdf":
                os.remove(file_path)

            return "\n".join(extracted_text)

        except FileNotFoundError:
            return "The specified file was not found."
        except Exception as e:
            return f"An error occurred: {e}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    # Example: Google search for a PDF link and then read it
    query = "sample PDF file"
    search_results = search(query, num_results=5)
    pdf_url = None

    for result in search_results:
        if result.endswith(".pdf"):
            pdf_url = result
            break

    if pdf_url:
        pdf_reader = PDFReader()
        ans = pdf_reader._run(pdf_url)
        print(ans)
    else:
        print("No PDF link found in the search results.")

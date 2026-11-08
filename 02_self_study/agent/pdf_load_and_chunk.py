from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

pdf_path = next(Path(".").glob("SPRi*.pdf"))

loader = PyPDFLoader(str(pdf_path))
pages = loader.load()

print("페이지 수:", len(pages))
print("메타데이터:", pages[0].metadata)

splitter = RecursiveCharacterTextSplitter(
  chunk_size=600,
  chunk_overlap=100
)

chunks = splitter.split_documents(pages)

print("청크 수:", len(chunks))
print("첫 청크:", chunks[0].page_content[:200])
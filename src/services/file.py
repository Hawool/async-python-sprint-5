from src.models.file import FileModel
from src.schemas.file import FileCreate, FileUpdate
from src.services.crud import RepositoryDB


class RepositoryFile(RepositoryDB[FileModel, FileCreate, FileUpdate]):
    pass


file_crud = RepositoryFile(FileModel)

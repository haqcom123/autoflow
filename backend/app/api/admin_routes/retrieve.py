import logging
from typing import Optional, List

from fastapi import APIRouter
from app.models import Document
from app.api.admin_routes.models import RetrieveRequest
from app.api.deps import SessionDep, CurrentSuperuserDep
from app.rag.retrieve import RetrieveService
from llama_index.core.schema import NodeWithScore

from app.exceptions import InternalServerError, KBNotFound

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/admin/retrieve/documents")
async def retrieve_documents(
    session: SessionDep,
    user: CurrentSuperuserDep,
    question: str,
    chat_engine: str = "default",
    top_k: Optional[int] = 5,
    similarity_top_k: Optional[int] = None,
    oversampling_factor: Optional[int] = 5,
) -> List[Document]:
    try:
        retrieve_service = RetrieveService(session, chat_engine)
        return retrieve_service.retrieve(
            question,
            top_k=top_k,
            similarity_top_k=similarity_top_k,
            oversampling_factor=oversampling_factor,
        )
    except KBNotFound as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise InternalServerError()


@router.get("/admin/embedding_retrieve")
async def embedding_retrieve(
    session: SessionDep,
    user: CurrentSuperuserDep,
    question: str,
    chat_engine: str = "default",
    top_k: Optional[int] = 5,
    similarity_top_k: Optional[int] = None,
    oversampling_factor: Optional[int] = 5,
) -> List[NodeWithScore]:
    try:
        retrieve_service = RetrieveService(session, chat_engine)
        return retrieve_service.embedding_retrieve(
            question,
            top_k=top_k,
            similarity_top_k=similarity_top_k,
            oversampling_factor=oversampling_factor,
        )
    except KBNotFound as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise InternalServerError()


@router.post("/admin/embedding_retrieve")
async def embedding_search(
    session: SessionDep,
    user: CurrentSuperuserDep,
    request: RetrieveRequest,
) -> List[NodeWithScore]:
    try:
        retrieve_service = RetrieveService(session, request.chat_engine)
        return retrieve_service.embedding_retrieve(
            request.query,
            top_k=request.top_k,
            similarity_top_k=request.similarity_top_k,
            oversampling_factor=request.oversampling_factor,
        )
    except KBNotFound as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise InternalServerError()

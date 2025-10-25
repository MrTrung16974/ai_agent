from fastapi import APIRouter, Depends, HTTPException, status

from .. import crud, schemas
from ..db import get_db

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[schemas.Item])
async def list_items(skip: int = 0, limit: int = 100, session=Depends(get_db)):
    return await crud.item_crud.get_multi(session=session, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
async def create_item(item_in: schemas.ItemCreate, session=Depends(get_db)):
    return await crud.item_crud.create(session=session, item_in=item_in)


@router.get("/{item_id}", response_model=schemas.Item)
async def get_item(item_id: int, session=Depends(get_db)):
    item = await crud.item_crud.get(session=session, item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=schemas.Item)
async def update_item(item_id: int, item_in: schemas.ItemUpdate, session=Depends(get_db)):
    item = await crud.item_crud.get(session=session, item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return await crud.item_crud.update(session=session, item=item, item_in=item_in)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, session=Depends(get_db)):
    item = await crud.item_crud.get(session=session, item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await crud.item_crud.remove(session=session, item=item)
    return None

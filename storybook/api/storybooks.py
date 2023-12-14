from datetime import datetime
from typing import List
from ninja import Router
from storybook.models import Storybook
from storybook.schema import StorybookSchema, StorybookResponseSchema, NotFoundSchema

router = Router()

@router.get("", response=List[StorybookResponseSchema])
def storybooks(request):
    return 200, Storybook.objects.all() 

@router.get("/{storybook_id}", response={200: StorybookResponseSchema, 404: NotFoundSchema})
def storybook(request, storybook_id: str):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        return storybook
    except Storybook.DoesNotExist as e:
        return 404, {"message": "Storybook does not exist"}

@router.post("", response={201: StorybookResponseSchema})
def create_storybook(request, storybook: StorybookSchema):
    storybook_data = storybook.dict()
    storybook_data['createdAt'] = datetime.now()
    new_storybook = Storybook.objects.create(**storybook_data)
    return 201, new_storybook

@router.put("/{storybook_id}", response={200:StorybookResponseSchema, 404: NotFoundSchema})
def change_storybook(request, storybook_id: str, data: StorybookSchema):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        for attribute, value in data.dict().items():
            setattr(storybook, attribute, value)
        storybook.save()
        return 200, storybook
    except Storybook.DoesNotExist as e:
        return 404, {"message", "Storybook does not exist"} 

@router.delete("/{storybook_id}", response={200: None, 404: NotFoundSchema})
def delete_storybook(request, storybook_id: str):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        storybook.delete()
        return 200
    except Storybook.DoesNotExist as e:
        return 404, {"message": "Storybook does not exist"}
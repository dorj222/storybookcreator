from typing import List
from ninja import NinjaAPI
from storybook.models import Storybook
from storybook.schema import StorybookSchema, NotFoundSchema

api = NinjaAPI()

@api.get("/storybooks", response=List[StorybookSchema])
def storybooks(request):
    return Storybook.objects.all()

@api.get("/storybooks/{storybook_id}", response={200: StorybookSchema, 404: NotFoundSchema})
def storybook(request, storybook_id: int):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        return storybook
    except Storybook.DoesNotExist as e:
        return 404, {"message": "Storybook does not exist"}

@api.post("/storybooks", response={201: StorybookSchema})
def create_storybook(request, storybook: StorybookSchema):
    storybook = Storybook.objects.create(**storybook.dict())
    return storybook

@api.put("/storybooks/{storybook_id}", response={200:StorybookSchema, 404: NotFoundSchema})
def change_storybook(request, storybook_id: int, data: StorybookSchema):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        for attribute, value in data.dict().items():
            setattr(storybook, attribute, value)
        storybook.save()
        return 200, storybook
    except Storybook.DoesNotExist as e:
        return 404, {"message", "Storybook does not exist"} 
    
@api.delete("/storybooks/{storybook_id}", response={200: None, 404: NotFoundSchema})
def delete_storybook(request, storybook_id: int):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        storybook.delete()
        return 200
    except Storybook.DoesNotExist as e:
        return 404, {"message": "Storybook does not exist"}
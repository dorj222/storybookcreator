import os
from uuid import UUID

from typing import List
from ninja import Router

from storybook.models import Storybook
from storybook.models import Description
from storybook.models import Image
from storybook.schema import DescriptionSchema, DescriptionResponseSchema, NotFoundSchema, DescriptionListResponseSchema

router = Router()

# Get all descriptions of a storybook
@router.get("/getall/{storybook_id}", response={200: DescriptionListResponseSchema, 404: NotFoundSchema})
def get_descriptions_by_storybook(request, storybook_id: UUID):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        descriptions = Description.objects.filter(storybook_id=storybook)
        description_data_list = [
            {
                "id": description.id,
                "image_id": description.image_id.id,
                "description": description.description,
            }
            for description in descriptions
        ]
        response_data = {
            "storybook_id": str(storybook.id),
            "description_list": description_data_list,
        }
        return 200, response_data 
    except Storybook.DoesNotExist:
        return 404, {"message": "Storybook does not exist"}
    except Description.DoesNotExist:
        return 404, {"message": "Storybook does not have any descriptions"}

# Get a description with the given description id
@router.get("/{description_id}", response={200: DescriptionResponseSchema, 404: NotFoundSchema})
def description(request, description_id: UUID):
    try:
        description = Description.objects.get(pk=description_id)
        response_data = {
            "id": str(description.id),
            "storybook_id": str(description.storybook_id.id), 
            "image_id": description.image_id.id,
            "description": description.description,
        }
        return 200, response_data
    except Description.DoesNotExist as e:
        return 404, {"message": "Description does not exist"}

# Create a description with a storybook id
@router.post("/create/{storybook_id}/{image_id}", response={201: DescriptionResponseSchema, 500: NotFoundSchema})
def create_description(request, storybook_id: UUID, image_id: UUID, description: DescriptionSchema):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        image = Image.objects.get(pk=image_id)
    except (Storybook.DoesNotExist, Image.DoesNotExist):
        return 404, {'message': 'Not Found'}

    try:
        description_data = description.dict()
        new_description = Description(
            storybook_id=storybook,
            image_id=image,
            description=description_data["description"]
        )
        new_description.save()
    except Exception as e:
        return 500, {"message": str(e)}

    response_data = {
        "id": str(new_description.id),
        "storybook_id": str(storybook.id),
        "image_id": str(image.id), 
        "description": new_description.description,
    }
    return 201, response_data
    
@router.delete("/{description_id}", response={200: None, 404: NotFoundSchema})
def delete_description(request, description_id: UUID):
    try:
        description = Description.objects.get(pk=description_id)
        description.delete()
        return 200
    except Description.DoesNotExist as e:
        return 404, {"message": "Description does not exist"}
    
@router.put("/{description_id}", response={200: DescriptionResponseSchema, 404: NotFoundSchema})
def update_description(request, description_id: UUID, updated_data: DescriptionSchema):
    try:
        existing_description = Description.objects.get(pk=description_id)
        existing_description.description = updated_data.description
        existing_description.save()

        response_data = {
            "id": str(existing_description.id),
            "storybook_id": str(existing_description.storybook_id.id),
            "image_id": str(existing_description.image_id.id),
            "description": existing_description.description,
        }
        return 200, response_data
    except Description.DoesNotExist as e:
        return 404, {"message": "Description does not exist"}
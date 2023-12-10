from datetime import datetime
from typing import List
from ninja import NinjaAPI
from storybook.models import Storybook
from storybook.models import Image
from storybook.schema import StorybookSchema, StorybookResponseSchema, NotFoundSchema
from storybook.schema import ImageSchema, ImageResponseSchema, ImageListResponseSchema
from uuid import UUID  # Import UUID

api = NinjaAPI()
# Retrieve all storybooks
@api.get("/storybooks", response=List[StorybookResponseSchema])
def storybooks(request):
    return 200, Storybook.objects.all() 

# Retrieve a storybook with a given id
@api.get("/storybooks/{storybook_id}", response={200: StorybookResponseSchema, 404: NotFoundSchema})
def storybook(request, storybook_id: str):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        return storybook
    except Storybook.DoesNotExist as e:
        return 404, {"message": "Storybook does not exist"}


# Create a new storybook
@api.post("/storybooks", response={201: StorybookResponseSchema})
def create_storybook(request, storybook: StorybookSchema):
     # Set the 'createdAt' field to the current date and time in the request data
    storybook_data = storybook.dict()
    storybook_data['createdAt'] = datetime.now()

    # Create a new storybook
    new_storybook = Storybook.objects.create(**storybook_data)

    # Return the id and other details of the newly created storybook
    return 201, new_storybook

# Edit a storybook with a given id
@api.put("/storybooks/{storybook_id}", response={200:StorybookResponseSchema, 404: NotFoundSchema})
def change_storybook(request, storybook_id: str, data: StorybookSchema):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        for attribute, value in data.dict().items():
            setattr(storybook, attribute, value)
        storybook.save()
        return 200, storybook
    except Storybook.DoesNotExist as e:
        return 404, {"message", "Storybook does not exist"} 

# Delete a storybook with a given id  
@api.delete("/storybooks/{storybook_id}", response={200: None, 404: NotFoundSchema})
def delete_storybook(request, storybook_id: str):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        storybook.delete()
        return 200
    except Storybook.DoesNotExist as e:
        return 404, {"message": "Storybook does not exist"}

# Retrieve storybook images with a given storybook id
@api.get("/images/{storybook_id}", response={200: ImageListResponseSchema, 404: NotFoundSchema})
def get_storybook_images(request, storybook_id: UUID):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
        images = Image.objects.filter(storybook_id=storybook)

        # Create a list of ImageSchema objects for each image
        image_schemas = [ImageSchema.from_orm(image) for image in images]

        response_data = {
        "storybook_id": str(storybook.id),  # Convert to string
        "description_list": image_schemas,
        }
        return response_data
    
    except Storybook.DoesNotExist:
        return 404, {"message": "Storybook does not exist"}
    except Image.DoesNotExist:
        return 404, {"message": "Storybook does not have any image"}


@api.post("/images/create/{storybook_id}", response={201: ImageResponseSchema, 404: NotFoundSchema})
def create_storybook_image(request, image: ImageSchema, storybook_id: UUID):
    try:
        storybook = Storybook.objects.get(pk=storybook_id)
    except Storybook.DoesNotExist:
        return 404, {'message': 'Not Found'}
    
    image_data = image.dict()
    image_data['storybook_id'] = storybook  # Use the correct UUID value here

    # Create a new image associated with the storybook
    new_image = Image.objects.create(**image_data)
    
    # Return the response with the correct UUID for storybook_id
    response_data = {
        "id": str(new_image.id),
        "storybook_id": str(storybook.id),  # Convert to string
        "description": new_image.description,
    }
    
    return 201, response_data
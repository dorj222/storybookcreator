from ninja import NinjaAPI, Router
from storybook.api.storybooks import router as storybooks_router
from storybook.api.images import router as images_router

api = NinjaAPI()
api.add_router("storybooks", storybooks_router)
api.add_router("images", images_router)
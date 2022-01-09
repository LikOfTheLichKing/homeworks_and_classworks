from .users import UserCRUD
from .posts import PostsCRUD
from .follow import FollowCRUD

users_crud = UserCRUD()
posts_crud = PostsCRUD()
follows_crud = FollowCRUD()

from models.posts import BaseCreatePostModel, CreatePostModel, ReturnPostModel
import sqlite3

from models.user import UserModel


class PostsCRUD:
    def create(
        self, conn: sqlite3.Connection, data: BaseCreatePostModel, user: UserModel
    ) -> None:
        data = CreatePostModel(**data.dict(), creator_id=user.id)
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO Posts(id, creator, image, description, created) "
                "VALUES(?, ?, ?, ?, ?)",
                (
                    data.id,
                    data.creator_id,
                    data.image,
                    data.description,
                    data.created,
                ),
            )
        finally:
            cur.close()

    def get_by_creator(
        self, conn: sqlite3.Connection, creator: UserModel
    ) -> list[ReturnPostModel]:
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT id, image, description, created "
                "FROM Posts "
                "WHERE creator=?"
                "ORDER BY created DESC",
                (creator.id,),
            )
            data = cur.fetchall()
            return [
                ReturnPostModel(
                    id=id,
                    creator=creator,
                    image=image,
                    description=description,
                    created=created,
                )
                for (id, image, description, created) in data
            ]
        finally:
            cur.close()

    def get_by_follower(
        self, conn: sqlite3.Connection, user: UserModel
    ) -> list[ReturnPostModel]:
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT Posts.id, Posts.image, Posts.description, Posts.created, User.id AS user_id, User.login "
                "FROM Posts "
                "JOIN Follow ON Posts.creator = Follow.follows "
                "JOIN User ON Posts.creator = User.id "
                "WHERE Follow.follower = ? "
                "ORDER BY created DESC",
                (user.id,),
            )
            data = cur.fetchall()
            return [
                ReturnPostModel(
                    id=id,
                    creator={"id": user_id, "login": user_login},
                    image=image,
                    description=description,
                    created=created,
                )
                for (id, image, description, created, user_id, user_login) in data
            ]
        finally:
            cur.close()

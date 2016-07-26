import uuid
import datetime
from src.models.post import Post
from src.common.database import Database

__author__ = 'sutirtho'


class Blog(object):
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        # title = input("Enter post title:")
        # content = input("Enter post content:")
        # date = input("Enter post date,or else leave blank for today in format DDMMYYYY):")
        # if date == "":
        #     date = datetime.datetime.utcnow()
        # else:
        #     date = datetime.datetime.strptime(date, "%d%m%Y")

        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'author_id': self.author_id,
            '_id': self._id,
        }

    @classmethod
    def from_mongo(cls, _id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': _id})
        return cls(author=blog_data['author'],
                   title=blog_data['title'],
                   description=blog_data['description'],
                   _id=blog_data['_id'],
                   author_id=blog_data['author_id'])

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs= Database.find(collection='blogs',query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]
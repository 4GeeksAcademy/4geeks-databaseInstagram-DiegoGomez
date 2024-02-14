import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

# Declaro la base de datos
Base = declarative_base()

# Clase usuario
class User(Base):
    # Nombre de la tabla
    __tablename__ = 'user'
    # Propiedades
    ID = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250))
    lastname = Column(String(250))
    email = Column(String(250), nullable=False)

    # La foreign_key hace referencia al user_to_id de la tabla followers, de esta forma 
    # en followers se almacenan los seguidores. Es una relacion de muchos a muchos, un usuario
    # puede ser seguido por otros muchos
    followers = relationship("Follower", foreign_keys="[Follower.user_to_id]")

    # De la misma forma, al almacenar los usuarios seguidos, se hace referencia a otro campo
    #de follower, pero esta vez al campo user_from_id, que almacena los ids de los usuarios seguidos.
    #Es una relación de muchos a muchos, ya que un usuario puede seguir a otros muchos.
    following = relationship("Follower", foreign_keys="[Follower.user_from_id]")

    # Esta relación hace referencia a user_id, el cual contiene el ID de la tabla usuarios.
    # Es una relación de uno a muchos, ya que muchos post pueden pertenecer a un usuario pero los post
    # solo pertenecen a un usuario concreto
    posts = relationship("Post", back_populates="user")

    # De la misma forma que con los post, esta es una relación de uno a muchos, ya que un usuario puede hacer
    # muchos comentarios pero todos pertenecen a ese usuario. Al usar back_populates, indico que author (se encuentra en la clase Comment)
    # es la propiedad a tener en cuenta al hacer de relación, de esta se relacionan los comentarios hechos por los usuarios.
    comments = relationship("Comment", back_populates="author")

# Clase Follower
class Follower(Base):
    # Nombre de la tabla
    __tablename__ = 'follower'
    # Propiedades
    ID = Column(Integer, primary_key=True)

    # Estas dos propiedades son las que se usan para los seguidores y los seguidos, hacen referencia al id
    # del usuario ya que es lo que se usa para identificarlos independiemente de si son seguidores o seguidos.
    user_from_id = Column(Integer, ForeignKey('user.ID'))
    user_to_id = Column(Integer, ForeignKey('user.ID'))

# Clase Media
class Media(Base):
    # Nombre de la tabla
    __tablename__ = 'media'
    # Propiedades
    ID = Column(Integer, primary_key=True)

    # Esta propiedad es distinta, es capaz de almacenar varios formatos debido a que con enum podemos especificar distintos
    # tipos de propiedad.
    type = Column(Enum('image', 'video', name='media_type_enum'), nullable=False)

    url = Column(String(250), nullable=False)
    # Esta foreign_key hace referencia al id de la tabla post, de esta forma, se crea una relación de muchos a uno, ya que 
    # aunque un post solo puede tener un id, esta publicación puede tener más de un elemento, como cuando se sube una foto y 2 videos
    # en un mismo post.
    post_id = Column(Integer, ForeignKey('post.ID'))

# Clase Post
class Post(Base):
    # Nombre de la tabla
    __tablename__ = 'post'
    # Propiedades
    ID = Column(Integer, primary_key=True)

    # Para asociar el post con un usuario, esta fk hace referencia al id del usuario que se encuentra en la tabla user.
    # Es una relación de muchos a uno, ya que un usuario puede tener varios post. Esto no sería el id de la publicación, sino
    # relacionar las publicaciones al id del usuario
    user_id = Column(Integer, ForeignKey('user.ID'))

    # Estas 2 relaciones no son obligatorias, pero facilitan el acceso a los post y comment de cada usuario, ya que al 
    # especificar la relación en back_populates es como hacer una especie de "acceso directo" para meterme a ver los post
    # y comentarios de cada usuario de una forma más fácil.
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    # En la clase media especifique sue puede almacenar varios tipos de post. Para que esto ocurra, he creado esta 
    # relación, que es unidireccional, es decir, que "los post se envían a media para almacenarlos ahí".
    media = relationship("Media")

# Clase Comment
class Comment(Base):
    # Nombre de la tabla
    __tablename__ = 'comment'
    # Propiedades
    ID = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)

    # Esta fk establece que un comentario está asociado a un único usuario, siendo el usuario identificado
    # por su ID como el autor del comentario, es decir, que el author_id es lo mismo que user.id. Es una relación de uno a uno.
    author_id = Column(Integer, ForeignKey('user.ID'))

    # Esta fk hace referencia al id de la tabla post, forma que un comentario puede pertenecer a un post
    # concreto, aunque podamos hacer varios comentarios en varios post. Es una relación de uno a muchos
    post_id = Column(Integer, ForeignKey('post.ID'))

    # Estas relaciones cumplen la misma función que las anteriormente mencionadas con back_populates, un acceso a los comentarios de 
    # cada autor y de cada post de una forma más fácil ya que relacionamos el contenido de comments directamente con las tablas User y Post
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

# Generar el diagrama de la base de datos
render_er(Base, 'diagram.png')

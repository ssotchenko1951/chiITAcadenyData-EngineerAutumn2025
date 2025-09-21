from typing import List, Optional, Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.domain.interfaces import (
    UserRepositoryInterface,
    PostRepositoryInterface, 
    CommentRepositoryInterface,
    PipelineRunRepositoryInterface
)
from src.domain.entities import User, Post, Comment, PipelineRun, PipelineStatus
from .models import UserModel, PostModel, CommentModel, PipelineRunModel

T = TypeVar('T')
M = TypeVar('M')


class BaseRepository(Generic[T, M]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, session: Session, model_class: Type[M], entity_class: Type[T]):
        self.session = session
        self.model_class = model_class
        self.entity_class = entity_class
    
    def add(self, entity: T) -> T:
        """Add a new entity"""
        model = self._entity_to_model(entity)
        self.session.add(model)
        self.session.flush()  # Get the ID without committing
        return self._model_to_entity(model)
    
    def get(self, id: int) -> Optional[T]:
        """Get entity by ID"""
        model = self.session.query(self.model_class).filter(
            self.model_class.id == id
        ).first()
        return self._model_to_entity(model) if model else None
    
    def get_all(self) -> List[T]:
        """Get all entities"""
        models = self.session.query(self.model_class).all()
        return [self._model_to_entity(model) for model in models]
    
    def update(self, entity: T) -> T:
        """Update an existing entity"""
        model = self.session.query(self.model_class).filter(
            self.model_class.id == entity.id
        ).first()
        if model:
            self._update_model_from_entity(model, entity)
            self.session.flush()
            return self._model_to_entity(model)
        return entity
    
    def delete(self, id: int) -> bool:
        """Delete entity by ID"""
        model = self.session.query(self.model_class).filter(
            self.model_class.id == id
        ).first()
        if model:
            self.session.delete(model)
            return True
        return False
    
    def _entity_to_model(self, entity: T) -> M:
        """Convert entity to model - to be implemented by subclasses"""
        raise NotImplementedError
    
    def _model_to_entity(self, model: M) -> T:
        """Convert model to entity - to be implemented by subclasses"""
        raise NotImplementedError
    
    def _update_model_from_entity(self, model: M, entity: T):
        """Update model from entity - to be implemented by subclasses"""
        raise NotImplementedError


class UserRepository(BaseRepository[User, UserModel], UserRepositoryInterface):
    """Repository for User entities"""
    
    def __init__(self, session: Session):
        super().__init__(session, UserModel, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        model = self.session.query(UserModel).filter(
            UserModel.email == email
        ).first()
        return self._model_to_entity(model) if model else None
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        model = self.session.query(UserModel).filter(
            UserModel.username == username
        ).first()
        return self._model_to_entity(model) if model else None
    
    def _entity_to_model(self, entity: User) -> UserModel:
        """Convert User entity to UserModel"""
        return UserModel(
            id=entity.id,
            name=entity.name,
            username=entity.username,
            email=entity.email,
            phone=entity.phone,
            website=entity.website,
            address=entity.address,
            company=entity.company,
            created_at=entity.created_at
        )
    
    def _model_to_entity(self, model: UserModel) -> User:
        """Convert UserModel to User entity"""
        return User(
            id=model.id,
            name=model.name,
            username=model.username,
            email=model.email,
            phone=model.phone,
            website=model.website,
            address=model.address,
            company=model.company,
            created_at=model.created_at
        )
    
    def _update_model_from_entity(self, model: UserModel, entity: User):
        """Update UserModel from User entity"""
        model.name = entity.name
        model.username = entity.username
        model.email = entity.email
        model.phone = entity.phone
        model.website = entity.website
        model.address = entity.address
        model.company = entity.company


class PostRepository(BaseRepository[Post, PostModel], PostRepositoryInterface):
    """Repository for Post entities"""
    
    def __init__(self, session: Session):
        super().__init__(session, PostModel, Post)
    
    def get_by_user_id(self, user_id: int) -> List[Post]:
        """Get posts by user ID"""
        models = self.session.query(PostModel).filter(
            PostModel.user_id == user_id
        ).all()
        return [self._model_to_entity(model) for model in models]
    
    def _entity_to_model(self, entity: Post) -> PostModel:
        """Convert Post entity to PostModel"""
        return PostModel(
            id=entity.id,
            user_id=entity.user_id,
            title=entity.title,
            body=entity.body,
            created_at=entity.created_at
        )
    
    def _model_to_entity(self, model: PostModel) -> Post:
        """Convert PostModel to Post entity"""
        return Post(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            body=model.body,
            created_at=model.created_at
        )
    
    def _update_model_from_entity(self, model: PostModel, entity: Post):
        """Update PostModel from Post entity"""
        model.user_id = entity.user_id
        model.title = entity.title
        model.body = entity.body


class CommentRepository(BaseRepository[Comment, CommentModel], CommentRepositoryInterface):
    """Repository for Comment entities"""
    
    def __init__(self, session: Session):
        super().__init__(session, CommentModel, Comment)
    
    def get_by_post_id(self, post_id: int) -> List[Comment]:
        """Get comments by post ID"""
        models = self.session.query(CommentModel).filter(
            CommentModel.post_id == post_id
        ).all()
        return [self._model_to_entity(model) for model in models]
    
    def _entity_to_model(self, entity: Comment) -> CommentModel:
        """Convert Comment entity to CommentModel"""
        return CommentModel(
            id=entity.id,
            post_id=entity.post_id,
            name=entity.name,
            email=entity.email,
            body=entity.body,
            created_at=entity.created_at
        )
    
    def _model_to_entity(self, model: CommentModel) -> Comment:
        """Convert CommentModel to Comment entity"""
        return Comment(
            id=model.id,
            post_id=model.post_id,
            name=model.name,
            email=model.email,
            body=model.body,
            created_at=model.created_at
        )
    
    def _update_model_from_entity(self, model: CommentModel, entity: Comment):
        """Update CommentModel from Comment entity"""
        model.post_id = entity.post_id
        model.name = entity.name
        model.email = entity.email
        model.body = entity.body


class PipelineRunRepository(BaseRepository[PipelineRun, PipelineRunModel], PipelineRunRepositoryInterface):
    """Repository for PipelineRun entities"""
    
    def __init__(self, session: Session):
        super().__init__(session, PipelineRunModel, PipelineRun)
    
    def get_recent(self, limit: int = 10) -> List[PipelineRun]:
        """Get recent pipeline runs"""
        models = self.session.query(PipelineRunModel).order_by(
            desc(PipelineRunModel.started_at)
        ).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    def _entity_to_model(self, entity: PipelineRun) -> PipelineRunModel:
        """Convert PipelineRun entity to PipelineRunModel"""
        return PipelineRunModel(
            id=entity.id,
            status=entity.status.value if isinstance(entity.status, PipelineStatus) else entity.status,
            started_at=entity.started_at,
            completed_at=entity.completed_at,
            error_message=entity.error_message,
            records_processed=entity.records_processed,
            metadata=entity.metadata
        )
    
    def _model_to_entity(self, model: PipelineRunModel) -> PipelineRun:
        """Convert PipelineRunModel to PipelineRun entity"""
        return PipelineRun(
            id=model.id,
            status=PipelineStatus(model.status) if model.status else PipelineStatus.PENDING,
            started_at=model.started_at,
            completed_at=model.completed_at,
            error_message=model.error_message,
            records_processed=model.records_processed,
            metadata=model.metadata
        )
    
    def _update_model_from_entity(self, model: PipelineRunModel, entity: PipelineRun):
        """Update PipelineRunModel from PipelineRun entity"""
        model.status = entity.status.value if isinstance(entity.status, PipelineStatus) else entity.status
        model.completed_at = entity.completed_at
        model.error_message = entity.error_message
        model.records_processed = entity.records_processed
        model.metadata = entity.metadata
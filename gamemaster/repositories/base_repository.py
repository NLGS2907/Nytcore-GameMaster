from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional, TypeAlias, Union

if TYPE_CHECKING:
    from peewee import Expression, Field

    from ..db.base import BaseModel

InsertDict: TypeAlias = dict[str, Any]
PreserveList: TypeAlias = list["Field"]
UpdateDict: TypeAlias = dict[Union[str, "Field"], Any]
DatasetType: TypeAlias = "BaseModel"
DatasetClassType: TypeAlias = type[DatasetType]


class BaseRepository[ModelType](ABC):
    """Base abstract repository to use as template for others."""

    @staticmethod
    @abstractmethod
    def dataset_cls() -> DatasetClassType:
        """Returns the linked dataset of this repository."""

        raise NotImplementedError


    def _create_dataset(self,
                        insert_args: InsertDict,
                        preserve_args: Optional[PreserveList]=None,
                        update_args: Optional[UpdateDict]=None,
                        get_args: Optional[InsertDict]=None) -> DatasetType:
        """Creates the dataset for this repository, or updates the existing one if needed.
        
        Args:
            insert_args: The data to attempt to insert.
            preserve_args: A list of dataset fields to update FROM THE NEW INCOMING DATA,
                           in case of conflict.
            update_args: A dictionary of values to update into the new row, in case of conflict.
            get_args: When a conflict was resolved and getting an updated row, use these filters
                      to retrieve it. If not defined, defaults to `insert_args`.

        Returns:
            The dataset of the relevant data.
        """

        with self.dataset_cls()._meta.database.atomic("IMMEDIATE"):
            self.dataset_cls().insert(**insert_args).on_conflict(
                action=("NOTHING" if (not preserve_args and not update_args) else None),
                conflict_target=self.dataset_cls().unique_columns(),
                preserve=preserve_args,
                update=update_args
            ).execute()

            get_options = get_args or insert_args
            return self.dataset_cls().get(**get_options)


    @abstractmethod
    def _model_to_dataset(self, model: ModelType) -> DatasetType:
        """Transforms the model to its dataset variant."""

        raise NotImplementedError


    @abstractmethod
    def _dataset_to_model(self, dataset: DatasetType) -> ModelType:
        """Transform the dataset into the functional model."""

        raise NotImplementedError


    def _exists(self, *filters: "Expression") -> bool:
        """Makes a query and checks if it returned something.
        
        Args:
            *filters: The collection of expressions to filter the result.

        Returns:
            A boolean value checking if the result exists or not.
        """

        return self.dataset_cls().select().where(*filters).exists()


    def save(self, model: ModelType):
        """Persist the model through the database.
        
        Args:
            model: The functional object.
        """

        ds = self._model_to_dataset(model)
        ds.save()


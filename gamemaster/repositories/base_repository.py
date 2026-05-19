from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, TypeAlias, Union

if TYPE_CHECKING:
    from peewee import Field

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
    def dataset() -> DatasetClassType:
        """Returns the linked dataset of this repository."""

        raise NotImplementedError


    def _create_dataset(self,
                        insert_args: InsertDict,
                        preserve_args: PreserveList,
                        update_args: UpdateDict) -> DatasetType:
        """Creates the dataset for this repository, or updates the existing one if needed.
        
        Args:
            insert_args: The data to attempt to insert.
            preserve_args: A list of dataset fields to update FROM THE NEW INCOMING DATA,
                           in case of conflict.
            update_args: A dictionary of values to update into the new row, in case of conflict.
        """

        rowid = (
            self.dataset().insert(**insert_args).on_conflict(
                conflict_target=self.dataset().unique_columns(),
                preserve=preserve_args,
                update=update_args
            ).execute()
        )

        return self.dataset().get_by_id(rowid)


    @abstractmethod
    def _model_to_dataset(self, model: ModelType) -> DatasetType:
        """Transforms the model to its dataset variant."""

        raise NotImplementedError


    @abstractmethod
    def _dataset_to_model(self, dataset: DatasetType) -> ModelType:
        """Transform the dataset into the functional model."""

        raise NotImplementedError


    def save(self, model: ModelType):
        """Persist the model through the database.
        
        Args:
            model: The functional object.
        """

        self._model_to_dataset(model).save()


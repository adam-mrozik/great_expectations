import json
import logging
from typing import Any, List, Optional

import great_expectations.exceptions as ge_exceptions
from great_expectations.core.batch import BatchDefinition
from great_expectations.datasource.data_connector.sorter import Sorter

logger = logging.getLogger(__name__)


class DictionarySorter(Sorter):
    def __init__(
        self,
        name: str,
        orderby: str = "asc",
        order_keys_by: str = "asc",
        key_reference_list: Optional[List[Any]] = None,
    ) -> None:
        super().__init__(name=name, orderby=orderby)
        if order_keys_by is None or order_keys_by == "asc":
            reverse_keys = False
        elif order_keys_by == "desc":
            reverse_keys = True
        else:
            raise ge_exceptions.SorterError(
                f'Illegal key sort order "{order_keys_by}" for attribute "{name}".'
            )
        self._reverse_keys = reverse_keys
        self._key_reference_list = key_reference_list

    def get_batch_key(self, batch_definition: BatchDefinition) -> Any:
        batch_identifiers: dict = batch_definition.batch_identifiers
        batch_keys: Optional[List[Any]]
        if self._key_reference_list is None:
            batch_keys = sorted(
                batch_identifiers[self.name].keys(), reverse=self.reverse_keys
            )
        else:
            batch_keys = [
                key
                for key in self.key_reference_list
                if key in batch_identifiers[self.name].keys()
            ]
        batch_values: List[Any] = [
            batch_identifiers[self.name][key] for key in batch_keys
        ]
        return batch_values

    def __repr__(self) -> str:
        doc_fields_dict = {
            "name": self.name,
            "reverse": self.reverse,
            "reverse_keys": self.reverse_keys,
            "key_reference_list": self.key_reference_list,
            "type": "DictionarySorter",
        }
        return json.dumps(doc_fields_dict, indent=2)

    @property
    def reverse_keys(self) -> bool:
        return self._reverse_keys

    @property
    def key_reference_list(self) -> List[Any]:
        return self._key_reference_list

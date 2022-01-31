import os
from torchtext.data.datasets_utils import (
    _wrap_split_argument,
    _find_match,
    _create_data_from_iob,
)


@_wrap_split_argument(('train', 'valid', 'test'))
def UDPOS(root, split):
    if split == 'valid':
        split = 'dev'

    path = os.path.join(
        root,
        _find_match(f'{split}.conll', os.listdir(root))
    )
    data = list(_create_data_from_iob(path))
    return data

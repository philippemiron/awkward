# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test():
    array = ak._v2.highlevel.Array(
        ak._v2.contents.RegularArray(
            ak._v2.contents.NumpyArray(np.r_[1, 2, 3, 4, 5, 6, 7, 8, 9]), 3
        )
    )
    condition = ak._v2.highlevel.Array(
        ak._v2.contents.NumpyArray(
            np.array([[True, True, True], [True, True, False], [True, False, True]])
        )
    )

    assert ak._v2.operations.where(condition == 2, array, 2 * array).tolist() == [
        [2, 4, 6],
        [8, 10, 12],
        [14, 16, 18],
    ]

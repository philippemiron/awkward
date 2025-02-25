# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

to_list = ak._v2.operations.to_list


def test_toregular():
    array = ak._v2.Array(
        [
            {
                "x": np.arange(2 * 3 * 5).reshape(2, 3, 5).tolist(),
                "y": np.arange(2 * 3 * 5 * 7).reshape(2, 3, 5, 7),
            }
        ]
    )

    assert str(array.type) in (
        "1 * {x: var * var * var * int64, y: var * var * var * var * int64}",
        "1 * {y: var * var * var * var * int64, x: var * var * var * int64}",
    )
    assert str(ak._v2.operations.to_regular(array, axis=-1).type) in (
        "1 * {x: var * var * 5 * int64, y: var * var * var * 7 * int64}",
        "1 * {y: var * var * var * 7 * int64, x: var * var * 5 * int64}",
    )
    assert str(ak._v2.operations.to_regular(array, axis=-2).type) in (
        "1 * {x: var * 3 * var * int64, y: var * var * 5 * var * int64}",
        "1 * {y: var * var * 5 * var * int64, x: var * 3 * var * int64}",
    )
    assert str(ak._v2.operations.to_regular(array, axis=-3).type) in (
        "1 * {x: 2 * var * var * int64, y: var * 3 * var * var * int64}",
        "1 * {y: var * 3 * var * var * int64, x: 2 * var * var * int64}",
    )


def test_cartesian():
    one = ak._v2.Array(np.arange(2 * 3 * 5 * 7).reshape(2, 3, 5, 7).tolist())
    two = ak._v2.Array(np.arange(2 * 3 * 5 * 7).reshape(2, 3, 5, 7).tolist())

    assert (
        str(ak._v2.operations.cartesian([one, two], axis=0, nested=True).type)
        == "2 * 2 * (var * var * var * int64, var * var * var * int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=1, nested=True).type)
        == "2 * var * var * (var * var * int64, var * var * int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=2, nested=True).type)
        == "2 * var * var * var * (var * int64, var * int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=3, nested=True).type)
        == "2 * var * var * var * var * (int64, int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=-1, nested=True).type)
        == "2 * var * var * var * var * (int64, int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=-2, nested=True).type)
        == "2 * var * var * var * (var * int64, var * int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=-3, nested=True).type)
        == "2 * var * var * (var * var * int64, var * var * int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=-4, nested=True).type)
        == "2 * 2 * (var * var * var * int64, var * var * var * int64)"
    )

    with pytest.raises(ValueError):
        ak._v2.operations.cartesian([one, two], axis=-5, nested=True)

    assert (
        str(ak._v2.operations.cartesian([one, two], axis=0).type)
        == "4 * (var * var * var * int64, var * var * var * int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=1).type)
        == "2 * var * (var * var * int64, var * var * int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=2).type)
        == "2 * var * var * (var * int64, var * int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=3).type)
        == "2 * var * var * var * (int64, int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=-1).type)
        == "2 * var * var * var * (int64, int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=-2).type)
        == "2 * var * var * (var * int64, var * int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=-3).type)
        == "2 * var * (var * var * int64, var * var * int64)"
    )
    assert (
        str(ak._v2.operations.cartesian([one, two], axis=-4).type)
        == "4 * (var * var * var * int64, var * var * var * int64)"
    )

    with pytest.raises(ValueError):
        ak._v2.operations.cartesian([one, two], axis=-5)


def test_firsts():
    array = ak._v2.Array([[[0, 1, 2], []], [[3, 4]], [], [[5], [6, 7, 8, 9]]])

    assert to_list(ak._v2.operations.firsts(array, axis=0)) == [[0, 1, 2], []]
    assert to_list(ak._v2.operations.firsts(array, axis=1)) == [
        [0, 1, 2],
        [3, 4],
        None,
        [5],
    ]
    assert to_list(ak._v2.operations.firsts(array, axis=2)) == [
        [0, None],
        [3],
        [],
        [5, 6],
    ]
    assert to_list(ak._v2.operations.firsts(array, axis=-1)) == [
        [0, None],
        [3],
        [],
        [5, 6],
    ]
    assert to_list(ak._v2.operations.firsts(array, axis=-2)) == [
        [0, 1, 2],
        [3, 4],
        None,
        [5],
    ]
    assert to_list(ak._v2.operations.firsts(array, axis=-3)) == [
        [0, 1, 2],
        [],
    ]

    with pytest.raises(ValueError):
        ak._v2.operations.firsts(array, axis=-4)

# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

# import os

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

pyarrow = pytest.importorskip("pyarrow")

to_list = ak._v2.operations.to_list


def test_list_to_arrow():
    ak_array = ak._v2.highlevel.Array([[1.1, 2.2, 3.3], [], [4.4, 5.5]]).layout
    pa_array = ak_array.to_arrow()
    assert isinstance(pa_array.type.storage_type, pyarrow.LargeListType)
    assert pa_array.to_pylist() == [[1.1, 2.2, 3.3], [], [4.4, 5.5]]

    ak_array = ak._v2.contents.ListOffsetArray(
        ak_array.offsets, ak._v2.contents.UnmaskedArray(ak_array.content)
    )
    pa_array = ak_array.to_arrow()
    assert isinstance(pa_array.type.storage_type, pyarrow.LargeListType)
    assert pa_array.to_pylist() == [[1.1, 2.2, 3.3], [], [4.4, 5.5]]

    ak_array = ak._v2.highlevel.Array([[1.1, 2.2, None], [], [4.4, 5.5]]).layout
    pa_array = ak_array.to_arrow()
    assert isinstance(pa_array.type.storage_type, pyarrow.LargeListType)
    assert pa_array.to_pylist() == [[1.1, 2.2, None], [], [4.4, 5.5]]


def test_record_to_arrow():
    x_content = ak._v2.highlevel.Array([1.1, 2.2, 3.3, 4.4, 5.5]).layout
    z_content = ak._v2.highlevel.Array([1, 2, 3, None, 5]).layout

    ak_array = ak._v2.contents.RecordArray(
        [
            x_content,
            ak._v2.contents.UnmaskedArray(x_content),
            z_content,
        ],
        ["x", "y", "z"],
    )
    pa_array = ak_array.to_arrow()
    assert isinstance(pa_array.type.storage_type, pyarrow.StructType)
    assert pa_array.to_pylist() == [
        {"x": 1.1, "y": 1.1, "z": 1},
        {"x": 2.2, "y": 2.2, "z": 2},
        {"x": 3.3, "y": 3.3, "z": 3},
        {"x": 4.4, "y": 4.4, "z": None},
        {"x": 5.5, "y": 5.5, "z": 5},
    ]


def test_union_to_arrow():
    ak_array = ak._v2.highlevel.Array([1.1, 2.2, None, [1, 2, 3], "hello"]).layout
    pa_array = ak_array.to_arrow()
    assert isinstance(pa_array.type.storage_type, pyarrow.DenseUnionType)
    assert pa_array.to_pylist() == [1.1, 2.2, None, [1, 2, 3], "hello"]

    ak_array = ak._v2.contents.UnmaskedArray(
        ak._v2.highlevel.Array([1.1, 2.2, [1, 2, 3], "hello"]).layout
    )
    pa_array = ak_array.to_arrow()
    assert isinstance(pa_array.type.storage_type, pyarrow.DenseUnionType)
    assert pa_array.to_pylist() == [1.1, 2.2, [1, 2, 3], "hello"]

    ak_array = ak._v2.highlevel.Array([1.1, 2.2, [1, 2, 3], "hello"]).layout
    pa_array = ak_array.to_arrow()
    assert isinstance(pa_array.type.storage_type, pyarrow.DenseUnionType)
    assert pa_array.to_pylist() == [1.1, 2.2, [1, 2, 3], "hello"]


def test_list_from_arrow():
    original = ak._v2.highlevel.Array([[1.1, 2.2, 3.3], [], [4.4, 5.5]]).layout
    pa_array = original.to_arrow()
    reconstituted = ak._v2.from_arrow(pa_array, highlevel=False)
    assert str(reconstituted.form.type) == "var * float64"
    assert to_list(reconstituted) == [[1.1, 2.2, 3.3], [], [4.4, 5.5]]

    original = ak._v2.highlevel.Array([[1.1, 2.2, None], [], [4.4, 5.5]]).layout
    pa_array = original.to_arrow()
    reconstituted = ak._v2.from_arrow(pa_array, highlevel=False)
    assert str(reconstituted.form.type) == "var * ?float64"
    assert to_list(reconstituted) == [[1.1, 2.2, None], [], [4.4, 5.5]]

    original = ak._v2.highlevel.Array([[1.1, 2.2, 3.3], [], None, [4.4, 5.5]]).layout
    pa_array = original.to_arrow()
    reconstituted = ak._v2.from_arrow(pa_array, highlevel=False)
    assert str(reconstituted.form.type) == "option[var * float64]"
    assert to_list(reconstituted) == [[1.1, 2.2, 3.3], [], None, [4.4, 5.5]]

    original = ak._v2.highlevel.Array([[1.1, 2.2, None], [], None, [4.4, 5.5]]).layout
    pa_array = original.to_arrow()
    reconstituted = ak._v2.from_arrow(pa_array, highlevel=False)
    assert str(reconstituted.form.type) == "option[var * ?float64]"
    assert to_list(reconstituted) == [[1.1, 2.2, None], [], None, [4.4, 5.5]]


def test_record_from_arrow():
    x_content = ak._v2.highlevel.Array([1.1, 2.2, 3.3, 4.4, 5.5]).layout
    z_content = ak._v2.highlevel.Array([1, 2, 3, None, 5]).layout

    original = ak._v2.contents.RecordArray(
        [
            x_content,
            ak._v2.contents.UnmaskedArray(x_content),
            z_content,
        ],
        ["x", "y", "z"],
    )
    pa_array = original.to_arrow()
    reconstituted = ak._v2.from_arrow(pa_array, highlevel=False)
    assert str(reconstituted.form.type) == "{x: float64, y: ?float64, z: ?int64}"
    assert to_list(reconstituted) == [
        {"x": 1.1, "y": 1.1, "z": 1},
        {"x": 2.2, "y": 2.2, "z": 2},
        {"x": 3.3, "y": 3.3, "z": 3},
        {"x": 4.4, "y": 4.4, "z": None},
        {"x": 5.5, "y": 5.5, "z": 5},
    ]

    original = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(np.array([False, True, False, False, False], np.int8)),
        original,
        valid_when=False,
    )
    pa_array = original.to_arrow()
    reconstituted = ak._v2.from_arrow(pa_array, highlevel=False)
    assert str(reconstituted.form.type) == "?{x: float64, y: ?float64, z: ?int64}"
    assert to_list(reconstituted) == [
        {"x": 1.1, "y": 1.1, "z": 1},
        None,
        {"x": 3.3, "y": 3.3, "z": 3},
        {"x": 4.4, "y": 4.4, "z": None},
        {"x": 5.5, "y": 5.5, "z": 5},
    ]


def test_union_from_arrow():
    original = ak._v2.highlevel.Array([1.1, 2.2, [1, 2, 3], "hello"]).layout
    pa_array = original.to_arrow()
    reconstituted = ak._v2.from_arrow(pa_array, highlevel=False)
    assert str(reconstituted.form.type) == "union[float64, var * int64, string]"
    assert to_list(reconstituted) == [1.1, 2.2, [1, 2, 3], "hello"]

    original = ak._v2.highlevel.Array([1.1, 2.2, None, [1, 2, 3], "hello"]).layout
    pa_array = original.to_arrow()
    reconstituted = ak._v2.from_arrow(pa_array, highlevel=False)
    assert (
        str(reconstituted.form.type) == "union[?float64, option[var * int64], ?string]"
    )
    assert to_list(reconstituted) == [1.1, 2.2, None, [1, 2, 3], "hello"]

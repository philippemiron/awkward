# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import os.path
import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

pyarrow_parquet = pytest.importorskip("pyarrow.parquet")


def through_arrow(
    akarray,
    extensionarray,
    tmp_path,
    list_to32=False,
    string_to32=False,
    bytestring_to32=False,
    categorical_as_dictionary=False,
):
    arrow_table = ak._v2.to_arrow_table(
        akarray,
        extensionarray=extensionarray,
        list_to32=list_to32,
        string_to32=string_to32,
        bytestring_to32=bytestring_to32,
        categorical_as_dictionary=categorical_as_dictionary,
    )
    array_form = ak._v2.from_arrow(arrow_table, generate_bitmasks=True).layout.form
    return arrow_table.schema, array_form


def through_parquet(
    akarray,
    extensionarray,
    tmp_path,
    list_to32=False,
    string_to32=False,
    bytestring_to32=False,
    categorical_as_dictionary=False,
):
    filename = os.path.join(tmp_path, "whatever.parquet")
    pyarrow_parquet.write_table(
        ak._v2.to_arrow_table(
            akarray,
            extensionarray=extensionarray,
            list_to32=list_to32,
            string_to32=string_to32,
            bytestring_to32=bytestring_to32,
            categorical_as_dictionary=categorical_as_dictionary,
        ),
        filename,
    )
    parquet_file = pyarrow_parquet.ParquetFile(filename)
    array_form = ak._v2.from_arrow(
        parquet_file.read_row_groups([0]), generate_bitmasks=True
    ).layout.form
    return parquet_file.schema_arrow, array_form


@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_schema_numpyarray(tmp_path, through, extensionarray):
    akarray = ak._v2.contents.NumpyArray(
        np.array([1.1, 2.2, 3.3]), parameters={"which": "inner"}
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.parametrize("dtype", [np.int32, np.uint32, np.int64])
@pytest.mark.parametrize("list_to32", [False, True])
@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_schema_listoffsetarray_numpyarray(
    tmp_path, dtype, list_to32, through, extensionarray
):
    akarray = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index(np.array([0, 3, 3, 5, 6, 10], dtype=dtype)),
        ak._v2.contents.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]),
            parameters={"which": "inner"},
        ),
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(
        akarray, extensionarray, tmp_path, list_to32=list_to32
    )
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index(np.array([0, 3, 3, 5, 6, 10], dtype=dtype)),
        ak._v2.contents.ByteMaskedArray(
            ak._v2.index.Index8(
                np.array(
                    [False, True, False, True, True, False, True, True, False, False],
                    dtype=np.int8,
                )
            ),
            ak._v2.contents.NumpyArray(
                np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]),
                parameters={"which": "inner"},
            ),
            valid_when=False,
            parameters={"which": "middle"},
        ),
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(
        akarray, extensionarray, tmp_path, list_to32=list_to32
    )
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(np.array([True, False, True, True, True], dtype=np.int8)),
        ak._v2.contents.ListOffsetArray(
            ak._v2.index.Index(np.array([0, 3, 3, 5, 6, 10], dtype=dtype)),
            ak._v2.contents.NumpyArray(
                np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]),
                parameters={"which": "inner"},
            ),
            parameters={"which": "middle"},
        ),
        valid_when=True,
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(
        akarray, extensionarray, tmp_path, list_to32=list_to32
    )
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(np.array([True, False, True, True, True], dtype=np.int8)),
        ak._v2.contents.ListOffsetArray(
            ak._v2.index.Index(np.array([0, 3, 3, 5, 6, 10], dtype=dtype)),
            ak._v2.contents.ByteMaskedArray(
                ak._v2.index.Index8(
                    np.array(
                        [
                            False,
                            True,
                            False,
                            True,
                            True,
                            False,
                            True,
                            True,
                            False,
                            False,
                        ],
                        dtype=np.int8,
                    )
                ),
                ak._v2.contents.NumpyArray(
                    np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]),
                    parameters={"which": "inner"},
                ),
                valid_when=False,
                parameters={"which": "middle-1"},
            ),
            parameters={"which": "middle-2"},
        ),
        valid_when=True,
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(
        akarray, extensionarray, tmp_path, list_to32=list_to32
    )
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.parametrize("dtype", [np.int32, np.uint32, np.int64])
@pytest.mark.parametrize("list_to32", [False, True])
@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_schema_listoffsetarray_numpyarray_2(
    tmp_path, dtype, list_to32, through, extensionarray
):
    akarray = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(np.array([True, False, True, False, True], dtype=np.int8)),
        ak._v2.contents.ListOffsetArray(
            ak._v2.index.Index(np.array([0, 3, 3, 5, 6, 10], dtype=dtype)),
            ak._v2.contents.NumpyArray(
                np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]),
                parameters={"which": "inner"},
            ),
            parameters={"which": "middle"},
        ),
        valid_when=True,
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(
        akarray, extensionarray, tmp_path, list_to32=list_to32
    )
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_numpyarray_bool(tmp_path, through, extensionarray):
    akarray = ak._v2.contents.NumpyArray(
        np.random.randint(0, 2, 14).astype(np.int8).view(np.bool_),
        parameters={"which": "inner"},
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(np.random.randint(0, 2, 14).astype(np.int8).view(np.bool_)),
        ak._v2.contents.NumpyArray(
            np.random.randint(0, 2, 14).astype(np.int8).view(np.bool_),
            parameters={"which": "inner"},
        ),
        valid_when=False,
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_indexedoptionarray_numpyarray(tmp_path, through, extensionarray):
    akarray = ak._v2.contents.IndexedOptionArray(
        ak._v2.index.Index64(np.array([2, 0, 0, -1, 3, 1, 5, -1, 2], dtype=np.int64)),
        ak._v2.contents.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5]),
            parameters={"which": "inner"},
        ),
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.IndexedArray(
        ak._v2.index.Index64(np.array([2, 0, 0, 3, 1, 5, 2], dtype=np.int64)),
        ak._v2.contents.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5]),
            parameters={"which": "inner"},
        ),
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_indexedoptionarray_emptyarray(tmp_path, through, extensionarray):
    akarray = ak._v2.contents.IndexedOptionArray(
        ak._v2.index.Index64(np.array([-1, -1, -1, -1, -1], dtype=np.int64)),
        ak._v2.contents.EmptyArray(parameters={"which": "inner"}),
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.parametrize("categorical_as_dictionary", [False, True])
@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_dictionary_encoding(
    tmp_path, categorical_as_dictionary, through, extensionarray
):
    akarray = ak._v2.contents.IndexedArray(
        ak._v2.index.Index64(np.array([3, 2, 2, 2, 0, 1, 3], dtype=np.uint64)),
        ak._v2.contents.NumpyArray([0.0, 1.1, 2.2, 3.3], parameters={"which": "inner"}),
        parameters={"__array__": "categorical", "which": "outer"},
    )

    # https://issues.apache.org/jira/browse/ARROW-14525
    if not (
        extensionarray and categorical_as_dictionary and through is through_parquet
    ):
        schema_arrow, array_form = through(
            akarray,
            extensionarray,
            tmp_path,
            categorical_as_dictionary=categorical_as_dictionary,
        )
        predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
            schema_arrow, pass_empty_field=True
        )
        assert predicted_form == array_form


@pytest.mark.parametrize("string_to32", [False, True])
@pytest.mark.parametrize("dtype", [np.int32, np.uint32, np.int64])
@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_listoffsetraray_string(tmp_path, string_to32, dtype, through, extensionarray):
    akarray = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(np.array([0, 3, 3, 5, 6, 10], dtype=dtype)),
        ak._v2.contents.NumpyArray(
            np.arange(97, 107, dtype=np.uint8), parameters={"__array__": "char"}
        ),
        parameters={"__array__": "string", "something": "else"},
    )

    schema_arrow, array_form = through(
        akarray, extensionarray, tmp_path, string_to32=string_to32
    )
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.parametrize("bytestring_to32", [False, True])
@pytest.mark.parametrize("dtype", [np.int32, np.uint32, np.int64])
@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_listoffsetraray_bytestring(
    tmp_path, bytestring_to32, dtype, through, extensionarray
):
    akarray = ak._v2.contents.ListOffsetArray(
        ak._v2.index.Index64(np.array([0, 3, 3, 5, 6, 10], dtype=dtype)),
        ak._v2.contents.NumpyArray(
            np.arange(97, 107, dtype=np.uint8), parameters={"__array__": "byte"}
        ),
        parameters={"__array__": "bytestring", "something": "else"},
    )

    schema_arrow, array_form = through(
        akarray, extensionarray, tmp_path, bytestring_to32=bytestring_to32
    )
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.parametrize("size", [5])
@pytest.mark.parametrize("list_to32", [False, True])
@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_regulararray_numpyarray(tmp_path, size, list_to32, through, extensionarray):
    akarray = ak._v2.contents.RegularArray(
        ak._v2.contents.NumpyArray(
            np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]),
            parameters={"which": "inner"},
        ),
        size,
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(
        akarray, extensionarray, tmp_path, list_to32=list_to32
    )
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.RegularArray(
        ak._v2.contents.ByteMaskedArray(
            ak._v2.index.Index8(
                np.array(
                    [False, True, False, True, True, False, True, True, False, False],
                    dtype=np.int8,
                )
            ),
            ak._v2.contents.NumpyArray(
                np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]),
                parameters={"which": "inner"},
            ),
            valid_when=False,
            parameters={"which": "middle"},
        ),
        size,
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(
        akarray, extensionarray, tmp_path, list_to32=list_to32
    )
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(np.array([True, False], dtype=np.int8)),
        ak._v2.contents.RegularArray(
            ak._v2.contents.NumpyArray(
                np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]),
                parameters={"which": "inner"},
            ),
            size,
            parameters={"which": "middle"},
        ),
        valid_when=True,
        parameters={"which": "outer"},
    )

    # https://issues.apache.org/jira/browse/ARROW-14547
    if through is through_arrow:
        schema_arrow, array_form = through(
            akarray, extensionarray, tmp_path, list_to32=list_to32
        )
        predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
            schema_arrow, pass_empty_field=True
        )
        assert predicted_form == array_form

    akarray = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(np.array([True, False], dtype=np.int8)),
        ak._v2.contents.RegularArray(
            ak._v2.contents.ByteMaskedArray(
                ak._v2.index.Index8(
                    np.array(
                        [
                            False,
                            True,
                            False,
                            True,
                            True,
                            False,
                            True,
                            True,
                            False,
                            False,
                        ],
                        dtype=np.int8,
                    )
                ),
                ak._v2.contents.NumpyArray(
                    np.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]),
                    parameters={"which": "inner"},
                ),
                valid_when=False,
                parameters={"which": "middle-1"},
            ),
            size,
            parameters={"which": "middle-2"},
        ),
        valid_when=True,
        parameters={"which": "outer"},
    )

    # https://issues.apache.org/jira/browse/ARROW-14547
    if through is through_arrow:
        schema_arrow, array_form = through(
            akarray, extensionarray, tmp_path, list_to32=list_to32
        )
        predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
            schema_arrow, pass_empty_field=True
        )
        assert predicted_form == array_form


@pytest.mark.parametrize("size", [5])
@pytest.mark.parametrize("bytestring_to32", [False, True])
@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_regularaarray_bytestring(
    tmp_path, size, bytestring_to32, through, extensionarray
):
    akarray = ak._v2.contents.RegularArray(
        ak._v2.contents.NumpyArray(
            np.arange(97, 107, dtype=np.uint8), parameters={"__array__": "byte"}
        ),
        size,
        parameters={"__array__": "bytestring", "something": "else"},
    )

    schema_arrow, array_form = through(
        akarray, extensionarray, tmp_path, bytestring_to32=bytestring_to32
    )
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_unmaskedarray_numpyarray(tmp_path, through, extensionarray):
    akarray = ak._v2.contents.UnmaskedArray(
        ak._v2.contents.NumpyArray(
            np.array([1.1, 2.2, 3.3]), parameters={"which": "inner"}
        )
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.parametrize("is_tuple", [False, True])
@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_recordarray(tmp_path, is_tuple, through, extensionarray):
    akarray = ak._v2.contents.RecordArray(
        [
            ak._v2.contents.NumpyArray(
                np.array([1.1, 2.2, 3.3]), parameters={"which": "inner1"}
            ),
            ak._v2.contents.ListOffsetArray(
                ak._v2.index.Index32(np.array([0, 3, 3, 5], dtype=np.int32)),
                ak._v2.contents.NumpyArray(
                    np.array([1.1, 2.2, 3.3, 4.4, 5.5]), parameters={"which": "inner2"}
                ),
            ),
        ],
        None if is_tuple else ["x", "y"],
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.RecordArray(
        [
            ak._v2.contents.ByteMaskedArray(
                ak._v2.index.Index8(np.array([False, True, False]).view(np.int8)),
                ak._v2.contents.NumpyArray(
                    np.array([1.1, 2.2, 3.3]), parameters={"which": "inner1"}
                ),
                valid_when=False,
            ),
            ak._v2.contents.ListOffsetArray(
                ak._v2.index.Index32(np.array([0, 3, 3, 5], dtype=np.int32)),
                ak._v2.contents.NumpyArray(
                    np.array([1.1, 2.2, 3.3, 4.4, 5.5]), parameters={"which": "inner2"}
                ),
            ),
        ],
        None if is_tuple else ["x", "y"],
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.RecordArray(
        [
            ak._v2.contents.ByteMaskedArray(
                ak._v2.index.Index8(np.array([False, True, False]).view(np.int8)),
                ak._v2.contents.NumpyArray(
                    np.array([1.1, 2.2, 3.3]), parameters={"which": "inner1"}
                ),
                valid_when=False,
            ),
            ak._v2.contents.UnmaskedArray(
                ak._v2.contents.ListOffsetArray(
                    ak._v2.index.Index32(np.array([0, 3, 3, 5], dtype=np.int32)),
                    ak._v2.contents.NumpyArray(
                        np.array([1.1, 2.2, 3.3, 4.4, 5.5]),
                        parameters={"which": "inner2"},
                    ),
                ),
            ),
        ],
        None if is_tuple else ["x", "y"],
        parameters={"which": "outer"},
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.IndexedOptionArray(
        ak._v2.index.Index64(np.array([2, 0, -1, 0, 1], dtype=np.int64)),
        ak._v2.contents.RecordArray(
            [
                ak._v2.contents.NumpyArray(
                    np.array([1.1, 2.2, 3.3]), parameters={"which": "inner1"}
                ),
                ak._v2.contents.ListOffsetArray(
                    ak._v2.index.Index32(np.array([0, 3, 3, 5], dtype=np.int32)),
                    ak._v2.contents.NumpyArray(
                        np.array([1.1, 2.2, 3.3, 4.4, 5.5]),
                        parameters={"which": "inner2"},
                    ),
                ),
            ],
            None if is_tuple else ["x", "y"],
            parameters={"which": "outer"},
        ),
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form

    akarray = ak._v2.contents.IndexedOptionArray(
        ak._v2.index.Index64(np.array([2, 0, -1, 0, 1], dtype=np.int64)),
        ak._v2.contents.RecordArray(
            [
                ak._v2.contents.ByteMaskedArray(
                    ak._v2.index.Index8(np.array([False, True, False]).view(np.int8)),
                    ak._v2.contents.NumpyArray(
                        np.array([1.1, 2.2, 3.3]), parameters={"which": "inner1"}
                    ),
                    valid_when=False,
                ),
                ak._v2.contents.ListOffsetArray(
                    ak._v2.index.Index32(np.array([0, 3, 3, 5], dtype=np.int32)),
                    ak._v2.contents.NumpyArray(
                        np.array([1.1, 2.2, 3.3, 4.4, 5.5]),
                        parameters={"which": "inner2"},
                    ),
                ),
            ],
            None if is_tuple else ["x", "y"],
            parameters={"which": "outer"},
        ),
    )

    schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
    predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
        schema_arrow, pass_empty_field=True
    )
    assert predicted_form == array_form


@pytest.mark.skipif(
    not ak._v2._util.numpy_at_least("1.20"), reason="NumPy >= 1.20 required for dates"
)
@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_numpyarray_datetime(tmp_path, through, extensionarray):
    # pyarrow doesn't yet support datetime/duration conversions to Parquet.
    # (FIXME: find or create a JIRA ticket.)

    akarray = ak._v2.contents.NumpyArray(
        np.array(
            ["2020-07-27T10:41:11", "2019-01-01", "2020-01-01"], dtype="datetime64[s]"
        )
    )

    if through is through_arrow:
        schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
        predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
            schema_arrow, pass_empty_field=True
        )
        assert predicted_form == array_form

    akarray = ak._v2.contents.NumpyArray(
        np.array(["41", "1", "20"], dtype="timedelta64[s]")
    )

    if through is through_arrow:
        schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
        predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
            schema_arrow, pass_empty_field=True
        )
        assert predicted_form == array_form


@pytest.mark.parametrize("through", [through_arrow, through_parquet])
@pytest.mark.parametrize("extensionarray", [False, True])
def test_unionarray(tmp_path, through, extensionarray):
    # pyarrow doesn't yet support union array conversions to Parquet.
    # (FIXME: find or create a JIRA ticket.)

    akarray = ak._v2.contents.UnionArray(
        ak._v2.index.Index8(np.array([0, 0, 1, 1, 1, 0, 1], dtype=np.int8)),
        ak._v2.index.Index64(np.array([0, 1, 3, 2, 1, 2, 0], dtype=np.int64)),
        [
            ak._v2.contents.NumpyArray(
                np.array([0.0, 1.1, 2.2]),
                parameters={"which": "inner1"},
            ),
            ak._v2.contents.NumpyArray(
                np.array([0, 10, 20, 30], dtype=np.int32),
                parameters={"which": "inner2"},
            ),
        ],
        parameters={"which": "outer"},
    )

    if through is through_arrow:
        schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
        predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
            schema_arrow, pass_empty_field=True
        )
        assert predicted_form == array_form

    akarray = ak._v2.contents.UnionArray(
        ak._v2.index.Index8(np.array([0, 0, 1, 1, 1, 0, 1], dtype=np.int8)),
        ak._v2.index.Index64(np.array([0, 1, 3, 2, 1, 2, 0], dtype=np.int64)),
        [
            ak._v2.contents.NumpyArray(
                np.array([0.0, 1.1, 2.2]),
                parameters={"which": "inner1"},
            ),
            ak._v2.contents.ByteMaskedArray(
                ak._v2.index.Index8(
                    np.array([False, False, True, False]).view(np.int8)
                ),
                ak._v2.contents.NumpyArray(
                    np.array([0, 10, 20, 30], dtype=np.int32),
                    parameters={"which": "inner2"},
                ),
                valid_when=False,
                parameters={"which": "middle"},
            ),
        ],
        parameters={"which": "outer"},
    )

    if through is through_arrow:
        schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
        predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
            schema_arrow, pass_empty_field=True
        )
        assert predicted_form == array_form

    akarray = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(
            np.array([False, True, False, True, False, True, True]).view(np.int8)
        ),
        ak._v2.contents.UnionArray(
            ak._v2.index.Index8(np.array([0, 0, 1, 1, 1, 0, 1], dtype=np.int8)),
            ak._v2.index.Index64(np.array([0, 1, 3, 2, 1, 2, 0], dtype=np.int64)),
            [
                ak._v2.contents.NumpyArray(
                    np.array([0.0, 1.1, 2.2]), parameters={"which": "inner1"}
                ),
                ak._v2.contents.NumpyArray(
                    np.array([0, 10, 20, 30], dtype=np.int32),
                    parameters={"which": "inner2"},
                ),
            ],
            parameters={"which": "middle"},
        ),
        valid_when=True,
        parameters={"which": "outer"},
    )

    if through is through_arrow:
        schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
        predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
            schema_arrow, pass_empty_field=True
        )
        assert predicted_form == array_form

    akarray = ak._v2.contents.ByteMaskedArray(
        ak._v2.index.Index8(
            np.array([False, True, False, True, False, True, True]).view(np.int8)
        ),
        ak._v2.contents.UnionArray(
            ak._v2.index.Index8(np.array([0, 0, 1, 1, 1, 0, 1], dtype=np.int8)),
            ak._v2.index.Index64(np.array([0, 1, 3, 2, 1, 2, 0], dtype=np.int64)),
            [
                ak._v2.contents.NumpyArray(
                    np.array([0.0, 1.1, 2.2]), parameters={"which": "inner1"}
                ),
                ak._v2.contents.ByteMaskedArray(
                    ak._v2.index.Index8(
                        np.array([False, False, True, False]).view(np.int8)
                    ),
                    ak._v2.contents.NumpyArray(
                        np.array([0, 10, 20, 30], dtype=np.int32),
                        parameters={"which": "inner2"},
                    ),
                    valid_when=False,
                    parameters={"which": "middle1"},
                ),
            ],
            parameters={"which": "middle2"},
        ),
        valid_when=True,
        parameters={"which": "outer"},
    )

    if through is through_arrow:
        schema_arrow, array_form = through(akarray, extensionarray, tmp_path)
        predicted_form = ak._v2._connect.pyarrow.form_handle_arrow(
            schema_arrow, pass_empty_field=True
        )
        assert predicted_form == array_form

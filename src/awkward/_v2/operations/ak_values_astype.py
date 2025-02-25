# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import awkward as ak

np = ak.nplike.NumpyMetadata.instance()


def values_astype(array, to, highlevel=True, behavior=None):
    """
    Args:
        array: Array whose numbers should be converted to a new numeric type.
        to (dtype or dtype specifier): Type to convert the numbers into.
        highlevel (bool): If True, return an #ak.Array; otherwise, return
            a low-level #ak.layout.Content subclass.
        behavior (None or dict): Custom #ak.behavior for the output array, if
            high-level.

    Converts all numbers in the array to a new type, leaving the structure
    untouched.

    For example,

        >>> array = ak.Array([1.1, 2.2, 3.3, 4.4, 5.5])
        >>> ak.values_astype(array, np.int32)
        <Array [1, 2, 3, 4, 5] type='5 * int32'>

    and

        >>> array = ak.Array([[1.1, 2.2, 3.3], [], [4.4, 5.5]])
        >>> ak.values_astype(array, np.int32)
        <Array [[1, 2, 3], [], [4, 5]] type='3 * var * int32'>

    Note, when converting values to a `np.datetime64` type that is unitless, a
    default '[us]' unit is assumed - until further specified as numpy dtypes.

    For example,

        >>> array = ak.Array([1567416600000])
        >>> ak.values_astype(array, "datetime64[ms]")
        <Array [2019-09-02T09:30:00.000] type='1 * datetime64'>

    or

        >>> array = ak.Array([1567416600000])
        >>> ak.values_astype(array, np.dtype("M8[ms]"))
        <Array [2019-09-02T09:30:00.000] type='1 * datetime64'>

    See also #ak.strings_astype.
    """
    with ak._v2._util.OperationErrorContext(
        "ak._v2.values_astype",
        dict(array=array, to=to, highlevel=highlevel, behavior=behavior),
    ):
        return _impl(array, to, highlevel, behavior)


def _impl(array, to, highlevel, behavior):
    to_dtype = np.dtype(to)
    to_str = ak._v2.types.numpytype._dtype_to_primitive_dict.get(to_dtype)

    if to_str is None:
        if to_dtype.name.startswith("datetime64"):
            to_str = to_dtype.name
        else:
            raise ak._v2._util.error(
                ValueError(
                    f"cannot use {to_dtype} to cast the numeric type of an array"
                )
            )

    layout = ak._v2.operations.to_layout(array, allow_record=False, allow_other=False)
    out = layout.numbers_to_type(to_str)
    return ak._v2._util.wrap(out, behavior, highlevel)

# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import awkward as ak
from awkward._v2.types.type import Type
from awkward._v2.forms.form import _parameters_equal


class RegularType(Type):
    def __init__(self, content, size, parameters=None, typestr=None):
        if not isinstance(content, Type):
            raise ak._v2._util.error(
                TypeError(
                    "{} 'content' must be a Type subtype, not {}".format(
                        type(self).__name__, repr(content)
                    )
                )
            )
        if not ak._util.isint(size) or size < 0:
            raise ak._v2._util.error(
                ValueError(
                    "{} 'size' must be of a positive integer, not {}".format(
                        type(self).__name__, repr(size)
                    )
                )
            )
        if parameters is not None and not isinstance(parameters, dict):
            raise ak._v2._util.error(
                TypeError(
                    "{} 'parameters' must be of type dict or None, not {}".format(
                        type(self).__name__, repr(parameters)
                    )
                )
            )
        if typestr is not None and not ak._util.isstr(typestr):
            raise ak._v2._util.error(
                TypeError(
                    "{} 'typestr' must be of type string or None, not {}".format(
                        type(self).__name__, repr(typestr)
                    )
                )
            )
        self._content = content
        self._size = size
        self._parameters = parameters
        self._typestr = typestr

    @property
    def content(self):
        return self._content

    @property
    def size(self):
        return self._size

    def _str(self, indent, compact):
        if self._typestr is not None:
            out = [self._typestr]

        elif self.parameter("__array__") == "string":
            return [f"string[{self._size}]"]

        elif self.parameter("__array__") == "bytestring":
            return [f"bytes[{self._size}]"]

        else:
            params = self._str_parameters()
            if params is None:
                out = [str(self._size), " * "] + self._content._str(indent, compact)
            else:
                out = (
                    ["[", str(self._size), " * "]
                    + self._content._str(indent, compact)
                    + [", ", params, "]"]
                )

        return [self._str_categorical_begin()] + out + [self._str_categorical_end()]

    def __repr__(self):
        args = [repr(self._content), repr(self._size)] + self._repr_args()
        return "{}({})".format(type(self).__name__, ", ".join(args))

    def __eq__(self, other):
        if isinstance(other, RegularType):
            return (
                self._typestr == other._typestr
                and self._size == other._size
                and _parameters_equal(
                    self._parameters, other._parameters, only_array_record=True
                )
                and self._content == other._content
            )
        else:
            return False

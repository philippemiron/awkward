# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import json

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401


def test_EmptyArray():
    v1 = json.loads(
        '{"class":"EmptyArray","has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "EmptyArray",
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_NumpyArray():
    v1 = json.loads(
        '{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "NumpyArray",
        "primitive": "float64",
        "inner_shape": [],
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"NumpyArray","inner_shape":[3,5],"itemsize":8,"format":"l","primitive":"int64","has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "NumpyArray",
        "primitive": "int64",
        "inner_shape": [3, 5],
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_RegularArray_NumpyArray():
    v1 = json.loads(
        '{"class":"RegularArray","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"size":3,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "RegularArray",
        "size": 3,
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"RegularArray","content":{"class":"EmptyArray","has_identities":false,"parameters":{},"form_key":null},"size":0,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "RegularArray",
        "size": 0,
        "content": {
            "class": "EmptyArray",
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_ListArray_NumpyArray():
    v1 = json.loads(
        '{"class":"ListArray64","starts":"i64","stops":"i64","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "ListArray",
        "starts": "i64",
        "stops": "i64",
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_ListOffsetArray_NumpyArray():
    v1 = json.loads(
        '{"class":"ListOffsetArray64","offsets":"i64","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "ListOffsetArray",
        "offsets": "i64",
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_RecordArray_NumpyArray():
    v1 = json.loads(
        '{"class":"RecordArray","contents":{"x":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"l","primitive":"int64","has_identities":false,"parameters":{},"form_key":null},"y":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "RecordArray",
        "contents": {
            "x": {
                "class": "NumpyArray",
                "primitive": "int64",
                "inner_shape": [],
                "has_identifier": False,
                "parameters": {},
                "form_key": None,
            },
            "y": {
                "class": "NumpyArray",
                "primitive": "float64",
                "inner_shape": [],
                "has_identifier": False,
                "parameters": {},
                "form_key": None,
            },
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"RecordArray","contents":[{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"l","primitive":"int64","has_identities":false,"parameters":{},"form_key":null},{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}],"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "RecordArray",
        "contents": [
            {
                "class": "NumpyArray",
                "primitive": "int64",
                "inner_shape": [],
                "has_identifier": False,
                "parameters": {},
                "form_key": None,
            },
            {
                "class": "NumpyArray",
                "primitive": "float64",
                "inner_shape": [],
                "has_identifier": False,
                "parameters": {},
                "form_key": None,
            },
        ],
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"RecordArray","contents":{},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "RecordArray",
        "contents": {},
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"RecordArray","contents":[],"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "RecordArray",
        "contents": [],
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_IndexedArray_NumpyArray():
    v1 = json.loads(
        '{"class":"IndexedArray64","index":"i64","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "IndexedArray",
        "index": "i64",
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_IndexedOptionArray_NumpyArray():
    v1 = json.loads(
        '{"class":"IndexedOptionArray64","index":"i64","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "IndexedOptionArray",
        "index": "i64",
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_ByteMaskedArray_NumpyArray():
    v1 = json.loads(
        '{"class":"ByteMaskedArray","mask":"i8","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"valid_when":true,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "ByteMaskedArray",
        "mask": "i8",
        "valid_when": True,
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"ByteMaskedArray","mask":"i8","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"valid_when":false,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "ByteMaskedArray",
        "mask": "i8",
        "valid_when": False,
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_BitMaskedArray_NumpyArray():
    v1 = json.loads(
        '{"class":"BitMaskedArray","mask":"u8","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"valid_when":true,"lsb_order":false,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "BitMaskedArray",
        "mask": "u8",
        "valid_when": True,
        "lsb_order": False,
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"BitMaskedArray","mask":"u8","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"valid_when":false,"lsb_order":false,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "BitMaskedArray",
        "mask": "u8",
        "valid_when": False,
        "lsb_order": False,
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"BitMaskedArray","mask":"u8","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"valid_when":true,"lsb_order":true,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "BitMaskedArray",
        "mask": "u8",
        "valid_when": True,
        "lsb_order": True,
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"BitMaskedArray","mask":"u8","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"valid_when":false,"lsb_order":true,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "BitMaskedArray",
        "mask": "u8",
        "valid_when": False,
        "lsb_order": True,
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_UnmaskedArray_NumpyArray():
    v1 = json.loads(
        '{"class":"UnmaskedArray","content":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "UnmaskedArray",
        "content": {
            "class": "NumpyArray",
            "primitive": "float64",
            "inner_shape": [],
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_UnionArray_NumpyArray():
    v1 = json.loads(
        '{"class":"UnionArray8_64","tags":"i8","index":"i64","contents":[{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"l","primitive":"int64","has_identities":false,"parameters":{},"form_key":null},{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}],"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "UnionArray",
        "tags": "i8",
        "index": "i64",
        "contents": [
            {
                "class": "NumpyArray",
                "primitive": "int64",
                "inner_shape": [],
                "has_identifier": False,
                "parameters": {},
                "form_key": None,
            },
            {
                "class": "NumpyArray",
                "primitive": "float64",
                "inner_shape": [],
                "has_identifier": False,
                "parameters": {},
                "form_key": None,
            },
        ],
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_RegularArray_RecordArray_NumpyArray():
    v1 = json.loads(
        '{"class":"RegularArray","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"size":3,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "RegularArray",
        "size": 3,
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"RegularArray","content":{"class":"RecordArray","contents":{"nest":{"class":"EmptyArray","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"size":0,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "RegularArray",
        "size": 0,
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "EmptyArray",
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_ListArray_RecordArray_NumpyArray():
    v1 = json.loads(
        '{"class":"ListArray64","starts":"i64","stops":"i64","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "ListArray",
        "starts": "i64",
        "stops": "i64",
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_ListOffsetArray_RecordArray_NumpyArray():
    v1 = json.loads(
        '{"class":"ListOffsetArray64","offsets":"i64","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "ListOffsetArray",
        "offsets": "i64",
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_IndexedArray_RecordArray_NumpyArray():
    v1 = json.loads(
        '{"class":"IndexedArray64","index":"i64","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "IndexedArray",
        "index": "i64",
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_IndexedOptionArray_RecordArray_NumpyArray():
    v1 = json.loads(
        '{"class":"IndexedOptionArray64","index":"i64","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "IndexedOptionArray",
        "index": "i64",
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_ByteMaskedArray_RecordArray_NumpyArray():
    v1 = json.loads(
        '{"class":"ByteMaskedArray","mask":"i8","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"valid_when":true,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "ByteMaskedArray",
        "mask": "i8",
        "valid_when": True,
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"ByteMaskedArray","mask":"i8","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"valid_when":false,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "ByteMaskedArray",
        "mask": "i8",
        "valid_when": False,
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_BitMaskedArray_RecordArray_NumpyArray():
    v1 = json.loads(
        '{"class":"BitMaskedArray","mask":"u8","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"valid_when":true,"lsb_order":false,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "BitMaskedArray",
        "mask": "u8",
        "valid_when": True,
        "lsb_order": False,
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"BitMaskedArray","mask":"u8","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"valid_when":false,"lsb_order":false,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "BitMaskedArray",
        "mask": "u8",
        "valid_when": False,
        "lsb_order": False,
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"BitMaskedArray","mask":"u8","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"valid_when":true,"lsb_order":true,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "BitMaskedArray",
        "mask": "u8",
        "valid_when": True,
        "lsb_order": True,
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

    v1 = json.loads(
        '{"class":"BitMaskedArray","mask":"u8","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"valid_when":false,"lsb_order":true,"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "BitMaskedArray",
        "mask": "u8",
        "valid_when": False,
        "lsb_order": True,
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_UnmaskedArray_RecordArray_NumpyArray():
    v1 = json.loads(
        '{"class":"UnmaskedArray","content":{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "UnmaskedArray",
        "content": {
            "class": "RecordArray",
            "contents": {
                "nest": {
                    "class": "NumpyArray",
                    "primitive": "float64",
                    "inner_shape": [],
                    "has_identifier": False,
                    "parameters": {},
                    "form_key": None,
                }
            },
            "has_identifier": False,
            "parameters": {},
            "form_key": None,
        },
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }


def test_UnionArray_RecordArray_NumpyArray():
    v1 = json.loads(
        '{"class":"UnionArray8_64","tags":"i8","index":"i64","contents":[{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"l","primitive":"int64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null},{"class":"RecordArray","contents":{"nest":{"class":"NumpyArray","inner_shape":[],"itemsize":8,"format":"d","primitive":"float64","has_identities":false,"parameters":{},"form_key":null}},"has_identities":false,"parameters":{},"form_key":null}],"has_identities":false,"parameters":{},"form_key":null}'
    )
    v2 = ak._v2.forms.from_iter(v1).tolist()
    assert v2 == {
        "class": "UnionArray",
        "tags": "i8",
        "index": "i64",
        "contents": [
            {
                "class": "RecordArray",
                "contents": {
                    "nest": {
                        "class": "NumpyArray",
                        "primitive": "int64",
                        "inner_shape": [],
                        "has_identifier": False,
                        "parameters": {},
                        "form_key": None,
                    }
                },
                "has_identifier": False,
                "parameters": {},
                "form_key": None,
            },
            {
                "class": "RecordArray",
                "contents": {
                    "nest": {
                        "class": "NumpyArray",
                        "primitive": "float64",
                        "inner_shape": [],
                        "has_identifier": False,
                        "parameters": {},
                        "form_key": None,
                    }
                },
                "has_identifier": False,
                "parameters": {},
                "form_key": None,
            },
        ],
        "has_identifier": False,
        "parameters": {},
        "form_key": None,
    }

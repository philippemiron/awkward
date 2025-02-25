// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

#ifndef AWKWARD_LISTOFFSETARRAY_H_
#define AWKWARD_LISTOFFSETARRAY_H_

#include <memory>

#include "awkward/common.h"
#include "awkward/Index.h"
#include "awkward/Identities.h"
#include "awkward/Content.h"

namespace awkward {
  /// @class ListOffsetForm
  ///
  /// @brief Form describing ListOffsetArray.
  class LIBAWKWARD_EXPORT_SYMBOL ListOffsetForm: public Form {
  public:
    /// @brief Creates a ListOffsetForm. See
    /// {@link ListOffsetArrayOf ListOffsetArray} for documentation.
    ListOffsetForm(bool has_identities,
                   const util::Parameters& parameters,
                   const FormKey& form_key,
                   Index::Form offsets,
                   const FormPtr& content);

    Index::Form
      offsets() const;

    const FormPtr
      content() const;

    const TypePtr
      type(const util::TypeStrs& typestrs) const override;

    void
      tojson_part(ToJson& builder, bool verbose) const override;

    const FormPtr
      shallow_copy() const override;

    const FormPtr
      with_form_key(const FormKey& form_key) const override;

    const std::string
      purelist_parameter(const std::string& key) const override;

    bool
      purelist_isregular() const override;

    int64_t
      purelist_depth() const override;

    bool
      dimension_optiontype() const override;

    const std::pair<int64_t, int64_t>
      minmax_depth() const override;

    const std::pair<bool, int64_t>
      branch_depth() const override;

    int64_t
      numfields() const override;

    int64_t
      fieldindex(const std::string& key) const override;

    const std::string
      key(int64_t fieldindex) const override;

    bool
      haskey(const std::string& key) const override;

    const std::vector<std::string>
      keys() const override;

    bool
      istuple() const override;

    bool
      equal(const FormPtr& other,
            bool check_identities,
            bool check_parameters,
            bool check_form_key,
            bool compatibility_check) const override;

    const FormPtr
      getitem_field(const std::string& key) const override;

    const FormPtr
      getitem_fields(const std::vector<std::string>& keys) const override;

  private:
    Index::Form offsets_;
    const FormPtr content_;
  };

  /// @class ListOffsetArrayOf
  ///
  /// @brief Represents an array of nested lists that can have different
  /// lengths using one index named #offsets.
  ///
  /// A single #offsets index requires the #content to be contiguous, in-order,
  /// and non-overlapping, though it need not start at zero (there can be
  /// "unreachable" elements before the first visible item if
  /// `offsets[0] != 0`).
  ///
  /// See #ListOffsetArrayOf for the meaning of each parameter.
  template <typename T>
  class
#ifdef AWKWARD_LISTOFFSETARRAY_NO_EXTERN_TEMPLATE
  LIBAWKWARD_EXPORT_SYMBOL
#endif
  ListOffsetArrayOf: public Content {
  public:
    /// @brief Creates a ListOffsetArray from a full set of parameters.
    ///
    /// @param identities Optional Identities for each element of the array
    /// (may be `nullptr`).
    /// @param parameters String-to-JSON map that augments the meaning of this
    /// array.
    /// @param offsets Positions where one nested list stops and the next
    /// starts in the #content; the `offsets` must be monotonically increasing.
    /// The length of `offsets` is one greater than the length of the array it
    /// represents, and as such must always have at least one element.
    /// @param content Data contained within all nested lists as a contiguous
    /// array.
    /// Values in `content[i]` where `i < offsets[0]` are "unreachable," and
    /// don't exist in the high level view, as are any where
    /// `i >= offsets[len(offsets) - 1]`.
    ListOffsetArrayOf<T>(const IdentitiesPtr& identities,
                         const util::Parameters& parameters,
                         const IndexOf<T>& offsets,
                         const ContentPtr& content,
                         bool represents_regular = false);

    /// @brief Positions where one nested list stops and the next starts in
    /// the #content; the `offsets` must be monotonically increasing.
    ///
    /// The length of `offsets` is one greater than the length of the array it
    /// represents, and as such must always have at least one element.
    const IndexOf<T>
      offsets() const;

    /// @brief Data contained within all nested lists as a contiguous array.
    ///
    /// Values in `content[i]` where `i < offsets[0]` are "unreachable," and
    /// don't exist in the high level view, as are any where
    /// `i >= offsets[len(offsets) - 1]`.
    const ContentPtr
      content() const;

    /// @brief Starting positions of each nested list, similar to
    /// {@link ListArrayOf#starts ListArray::starts}, but derived from
    /// #offsets.
    ///
    /// This is a view of all but the last element of #offsets.
    const IndexOf<T>
      starts() const;

    /// @brief Stopping positions of each nested list, similar to
    /// {@link ListArrayOf#stops ListArray::stops}, but derived from
    /// #offsets.
    ///
    /// This is a view of all but the first element of #offsets.
    const IndexOf<T>
      stops() const;

    /// @brief Returns 64-bit offsets, possibly starting with `offsets[0] = 0`.
    ///
    /// If the #offsets of this array satisfies the constraint, it is not
    /// copied. Otherwise, a new {@link IndexOf Index64} is returned.
    ///
    /// @param start_at_zero If `true`, the first offset will be `0`, meaning
    /// there are no "unreachable" elements in the `content` that corresponds
    /// to these offsets.
    Index64
      compact_offsets64(bool start_at_zero) const;

    /// @brief Moves #content elements if necessary to match a given set of
    /// `offsets` and return a {@link ListOffsetArrayOf ListOffsetArray} that
    /// matches.
    ///
    /// As indicated by the name, this is a basic element of broadcasting.
    const ContentPtr
      broadcast_tooffsets64(const Index64& offsets) const;

    /// @brief Converts this array to a RegularArray if all nested lists have
    /// the same size (error otherwise).
    const ContentPtr
      toRegularArray() const;

    /// @brief Returns a {@link ListOffsetArrayOf ListOffsetArray} with
    /// 64-bit #offsets and possibly starting with `offsets[0] = 0`; a
    /// #shallow_copy if possible.
    ///
    /// @param start_at_zero If `true`, the first offset will be `0`, meaning
    /// there are no "unreachable" elements in the `content` that corresponds
    /// to these offsets.
    const ContentPtr
      toListOffsetArray64(bool start_at_zero) const;

    /// @brief User-friendly name of this class: `"ListOffsetArray32"`,
    /// `"ListOffsetArrayU32"`, or `"ListOffsetArray64"`.
    const std::string
      classname() const override;

    void
      setidentities() override;

    void
      setidentities(const IdentitiesPtr& identities) override;

    const TypePtr
      type(const util::TypeStrs& typestrs) const override;

    const FormPtr
      form(bool materialize) const override;

    kernel::lib
      kernels() const override;

    void
      caches(std::vector<ArrayCachePtr>& out) const override;

    const std::string
      tostring_part(const std::string& indent,
                    const std::string& pre,
                    const std::string& post) const override;

    void
      tojson_part(ToJson& builder, bool include_beginendlist) const override;

    void
      nbytes_part(std::map<size_t, int64_t>& largest) const override;

    /// @copydoc Content::length()
    ///
    /// Equal to `len(offsets) - 1`.
    int64_t
      length() const override;

    const ContentPtr
      shallow_copy() const override;

    const ContentPtr
      deep_copy(bool copyarrays,
                bool copyindexes,
                bool copyidentities) const override;

    void
      check_for_iteration() const override;

    const ContentPtr
      getitem_nothing() const override;

    const ContentPtr
      getitem_at(int64_t at) const override;

    const ContentPtr
      getitem_at_nowrap(int64_t at) const override;

    const ContentPtr
      getitem_range(int64_t start, int64_t stop) const override;

    const ContentPtr
      getitem_range_nowrap(int64_t start, int64_t stop) const override;

    const ContentPtr
      getitem_field(const std::string& key) const override;

    const ContentPtr
      getitem_field(const std::string& key,
                    const Slice& only_fields) const override;

    const ContentPtr
      getitem_fields(const std::vector<std::string>& keys) const override;

    const ContentPtr
      getitem_fields(const std::vector<std::string>& keys,
                     const Slice& only_fields) const override;

    const ContentPtr
      getitem_next_jagged(const Index64& slicestarts,
                          const Index64& slicestops,
                          const SliceItemPtr& slicecontent,
                          const Slice& tail) const override;

    const ContentPtr
      carry(const Index64& carry, bool allow_lazy) const override;

    int64_t
      purelist_depth() const override;

    const std::pair<int64_t, int64_t>
      minmax_depth() const override;

    const std::pair<bool, int64_t>
      branch_depth() const override;

    int64_t
      numfields() const override;

    int64_t
      fieldindex(const std::string& key) const override;

    const std::string
      key(int64_t fieldindex) const override;

    bool
      haskey(const std::string& key) const override;

    const std::vector<std::string>
      keys() const override;

    bool
      istuple() const override;

    // operations
    const std::string
      validityerror(const std::string& path) const override;

    /// @copydoc Content::shallow_simplify()
    ///
    /// For {@link ListOffsetArrayOf ListOffsetArray}, this method returns
    /// #shallow_copy (pass-through).
    const ContentPtr
      shallow_simplify() const override;

    const ContentPtr
      num(int64_t axis, int64_t depth) const override;

    const std::pair<Index64, ContentPtr>
      offsets_and_flattened(int64_t axis, int64_t depth) const override;

    bool
      mergeable(const ContentPtr& other, bool mergebool) const override;

    bool
      referentially_equal(const ContentPtr& other) const override;

    const ContentPtr
      mergemany(const ContentPtrVec& others) const override;

    const SliceItemPtr
      asslice() const override;

    const ContentPtr
      fillna(const ContentPtr& value) const override;

    const ContentPtr
      rpad(int64_t target, int64_t axis, int64_t depth) const override;

    const ContentPtr
      rpad_and_clip(int64_t target,
                    int64_t axis,
                    int64_t depth) const override;

    const ContentPtr
      reduce_next(const Reducer& reducer,
                  int64_t negaxis,
                  const Index64& starts,
                  const Index64& shifts,
                  const Index64& parents,
                  int64_t outlength,
                  bool mask,
                  bool keepdims) const override;

    const ContentPtr
      sort_next(int64_t negaxis,
                const Index64& starts,
                const Index64& parents,
                int64_t outlength,
                bool ascending,
                bool stable) const override;

    const ContentPtr
      argsort_next(int64_t negaxis,
                   const Index64& starts,
                   const Index64& shifts,
                   const Index64& parents,
                   int64_t outlength,
                   bool ascending,
                   bool stable) const override;

    const ContentPtr
      localindex(int64_t axis, int64_t depth) const override;

    const ContentPtr
      combinations(int64_t n,
                   bool replacement,
                   const util::RecordLookupPtr& recordlookup,
                   const util::Parameters& parameters,
                   int64_t axis,
                   int64_t depth) const override;

    const ContentPtr
      getitem_next(const SliceAt& at,
                   const Slice& tail,
                   const Index64& advanced) const override;

    const ContentPtr
      getitem_next(const SliceRange& range,
                   const Slice& tail,
                   const Index64& advanced) const override;

    const ContentPtr
      getitem_next(const SliceArray64& array,
                   const Slice& tail,
                   const Index64& advanced) const override;

    const ContentPtr
      getitem_next(const SliceJagged64& jagged,
                   const Slice& tail,
                   const Index64& advanced) const override;

    const ContentPtr
      getitem_next_jagged(const Index64& slicestarts,
                          const Index64& slicestops,
                          const SliceArray64& slicecontent,
                          const Slice& tail) const override;

    const ContentPtr
      getitem_next_jagged(const Index64& slicestarts,
                          const Index64& slicestops,
                          const SliceMissing64& slicecontent,
                          const Slice& tail) const override;

    const ContentPtr
      getitem_next_jagged(const Index64& slicestarts,
                          const Index64& slicestops,
                          const SliceJagged64& slicecontent,
                          const Slice& tail) const override;

    const ContentPtr
      copy_to(kernel::lib ptr_lib) const override;

    const ContentPtr
      numbers_to_type(const std::string& name) const override;

    /// @brief Returns 'true' if all components of the array are unique
    bool
      is_unique() const override;

    /// @brief Returns an array where all components are unique
    const ContentPtr
      unique() const override;

    /// @brief Returns 'true' if subranges are equal
    bool
      is_subrange_equal(const Index64& start, const Index64& stop) const override;

  private:
    /// @brief See #offsets.
    const IndexOf<T> offsets_;
    /// @brief See #content.
    const ContentPtr content_;
    const bool represents_regular_;
  };

#ifndef AWKWARD_LISTOFFSETARRAY_NO_EXTERN_TEMPLATE
  extern template class ListOffsetArrayOf<int32_t>;
  extern template class ListOffsetArrayOf<uint32_t>;
  extern template class ListOffsetArrayOf<int64_t>;
#endif

  using ListOffsetArray32  = ListOffsetArrayOf<int32_t>;
  using ListOffsetArrayU32 = ListOffsetArrayOf<uint32_t>;
  using ListOffsetArray64  = ListOffsetArrayOf<int64_t>;
}

#endif // AWKWARD_LISTOFFSETARRAY_H_

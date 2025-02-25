// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

#define FILENAME(line) FILENAME_FOR_EXCEPTIONS("src/libawkward/layoutbuilder/IndexedOptionArrayBuilder.cpp", line)

#include "awkward/layoutbuilder/IndexedOptionArrayBuilder.h"
#include "awkward/layoutbuilder/LayoutBuilder.h"

namespace awkward {

  ///
  template <typename T, typename I>
  IndexedOptionArrayBuilder<T, I>::IndexedOptionArrayBuilder(FormBuilderPtr<T, I> content,
                                                             const util::Parameters& parameters,
                                                             const std::string& form_key,
                                                             const std::string& form_index,
                                                             bool is_categorical,
                                                             const std::string attribute,
                                                             const std::string partition)
    : content_(content),
      parameters_(parameters),
      is_categorical_(is_categorical),
      form_index_(form_index) {
    vm_output_data_ = std::string("part")
      .append(partition).append("-")
      .append(form_key).append("-")
      .append(attribute);

    vm_func_name_ = std::string(form_key).append("-").append(attribute);

    vm_func_type_ = content_.get()->vm_func_type();

    vm_output_ = std::string("output ")
      .append(vm_output_data_)
      .append(" ")
      .append(form_index)
      .append(" ")
      .append(content_.get()->vm_output());

    vm_func_.append(content_.get()->vm_func())
      .append(": ").append(vm_func_name())
      .append(" dup ").append(std::to_string(static_cast<utype>(state::null)))
      .append(" = if ")
      .append("drop ")
      .append("variable null    -1 null ! ")
      .append("null @ ")
      .append(vm_output_data_).append(" <- stack ")
      .append("exit ")
      .append("else ")
      .append("variable index    1 index +! ")
      .append("index @ 1- ")
      .append(vm_output_data_).append(" <- stack ")
      .append(content_.get()->vm_func_name())
      .append(" then ")
      .append("; ");

    vm_data_from_stack_ = std::string(content_.get()->vm_from_stack())
      .append("0 ").append(vm_output_data_).append(" <- stack ");

    vm_error_ = content_.get()->vm_error();
    validate();
  }

  template <typename T, typename I>
  void
  IndexedOptionArrayBuilder<T, I>::validate() const {
    if (is_categorical_) {
      throw std::invalid_argument(
        std::string("categorical form of a ") + classname()
        + std::string(" is not supported yet ")
        + FILENAME(__LINE__));
    }
  }

  template <typename T, typename I>
  const std::string
  IndexedOptionArrayBuilder<T, I>::classname() const {
    return "IndexedOptionArrayBuilder";
  }

  template <typename T, typename I>
  const std::string
  IndexedOptionArrayBuilder<T, I>::vm_output() const {
    return vm_output_;
  }

  template <typename T, typename I>
  const std::string
  IndexedOptionArrayBuilder<T, I>::vm_output_data() const {
    return vm_output_data_;
  }

  template <typename T, typename I>
  const std::string
  IndexedOptionArrayBuilder<T, I>::vm_func() const {
    return vm_func_;
  }

  template <typename T, typename I>
  const std::string
  IndexedOptionArrayBuilder<T, I>::vm_func_name() const {
    return vm_func_name_;
  }

  template <typename T, typename I>
  const std::string
  IndexedOptionArrayBuilder<T, I>::vm_func_type() const {
    return vm_func_type_;
  }

  template <typename T, typename I>
  const std::string
  IndexedOptionArrayBuilder<T, I>::vm_from_stack() const {
    return vm_data_from_stack_;
  }

  template <typename T, typename I>
  const std::string
  IndexedOptionArrayBuilder<T, I>::vm_error() const {
    return vm_error_;
  }

  template <typename T, typename I>
  void
  IndexedOptionArrayBuilder<T, I>::boolean(bool x, LayoutBuilderPtr<T, I> builder) {
    content_.get()->boolean(x, builder);
  }

  template <typename T, typename I>
  void
  IndexedOptionArrayBuilder<T, I>::int64(int64_t x, LayoutBuilderPtr<T, I> builder) {
    content_.get()->int64(x, builder);
  }

  template <typename T, typename I>
  void
  IndexedOptionArrayBuilder<T, I>::float64(double x, LayoutBuilderPtr<T, I> builder) {
    content_.get()->float64(x, builder);
  }

  template <typename T, typename I>
  void
  IndexedOptionArrayBuilder<T, I>::complex(std::complex<double> x, LayoutBuilderPtr<T, I> builder) {
    content_.get()->complex(x, builder);
  }

  template <typename T, typename I>
  void
  IndexedOptionArrayBuilder<T, I>::bytestring(const std::string& x, LayoutBuilderPtr<T, I> builder) {
    content_.get()->bytestring(x, builder);
  }

  template <typename T, typename I>
  void
  IndexedOptionArrayBuilder<T, I>::string(const std::string& x, LayoutBuilderPtr<T, I> builder) {
    content_.get()->string(x, builder);
  }

  template <typename T, typename I>
  void
  IndexedOptionArrayBuilder<T, I>::begin_list(LayoutBuilderPtr<T, I> builder) {
    content_.get()->begin_list(builder);
  }

  template <typename T, typename I>
  void
  IndexedOptionArrayBuilder<T, I>::end_list(LayoutBuilderPtr<T, I> builder) {
    content_.get()->end_list(builder);
  }

  template class EXPORT_TEMPLATE_INST IndexedOptionArrayBuilder<int32_t, int32_t>;
  template class EXPORT_TEMPLATE_INST IndexedOptionArrayBuilder<int64_t, int32_t>;

}

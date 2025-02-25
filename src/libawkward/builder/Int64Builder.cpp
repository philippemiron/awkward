// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

#define FILENAME(line) FILENAME_FOR_EXCEPTIONS("src/libawkward/builder/Int64Builder.cpp", line)

#include <stdexcept>

#include "awkward/builder/ArrayBuilderOptions.h"
#include "awkward/builder/Complex128Builder.h"
#include "awkward/builder/Float64Builder.h"
#include "awkward/builder/OptionBuilder.h"
#include "awkward/builder/UnionBuilder.h"

#include "awkward/builder/Int64Builder.h"

namespace awkward {
  const BuilderPtr
  Int64Builder::fromempty(const ArrayBuilderOptions& options) {
    return std::make_shared<Int64Builder>(options,
                                          GrowableBuffer<int64_t>::empty(options));
  }

  Int64Builder::Int64Builder(const ArrayBuilderOptions& options,
                             GrowableBuffer<int64_t> buffer)
      : options_(options)
      , buffer_(std::move(buffer)) { }

  GrowableBuffer<int64_t>
  Int64Builder::buffer() {
    // FIXME: swap with an empty buffer!
    return std::move(buffer_);
  }

  const std::string
  Int64Builder::classname() const {
    return "Int64Builder";
  };

  const std::string
  Int64Builder::to_buffers(BuffersContainer& container, int64_t& form_key_id) const {
    std::stringstream form_key;
    form_key << "node" << (form_key_id++);

    container.copy_buffer(form_key.str() + "-data",
                          buffer_.ptr().get(),
                          (int64_t)(buffer_.length() * sizeof(int64_t)));

    return "{\"class\": \"NumpyArray\", \"primitive\": \"int64\", \"form_key\": \""
           + form_key.str() + "\"}";
  }

  int64_t
  Int64Builder::length() const {
    return (int64_t)buffer_.length();
  }

  void
  Int64Builder::clear() {
    buffer_.clear();
  }

  bool
  Int64Builder::active() const {
    return false;
  }

  const BuilderPtr
  Int64Builder::null() {
    BuilderPtr out = OptionBuilder::fromvalids(options_, shared_from_this());
    out.get()->null();
    return std::move(out);
  }

  const BuilderPtr
  Int64Builder::boolean(bool x) {
    BuilderPtr out = UnionBuilder::fromsingle(options_, shared_from_this());
    out.get()->boolean(x);
    return std::move(out);
  }

  const BuilderPtr
  Int64Builder::integer(int64_t x) {
    buffer_.append(x);
    return nullptr;
  }

  const BuilderPtr
  Int64Builder::real(double x) {
    BuilderPtr out = Float64Builder::fromint64(options_, std::move(buffer_));
    out.get()->real(x);
    return std::move(out);
  }

  const BuilderPtr
  Int64Builder::complex(std::complex<double> x) {
    BuilderPtr out = Complex128Builder::fromint64(options_, std::move(buffer_));
    out.get()->complex(x);
    return std::move(out);
  }

  const BuilderPtr
  Int64Builder::datetime(int64_t x, const std::string& unit) {
    BuilderPtr out = UnionBuilder::fromsingle(options_, shared_from_this());
    out.get()->datetime(x, unit);
    return std::move(out);
  }

  const BuilderPtr
  Int64Builder::timedelta(int64_t x, const std::string& unit) {
    BuilderPtr out = UnionBuilder::fromsingle(options_, shared_from_this());
    out.get()->timedelta(x, unit);
    return std::move(out);
  }

  const BuilderPtr
  Int64Builder::string(const char* x, int64_t length, const char* encoding) {
    BuilderPtr out = UnionBuilder::fromsingle(options_, shared_from_this());
    out.get()->string(x, length, encoding);
    return std::move(out);
  }

  const BuilderPtr
  Int64Builder::beginlist() {
    BuilderPtr out = UnionBuilder::fromsingle(options_, shared_from_this());
    out.get()->beginlist();
    return std::move(out);
  }

  const BuilderPtr
  Int64Builder::endlist() {
    throw std::invalid_argument(
      std::string("called 'end_list' without 'begin_list' at the same level before it")
      + FILENAME(__LINE__));
  }

  const BuilderPtr
  Int64Builder::begintuple(int64_t numfields) {
    BuilderPtr out = UnionBuilder::fromsingle(options_, shared_from_this());
    out.get()->begintuple(numfields);
    return std::move(out);
  }

  const BuilderPtr
  Int64Builder::index(int64_t index) {
    throw std::invalid_argument(
      std::string("called 'index' without 'begin_tuple' at the same level before it")
      + FILENAME(__LINE__));
  }

  const BuilderPtr
  Int64Builder::endtuple() {
    throw std::invalid_argument(
      std::string("called 'end_tuple' without 'begin_tuple' at the same level before it")
      + FILENAME(__LINE__));
  }

  const BuilderPtr
  Int64Builder::beginrecord(const char* name, bool check) {
    BuilderPtr out = UnionBuilder::fromsingle(options_, shared_from_this());
    out.get()->beginrecord(name, check);
    return std::move(out);
  }

  void
  Int64Builder::field(const char* key, bool check) {
    throw std::invalid_argument(
      std::string("called 'field' without 'begin_record' at the same level before it")
      + FILENAME(__LINE__));
  }

  const BuilderPtr
  Int64Builder::endrecord() {
    throw std::invalid_argument(
      std::string("called 'end_record' without 'begin_record' at the same level before it")
      + FILENAME(__LINE__));
  }

}

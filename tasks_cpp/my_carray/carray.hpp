#pragma once

#include <exception>
#include <limits>

template <typename Value>
class IteratorBase
{
public:
  using iterator_category = std::random_access_iterator_tag;
  using value_type = Value;
  using difference_type = ptrdiff_t;
  using pointer = Value *;
  using reference = Value &;

  explicit IteratorBase(
      Value * _ptr
    ) noexcept :
    p_(_ptr)
  {
  }

  IteratorBase(
      const IteratorBase & _it
    ) noexcept :
    p_(_it.p_)
  {
  }

  IteratorBase & operator=(
      Value * _ptr
    ) noexcept
  {
    p_ = _ptr;
    return *this;
  }

  IteratorBase & operator=(
      const IteratorBase & _it
    ) noexcept
  {
    p_ = _it.p_;
    return *this;
  }

  explicit operator bool() const noexcept
  {
    return p_ != nullptr;
  }

  IteratorBase & operator++() noexcept
  {
    ++p_;
    return *this;
  }

  IteratorBase & operator--() noexcept
  {
    --p_;
    return *this;
  }

  IteratorBase operator++(int) noexcept
  {
    IteratorBase t(*this);
    ++p_;
    return t;
  }

  IteratorBase operator--(int) noexcept
  {
    IteratorBase t(*this);
    --p_;
    return t;
  }

  IteratorBase & operator+=(
      const std::ptrdiff_t & _dx
    ) noexcept
  {
    p_ += _dx;
    return *this;
  }

  IteratorBase & operator-=(
      const std::ptrdiff_t & _dx
    ) noexcept
  {
    p_ -= _dx;
    return *this;
  }

  IteratorBase operator+(
      const std::ptrdiff_t & _dx
    ) noexcept
  {
    Value * p = p_;
    p_ += _dx;
    IteratorBase t(*this);
    p_ = p;
    return t;
  }

  IteratorBase operator-(
      const std::ptrdiff_t & _dx
    ) noexcept
  {
    Value * p = p_;
    p_ -= _dx;
    IteratorBase t(*this);
    p_ = p;
    return t;
  }

  bool operator==(
      const IteratorBase & _it
    ) const noexcept
  {
    return p_ == _it.p_;
  }

  bool operator!=(
      const IteratorBase & _it
    ) const noexcept
  {
    return p_ != _it.p_;
  }

  Value & operator *() noexcept
  {
    return *p_;
  }

  const Value & operator *() const noexcept
  {
    return *p_;
  }

  Value & operator->() noexcept
  {
    return p_;
  }

  std::ptrdiff_t operator-(
      const IteratorBase & _it
    ) const noexcept
  {
    return p_ - _it.p_;
  }

  bool operator<(
      const IteratorBase & _it
    ) const noexcept
  {
    return p_ < _it.p_;
  }

private:
  Value * p_;
};

template <typename Value, typename Size = size_t>
class CArray
{
public:
  using value_type = Value;
  using size_type = Size;

  using iterator = IteratorBase<value_type>;
  using const_iterator = const iterator;

  CArray() noexcept :
    capa_(0),
    size_(0),
    data_(nullptr)
  {
  }

  CArray(
      const CArray & _other
    )
  {
    size_type newsize = _other.size();
    try_grow(newsize);
    copy(_other.data_, newsize, data_, false, false);
    size_ = newsize;
  }

  CArray & operator=(
    const CArray & _other
    ) noexcept
  {
    if (_other != *this)
    {
      size_type newsize = _other.size();
      try_grow(newsize);
      copy(_other.data_, newsize, data_, false, false);
      size_ = newsize;
    }
    return *this;
  }

  ~CArray()
  {
    delete[] data_;
  }

  void push_back(
      const value_type & _value
    )
  {
    try_grow(size() + 1);
    data_[size()] = _value;
    ++size_;
  }

  void insert(
      size_type _index,
      const value_type & _value
    )
  {
    if ((_index >= 0) && (_index <= size_))
    {
      try_grow(size() + 1);
      copy(&data_[size() - 1], size() - _index, &data_[size()], true, true);
      data_[_index] = _value;
      ++size_;
    }
    else
      throw std::out_of_range("Invalid index");
  }

  void erase(
      size_type _index
    )
  {
    if ((_index >= 0) && (_index < size_))
    {
      copy(&data_[_index + 1], size() - _index - 1, &data_[_index], false, true);
      --size_;
    }
    else
      throw std::out_of_range("Invalid index");
  }

  void reserve(
      size_type _n
    )
  {
    try_grow(_n);
  }

  void resize(
      size_type _n
    )
  {
    if (!try_grow(_n))
    {
      if (_n < size_)
      {
        for (size_type i = _n; i < size_; ++i)
          (data_[i]).~value_type();
      }
      size_ = _n;
    }
  }

  void resize(
      size_type _n,
      const value_type & _v
    )
  {
    size_type old_size = size_;
    resize(_n);
    if (old_size < size_)
    {
      for (size_type i = old_size; i < size_; ++i)
        data_[i] = _v;
    }
  }

  void clear() noexcept
  {
    for (size_type i = 0; i < size_; ++i)
      (data_[i]).~value_type();
    size_ = 0;
  }

  size_type size() const noexcept
  {
    return size_;
  }

  size_type max_size() const noexcept
  {
    return std::numeric_limits<size_type>::max();
  }

  bool empty() const noexcept
  {
    return size_ == 0;
  }

  size_type capacity() const noexcept
  {
    return capa_;
  }

  value_type & operator[](
      size_type _index
    ) noexcept
  {
    return data_[_index];
  }

  const value_type & operator[](
      size_type _index
    ) const noexcept
  {
    return data_[_index];
  }

  value_type & at(
      size_type _index
    )
  {
    if ((_index >= 0) && (_index < size_))
      return data_[_index];
    else
      throw std::out_of_range("Invalid index");
  }

  const value_type & at(
      size_type _index
    ) const
  {
    if ((_index >= 0) && (_index < size_))
      return data_[_index];
    else
      throw std::out_of_range("Invalid index");
  }

  value_type & front() noexcept
  {
    return data_[0];
  }

  const value_type & front() const noexcept
  {
    return data_[0];
  }

  value_type & back() noexcept
  {
    return data_[size_ - 1];
  }

  const value_type & back() const noexcept
  {
    return data_[size_ - 1];
  }

  iterator begin() noexcept
  {
    return iterator(data_);
  }

  iterator end() noexcept
  {
    return iterator(data_ + size_);
  }

  const_iterator cbegin() const noexcept
  {
    return iterator(data_);
  }

  const_iterator cend() const noexcept
  {
    return iterator(data_ + size_);
  }

protected:

  void copy(
      value_type *_from,
      size_type _count,
      value_type *_to,
      bool _revert = false,
      bool _move = true
    )
  {
    if (_count)
    {
      if (!_revert)
      {
        if (_move)
        {
          for (size_type i = 0; i < _count; ++i)
            *_to++ = std::move(*_from++);
        }
        else
        {
          for (size_type i = 0; i < _count; ++i)
            *_to++ = *_from++;
        }
      }
      else
      {
        if (_move)
        {
          for (size_type i = 0; i < _count; ++i)
            *_to-- = std::move(*_from--);
        }
        else
        {
          for (size_type i = 0; i < _count; ++i)
            *_to-- = *_from--;
        }
      }
    }
  }

  bool try_grow(
      size_type _new_size
    )
  {
    if (_new_size <= max_size())
    {
      if (_new_size > capa_)
      {
        const size_type new_capa = capa_ != 0 ? capa_ + capa_ / 2 : 16;
        if (new_capa > _new_size)
          _new_size = new_capa;
        value_type *new_buf = new value_type[_new_size];
        if (size_ > 0)
          copy(data_, size_, new_buf);
        delete[] data_;
        data_ = new_buf;
        capa_ = _new_size;
        return true;
      }
      else
        return false;
    }
    else
      throw std::out_of_range("Invalid new size");
  }

  size_type capa_;
  size_type size_;
  value_type * data_;
};

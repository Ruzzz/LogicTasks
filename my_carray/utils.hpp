#pragma once

#include <chrono>
#include <random>

template <typename T>
struct Rand
{
  Rand(
      T from,
      T to
    ) :
    e_(static_cast<unsigned int>(std::chrono::system_clock::now().time_since_epoch().count())),
    d_(from, to)
  {
  }

  T operator()()
  {
    return d_(e_);
  }

private:
  std::default_random_engine e_;
  std::uniform_int_distribution<T> d_;
};

template <typename T>
struct RandEx
{
  RandEx() :
    e_(static_cast<unsigned int>(std::chrono::system_clock::now().time_since_epoch().count()))
  {
  }

  T operator()(
      T from,
      T to
    )
  {
    std::uniform_int_distribution<T> d_(from, to);
    return d_(e_);
  }

private:
  std::default_random_engine e_;
};

template <typename String>
String gen_word(
    size_t size = 0
  )
{
  if (!size)
  {
    Rand<size_t> rand_word_size(3, 7);
    size = rand_word_size();
  }
  Rand<int> rand_aplha(static_cast<int>('a'), static_cast<int>('z'));
  String ret;
  for (size_t i = 0; i < size; ++i)
    ret.push_back(static_cast<typename String::value_type>(rand_aplha()));
  return ret;
}

template <typename T>
void print_array(
    const T & a
  )
{
  for (size_t i = 0, l = a.size(); i < l; ++i)
    std::cout << a[i] << ' ';
  std::cout << '\n';
}

template <typename T>
void print_strings(
    const T & a
  )
{
  for (size_t i = 0, l = a.size(); i < l; ++i)
    std::cout << a[i].c_str() << ' ';
  std::cout << '\n';
}
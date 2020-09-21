#ifdef _DEBUG
#ifdef _WIN32
#define _CRTDBG_MAP_ALLOC
#include <stdlib.h>
#include <crtdbg.h>
#endif
#endif

#include <algorithm>
#include <iostream>

#include "utils.hpp"
#include "carray.hpp"

void process_int()
{
  // Create
  Rand<int> rand_value(0, 100);
  CArray<int> a;
  for (size_t i = 0; i < 20; ++i)
    a.push_back(rand_value());
  print_array(a);

  // Sort
  std::sort(a.begin(), a.end());
  print_array(a);

  // Erase
  for (size_t i = 1; i < a.size(); ++i)
    a.erase(i);
  print_array(a);

  // Insert
  RandEx<size_t> rand_index;
  for (size_t i = 0; i < 10; ++i)
  {
    auto ins_val = rand_value();
    size_t pos = rand_index(0, a.size() - 1);
    std::cout << ins_val << " to " << pos << ": ";
    a.insert(pos, ins_val);
    print_array(a);
  }

  // Clear
  a.clear();
  print_array(a);
}

void process_str()
{
  // Create
  CArray<std::string> a;
  for (size_t i = 0; i < 15; ++i)
    a.push_back(gen_word<std::string>());
  print_strings(a);

  // Sort
  std::sort(a.begin(), a.end());
  print_strings(a);

  // Erase
  {
    size_t i = 0;
    while (i < a.size())
    {
      if (a[i].find_first_of("abcde") != std::string::npos)
        a.erase(i);
      else
        ++i;
    }
    print_strings(a);
  }

  // Insert
  RandEx<size_t> rand_index;
  for (size_t i = 0; i < 3; ++i)
  {
    std::string s = gen_word<std::string>();
    size_t pos = rand_index(0, a.size() - 1);
    std::cout << s.c_str() << " to " << pos << ": ";
    a.insert(pos, s);
    print_strings(a);
  }

  // Clear
  a.clear();
  print_strings(a);
}

int main()
{
#ifdef _DEBUG
#ifdef _WIN32
  _CrtSetDbgFlag(_CRTDBG_ALLOC_MEM_DF | _CRTDBG_LEAK_CHECK_DF);
#endif
#endif
  process_int();
  process_str();
  return 0;
}

#include <algorithm>
#include <iostream>
#include <exception>
#include <vector>
#include <unordered_map>

template <typename Int>
inline void check_range(Int value, Int from, Int to)
{
    if ((from > value) || (value > to))
        throw std::out_of_range("Out of range");
}

int main(int argc, char **argv)
{
    uint32_t n = 0, m = 0, k = 0, r = 0, c1 = 0, c2 = 0;

    std::cin >> n >> m >> k;
    check_range(n, 1u, 1000000000u);
    check_range(m, 1u, 1000000000u);
    check_range(k, 1u, 1000u);

    typedef std::pair<uint32_t, uint32_t> Range;
    typedef std::vector<Range> RowRails;
    std::unordered_map<uint32_t, RowRails> rails_map;

    uint64_t total = static_cast<uint64_t>(n) * static_cast<uint64_t>(m);

    for (size_t i = 1; i <= k; ++i)
    {
        std::cin >> r >> c1 >> c2;
        check_range(r, 1u, n);
        check_range(c1, 1u, m);
        check_range(c2, 1u, m);

        rails_map[r].push_back(std::make_pair(c1, c2));
    }

    for (auto &kv : rails_map)
    {
        auto &rails = kv.second;
        std::sort(rails.begin(), rails.end(), [](const Range &lhs, const Range &rhs)
        {
            return (lhs.first < rhs.first) || ((lhs.first == rhs.first) && (lhs.second < rhs.second));
        });

        RowRails norm_rails;
        auto it = rails.begin();
        norm_rails.push_back(*it);
        ++it;
        for (;it != rails.end(); ++it)
        {
            auto &norm_last = norm_rails.back();
            if (norm_last.first == it->first)
                norm_last.second = it->second;
            else if (norm_last.second >= it->second)
                continue;
            else if (norm_last.second + 1 >= it->first)
            {
                if (norm_last.second < it->second)
                    norm_last.second = it->second;
            }
            else
                norm_rails.push_back(*it);
        }

        for (const auto &p : norm_rails)
            total -= p.second - p.first + 1;
    }

    std::cout << total << '\n';
    return 0;
}

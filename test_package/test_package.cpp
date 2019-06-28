#include <iostream>
#include <samplerate.h>

int main()
{
    std::cout << src_get_version() << std::endl;
    for (int i = SRC_SINC_BEST_QUALITY; i <= SRC_LINEAR; ++i)
    {
        std::cout << src_get_name(i) << std::endl;
        std::cout << src_get_description(i) << std::endl;
    }
    return 0;
}

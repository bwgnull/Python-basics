
#include <iostream>
#include <string>

int main()
{
    std::string satellite = "LEO-7";
    int packets = 150;
    double latency = 42.5;

    std::cout << "Satellite: " << satellite << '\n';
    std::cout << "Packets: " << packets << '\n';
    std::cout << "Latency: " << latency << " ms\n";

    if (packets > 100)
    {
        std::cout << "High traffic detected.\n";
    }
    else
    {
        std::cout << "Traffic is normal.\n";
    }

    return 0;
}

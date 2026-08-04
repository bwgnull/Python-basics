#include <iostream>
#include <string>

int main()
{
    const int HIGH_TRAFFIC = 1000;

    const double EXCELLENT_LATENCY = 20.0;
    const double NORMAL_LATENCY = 50.0;
    const double POOR_LATENCY = 100.0;

    std::string satelliteName;
    std::string trafficStatus;
    std::string latencyStatus;

    int packets = 0;
    double latency = 0.0;
    double bandwidth = 0.0;
    double averageData = 0.0;

    std::cout << "Enter satellite name: ";
    std::getline(std::cin, satelliteName);

    std::cout << "Enter number of packets: ";
    std::cin >> packets;

    if (packets < 0)
    {
        std::cout << "Packet count cannot be negative.\n";
        return 1;
    }

    if (packets > HIGH_TRAFFIC)
    {
        trafficStatus = "High Traffic";
    }
    else
    {
        trafficStatus = "Normal Traffic";
    }

    std::cout << "Enter latency (ms): ";
    std::cin >> latency;

    if (latency < 0.0)
    {
        std::cout << "Latency cannot be negative.\n";
        return 1;
    }

    if (latency >= POOR_LATENCY)
    {
        latencyStatus = "Poor";
    }
    else if (latency > NORMAL_LATENCY)
    {
        latencyStatus = "Moderate";
    }
    else if (latency > EXCELLENT_LATENCY)
    {
        latencyStatus = "Normal";
    }
    else
    {
        latencyStatus = "Excellent";
    }

    std::cout << "Enter bandwidth (Mbps): ";
    std::cin >> bandwidth;

    if (bandwidth < 0.0)
    {
        std::cout << "Bandwidth cannot be negative.\n";
        return 1;
    }

    if (packets > 0)
    {
        averageData = bandwidth / packets;
    }

    std::cout << "\n----- Report -----\n";
    std::cout << "Satellite Name: " << satelliteName << '\n';
    std::cout << "Packets: " << packets << '\n';
    std::cout << "Latency: " << latency << " ms\n";
    std::cout << "Bandwidth: " << bandwidth << " Mbps\n";
    std::cout << "Average Data Per Packet: " << averageData << " Mbps\n";
    std::cout << "Traffic Status: " << trafficStatus << '\n';
    std::cout << "Latency Status: " << latencyStatus << '\n';

    return 0;
}
#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <algorithm>

int main() {
    std::map<std::string, std::vector<int>> gradebook = {
        {"alice",   {90, 85, 92}},
        {"bob",     {78, 88}},
        {"charlie", {95, 70, 80}},
    };

    std::map<std::string, int> averages;
    for (auto& [name, scores] : gradebook) {
        int sum = 0;
        for (int s : scores) sum += s;
        averages[name] = sum / scores.size();
    }

    std::vector<std::pair<std::string, int>> ranking_vector(averages.begin(), averages.end());

    std::sort(ranking_vector.begin(), ranking_vector.end(), [](const auto& a, const auto& b) {
        return a.second > b.second; // Sortare de la cea mai mare medie la cea mai mică
    });

    std::cout << "Rankings (Sorted by Average):" << std::endl;
    for (auto& [name, avg] : ranking_vector) {
        std::cout << "  " << name << ": " << avg << std::endl;
    }

    return 0;
}
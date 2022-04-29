#include <iostream>
#include <string>
#include <map>
#include <vector>

using namespace std;


struct deck {
    vector<string> cards_arr = {
        "ac","2c","3c","4c","5c","6c","7c","8c","9c","10c","jc","qc","kc",
        "as","2s","3s","4s","5s","6s","7s","8s","9s","10s","js","qs","ks",
        "ad","2d","3d","4d","5d","6d","7d","8d","9d","10d","jd","qd","kd",
        "ah","2h","3h","4h","5h","6h","7h","8h","9h","10h","jh","qh","kh",
    };

    map<string, int> cards_map {
        {"ac", 1},
        {"as", 2},
        {"ad", 3},
        {"ah", 4},
        {"2c", 5}, 
        {"2s", 6}, 
        {"2d", 7},
        {"2h", 8},
        {"3c", 9},
        {"3s", 10},
        {"3d", 11},
        {"3h", 12},
        {"4c", 13},
        {"4s", 14},
        {"4d", 15},
        {"4h", 16},
        {"5c", 17},
        {"5s", 18},
        {"5d", 19},
        {"5h", 20},
        {"6c", 21},
        {"6s", 22},
        {"6d", 23},
        {"6h", 24},
        {"7c", 25},
        {"7s", 26},
        {"7d", 27},
        {"7h", 28},
        {"8c", 29},
        {"8s", 30},
        {"8d", 31},
        {"8h", 32},
        {"9c", 33},
        {"9s", 34},
        {"9d", 35},
        {"9h", 36},
        {"10c", 37},
        {"10s", 38},
        {"10d", 39},
        {"10h", 40},
        {"jc", 41},
        {"js", 42},
        {"jd", 43},
        {"jh", 44},
        {"qc", 45},
        {"qs", 46},
        {"qd", 47},
        {"qh", 48},
        {"kc", 49},
        {"ks", 50},
        {"kd", 51},
        {"kh", 52}
    };
};

struct board {
    vector<string> cards; 
};

struct player {
    string card1, card2;
    string hand;
};

class Game {
public:
    Game();
    void start();
    void dealPlayers();
    void dealFlop();
    void printInfo();
private:
    deck game_deck;
    board game_board;
    player game_players[];

    void chooseCard();
};



int main() {

    return 0;
}
// 2023-09-21
// bj24290_마법사 상어와 복제
// 4시간 조금
// bfs, 중복순열(상어 루트) 
// bfs, 빡구현

#include <bits/stdc++.h>

#define MAX 5
#define X   first
#define Y   second

using namespace std;

struct fish {
    int x;
    int y;
    int dir;
};
 
int n = 4;
int m, s, max_eat;

int temp_route[3], route[3];

int smell[MAX][MAX];
vector<fish> fish_box[MAX][MAX], init_box[MAX][MAX];

pair<int, int> shark;
 
int fish_dx[] = {0, 0, -1, -1, -1, 0, 1, 1, 1};
int fish_dy[] = {0, -1, -1, 0, 1, 1, 1, 0, -1};
 
int shark_dx[] = {0, -1, 0, 1, 0};
int shark_dy[] = {0, 0, -1, 0, 1};
 
 
void input() 
{
    cin >> m >> s;
    for (int i = 0; i < m; i++) 
    {
        int x, y, d;
        cin >> x >> y >> d;
        x--; y--;
        fish f = { x, y, d };
        fish_box[x][y].push_back(f);
    }
    cin >> shark.X >> shark.Y;
    shark.X--; shark.Y--;
}
 
void copy_box(vector<fish> A[][MAX], vector<fish> B[][MAX]) 
{
    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < n; j++) {
            A[i][j] = B[i][j];
        }
    }
}
 
void init_copy() 
{
    copy_box(init_box, fish_box);
}
 
void fish_move() 
{
    vector<fish> temp_box[MAX][MAX];
 
    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < n; j++) 
        {
            for (int k = 0; k < fish_box[i][j].size(); k++) 
            {
                int x = fish_box[i][j][k].x;
                int y = fish_box[i][j][k].y;
                int dir = fish_box[i][j][k].dir;
                int nx = x;
                int ny = y;
                bool success = false;
                for (int l = 0; l < 8; l++) 
                {
                    nx = x + fish_dx[dir];
                    ny = y + fish_dy[dir];
                    if (nx >= 0 && ny >= 0 && nx < n && ny < n) 
                    {
                        if ((nx != shark.X || ny != shark.Y) && smell[nx][ny] == 0) 
                        {
                            success = true;
                            break;
                        }
                    }
                    dir--;
                    if (dir == 0) dir = 8;
                }
                if (success == true) 
                {
                    fish f = {nx, ny, dir};
                    temp_box[nx][ny].push_back(f);
                }
                else 
                {
                    fish f = { x, y, dir };
                    temp_box[x][y].push_back(f);
                }
            }
        }
    }
    copy_box(fish_box, temp_box);
}
 
int find_max_eat() 
{
    int visit[MAX][MAX] = {0,};
    int x = shark.X;
    int y = shark.Y;
    int eat = 0;
    for (int i = 0; i < 3; i++) 
    {
        int dir = temp_route[i];
        int nx = x + shark_dx[dir];
        int ny = y + shark_dy[dir];
        if (nx < 0 || ny < 0 || nx >= n || ny >= n) return -1;
        if (visit[nx][ny] == 0) 
        {
            visit[nx][ny] = 1;
            eat += fish_box[nx][ny].size();
        }
        x = nx;
        y = ny;
    }
    return eat;
}
 
void find_route(int cnt) 
{
    if (cnt == 3) {
        int eatNum = find_max_eat();
        if (eatNum > max_eat) 
        {
            for (int i = 0; i < 3; i++) 
                route[i] = temp_route[i];
            max_eat = eatNum;
        }
        return;
    }
 
    for (int i = 1; i <= 4; i++) 
    {
        temp_route[cnt] = i;
        find_route(cnt + 1);
    }
}
 
void shark_move(int time) 
{
    vector<fish> temp_box[MAX][MAX];
    copy_box(temp_box, fish_box);
 
    int x = shark.X;
    int y = shark.Y;
    for (int i = 0; i < 3; i++) 
    {
        int dir = route[i];
        int nx = x + shark_dx[dir];
        int ny = y + shark_dy[dir];
        if (temp_box[nx][ny].size() != 0) 
        {
            smell[nx][ny] = time;
            temp_box[nx][ny].clear();
        }
        x = nx;
        y = ny;
        shark.X = x;
        shark.Y = y;
    }
    copy_box(fish_box, temp_box);
}
 
void shark_func(int time) 
{
    max_eat = -1;
    find_route(0);
    shark_move(time);
}
 
void smell_remove(int time) 
{
    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < n; j++) 
        {
            if (smell[i][j] == 0) continue;
            if (time - smell[i][j] == 2)
                smell[i][j] = 0;
        }
    }
}
 
void fish_generate() 
{
    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < n; j++) 
        {
            for (int k = 0; k < init_box[i][j].size(); k++) 
                fish_box[i][j].push_back(init_box[i][j][k]);
        }
    }
}
 
int find_ans() 
{
    int ret = 0;
    for (int i = 0; i < n; i++) 
    {
        for (int j = 0; j < n; j++) 
            ret += fish_box[i][j].size();
    }
    return ret;
}
 
void solution() 
{
    for (int i = 1; i <= s; i++) 
    {
        init_copy();
        fish_move();
        shark_func(i);
        smell_remove(i);
        fish_generate();
    }
    cout << find_ans() << endl;
}
 
int main(void) 
{
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
    
    input();
    solution();
 
    return 0;
}

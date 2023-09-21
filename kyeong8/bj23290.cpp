// 2023-09-21 
// bj23290_마법사 상어와 복제    
// 5시간 30분 (화가 매우 납니다~ 변수 이름 잘못 기입하기도 하고 이동 불가능 잘못 계산하기도 하고)
// 백트래킹 및 조건 따라가기
// 구현, 시뮬레이션
// vector, 우선순위 큐

#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <cstring>
#include <queue>
#include <vector>
#include <cmath>

using namespace std;

struct Pos {
	int row;
	int col;
};

int erow[8] = { 0, -1, -1, -1, 0, 1, 1, 1 };
int ecol[8] = { -1, -1, 0, 1, 1, 1, 0, -1 };

int frow[4] = { -1, 0, 1, 0 };
int fcol[4] = { 0, -1, 0, 1 };

struct cmp {
	bool operator() (pair<int, int> a, pair<int, int> b)
	{
		if (a.first < b.first)
			return true;
		else if (a.first == b.first)
		{
			if (a.second > b.second)
				return true;
			else
				return false;
		}
		else
			return false;
	}
};

int main()
{
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);

	freopen("input.txt", "r", stdin);

	vector<int> map[5][5];
	int fishCnt[5][5] = { 0 };

	vector<int> mem[5][5];
	int memCnt[5][5] = { 0 };

	int smell[5][5] = { 0 };

	Pos shark;
	int answer = 0;

	int M, S;
	cin >> M >> S;

	int x, y, d;
	for (int i = 0; i < M; i++)
	{
		cin >> x >> y >> d;
		map[x][y].push_back(d);
		++fishCnt[x][y];
	}

	cin >> x >> y;
	shark = Pos{ x, y };

	for (int prac = 0; prac < S; prac++)
	{
		answer = 0;
		// 1. 상어가 모든 물고기에게 복제 마법을 시전한다.
		for (int i = 1; i <= 4; i++)
		{
			for (int j = 1; j <= 4; j++)
			{
				for (int k = 0; k < fishCnt[i][j]; k++)
					mem[i][j].push_back(map[i][j][k]);
				memCnt[i][j] = fishCnt[i][j];
			}
		}

		// 2. 모든 물고기가 한 칸 이동한다. 상어가 있는 칸, 물고기의 냄새가 있는 칸, 격자의 범위를 벗어나는 칸으로는 이동할 수 없다. 
		queue<pair<Pos, int>> q;

		for (int i = 1; i <= 4; i++)
		{
			for (int j = 1; j <= 4; j++)
			{
				int del = 0;
				int cnt = fishCnt[i][j];
				if (cnt == 0)
					continue;

				for (int k = 0; k < cnt; k++)
				{
					// 이동할 수 있는 칸을 향할 때까지 방향을 45도 반시계 회전시킨다.
					int direct = map[i][j][k];
					int escape = 0;

					while (true)
					{
						++escape;
						if (escape == 9)
							break;
						int nrow = i + erow[direct - 1];
						int ncol = j + ecol[direct - 1];

						if (1 <= nrow && nrow <= 4 && 1 <= ncol && ncol <= 4)
						{
							if (smell[nrow][ncol] == 0 && (nrow != shark.row || ncol != shark.col))
							{		
								q.push(make_pair(Pos{ nrow, ncol }, direct));
								break;
							}
						}
						//  ←, ↖, ↑, ↗, →, ↘, ↓, ↙ 
						if (direct == 1)
							direct = 8;
						else
							direct -= 1;
					}

					if (escape == 9)
					{
						q.push(make_pair(Pos{ i, j }, direct));
					}
				}
			}
		}

		for (int i = 1; i <= 4; i++)
		{
			for (int j = 1; j <= 4; j++)
			{
				map[i][j].clear();
				fishCnt[i][j] = 0;
			}
		}

		while(!q.empty())
		{
			int row = q.front().first.row;
			int col = q.front().first.col;
			int d = q.front().second;
			map[row][col].push_back(d);
			++fishCnt[row][col];
			q.pop();
		}

		// 3. 가능한 이동 방법 중에서 제외되는 물고기의 수가 가장 많은 방법으로 이동하며, 그러한 방법이 여러가지인 경우 사전 순으로 가장 앞서는 방법을 이용한다. 
		priority_queue<pair<int, int>, vector<pair<int, int>>, cmp> pq;

		for (int i = 0; i < 4; i++)
		{
			for (int j = 0; j < 4; j++)
			{
				for (int k = 0; k < 4; k++)
				{
					vector<pair<Pos, int>> back;

					int value = 100 * (i + 1) + 10 * (j + 1) + k + 1;
					int eat = 0;

					int nrow = shark.row + frow[i];
					int ncol = shark.col + fcol[i];

					if (1 > nrow || nrow > 4 || 1 > ncol || ncol > 4)
						continue;

					back.push_back(make_pair(Pos{ nrow, ncol }, fishCnt[nrow][ncol]));
					eat += fishCnt[nrow][ncol];
					fishCnt[nrow][ncol] = 0;

					nrow += frow[j];
					ncol += fcol[j];

					if (1 > nrow || nrow > 4 || 1 > ncol || ncol > 4)
					{
						for (auto b : back)
							fishCnt[b.first.row][b.first.col] = b.second;
						continue;
					}
						
					back.push_back(make_pair(Pos{ nrow, ncol }, fishCnt[nrow][ncol]));
					eat += fishCnt[nrow][ncol];
					fishCnt[nrow][ncol] = 0;

					nrow += frow[k];
					ncol += fcol[k];

					if (1 > nrow || nrow > 4 || 1 > ncol || ncol > 4)
					{
						for (auto b : back)
							fishCnt[b.first.row][b.first.col] = b.second;
						continue;
					}
						
					//back.push_back(make_pair(Pos{ nrow, ncol }, fishCnt[nrow][ncol]));
					eat += fishCnt[nrow][ncol];
					//fishCnt[nrow][ncol] = 0;

					pq.push(make_pair(eat, value));

					for (auto b : back)
						fishCnt[b.first.row][b.first.col] = b.second;
				}
			}
		}

		int path = pq.top().second;
		//cout << "path: " << path << "\n";

		// 3. 그 칸에 있는 모든 물고기는 격자에서 제외되며, 물고기 냄새를 남긴다.
		for (int i = 2; i >= 0; i--)
		{
			int div = pow(10, i);
			int row = shark.row + frow[path / div - 1];
			int col = shark.col + fcol[path / div - 1];
			path = path % div;

			if (fishCnt[row][col] > 0)
			{
				smell[row][col] = 3;
				map[row][col].clear();
				fishCnt[row][col] = 0;
			}

			shark.row = row;
			shark.col = col;
		}

		for (int i = 1; i <= 4; i++)
		{
			for (int j = 1; j <= 4; j++)
			{
				// 4. 두 번 전 연습에서 생긴 물고기의 냄새가 격자에서 사라진다.
				if (smell[i][j] > 0)
					--smell[i][j];

				// 5. 1에서 사용한 복제 마법이 완료된다. 모든 복제된 물고기는 1에서의 위치와 방향을 그대로 갖게 된다.
				for (int k = 0; k < memCnt[i][j]; k++)
					map[i][j].push_back(mem[i][j][k]);

				fishCnt[i][j] += memCnt[i][j];
				answer += fishCnt[i][j];
			}
		}

		//for (int i = 1; i <= 4; i++)
		//{
		//	for (int j = 1; j <= 4; j++)
		//	{
		//		cout << fishCnt[i][j] << " ";
		//	}
		//	cout << "\n";
		//}
		//cout << "\n";

		for (int i = 1; i <= 4; i++)
		{
			for (int j = 1; j <= 4; j++)
			{
				mem[i][j].clear();
				memCnt[i][j] = 0;
			}
		}
	}

	cout << answer << "\n";
}

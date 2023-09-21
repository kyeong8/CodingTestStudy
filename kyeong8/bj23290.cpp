// 2023-09-21 
// bj23290_������ ���� ����    
// 5�ð� 30�� (ȭ�� �ſ� ���ϴ�~ ���� �̸� �߸� �����ϱ⵵ �ϰ� �̵� �Ұ��� �߸� ����ϱ⵵ �ϰ�)
// ��Ʈ��ŷ �� ���� ���󰡱�
// ����, �ùķ��̼�
// vector, �켱���� ť

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
		// 1. �� ��� ����⿡�� ���� ������ �����Ѵ�.
		for (int i = 1; i <= 4; i++)
		{
			for (int j = 1; j <= 4; j++)
			{
				for (int k = 0; k < fishCnt[i][j]; k++)
					mem[i][j].push_back(map[i][j][k]);
				memCnt[i][j] = fishCnt[i][j];
			}
		}

		// 2. ��� ����Ⱑ �� ĭ �̵��Ѵ�. �� �ִ� ĭ, ������� ������ �ִ� ĭ, ������ ������ ����� ĭ���δ� �̵��� �� ����. 
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
					// �̵��� �� �ִ� ĭ�� ���� ������ ������ 45�� �ݽð� ȸ����Ų��.
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
						//  ��, ��, ��, ��, ��, ��, ��, �� 
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

		// 3. ������ �̵� ��� �߿��� ���ܵǴ� ������� ���� ���� ���� ������� �̵��ϸ�, �׷��� ����� ���������� ��� ���� ������ ���� �ռ��� ����� �̿��Ѵ�. 
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

		// 3. �� ĭ�� �ִ� ��� ������ ���ڿ��� ���ܵǸ�, ����� ������ �����.
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
				// 4. �� �� �� �������� ���� ������� ������ ���ڿ��� �������.
				if (smell[i][j] > 0)
					--smell[i][j];

				// 5. 1���� ����� ���� ������ �Ϸ�ȴ�. ��� ������ ������ 1������ ��ġ�� ������ �״�� ���� �ȴ�.
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

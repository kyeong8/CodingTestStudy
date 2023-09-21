// 2023-09-20  
// bj23291_어항정리    
// 3시간 5분  
// 문제 조건을 따라가며 직사각형 배열 회전 및 시뮬레이션
// 구현, 시뮬레이션, 회전
// vector, linked list

#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <vector>
#include <cstring>

using namespace std;

int map[100][100] = { 0 };
int N, K;

bool visited[100][100] = { false };

int r[4] = { -1, 1, 0, 0 };
int c[4] = { 0, 0, -1, 1 };

void bfs(int prevRow, int index)
{
	memset(visited, false, sizeof(visited));

	int mem[100][100] = { 0 };


	for (int a = 0; a < prevRow + 1; a++)
	{
		for (int b = index; b < N; b++)
		{
			if (map[a][b] != 0)
			{
				for (int i = 0; i < 4; i++)
				{
					int nrow = a + r[i];
					int ncol = b + c[i];

					if (0 <= nrow && nrow < N && 0 <= ncol && ncol < N)
					{
						if (!visited[nrow][ncol] && map[nrow][ncol] != 0 && abs(map[nrow][ncol] - map[a][b]) >= 5)
						{
							int value = abs(map[nrow][ncol] - map[a][b]);
							if (map[nrow][ncol] > map[a][b])
							{
								mem[nrow][ncol] -= value / 5;
								mem[a][b] += value / 5;
							}
							else
							{
								mem[nrow][ncol] += value / 5;
								mem[a][b] -= value / 5;
							}
						}
					}
				}

				visited[a][b] = true;
			}
		}
	}


	for (int a = 0; a < prevRow + 1; a++)
	{
		for (int b = index; b < N; b++)
		{
			map[a][b] += mem[a][b];
		}
	}

}

void printArray()
{
	for (int i = 5; i >= 0; i--)
	{
		for (int j = 0; j < N; j++)
		{
			cout << map[i][j] << " ";
		}
		cout << "\n";
	}
	cout << "\n";
}

int main()
{
	ios_base::sync_with_stdio(false);
	cin.tie(NULL);
	cout.tie(NULL);

	freopen("input.txt", "r", stdin);

	int index;
	int answer = 0;

	vector<pair<int, int>> small;
	cin >> N >> K;

	for (int i = 0; i < N; i++)
		cin >> map[0][i];


	while (true)
	{
		int maxNum = 0;
		int minNum = 10001;
		// 물고기가 가장 적은 어항의 위치와 물고기 수의 차이를 구하는 과정
		for (int i = 0; i < N; i++)
		{
			maxNum = max(maxNum, map[0][i]);

			if (minNum == map[0][i])
				small.push_back(make_pair(0, i));
			else if (minNum > map[0][i])
			{
				minNum = map[0][i];
				small.clear();
				small.push_back(make_pair(0, i));
			}
		}

		if (maxNum - minNum <= K)
			break;

		++answer;

		// 물고기의 수가 가장 적은 어항에 물고기를 한 마리 넣는다.
		for (auto i : small)
			++map[i.first][i.second];

		// 먼저, 가장 왼쪽에 있는 어항을 그 어항의 오른쪽에 있는 어항의 위에 올려 놓는다.
		map[1][1] = map[0][0];
		map[0][0] = 0;
		index = 1;

		//printArray();

		// 2개 이상 쌓여있는 어항을 모두 공중 부양시킨 다음, 전체를 시계방향으로 90도 회전시킨다

		int row;
		int col;

		while (true)
		{
			row = 0;
			col = 0;

			for (int i = index; i < N; i++)
			{
				if (map[1][i] != 0)
					++col;
				else
					break;
				//cout << "map[1][i]: " << map[1][i] << "\n";
				//cout << "col: " << col << "\n";
			}

			for (int i = 0; i < N; i++)
			{
				if (map[i][index] != 0)
					++row;
				else
					break;
			}

			if (row + index + col > N)
				break;

			//cout << "row: " << row << " col: " << col << "\n\n";

			for (int i = 0; i < row; i++)
			{
				for (int j = index; j < col + index; j++)
				{
					map[col + index - j][index + i + col] = map[i][j];
					map[i][j] = 0;
				}
			}

			//printArray();

			index += col;
		}

		bfs(row, index);

		//printArray();

		//cout << "index: " << index << " row: " << row << " col: " << col << "\n";
		for (int i = 0; i < col; i++)
		{
			for (int j = 0; j < row; j++)
			{
				map[0][i * row + j] = map[j][index + i];
				map[j][index + i] = 0;
			}
		}

		//printArray();

		// 첫번째 접기
		for (int i = 0; i < N / 2; i++)
		{
			map[1][N - 1 - i] = map[0][i];
			map[0][i] = 0;
		}

		//printArray();

		// 두번째 접기
		for (int i = 0; i < 2; i++)
		{
			for (int j = 0; j < N / 4; j++)
			{
				map[3 - i][N - 1 - j] = map[i][j + N / 2];
				map[i][j + N / 2] = 0;
			}
		}

		//printArray();

		bfs(4, N - N / 4 - 1);

		for (int i = 0; i < N / 4; i++)
		{
			for (int j = 0; j < 4; j++)
			{
				map[0][i * 4 + j] = map[j][N - N / 4 + i];
				map[j][N - N / 4 + i] = 0;
			}
		}

		//printArray();

		//cout << "answer: " << answer << "\n\n";
	}

	cout << answer << "\n";

	// (0, 0), (1, 0) -> (1, 0), (1, 1)

	// j -> row = j, i -> col = N - j - 1  [-90]
	// row = N - j - 1, col = i             [90]
	// (0, 1), (1, 1) -> (1, 2) (1, 3)
	// (0, 2), (0, 3), (1, 2), (1, 3) -> 


	// 물고기 수의 차이가 K이하이면 종료
	//if (maxNum - minNum >= K)
	//	cout << answer << "\n";
}
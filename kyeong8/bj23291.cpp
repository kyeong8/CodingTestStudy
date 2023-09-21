// 2023-09-20  
// bj23291_��������    
// 3�ð� 5��  
// ���� ������ ���󰡸� ���簢�� �迭 ȸ�� �� �ùķ��̼�
// ����, �ùķ��̼�, ȸ��
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
		// ����Ⱑ ���� ���� ������ ��ġ�� ����� ���� ���̸� ���ϴ� ����
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

		// ������� ���� ���� ���� ���׿� ����⸦ �� ���� �ִ´�.
		for (auto i : small)
			++map[i.first][i.second];

		// ����, ���� ���ʿ� �ִ� ������ �� ������ �����ʿ� �ִ� ������ ���� �÷� ���´�.
		map[1][1] = map[0][0];
		map[0][0] = 0;
		index = 1;

		//printArray();

		// 2�� �̻� �׿��ִ� ������ ��� ���� �ξ��Ų ����, ��ü�� �ð�������� 90�� ȸ����Ų��

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

		// ù��° ����
		for (int i = 0; i < N / 2; i++)
		{
			map[1][N - 1 - i] = map[0][i];
			map[0][i] = 0;
		}

		//printArray();

		// �ι�° ����
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


	// ����� ���� ���̰� K�����̸� ����
	//if (maxNum - minNum >= K)
	//	cout << answer << "\n";
}
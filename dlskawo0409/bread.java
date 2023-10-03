import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.LinkedList;
import java.util.Queue;
import java.util.StringTokenizer;

class pairInBread{
	int row;
	int col;
	pairInBread(int row, int col){
		this.row = row;
		this.col = col;
	}
	
	public int getRow() {
		return row;
	}
	
	public int getCol() {
		return col;
	}
	
}

class Human{
	int row = -1;
	int col = -1;
	boolean arrived = false;
	
	int destRow;
	int destCol;
	
	Human(int destRow, int destCol){
		this.destRow = destRow;
		this.destCol = destCol;
	}
	
	public void updateLocation(int row, int col) {
		this.row = row;
		this.col = col;
	}
	
	public boolean getArraived() {
		return arrived;
	}
	
	public void updateArraived() {
		arrived = true;
	}
	
	public int getDestRow() {
		return destRow;
	}
	
	public int getDestCol() {
		return destCol;
	}
	
	public int getRow() {
		return row;
	}
	
	public int getCol() {
		return col;
	}
}

public class Main {
	int N;
	int M;
	int Map[][];
	Human[] humanList;
	
	int INF = Integer.MAX_VALUE;
	
	int rowAppend[] = {-1, 0, 0, 1}; //상 좌 우 하
	int colAppend[] = { 0, -1, 1, 0};
	
	
	public void solution() throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st = new StringTokenizer(br.readLine());
		
		N = Integer.parseInt(st.nextToken());
		M = Integer.parseInt(st.nextToken());
		
		Map = new int [N+1][N+1];
		
		humanList = new Human[M];
		
		for(int i = 1; i <N+1; i++) {
			st = new StringTokenizer(br.readLine());
			for(int j = 1; j<N+1; j++) {
				Map[i][j] = Integer.parseInt(st.nextToken());
			}
		}
		
		for(int i = 0; i<M; i++) {
			st = new StringTokenizer(br.readLine());
			humanList[i] = new Human(Integer.parseInt(st.nextToken()), Integer.parseInt(st.nextToken()));
		}
		int t = 0;
		while(!allArrived()) {
			moveHuman();
			if(t < M) {
				getBaseCamp(humanList[t]);
			}
			t+=1;
		}
		System.out.println(t);
		
	}
	
	protected boolean allArrived() {
		for(Human now : humanList) {
			if(!now.getArraived()) {
				return false;
			}
		}
		return true;
	}
	
	protected void moveHuman() {
		for (Human now : humanList) {
			if(now.getRow() == -1 || now.getCol() == -1 || now.getArraived() ) {
//				System.out.println("continue");
				continue;
			}
			int distance = INF;
			int newRow = now.getRow();
			int newCol = now.getCol();
			for(int i = 0; i<4; i++) {
				int tempRow = now.getRow() + rowAppend[i];
				int tempCol = now.getCol() + colAppend[i];
				
				if(isInMap(tempRow, tempCol) && Map[tempRow][tempCol] != -1) {
					int tempDist = Math.abs(now.getDestRow() - tempRow) + Math.abs(now.getDestCol() - tempCol);
					
					if(tempDist < distance) {
						distance = tempDist;
						newRow = tempRow;
						newCol = tempCol;
					}
				}
			}
			if(newRow == now.getDestRow() && newCol == now.getDestCol()) {
				now.updateArraived();
				Map[newRow][newCol] = -1;
			}
			now.updateLocation(newRow, newCol);
		}
	}
	
	protected void getBaseCamp(Human human) {
		int destRow = human.getDestRow();
		int destCol = human.getDestCol();
	
		
		boolean visited[][] = new boolean [N+1][N+1];
		
		Queue<pairInBread> q = new LinkedList<pairInBread>();
		q.add(new pairInBread(destRow, destCol));
		while(!q.isEmpty()) {
			pairInBread now = q.poll();
			for(int i = 0; i <4 ;i++) {
				int tempRow = now.getRow() + rowAppend[i];
				int tempCol = now.getCol() + colAppend[i];
				
				if(isInMap(tempRow, tempCol) && Map[tempRow][tempCol] != -1 && visited[tempRow][tempCol] == false) {
					visited[tempRow][tempCol] = true;
					if(Map[tempRow][tempCol] == 1) {
//						System.out.println("set startRow :" + tempRow +" start Col : "+ tempCol);
						human.updateLocation(tempRow, tempCol);
						Map[tempRow][tempCol] = -1;
						return;
					}
					
					q.add(new pairInBread(tempRow, tempCol));
				}
			}
		}
	}
	
	protected boolean isInMap(int row, int col) {
		if(1<=row && row <= N && 1 <= col && col <= N) {
			return true;
		}
		return false;
	}
	
	public static void main(String[]args) throws IOException {
		new Main().solution();
	}
}
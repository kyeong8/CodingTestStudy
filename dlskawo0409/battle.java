import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.StringTokenizer;


class pairInBattle{
	int row;
	int col;
	
	pairInBattle(int row, int col){
		this.row = row;
		this.col = col;
	}
	
}

class HumanInBattle{
	int row;
	int col;
	int d;
	int s;
	int point = 0;
	int gun = 0;
	
	HumanInBattle(int row, int col, int d, int s){
		this.row = row;
		this.col = col;
		this.d = d;
		this.s = s;
	}
	
	public void updatePoint(int point) {
		this.point += point;
	}
	
	public int changeGun(int gun) {
		int temp = this.gun;
		this.gun = gun;
		return temp;
	}
	
	public void updateDirection() {
		d = d+2 >= 4 ? d+2 - 4 : d+2;
	}
	public void rotateDirection() {
		d = d+1 >= 4 ? 0 : d+1;
	}
	public int getRow() {
		return row;
	}
	
	public int getCol() {
		return col;
	}
	public void updateLocation(int row, int col) {
		this.row = row;
		this.col = col;
	}
}


public class Main {
	int N;
	int M;
	int K;
	
	PriorityQueue<Integer> Gun [][];
	
	HumanInBattle[] HumanList;
	
	int[] rowAppend = {-1, 0, 1, 0}; // 상 우 하 좌
	int[] colAppend = {0, 1, 0, -1};
	
	public void solution() throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringTokenizer st = new StringTokenizer(br.readLine());
		
		N = Integer.parseInt(st.nextToken());
		M = Integer.parseInt(st.nextToken());
		K = Integer.parseInt(st.nextToken());
		
		Gun = new PriorityQueue[N+1][N+1];
		HumanList = new HumanInBattle[M];
		
		for(int i = 1; i<=N ;i ++) {
			st = new StringTokenizer(br.readLine());
			for(int j = 1; j<= N; j++) {
				Gun[i][j] = new PriorityQueue<>(Collections.reverseOrder());
				Gun[i][j].add(Integer.parseInt(st.nextToken()));
			}
		}
		
		for(int i = 0; i<M; i++) {
			st = new StringTokenizer(br.readLine());
			int row = Integer.parseInt(st.nextToken());
			int col = Integer.parseInt(st.nextToken());
			int d = Integer.parseInt(st.nextToken());
			int s = Integer.parseInt(st.nextToken());
			
			HumanList[i] = new HumanInBattle(row, col, d ,s);
		}
		
		
		for(int k = 0; k<K; k++) {
			simulation();
		}
		for(HumanInBattle now : HumanList) {
			System.out.print(now.point+" ");
		}
		
	}
	
	protected void simulation() {
		for(HumanInBattle now : HumanList) {
			humanMove(now);
		}
	}
	
	protected void humanMove(HumanInBattle now) {
		int row = now.getRow() + rowAppend[now.d];
		int col = now.getCol() + colAppend[now.d];
		
		if(!isInMap(row,col)) {
			now.updateDirection();
			row = now.getRow() + rowAppend[now.d];
			col = now.getCol() + colAppend[now.d];
		}
		int battlePepole = checkAnother(row,col);
		now.updateLocation(row, col);
		if(battlePepole != -1) {
			battle(now, HumanList[battlePepole]);
		}
		else {
			updateGun(now);
		}
	}
	
	protected boolean isInMap(int row, int col) {
		if(0 < row && row <= N && 0 < col && col <=N) {
			return true;
		}
		return false;
	}
	
	protected int checkAnother(int row, int col) {
		
		for(int i =0; i<HumanList.length; i++) {
			HumanInBattle now = HumanList[i];
			int tempRow = now.getRow();
			int tempCol = now.getCol();
			
			if(tempRow == row && tempCol == col) {
				return i;
			}
		}
		return -1;
	}
	
	protected void battle(HumanInBattle now, HumanInBattle attacked) {
		int nowDamage = now.s + now.gun;
		int attackedDamage = attacked.s + attacked.gun;
		int difference = Math.abs(nowDamage - attackedDamage);
		
		HumanInBattle winner;
		HumanInBattle loser;
		
		if(nowDamage > attackedDamage) {
			now.updatePoint(difference);
			loser = attacked;
			winner = now;
		}
		else if (nowDamage == attackedDamage) {
			if(now.s > attacked.s) {
				now.updatePoint(difference);
				loser = attacked;
				winner = now;
			}
			else {
				attacked.updatePoint(difference);
				loser = now;
				winner = attacked;
			}
		}
		else {
			attacked.updatePoint(difference);
			loser = now;
			winner = attacked;
		}
		lose(loser);
		win(winner);
		
		
	}
	
	protected void lose(HumanInBattle loser) {
		if(loser.gun != 0) {
			Gun[loser.getRow()][loser.getCol()].add(loser.gun);
		}
		
		loser.gun = 0;
		int tempRow = loser.getRow() + rowAppend[loser.d];
		int tempCol = loser.getCol() + colAppend[loser.d];
		
		while(!(isInMap(tempRow,tempCol) && checkAnother(tempRow, tempCol)== -1)) {
			loser.rotateDirection();;
			tempRow = loser.getRow() + rowAppend[loser.d];
			tempCol = loser.getCol() + colAppend[loser.d];
		}
		
		loser.updateLocation(tempRow, tempCol);
		
		if(!Gun[loser.getRow()][loser.getCol()].isEmpty()) { // 새로운 자리에 총이 있을 경우
			loser.gun = Gun[loser.getRow()][loser.getCol()].poll(); // 총 습득
		}
		
	}
	
	protected void win(HumanInBattle winner) {
		updateGun(winner);
	}
	
	protected void updateGun(HumanInBattle human) {
		if(human.gun != 0) {
			Gun[human.getRow()][human.getCol()].add(human.gun);
		}
		if(!Gun[human.getRow()][human.getCol()].isEmpty()) { // 새로운 자리에 총이 있을 경우
			human.gun = Gun[human.getRow()][human.getCol()].poll(); // 총 습득
		}
	}
	
	
	public static void main (String [] args) throws IOException {
		new Main().solution();
	}
}
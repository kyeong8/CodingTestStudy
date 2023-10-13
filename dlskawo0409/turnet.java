package codeTree;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.LinkedList;
import java.util.Queue;
import java.util.StringTokenizer;

import javax.swing.RowFilter.ComparisonType;

class pairInTurnet{
   int row;
   int col;
   
   pairInTurnet(int row, int col) {
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


public class turnet {
   int INF = Integer.MAX_VALUE;
   int N;
   int M;
   int K;
   
   int [][] attackPowerMap;
   int [][] attackTimeMap;
   int min = INF;
   boolean [][] attacked;
   
   
   int rowAppend[] = {0, 1, 0, -1}; // 우/하/좌/상
   int colAppend[] = {1, 0, -1, 0};
   
   int shellRow[] = {0, -1, -1, -1, 0, 1, 1, 1}; //좌 좌상 상 우상 우 우하 하 좌하
   int shellCol[] = {-1, -1, 0, 1, 1, 1, 0, -1};
   
   pairInTurnet [][] visited;
   LinkedList<pairInTurnet> visitedLocation  = new LinkedList<>();
   

   
   public void solution() throws IOException {
      BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
      StringTokenizer st = new StringTokenizer(br.readLine());
      N = Integer.parseInt(st.nextToken());
      M = Integer.parseInt(st.nextToken());
      K = Integer.parseInt(st.nextToken());
      
      attackPowerMap = new int[N+1][M+1];
      attackTimeMap = new int[N+1][M+1];
      attacked = new boolean [N+1][M+1];
      visited = new pairInTurnet [N+1][M+1];
      
      for(int i = 1; i<=N; i++) {
         st = new StringTokenizer(br.readLine());
         for(int j =1; j<=M; j++) {
            attackPowerMap[i][j] = Integer.parseInt(st.nextToken());
         }
      }
      
      attackTimeMap[0][0] = Integer.MIN_VALUE;
      attackTimeMap[0][1] = INF;
      
      for(int k = 1; k <= K; k++) {
         pairInTurnet attacker = getAttacker();
//         System.out.println();
//         System.out.println("attacker Row :" + attacker.getRow() +" attacker Col :" + attacker.getCol());
         pairInTurnet target = getTarget();
//         System.out.println("target Row :" + target.getRow() +" target Col :" + target.getCol());
         if(attacker.getRow() == target.getRow() && attacker.getCol() == target.getCol()) {
        	 break;
         }
         
         
         upgrageAttack(attacker);
         if(!laser(attacker, target)) {
            shell(attacker, target);
         }
         attackTimeMap[attacker.getRow()][attacker.getCol()] = k;
         
//         for(int i = 1; i<=N; i++) {
//        	 for(int j = 1; j<= M; j++) {
//        		 System.out.print(attackPowerMap[i][j] + " ");
//        	 }
//        	 System.out.println();
//         }

         repair();
         visited = new pairInTurnet [N+1][M+1];
//         System.out.println();
//         System.out.println("repair");
//         for(int i = 1; i<=N; i++) {
//        	 for(int j = 1; j<= M; j++) {
//        		 System.out.print(attackPowerMap[i][j] + " ");
//        	 }
//        	 System.out.println();
//         }
      }
      getMax();
      
   }
   protected pairInTurnet getAttacker() {
      int attack = INF;
      pairInTurnet returnPair = new pairInTurnet(0, 0);
      for(int i= 1; i<=N; i++) {
         for(int j = 1; j<=M; j++) {
            if(attackPowerMap[i][j] !=0 && attackPowerMap[i][j] < attack) { // 공격력이 낮은 걸 찾음
               attack = attackPowerMap[i][j];
               returnPair = new pairInTurnet(i,j);
            }
            else if(attackPowerMap[i][j] !=0 && attackPowerMap[i][j] == attack) {
               if(attackTimeMap[i][j] > attackTimeMap[returnPair.getRow()][returnPair.getCol()]) { // 공격력이 같으면 가장 최근에 공격한 포탑
                  attack = attackPowerMap[i][j];
                  returnPair = new pairInTurnet(i,j);
               }
               else if(attackTimeMap[i][j] == attackTimeMap[returnPair.getRow()][returnPair.getCol()]) {//공격력, 최근에 공격한 포탑이 같으면 합
                  if(i+j > returnPair.getRow() + returnPair.getCol()) {
                     attack = attackPowerMap[i][j];
                     returnPair = new pairInTurnet(i, j);
                  }
                  else if (i+j == returnPair.getRow() + returnPair.getCol() && returnPair.getCol() < j) {//공격력, 최근에 공격한 포탑, 합까지 같으면
                     attack = attackPowerMap[i][j];
                     returnPair = new pairInTurnet(i, j);
                  }
               }
            }
         }
      }
      attacked[returnPair.getRow()][returnPair.getCol()] = true;
      return returnPair;
   }
   protected void upgrageAttack(pairInTurnet attacker) {
      attackPowerMap[attacker.getRow()][attacker.getCol()] += (N+M);
   }
   
   protected pairInTurnet getTarget() {
      int attack = -1;
      pairInTurnet returnPair = new pairInTurnet(0, 1);
      for(int i = 1; i<=N; i++) {
         for(int j = 1; j<=M;j++) {
            if(attackPowerMap[i][j] !=0 && attackPowerMap[i][j] > attack) {
//            	System.out.println(" target update :" +attackPowerMap[i][j]);
               attack = attackPowerMap[i][j];
               returnPair = new pairInTurnet(i,j);
            }
            else if( attackPowerMap[i][j] !=0 && attackPowerMap[i][j] == attack) {
               if(attackTimeMap[i][j] < attackTimeMap[returnPair.getRow()][returnPair.getCol()]) { // 공격력이 같으면 가장 최근에 공격한 포탑
                  attack = attackPowerMap[i][j];
                  returnPair = new pairInTurnet(i,j);
               }
               else if(attackTimeMap[i][j] == attackTimeMap[returnPair.getRow()][returnPair.getCol()]) {//공격력, 최근에 공격한 포탑이 같으면 합
                  if(i+j  < returnPair.getRow() + returnPair.getCol()) {
                     attack = attackPowerMap[i][j];
                     returnPair = new pairInTurnet(i,j);
                  }
                  else if (i+j == returnPair.getRow() + returnPair.getCol() && returnPair.getCol() > j) {//공격력, 최근에 공격한 포탑, 합까지 같으면
                     attack = attackPowerMap[i][j];
                     returnPair = new pairInTurnet(i, j);
                  }
                  
               }
            }   
         }
      }
      attacked[returnPair.getRow()][returnPair.getCol()] = true;
      return returnPair;
   }
   protected boolean laser(pairInTurnet attacker, pairInTurnet target) {
      boolean canAttack = bfs(attacker,target);
      if(!canAttack)
         return false;
      else {
//    	  System.out.println("can laser");
         int damage = (int)(attackPowerMap[attacker.getRow()][attacker.getCol()] /2);
         
         pairInTurnet temp = visited[target.getRow()][target.getCol()];
         
         while(!(temp.getRow() == attacker.getRow() && temp.getCol() == attacker.getCol())) {
        	 int row = temp.getRow();
        	 int col = temp.getCol();
        	 
//        	 System.out.println("laser row : "+ row + " laser col : " + col);
        	 
        	 attackPowerMap[row][col] = attackPowerMap[row][col] <= damage ? 0 : attackPowerMap[row][col] - damage;
        	 attacked[row][col] = true;
        	 temp = visited[row][col];
        	 
         }
  
         
         
         attackPowerMap[target.getRow()][target.getCol()] =  attackPowerMap[attacker.getRow()][attacker.getCol()] >= attackPowerMap[target.getRow()][target.getCol()]? 0 :
            attackPowerMap[target.getRow()][target.getCol()] - attackPowerMap[attacker.getRow()][attacker.getCol()]  ;
      }
      return true;
   }
   
   protected boolean bfs(pairInTurnet attacker, pairInTurnet target) {
	   Queue<pairInTurnet> q = new LinkedList<pairInTurnet>();
	   q.add(attacker);
	   visited[attacker.getRow()][attacker.getCol()] = attacker;
	   
	   while(!q.isEmpty()) {
		   pairInTurnet now = q.poll();
		   int row = now.getRow();
		   int col = now.getCol();
		   
		   for(int i = 0; i<4; i++) {
			   int tempRow = getTempIndex(row, rowAppend[i], N);
			   int tempCol = getTempIndex(col, colAppend[i], M);
			   
			   if(visited[tempRow][tempCol] == null && attackPowerMap[tempRow][tempCol] != 0) {
//				   System.out.println("visited row :" + tempRow + " visited col :"+ tempCol);
				   visited[tempRow][tempCol] = now;
				   if(tempRow == target.getRow() && tempCol == target.getCol()) {
					   return true;
				   }
					   
				   q.add(new pairInTurnet(tempRow, tempCol));
			   }
 		   }
	   }
	   return false;
   }
   
   protected int getTempIndex(int index, int append, int Q) {
	   int tempIndex = index + append;
	   tempIndex = tempIndex > Q ? 1 : tempIndex;
	   tempIndex = tempIndex < 1 ? Q : tempIndex;
	   return tempIndex;
	   
   }
   

   
   
   protected void shell(pairInTurnet attacker, pairInTurnet target) {
      int damage = (int)(attackPowerMap[attacker.getRow()][attacker.getCol()] /2);
      for (int i = 0; i<8; i++) {
         int tempRow = getTempIndex(target.getRow() , shellRow[i], N);
         int tempCol = getTempIndex(target.getCol() , shellCol[i], M);
         
         
         
         if(!(tempRow == attacker.getRow() && tempCol == attacker.getCol())) {
//        	 System.out.println("shell row :" + tempRow + " shell col : " + tempCol);
            attackPowerMap[tempRow][tempCol] = attackPowerMap[tempRow][tempCol] <= damage ? 0 : attackPowerMap[tempRow][tempCol] - damage;
            attacked[tempRow][tempCol] = true;
         }
         
      }
      attackPowerMap[target.getRow()][target.getCol()] =  attackPowerMap[attacker.getRow()][attacker.getCol()] >= attackPowerMap[target.getRow()][target.getCol()]? 0 :
         attackPowerMap[target.getRow()][target.getCol()] - attackPowerMap[attacker.getRow()][attacker.getCol()]  ;
   }
   
   protected void repair() {
      for(int i = 1; i <= N; i++) {
         for(int j = 1; j <=M; j++) {
            if(!attacked[i][j] && attackPowerMap[i][j]!= 0) {
               attackPowerMap[i][j]+=1;
            }
         }
      }
      attacked = new boolean[N+1][M+1];
   }
   
   protected void getMax() {
      int max = Integer.MIN_VALUE;
      for (int i = 1; i<=N; i++) {
         for (int j = 1; j<=M; j++) {
            if(max < attackPowerMap[i][j]) {
               max = attackPowerMap[i][j];
            }
         }
      }
      System.out.println(max);
   }
   
   public static void main(String [] args) throws IOException {
      new turnet().solution();
   }

}
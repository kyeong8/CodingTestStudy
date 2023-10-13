package codeTree;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.LinkedList;
import java.util.Queue;
import java.util.StringTokenizer;

class rowAndColinRunner{
   int row ;
   int col;
   
   rowAndColinRunner(int row, int col){
      this.row = row;
      this.col = col;
   }
   
   public int getRow() {
      return row;
   }
   public int getCol() {
      return col;
   }
   
   
   public void updateRowAndCol(int row, int col) {
      this.row = row;
      this.col = col;
   }
}


class Runner{
   int row;
   int col;
   boolean exit = false;
   int moveMent = 0;
   
   Runner(int row, int col){
      this.row = row;
      this.col = col;
   }
   
   public int getRow() {
      return row;
   }
   
   public int getCol() {
      return col;
   }
   
   public void updateRowAndCol(int row, int col) {
      this.row = row;
      this.col = col;
   }
   
   public void exit() {
	   exit = true;
   }
   
   public void upMovement() {
	   moveMent +=1;
   }
   
   public int getMoveMent() {
	   return moveMent;
   }
   
   public boolean getExit() {
	   return exit;
   }
}

public class mazeRunner {

   int N;
   int M;
   int K;
   int Map[][];
   
   LinkedList<Runner> runnerList = new LinkedList<>();
   
   int exitRow;
   int exitCol;
   
   int rowAppend[] = {-1, 1, 0, 0}; // 상 하 좌 우
   int colAppend[] = { 0, 0, -1,1};
   
   int INF = Integer.MAX_VALUE;
   

   
   public void solution() throws IOException {
      BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
      StringTokenizer st = new StringTokenizer(br.readLine());
      
      N = Integer.parseInt(st.nextToken());
      M = Integer.parseInt(st.nextToken());
      K = Integer.parseInt(st.nextToken());
      
      Map = new int[N+1][N+1];
      
      for(int i = 1; i<=N; i++) {
         StringTokenizer line = new StringTokenizer(br.readLine());
         
         for(int j = 1; j<=N; j++) {
            Map[i][j] = Integer.parseInt(line.nextToken());
         }
      }
      
      for(int i = 0; i <M; i++) {
         StringTokenizer line = new StringTokenizer(br.readLine());         
         runnerList.add(new Runner(Integer.parseInt(line.nextToken()), Integer.parseInt(line.nextToken())));
      }
      
      StringTokenizer line = new StringTokenizer(br.readLine());
      exitRow = Integer.parseInt(line.nextToken());
      exitCol = Integer.parseInt(line.nextToken());
      Map[exitRow][exitCol] = -1;
      
      
      // input 종료
      
      for(int i = 0; i<K; i++) {
         runnerMove();
         
         if(checkAllExit()) 
        	 break;h
         
         rotateMap();
//         System.out.println();
//         for(int j =1; j<=N; j++) {
//        	 for(int k = 1; k<=N; k++) {
//        		 System.out.print(Map[j][k]+"\t");
//        	 }
//        	 System.out.println();
//         }
//   
//         printResult();
      }
      
      printResult();
     
      
   }
   
   protected void runnerMove() {
	   int idx = 0;
      for(Runner now : runnerList) {
    	  if(!now.getExit()) {
    		  int distance = distanceRunnerAndExit(now);
    	      int nextRow = now.getRow();
    	      int nextCol = now.getCol();
    	         
    	      for(int i = 0; i<4; i++) {
    	    	  int tempRow = now.getRow() + rowAppend[i];
    	          int tempCol = now.getCol() + colAppend[i];
    	            
    	          int rowDiff = Math.abs(tempRow - exitRow);
    	          int colDiff = Math.abs(tempCol - exitCol);
    	            
    	            
    	          int tempDistance = rowDiff + colDiff;
    	            
    	            
//    	            System.out.println("distance :" + distance + "tempDistance" + tempDistance);
    	            
    	          if(tempDistance < distance && Map[tempRow][tempCol] <= 0) {
    	               distance = tempDistance;
    	               nextRow = tempRow;
    	               nextCol = tempCol;
    	            }
    	         }
//    	         System.out.println();
//    	         System.out.println(now.getRow() +" " + now.getCol() );
//    	         System.out.println(nextRow +" "+nextCol);
//    	         
    	         if(nextRow != now.getRow() || nextCol != now.getCol()) {
    	        	 now.upMovement();
    	         }
    	         
    	         now.updateRowAndCol(nextRow, nextCol);
    	        
    	         
    	         if(exitRow == nextRow && exitCol == nextCol) {
    	            now.exit();
    	          
    	         }
    	  }
    	
      }
   }
   
   protected int distanceRunnerAndExit(Runner now) {
      int nowRowDiff = Math.abs(now.getRow() - exitRow);
      int nowColDiff = Math.abs(now.getCol() - exitCol);
      
      int distance = nowRowDiff +nowColDiff;
      
      return distance;
      
   }
   
   protected int distanceSquareRunnerAndExit(Runner now) {
	      int nowRowDiff = Math.abs(now.getRow() - exitRow);
	      int nowColDiff = Math.abs(now.getCol() - exitCol);
	      
	      int distance = Math.max(nowRowDiff, nowColDiff);
	      
	      return distance;
	      
	   }
	   
   
   protected boolean checkAllExit() {
	   for( Runner now : runnerList) {
		   if(!now.getExit()) {
			   return false;
		   }
	   }
	   return true;
   }
   
   protected void rotateMap() {
      int distance = INF;
      Runner runner = runnerList.get(0);
      
      rowAndColinRunner point = getPoint(runner,distanceSquareRunnerAndExit(runner));
      for(Runner now : runnerList) {
    	  if(!now.getExit()) {
//    		  System.out.println("now.row :" + now.getRow() + " now.col :" + now.getCol());
        	  
    	         int tempDistance = distanceSquareRunnerAndExit(now);
    	         if (tempDistance < distance) {
    	        	 distance = tempDistance;
//    	        	 System.out.println("temp < dis");
    	        	runner = now;
    	        	point = getPoint(runner,distanceSquareRunnerAndExit(runner));
    	         }
    	         else if(tempDistance == distance) {
    	        	 int rowDiff = Math.abs(runner.getRow() - exitRow);
    	             int colDiff = Math.abs(runner.getCol() - exitCol);
    	             
    	             int min = Math.max(rowDiff, colDiff);
    	        	 rowAndColinRunner tempPoint = getPoint(now, min);
    	        	 if(point.getRow() > tempPoint.getRow()) {
    	        		 runner = now;
    	        		 point = tempPoint;
    	        	 }
    	        	 
    	        	 else if(point.getRow() == tempPoint.getRow()) {
    	        		 if(point.getCol()>tempPoint.getCol() ) {
    	        			 runner = now;
        	        		 point = tempPoint;
    	        		 }
    	        	 }
    	        	 
    	        	 
    	         }
    	  }
    	
      }
//      System.out.println("runner row:"+runner.getRow() + " runner col :" + runner.getCol() );
      
      int rowDiff = Math.abs(runner.getRow() - exitRow);
      int colDiff = Math.abs(runner.getCol() - exitCol);
      
      int min = Math.max(rowDiff, colDiff);
      
      rowAndColinRunner[] list4Point = null;
      
      for(rowAndColinRunner temp : squareInMap(runner, min)) { //가능한 시작점을 모두 넣는다
         list4Point = get4Point(temp, min); 
         
         if(isInMap(list4Point) && exitInMap(list4Point[0], min)) {
            break;
         }
      }
      int [][] tempMap = new int [min +2][min +2];
      
   
//      System.out.println("row :" + list4Point[0].row + " col : " + list4Point[0].col + " min : "+ min);
      

      for(int i = 0; i<= min ; i++) {
         for(int j = 0; j<= min ;j++) {
            tempMap[i+1][j+1] = Map[list4Point[0].getRow()+i][list4Point[0].getCol()+j];
            if(tempMap[i+1][j+1] >0) {
            	tempMap[i+1][j+1] -=1;
            }
         }
      }
      
      for(int i = 1; i<= min + 1 ; i++) {
          for(int j = 1; j<= min + 1;j++) {
        	 Map[list4Point[0].getRow() + j -1][ list4Point[0].getCol() + min + 1 - i] = tempMap[i][j];
        	 if(Map[list4Point[0].getRow() + j -1][ list4Point[0].getCol() + min + 1 - i] == -1) {
        		 exitRow = list4Point[0].getRow() + j -1;
        		 exitCol = list4Point[0].getCol() + min + 1 - i;
//        		  System.out.println("exitRow : " + exitRow + " exitCol : " + exitCol);
        	 }
         }
      }
      
      for(Runner now : runnerList) {
    	  if(!now.getExit()) {
    		  if(now.getRow() >= list4Point[0].getRow() && now.getRow() <= list4Point[0].getRow() + min && now.getCol()>= list4Point[0].getCol() && now.getCol() <= list4Point[0].getCol()+min) {
    			  int beforeRow = now.getRow();
    			  int beforeCol = now.getCol();
    			  now.updateRowAndCol(list4Point[0].getRow() - list4Point[0].getCol() + beforeCol, list4Point[0].getCol() + min + list4Point[0].getRow() - beforeRow);
    			  
    		  }
    	  }
    	  
      }
      
  
      
     
      
   }
   
   protected LinkedList<rowAndColinRunner> squareInMap(Runner runner, int min) {
      LinkedList<rowAndColinRunner> rowAndColList = new LinkedList<rowAndColinRunner>();
      for(int i = runner.getRow() - min; i<= runner.getRow(); i++) {
    	  for(int j = runner.getCol() - min; j<= runner.getCol(); j++) {
    		  rowAndColList.add(new rowAndColinRunner(i, j));
    	  }
      }

      return rowAndColList;
      
      
   }
   protected rowAndColinRunner[] get4Point(rowAndColinRunner now, int min) {
      rowAndColinRunner [] returnList = new rowAndColinRunner[4];
      returnList[0] = now;
      returnList[1] = new rowAndColinRunner(now.getRow(), (now.getCol() +min));
      returnList[2] = new rowAndColinRunner(now.getRow() + min , now.getCol());
      returnList[3] = new rowAndColinRunner(now.getRow() + min , now.getCol() + min);
      
      
      
      return returnList;
   }
   
   protected boolean isInMap(rowAndColinRunner[] returList) {
      for(rowAndColinRunner now : returList) {
         if(now.getRow() <= 0 || now.getRow() > N || now.getCol() <=0 || now.getCol() > N) {
//        	 System.out.println("is In Map false");
            return false;
         }
      }
//      System.out.println("is In Map true");
      return true;
   }
   
   protected boolean exitInMap(rowAndColinRunner list4Point, int min) {
      if(list4Point.getRow() <= exitRow && exitRow <= list4Point.getRow() + min && list4Point.getCol() <= exitCol && exitCol <= list4Point.getCol() + min ) {
//    	  System.out.println("exit true");
         return true;
      }
//      System.out.println("exit false");
      return false;
   }
   
   protected rowAndColinRunner getPoint(Runner runner ,int min) {
	   rowAndColinRunner[] list4Point = null;
	   for(rowAndColinRunner temp : squareInMap(runner, min)) { //가능한 시작점을 모두 넣는다
	         list4Point = get4Point(temp, min); 
	         
	         if(isInMap(list4Point) && exitInMap(list4Point[0], min)) {
	            break;
	         }
	      }
	   return list4Point[0];
   }
   
   protected void printResult() {
	   int sum = 0;
	   for(Runner now : runnerList) {
//		   System.out.println("row : " + now.getRow() + " col : "+ now.getCol() + " move : "+now.getMoveMent());
		   sum +=now.getMoveMent();
	   }
	   System.out.println(sum);
	   System.out.println(exitRow + " "+ exitCol);
   }
  
   
   public static void main(String[]args) throws IOException {
      new mazeRunner().solution();
   }
}
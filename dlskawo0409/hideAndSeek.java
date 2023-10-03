import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;


class pairInhideAndSeek{
   int row;
   int col;
   
   pairInhideAndSeek(int row, int col) {
      this.row = row;
      this.col = col;
   }
}

class Seeker{
   pairInhideAndSeek pair;
   int rowAppend[] = {-1, 0, 1, 0}; // 위 오 하 좌
   int colAppend[] = {0, 1, 0, -1};
   
   int rowSize = 1;
   int colSize = 1;
   
   int rowIndex = 0;
   int colIndex = 0;
   
   int direction = 0;
   
   boolean plus = true;
   
   int N;
   
   Seeker(int N){
      this.N = N;
      this.pair = new pairInhideAndSeek(N/2+1, N/2+1);
      
   }
   
   protected pairInhideAndSeek move() {
      if(pair.row == 1 && pair.col == 1) {
         plus = false;
         rowSize = N;
         colSize = N-1;
         rowIndex = N-1;
         colIndex = colSize;
         direction = 2;
      }
      if(pair.row == N/2+1 && pair.col == N/2 +1 ) {
    	  rowSize = 1;
    	  colSize = 1;
    	  rowIndex = 0;
    	  colIndex = 0;
    	  direction = 0;
    	  plus = true;
      }
      
      
      int tempRow = pair.row + rowAppend[direction];
      int tempCol = pair.col + colAppend[direction];
      
//
//      rowIndex += Math.abs(rowAppend[direction]);
//      colIndex += Math.abs(colAppend[direction]);
      
      if(plus) {
    	  if(direction == 0 || direction ==2) {
    		  rowIndex+=1;
        	  if(rowIndex == rowSize) {
        		  rowIndex = 0;
            	  rowSize += 1;
//            	  System.out.println("rowSize : "+ rowSize);
            	  direction = direction + 1 > 3 ? 0: direction + 1;
        	  }
    	  }
    	  else if(direction == 1 || direction == 3) {
    		  colIndex+=1;
    		  if(colIndex == colSize) {
    			  
    			  colIndex = 0;
    			  colSize += 1;
//    			  System.out.println("colSize : "+ colSize);
    			  direction = direction + 1 > 3 ? 0: direction + 1;
    		  }
    	  }
    	
    	  
      }
      else if(!plus) {
    	  if(direction == 0 || direction ==2) {
    		  rowIndex -=1;
    		  if(rowIndex == 0) {
    			  rowSize -=1;
    			  rowIndex = rowSize;
    			  direction = direction - 1 < 0 ? 3 : direction -1; 
    		  }
    	  }
    	  else if(direction == 1 || direction == 3) {
    		  colIndex -=1;
    		  if(colIndex == 0) {
    			  colSize -=1;
    			  colIndex = colSize;
    			  direction = direction - 1 < 0 ? 3 : direction -1; 
    		  }
    	  }
      }
      
//      if(tempRow == 1 && tempCol == 1) {
//    	  direction +=1;
//      }
//      if(tempRow == N/2+1 && tempCol == N/2 +1 ) {
//    	  System.out.println( N/2+1);
//    	  direction -=1;
//      }
  
      pair.row = tempRow;
      pair.col = tempCol;
      return new pairInhideAndSeek(tempRow, tempCol);
   }
   
   
}

class Hidder{
   pairInhideAndSeek pair;
   int d; // 방향 1 좌우    2 상하
   int rowAppend[] = {-1, 0, 1, 0}; // 위 오 하 좌
   int colAppend[] = {0, 1, 0, -1};
   int head;
   boolean catched = false;
   
   Hidder(int row, int col, int d){
      this.d = d;
      this.pair = new pairInhideAndSeek(row, col);
      
      
      if(d == 1) {
         this.head = 1;
      }
      else if(d == 2) {
         this.head = 2;
      }
   }
   
   public pairInhideAndSeek move(int sRow, int scol , int N) {
      int tempRow = pair.row + rowAppend[head];
      int tempCol = pair.col + colAppend[head];
      
      if(!isInMap(tempRow, tempCol, N)) {
         head = head + 2 > 3 ? head - 2 : head + 2;
         tempRow = pair.row + rowAppend[head];
         tempCol = pair.col + colAppend[head];
      }
      if(sRow == tempRow && scol == tempCol) {
         return pair;
      }
      
      pairInhideAndSeek result = new pairInhideAndSeek(tempRow, tempCol);
      pair = result;
      return result;
   }
   
   protected boolean isInMap(int row, int col, int N) {
      if(1<=row && row<=N && 1<=col && col<=N) {
         return true;
      }
      return false;
   }
}

public class Main {
   
   int N;
   int M;
   int H;
   int K;
   
   int rowAppend[] = {-1, 0, 1, 0}; // 위 오 하 좌
   int colAppend[] = {0, 1, 0, -1};
   
   Hidder[] hidderList;
   boolean treeMap[][];
   Seeker seeker;
   
   public void solution() throws IOException {    
      BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
      StringTokenizer st = new StringTokenizer(br.readLine()); 
      
      N = Integer.parseInt(st.nextToken());
      M = Integer.parseInt(st.nextToken());
      H = Integer.parseInt(st.nextToken());
      K = Integer.parseInt(st.nextToken());
      
      hidderList = new Hidder[M];
   
      treeMap = new boolean [N+1][N+1];
      seeker = new Seeker(N);
      for(int m = 0; m<M; m++) {
         st = new StringTokenizer(br.readLine());
         int row = Integer.parseInt(st.nextToken());
         int col = Integer.parseInt(st.nextToken());
         int d = Integer.parseInt(st.nextToken());
         
         hidderList[m] = new Hidder(row, col ,d);
      }
      
      for(int h = 0; h<H; h++) {
         st = new StringTokenizer(br.readLine());
         int row = Integer.parseInt(st.nextToken());
         int col = Integer.parseInt(st.nextToken());
         treeMap[row][col] = true; //tree
      }
      
      int result =0;
      for(int k = 1; k<=K; k++) {
         moveHidder();
         result += moveSeeker(k);
//         System.out.println(result);
      }
      System.out.println(result);
   }
   
   protected void moveHidder() {
      for(int i = 0; i<hidderList.length; i++) {
         Hidder hidder = hidderList[i];
//         System.out.println("seeker row : "+ seeker.pair.row+ " seekcer col :" + seeker.pair.col);
//         System.out.println("before hidder row :"+ hidder.pair.row + "  before hidder col :" + hidder.pair.col );
         if(hidder.catched) {
        	 
            continue;
         }
         
         int distance = Math.abs(hidder.pair.row - seeker.pair.row) + Math.abs(hidder.pair.col - seeker.pair.col);
//         System.out.println("distance :" +distance);
         if(distance >3) {
            continue;
         }
      
         pairInhideAndSeek location = hidder.move(seeker.pair.row, seeker.pair.col, N);
//         System.out.println("hidder row :"+ location.row + " hidder col :" + location.col );
      }
     
      
   }
   
   protected int moveSeeker(int k ) {
      int result = 0;
      int count = 0;
      pairInhideAndSeek location = seeker.move();
//      System.out.println("seekerRow :" + seeker.pair.row + " seekcer Col:"+ seeker.pair.col);
//      System.out.println("seeker Dierction :" + seeker.direction);
      int tempRow =location.row;
      int tempCol =location.col;
      for(int i = 0; i<3; i++) {
    	  if(i!=0) {
    		  tempRow = tempRow+ rowAppend[seeker.direction];
    	      tempCol = tempCol+ colAppend[seeker.direction];
    	  }
         
         
         
//         System.out.println("tempRow : "+ tempRow + " tempCol :"+ tempCol);
         
         for(Hidder hidder : hidderList) {
            if(hidder.catched) {
               continue;
            }
            if(isInMap(tempRow, tempCol, N)&&!treeMap[tempRow][tempCol]  && hidder.pair.row == tempRow && hidder.pair.col == tempCol) {
               count+=1;
               hidder.catched = true;
            }
         }
         
         
      }
      result = count * k;
      return result;
      
   }
   protected boolean isInMap(int row, int col, int N) {
      if(1<=row && row<=N && 1<=col && col<=N) {
         return true;
      }
      return false;
   }

   
   public static void main(String[]args) throws IOException {
      new Main().solution();
   }
}
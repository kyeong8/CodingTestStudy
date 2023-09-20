// 2023-09-21  
// bj23291_어항정리    
// 5시간
// 규칙 사용
// 구현, 시뮬레이션  


package bj;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

class rowAndCol23291 {
   int row;
   int col;
   
   rowAndCol23291(int row, int col){
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

public class Main {
   int N;
   int K;
   int [] line;
   int [][]levitation;
   boolean [][] visited;

   
   int []rowAppend = { 0,  -1, 0, 1}; // 좌 위 오 아
   int []colAppend = {-1,  0, 1,  0};
   
   
   public void solution() throws IOException {
       BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
       StringTokenizer st = new StringTokenizer(br.readLine());
      
      N = Integer.parseInt(st.nextToken());
      K = Integer.parseInt(st.nextToken());
      
      line = new int[N];
      st = new StringTokenizer(br.readLine());
      for(int i = 0; i<N; i++) {
         line[i] = Integer.parseInt(st.nextToken());
      }
      
      int result = 0;
      
      while(differenceOfMaxMin() > K) {

         
         addOneMinFishbowl();
         

         levitationAndRotationClockwise();
         
         
         moveFish();
         
         
         levitationToOneLine();
         

         levitationWithTwo();
         
         
         moveFish();

          levitationToOneLine();

         result +=1;
      }
      
      System.out.println(result);
      
   }
   
   protected int differenceOfMaxMin() {
      return Arrays.stream(line).max().getAsInt() - Arrays.stream(line).min().getAsInt();
   }
   
   protected void addOneMinFishbowl() {
      int min = Arrays.stream(line).min().getAsInt();
      for(int i = 0; i < N; i++) {
         line[i] = line[i] == min ? line[i]+1 : line[i];
      }
      
   }
   
   protected void levitationAndRotationClockwise() {
      rowAndCol23291 shape = setlevitation();
      
      int multiOfShape = shape.getRow() * shape.getCol();
      int direction = (shape.getRow() + shape.getCol()) % 4; // 시작되는 방향이 반복되기 때문에 모양의 합 을 4로 나눈 나머지와 같게 된다.  
      
      rowAndCol23291 start = getStartRowAndCol(shape, direction);
      
      int nowRow = start.getRow();
      int nowCol = start.getCol();
      
      
      int filledRow = 1;
      int filledCol = 1;
      
      levitation[nowRow][nowCol] = line[0];
      
      
      for(int i = 1; i<=multiOfShape-1;) {
         
         if(direction == 0 || direction == 2) {// 
            
            for(int j = 1; j <= filledCol; i++, j++) {  // 처음 1
               if( i > multiOfShape-1 ) {
                  break;
               }
               
               nowRow += rowAppend[direction];
               nowCol += colAppend[direction];
               levitation[nowRow][nowCol] = line[i];
            }
            
            filledCol += 1;
         }
         
         if(direction == 1 || direction == 3) {
            for(int j = 1; j<=filledRow; i++, j++) {
               if( i > multiOfShape-1 ) {
                  break;
               }
               nowRow += rowAppend[direction];
               nowCol += colAppend[direction];


            }
            filledRow += 1;
         }
         
         
   
         
         direction = direction - 1 < 0 ? 3 : direction - 1; 
      }

      for(int i = 0; i < shape.getRow()-1 ;i++) { // 나머지 부분 -1 채움
         for(int j = shape.getCol(); j< levitation[0].length; j++) {
            levitation[i][j] = -1;
            visited[i][j] = true;
         }
         
      }
      
      for(int i = 1; i <= N - multiOfShape; i++) { // shape에서 벗어난 것을 채워 넣음
         levitation[shape.getRow()-1][shape.getCol() - 1 + i] = line[multiOfShape - 1 + i];
      }
      
      
   }
   
   protected rowAndCol23291 getStartRowAndCol(rowAndCol23291 shape, int direction) {
      rowAndCol23291 start = new rowAndCol23291(0,0);
      
      switch(direction) {
      case 0:
         start = new rowAndCol23291((int)shape.getRow()/2 -1, (int)shape.getCol()/2 );
         break;
      case 1:
         start = new rowAndCol23291((int)shape.getRow()/2, (int)shape.getCol()/2 );
         break;
      case 2:
         start = new rowAndCol23291((int)shape.getRow()/2, (int)shape.getCol()/2 );
         break;
      case 3:
         start = new rowAndCol23291((int)shape.getRow()/2-1, (int)shape.getCol()/2 );
         break;
      }
      return start;
   }
   
   protected rowAndCol23291 setlevitation() {
      int row = 2;
      int col = 2;
      int tempRow = 3;
      int tempCol = 2;
      
      while(tempRow*tempCol <= N) {
         row = tempRow;
         col = tempCol;
      
         if(row == col) {
            tempRow += 1;
         }
         else if(row > col ) {
            tempCol += 1;
         }
         
      }
      int remain = N - row * col; // 마지막에 올리지 못하고 남은 것들
      
      
      levitation = new int [row][col + remain];
      visited = new boolean [row][col + remain];
      return new rowAndCol23291(row, col);
         
   }
   
   
   protected void moveFish() {
      int[][]tempLevitation = new int [levitation.length][levitation[0].length];
      
      for(int i =0; i<tempLevitation.length; i++) {
         tempLevitation[i] = levitation[i].clone();
      }
      
      for(int i =0; i<tempLevitation.length; i++) {
         for(int j = 0; j< tempLevitation[0].length - 1; j++) {
            
            int a = levitation[i][j];
            int b = levitation[i][j+1];
            
            if(a == -1 || b == -1) {
               break;
            }
            
            int d =(int) Math.abs(a - b) / 5;
            if(a > b) {
               tempLevitation[i][j] -= d;
               tempLevitation[i][j+1] += d;
            }
            if(b > a) {
               tempLevitation[i][j] += d;
               tempLevitation[i][j+1] -= d;
             }
         }
      }
      
      for(int j = 0; j<tempLevitation[0].length; j++) {
         for(int i = 0; i<tempLevitation.length - 1; i++) {
            
            int a = levitation[i][j];
            int b = levitation[i+1][j];
            
            if(a == -1 || b == -1) {
               break;
            }
            
            
            int d =(int) Math.abs(a - b) / 5;
            
            if(a > b) {
               tempLevitation[i][j] -= d;
               tempLevitation[i+1][j] += d;
            }
            if(b > a) {
               tempLevitation[i][j] += d;
               tempLevitation[i+1][j] -= d;
             }
         }
      }
      levitation = tempLevitation;
      
   }
   
   protected boolean isInMap(int row, int col) {
      if(0<= row && row < levitation.length && 0<= col && col < levitation[0].length) {
         return true;
      }
      return false;
   }
   
   protected void levitationToOneLine() {
      int index = 0;
      for(int j = 0; j<levitation[0].length; j++) {
         for(int i = levitation.length-1; i>=0;i--) {
            if(levitation[i][j] != -1) {
               line[index++] = levitation[i][j]; 
            }
         }
      }
   }
   
   protected void levitationWithTwo() {
      int q = (int)N/4;
      levitation = new int [4][q];
      visited = new boolean [4][q];
            
      for(int i = 0; i<q;i++) {
         levitation[0][i] = line[(int)(6*q+1)/2 - i -1];
         levitation[1][i] = line[(int)(2*q+1)/2 + 1 + i -1];
         levitation[2][i] = line[q - i -1];
         levitation[3][i] = line[(int)(6*q+1)/2 + 1 + i -1];
      }
      
   }
   
   public static void main(String[]args) throws IOException {
      new Main().solution();
   }

}

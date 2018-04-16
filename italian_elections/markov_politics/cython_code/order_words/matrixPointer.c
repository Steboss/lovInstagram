#include <stdio.h>
#include <stdlib.h>


int main () {

  int nRows, nCols;
  nRows= 2;
  nCols = 3;
  int i, j;
  double** pM = 0;
  pM = malloc(nRows*sizeof(double)); //request memory from the heap for the rows
  //now obtain the memory for the two rows
  for (i =0; i< nRows; i++){

    pM[i] = malloc(nCols*sizeof(double)); //and here we don't need * since it's the second one

  }
  printf("The value of pM is %x\n", pM);
  for (i =0; i< nRows; i++){
    printf("The address of pM[%d] is %x\n", i, &pM[i]);
  }

  for(i =0; i<nRows;i++){
    printf("The value of pM[%d] is %x\n",i,pM[i]);
    for (j=0; j<nCols;j++){
      printf("  The address of pM[%d][%d] is %x\n", i,j,&pM[i][j]);
    }
    printf("\n");
  }

  for (i =0;i<nRows;i++){
    for(j = 0; j<nCols;j++){
      pM[i][j] = i*j;
      printf("pM[%d][%d] = %d", i,j,pM[i][j]);
    }
    printf("\n");
  }

  //clean up
  for (i=0; i<nRows; i++){
    free(pM[i]);

  }
  free(pM);
  return 0;
}

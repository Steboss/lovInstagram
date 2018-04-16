#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#include<string.h>

//compute the probability matrix
double probability_matrix()
{
  char string[100] ="Today is a beautiful day";
  int string_len = strlen(string);
  char *splitter ;
  splitter = strtok(string," ");
  int splitter_len;
  splitter_len = strlen(splitter);
  printf("%d\n", splitter_len);
  int i;
  int counter ;
  counter =0 ;
  for (i=0; i<splitter_len; i++)
  {

    while(splitter!=NULL)
    {
      printf("%s\n", splitter);
      splitter = strtok(NULL," ");
      counter+=1;
    }
  }
  printf("%d\n", counter);
  return 0 ;

}

int main ()
{
  //char *filename="berlusconi.csv";
  probability_matrix();//(filename);
}

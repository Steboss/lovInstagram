#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#include<string.h>

int find_indx(char **words, char *tmp, int words_dim)
{
  //find the index of tmp in words
  int i;
  int index= words_dim+1;
  for(i=0; i<words_dim; i++)
  {
    if (strcmp(words[i],tmp)==0)
    {
      index = i;
    }
  }

  return index;

}

//compute the probability matrix
double probability_matrix(char **sentences,char **words, int lines_dim ,int words_dim)
{
  //*sentences:  array with all the comments
  //*words : array with all the words from the comments
  //lines_dim: how many lines do we have
  //words_dim: how many words do we have
  int nRows = words_dim;
  int nCols = words_dim;
  int i,j ;
  //create a words_dim*word_dim matrix
  int **matrix ;
  //get the space
  matrix = (int**)malloc(sizeof(int*)*nRows); //request memory from the heap for the rows
  //now obtain the memory for the cols
  for (i=0; i< nRows; i++){
    matrix[i] = (int*)malloc(sizeof(int)*nCols); //and here we don't need * since it's the second one
  }
  //initialize all the elements to zero
  printf("Initialize matrix elements...\n");
  for(i=0;i<nRows;i++)
  {
    for(j=0;j<nCols;j++)
    {
      matrix[i][j] = 0;
      //printf("%d\n",matrix[i][j]);
    }
  }


  //TODO: here add a sanity check: are all the lines words in words?
  //Consider the sanity check in python and not here?

  //now fill the array, so compute the transition
  int idx_prev ; //index of the previous part of the sentence
  int idx_forw ; //index of the forward part of the sentence -- for end states
  int idx_curr ; //current index of the word
  char * tmp; //temporary variables where I am going to store the splitter values
  int splitter_len ; //int to know the number of elmenets in splitters
  char * splitter; //strtok result

  for (i=0;i<lines_dim-1;i++)
  {
    printf("%s\n", sentences[i]);
    //split each line
    splitter = strtok(sentences[i]," ");
    splitter_len=strlen(splitter);
    //define a counter
    int counter =0 ;
    for(j=0;j<splitter_len-1;j++)
    {
      //"TOday" "is" "a " "day"

      while(splitter!=NULL)
      {
        if(counter==0)
        {
          //this is the first item
          tmp = splitter; //"Today"
          //find the index of tmp
          idx_prev = find_indx(words, tmp, words_dim); //"Today" indx
          counter+=1;
          splitter = strtok(NULL," ");
        }
        else if(counter==1 || counter==splitter_len)
        {
          //count a +1 for the previous (tmp) word
          idx_forw =find_indx(words,splitter,words_dim);  //"is"  indx
          //fill the array at position  [indx_prev][indx_forw]
          matrix[idx_forw][idx_prev]+=1;  //matrix[is][Today] +=1  , is comes after Today
          counter+=1;
          tmp = splitter;
          splitter = strtok(NULL," ");
        }
        else
        {
          idx_curr = find_indx(words,splitter,words_dim); //"a" index //"day" indx
          //refer to the previosu indx_forw
          //so the word at indx_forw now is a reference
          //the word at index_curr is what is following the indx_forw word
          matrix[idx_curr][idx_curr]+=1; //matrix[a][is]  a comes after "is"
          //update the indexes
          idx_forw = idx_curr; //"is"indx-> a index
          counter+=1;
          splitter = strtok(NULL," ");
        }
      }
    }
  }

  //return  matrix;

    printf("Here the  transition matrix...\n");
    for(i=0;i<nRows;i++)
    {
      for(j=0;j<nCols;j++)
      {
        printf("Element %d,%d = %d\n",i,j,matrix[i][j]);
      }
    }

  //return 0 ;

}

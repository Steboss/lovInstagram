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
double** probability_matrix(char **sentences,char **words, int lines_dim ,int words_dim)
{
  //*sentences:  array with all the comments
  //*words : array with all the words from the comments
  //lines_dim: how many lines do we have
  //words_dim: how many words do we have
  int nRows = words_dim;
  int nCols = words_dim;
  int i,j ;
  //create a words_dim*word_dim matrix
  double **matrix ;
  //get the space
  matrix = (double**)malloc(sizeof(double*)*nRows); //request memory from the heap for the rows
  //now obtain the memory for the cols
  for (i=0; i< nRows; i++){
    matrix[i] = (double*)malloc(sizeof(double)*nCols); //and here we don't need * since it's the second one
  }
  //initialize all the elements to zero
  printf("Initialize matrix elements...\n");
  for(i=0;i<nRows;i++)
  {
    for(j=0;j<nCols;j++)
    {
      matrix[i][j] = 0.0;
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

  //test the first 10 lines
  for (i=0;i<lines_dim-1;i++)
  {
      //printf("%s\n", sentences[i]);
      //split each line
      splitter = strtok(sentences[i]," ");
      splitter_len=strlen(splitter);
      //define a counter
      int counter =0 ;
      //here we need  store the splitter into an array
      //the array will be sent to a function
      //there we will take n elements from the array and see what's on the n+1 elements
      int i =0;
      char *array[] ; //can we define it dynamically?
      while(splitter!=NULL)
      {
        array[i++]=splitter;
        splitter= strtok(NULL," ");
      }
      //
      //in the  function we will have#
      /*
      for (i=0; i<len_array;i++)
      {
          //take from i to i+n elements
          //
      }
      */

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
          //  printf("Temporary: %s\n, index : %d\n", tmp, idx_prev);
          }
          else if (counter==splitter_len)
          {
            //this is the last word
            //which follows the previous one
            idx_curr = find_indx(words,splitter,words_dim);
            //printf("Previous word :%s, %d, following %s, %d\n", tmp, idx_prev,splitter,idx_curr);
            matrix[idx_curr][idx_prev]+=1.0;
            splitter=strtok(NULL," ");
          }
          else
          {
            //printf("Current Splitter:%s,current tmp %s\n", splitter,tmp);
            idx_curr = find_indx(words,splitter,words_dim); //"a" index //"day" indx
            //refer to the previosu indx_forw
            //so the word at indx_forw now is a reference
            //the word at index_curr is what is following the indx_forw word
            //printf("Previous word: %s, %d, following %s,%d \n ", tmp, idx_prev, splitter,idx_curr);
            matrix[idx_curr][idx_prev]+=1.0; //matrix[a][is]  a comes after "is"
            //update the indexes
            idx_prev = idx_curr; //"is"indx-> a index
            counter+=1;
            splitter = strtok(NULL," ");
            tmp = words[idx_curr];
          }
        }
      }
  }

  //normalize the probability
  /*printf("Normalizing transition matrix...\n");

  double tot_sum = 0.0;

  for(i=0;i<nRows;i++)
  {
    for(j=0;j<nCols;j++)
    {
      tot_sum += matrix[i][j]; //sum over all the rows
    }
    //normalize
    for(j=0;j<nCols;j++)
    {
      if (tot_sum==0)
      {
        matrix[i][j]=0;
      }
      else
      {
        matrix[i][j]/=tot_sum;
      }
      //printf("%.2f\n",matrix[i][j]);
    }
  }*/

  printf("writing output matrix...\n");
  //lets try to save a file
  FILE *outputfile ;
  outputfile = fopen("transition_matrix.csv","w");
  //fill the write line as  space, words1, words2 ...
  for (j=0;j<words_dim;j++)
  {
    fprintf(outputfile,",%s", words[j]);
  }

  for (i=0;i<nRows;i++)
  {
    //go onto a new line, write the words and theiry values
    fprintf(outputfile,"\n%s,", words[i]);
    for(j=0;j<nCols;j++)
    {
      fprintf(outputfile,"%.2f,",matrix[i][j]);
    }

  }

  fclose(outputfile);

  return matrix;

  //return 0 ;

}

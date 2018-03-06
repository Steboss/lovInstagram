#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#include<string.h>

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
  double **matrix ;
  //get the space
  matrix = malloc(nRows*sizeof(int)); //request memory from the heap for the rows
  //now obtain the memory for the cols
  for (i =0; i< nRows; i++){
    matrix[i] = malloc(nCols*sizeof(int)); //and here we don't need * since it's the second one
  }
  //initialize all the elements to zero
  printf("Initialize matrix elements...\n");
  printf("Total number of words %d\n", words_dim);
  for(i=0;i<nRows;i++)
  {
    for(j-0;j<nCols;j++)
    {
      matrix[i][j] = 0;
    }
  }
  //TODO: here add a sanity check: are all the lines words in words?
  int sanity_counter=0;
  char *splitter;
  char **repeated;
  repeated = malloc(lines_dim*sizeof(char));

  for(i=0; i<lines_dim;i++)
  {
    //char *splitter=strtok(sentences[i]," ");

    for (char *splitter=strtok(sentences[i]," "); splitter!=NULL; splitter=strtok(NULL, " "))
    {
      //printf("%s\n", splitter);
      for(j=0;j<words_dim;j++)
      {
        if(strcmp(splitter,words[j])==0)
        {
          //check if splitter in repeate
          //if it's there do not add
          //otherwise sanity_counter+=1
          
          sanity_counter+=1;
        }
      }
    }
  }
  printf("Total number of splitters in words %d\n", sanity_counter);

  //now fill the array, so compute the transition
  int idx_prev ;
  char * tmp; //temporary variables where I am going to store the splitter values
  int splitter_len ; //length of the splitters
  // the algorithm:
  //- cycle through all the lines/
//- Split the lines and cycle through the splitS/
//- Cycle thriugh each word
//- If the word==split[i] take the previous split, which is stored in a tmp variables
//- Retrieve the tmp variables number
//- Add +1  to the matrix element k, index of tje word from the list of words, and j, index of the variable tmp in list of wordS. That mean word k has a +1 transition after word k
//- At the end normalize the counter. For each row sum the total numb of counter
//- Compute the probability matrix as the M[ij]/total numb counter x row
  for (i=0;i<lines_dim;i++)
  {
    //split each line
    //char *splitter = strtok(sentences[i]," ");
    splitter_len =strlen(splitter);
    //define a counter
    int counter =0 ;
    //if counter==0 we have the first element, so :
    //1) look for the word == splitter[0]
    //2) we need to find the next splitter indx in words
    //if counter==splitter_len  this is the last element of the word
    //1) we can do with th eprevious index
    for (char *splitter=strtok(sentences[i]," "); splitter!=NULL; splitter=strtok(NULL, " "))
    {
      //cylce through each word
      for(j=0;j<words_dim;j++)
      {
        //printf("Word:%s\n", words[j]);
        //printf("splitter:%s\n", splitter);
        if (strcmp(splitter,words[j]) == 0)
        {
          //printf("Word:%s\n", words[j]);
          //printf("splitter%s\n",splitter);
          //find the index of the previous words
          idx_prev = find_prev(words, tmp, words_dim);
          printf("index_prev %d\n", idx_prev);

          //add a +1 to the matrix element
          matrix[j][idx_prev]+=1;
          //update tmp
          tmp = splitter;
        }
        else
        {
          tmp = splitter;
        }
      }
    }


  }

  /*
  for(i=0;i<nRows;i++)
  {
    for(j=0;j<nCols;j++)
    {
      printf("Element %d,%d = %d\n",i,j,matrix[i][j]);
    }
  }*/
  return 0 ;
  //clean up and free everything
  /*for (i=0; i<nRows; i++){
    free(matrix[i]);
  }
  free(matrix);
  return 0;*/

}

int find_prev(char **words, char *tmp, int words_dim)
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
/*
int main ()
{
  //char *filename="berlusconi.csv";
  probability_matrix();//(filename);
}
/**

    fclose(fp);
    if (line)
        free(line);
    exit(EXIT_SUCCESS);
}

double kendalT(double *x, int len_x, double * y, int len_y)
{
    //the two array MUST be have the same length
    int n2=0, n1=0, k, j;
    int is =0;
    double aa, a2, a1;

    for(j=1;j<len_x;j++){
      for(k=(j+1);k<=len_x;k++){
        a1=x[j]-x[k];
        a2=y[j]-y[k];
        aa = a1*a2;
        if (aa) {
          ++n1;
          ++n2;
          aa>0.0 ? ++is: --is;
        }
        else {
          if (a1) ++n1;
          if (a2) ++n2;
        }
      }
    }

    double tau;
    tau = is/(sqrt((double)n1)*sqrt((double)n2) );
    //printf("Tau is %.4f\n", tau);
    return tau;

}


double mean(double *x, int length){

  int i;
  double avg;
  //avg = 0.0;
  for(i=0; i<length;i++){
    if (i==0){
      avg = x[i];

    }
    else{
      avg = avg + (x[i]-avg)/i;
    }
  }
  return avg;
}


double PearsonR(double *x, int len_x, double *y, int len_y)
{
  //compute the mean for each array
  double mean_x, mean_y;
  mean_x = mean(x, len_x);
  mean_y = mean(y, len_y);
  double xt, yt, sxx, syy, sxy;
  //initialization
  sxx= 0.0;
  sxy = 0.0;
  syy = 0.0;

  int i;


  for(i=0;i<len_x;i++){
    xt = x[i]-mean_x;
    yt = y[i]-mean_y;
    sxx+=xt*xt;
    syy+=yt*yt;
    sxy+=xt*yt;
    //printf("Xt %.4f\n", xt);
  }
  //now take the pearson R
  double R ;
  R = sxy/(sqrt(sxx*syy));
  //printf("Correlation %.4f\n", pow(R,2));
  return R;

}



double boxMuller(double mean,double sigma){
  //set the seed
  //int seed = (int)time(NULL);
  //srand(seed);
  //rand();

  double two_pi =2*M_PI;

  double z1, u1,u2, z0;
  u1 = 0.0;
  while(u1==0.0){
    u1 = rand()*(1.0/RAND_MAX);
  }
  u2 = 0.0;
  while(u2==0.0){
    u2 = rand()*(1.0/RAND_MAX);
  }
  z1=sqrt(-2.0*log(u1))*cos(two_pi*u2);
  z0 = z1*sigma + mean;

  return z0;
}
/*
int main(){

  //FILE *ofile;
  //ofile =fopen("test.dat","w");

  double array1[10]={2,3,4,4,4,2,3,4,5,2};
  double array2[10]={2,4,4,2,4,2,6,1,4,1};
  kendalT(array1,10,array2,10);
}*/

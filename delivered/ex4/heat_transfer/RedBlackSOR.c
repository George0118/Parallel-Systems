#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include "mpi.h"
#include "utils.h"  

//#define TEST_CONV 

int main(int argc, char ** argv) {
    int rank,size;
    int global[2],local[2]; //global matrix dimensions and local matrix dimensions (2D-domain, 2D-subdomain)
    int global_padded[2];   //padded global matrix dimensions (if padding is not needed, global_padded=global)
    int grid[2];            //processor grid dimensions
    int i,j,t;
    int global_converged=0,converged=0; //flags for convergence, global and per process
    MPI_Datatype dummy;     //dummy datatype used to align user-defined datatypes in memory
    double omega;                       //relaxation factor - useless for Jacobi

    struct timeval tts,ttf,tcomps,tcompf,tcomms,tcommf;   //Timers: total-> tts,ttf, computation -> tcs,tcf
    double ttotal=0,tcomp=0,tcomm=0,total_time,comp_time,comm_time;

    double ** U, ** u_current, ** u_previous, ** swap; //Global matrix, local current and previous matrices, pointer to swap between current and previous

    MPI_Status status;

    MPI_Init(&argc,&argv);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);

    //----Read 2D-domain dimensions and process grid dimensions from stdin----//

    if (argc!=5) {
        fprintf(stderr,"Usage: mpirun .... ./exec X Y Px Py");
        exit(-1);
    }
    else {
        global[0]=atoi(argv[1]);
        global[1]=atoi(argv[2]);
        grid[0]=atoi(argv[3]);
        grid[1]=atoi(argv[4]);
    }


    //----Create 2D-cartesian communicator----//
    //----Usage of the cartesian communicator is optional----//

    MPI_Comm CART_COMM;         //CART_COMM: the new 2D-cartesian communicator
    int periods[2]={0,0};       //periods={0,0}: the 2D-grid is non-periodic
    int rank_grid[2];           //rank_grid: the position of each process on the new communicator

    MPI_Cart_create(MPI_COMM_WORLD,2,grid,periods,0,&CART_COMM);    //communicator creation
    MPI_Cart_coords(CART_COMM,rank,2,rank_grid);                  //rank mapping on the new communicator


    //----Compute local 2D-subdomain dimensions----//
    //----Test if the 2D-domain can be equally distributed to all processes----//
    //----If not, pad 2D-domain----//

    for (i=0;i<2;i++) {
        if (global[i]%grid[i]==0) {
            local[i]=global[i]/grid[i];
            global_padded[i]=global[i];
        }
        else {
            local[i]=(global[i]/grid[i])+1;
            global_padded[i]=local[i]*grid[i];
        }
    }


    //----Allocate global 2D-domain and initialize boundary values----//
    //----Rank 0 holds the global 2D-domain----//
    if (rank==0) {
        //  rank, global[0], global[1], grid[0], grid[1], local[0], local[1], global_padded[0], global_padded[1]);
        U=allocate2d(global_padded[0],global_padded[1]);
        init2d(U,global[0],global[1]);
    }

    //----Allocate local 2D-subdomains u_current, u_previous----//
    //----Add a row/column on each size for ghost cells----//

    u_previous=allocate2d(local[0]+2,local[1]+2);
    u_current=allocate2d(local[0]+2,local[1]+2);

    //----Distribute global 2D-domain from rank 0 to all processes----//

    //----Appropriate datatypes are defined here----//
    /*****The usage of datatypes is optional*****/

    //----Datatype definition for the 2D-subdomain on the global matrix----//

    MPI_Datatype global_block;
    MPI_Type_vector(local[0],local[1],global_padded[1],MPI_DOUBLE,&dummy);
    MPI_Type_create_resized(dummy,0,sizeof(double),&global_block);
    MPI_Type_commit(&global_block);

    //----Datatype definition for the 2D-subdomain on the local matrix----//

    MPI_Datatype local_block;
    MPI_Type_vector(local[0],local[1],local[1]+2,MPI_DOUBLE,&dummy);
    MPI_Type_create_resized(dummy,0,sizeof(double),&local_block);
    MPI_Type_commit(&local_block);

    //----Rank 0 defines positions and counts of local blocks (2D-subdomains) on global matrix----//
    int * scatteroffset, * scattercounts;
    if (rank==0) {
        scatteroffset=(int*)malloc(size*sizeof(int));
        scattercounts=(int*)malloc(size*sizeof(int));
        for (i=0;i<grid[0];i++)
            for (j=0;j<grid[1];j++) {
                scattercounts[i*grid[1]+j]=1;
                scatteroffset[i*grid[1]+j]=(local[0]*local[1]*grid[1]*i+local[1]*j);
            }
    }


    //----Rank 0 scatters the global matrix----//

    //----Rank 0 scatters the global matrix----//

    MPI_Scatterv(&(U[0][0]), scattercounts, scatteroffset, global_block, &(u_previous[1][1]), 1, local_block, 0, MPI_COMM_WORLD);
    MPI_Scatterv(&(U[0][0]), scattercounts, scatteroffset, global_block, &(u_current[1][1]), 1, local_block, 0, MPI_COMM_WORLD);

     //************************************//

    if (rank==0)
        free2d(U);

        //----Define datatypes or allocate buffers for message passing----//

        //*************TODO*******************//

        /*Fill your code here*/

    MPI_Datatype local_horizontal_edge;
    MPI_Type_contiguous(local[1], MPI_DOUBLE, &local_horizontal_edge);
    MPI_Type_commit(&local_horizontal_edge);

    MPI_Datatype local_vertical_edge;
    MPI_Type_vector(local[0], 1, local[1] + 2, MPI_DOUBLE, &dummy);
    MPI_Type_create_resized(dummy,0,sizeof(double),&local_vertical_edge);
    MPI_Type_commit(&local_vertical_edge);


        //************************************//

    //----Find the 4 neighbors with which a process exchanges messages----//

        //*************TODO*******************//
    int north, south, east, west;

        /*Fill your code here*/

        /*Make sure you handle non-existing
                neighbors appropriately*/

    MPI_Cart_shift(CART_COMM, 0, 1, &north, &south);
    MPI_Cart_shift(CART_COMM, 1, 1, &west, &east);

        //************************************//

    //---Define the iteration ranges per process-----//
        //*************TODO*******************//

    int i_min,i_max,j_min,j_max;

        /*Fill your code here*/

        /*Three types of ranges:
                -internal processes
                -boundary processes
                -boundary processes and padded global array
        */
    int padding[2];

    // i_min
    if(rank_grid[0] == 0) {   // checking if we are in the first line (boundary)    
        i_min = 2;
    }
    else {
        i_min = 1;
    }

    // j_min
    if(rank_grid[1] == 0) { // checking if we are in the first column (boundary)
        j_min = 2;
    }
    else {
        j_min = 1;
    }

    // i_max
    if(rank_grid[0] == grid[0] - 1) {  //checking if we are in the last line (boundary) and for padding
        padding[0] = global_padded[0] - global[0];
        i_max = local[0] - padding[0] - 1;
    }
    else {
        i_max = local[0];
    }

    // j_max
    if(rank_grid[1] == grid[1] - 1) {  //checking if we are in the last column (boundary) and for padding
        padding[1] = global_padded[1] - global[1];
        j_max = local[1] - padding[1] - 1;
    }
    else {
        j_max = local[1];
    }


        //************************************//

    omega=2.0/(1+sin(3.14/global[0]));

        //----Computational core----//
    gettimeofday(&tts, NULL);
    
    #ifdef TEST_CONV
    for (t=0;t<T && !global_converged;t++) {
    #endif
    #ifndef TEST_CONV
    #undef T
    #define T 256
    for (t=0;t<T;t++) {
    #endif


                //*************TODO*******************//

                /*Fill your code here*/

                /*Compute and Communicate*/

                /*Add appropriate timers for computation*/

        swap=u_previous;
        u_previous=u_current;
        u_current=swap;

        // RED PIECES

        gettimeofday(&tcomms, NULL);

        if(north != MPI_PROC_NULL) {
            MPI_Sendrecv(&u_previous[1][1], 1, local_horizontal_edge, north, 0, 
                        &u_previous[0][1], 1, local_horizontal_edge, north, 0, MPI_COMM_WORLD, &status);
        }

        if(south != MPI_PROC_NULL) {
            MPI_Sendrecv(&u_previous[local[0]][1], 1, local_horizontal_edge, south, 0, 
                        &u_previous[local[0]+1][1], 1, local_horizontal_edge, south, 0, MPI_COMM_WORLD, &status);
        }

        if(east != MPI_PROC_NULL) {
            MPI_Sendrecv(&u_previous[1][local[1]], 1, local_vertical_edge, east, 0, 
                        &u_previous[1][local[1]+1], 1, local_vertical_edge, east, 0, MPI_COMM_WORLD, &status);
        }

        if(west != MPI_PROC_NULL) {
            MPI_Sendrecv(&u_previous[1][1], 1, local_vertical_edge, west, 0, 
                        &u_previous[1][0], 1, local_vertical_edge, west, 0, MPI_COMM_WORLD, &status);
        }

        gettimeofday(&tcommf, NULL);

        tcomm+=(tcommf.tv_sec-tcomms.tv_sec)+(tcommf.tv_usec-tcomms.tv_usec)*0.000001;

        gettimeofday(&tcomps, NULL);

        for(i = i_min; i <= i_max; i++) {
            for(j = j_min; j <= j_max; j++) {
                if ((i+j)%2==0)
                    u_current[i][j] = u_previous[i][j] + (omega/4.0) * (u_previous[i-1][j] + u_previous[i+1][j] + u_previous[i][j-1] + u_previous[i][j+1] - 4*u_previous[i][j]);
            }
        }

        gettimeofday(&tcompf, NULL);

        tcomp+=(tcompf.tv_sec-tcomps.tv_sec)+(tcompf.tv_usec-tcomps.tv_usec)*0.000001;

        // BLACK PIECES

        gettimeofday(&tcomms, NULL);

        if(north != MPI_PROC_NULL) {
            MPI_Sendrecv(&u_current[1][1], 1, local_horizontal_edge, north, 0, 
                        &u_current[0][1], 1, local_horizontal_edge, north, 0, MPI_COMM_WORLD, &status);
        }

        if(south != MPI_PROC_NULL) {
            MPI_Sendrecv(&u_current[local[0]][1], 1, local_horizontal_edge, south, 0, 
                        &u_current[local[0]+1][1], 1, local_horizontal_edge, south, 0, MPI_COMM_WORLD, &status);
        }

        if(east != MPI_PROC_NULL) {
            MPI_Sendrecv(&u_current[1][local[1]], 1, local_vertical_edge, east, 0, 
                        &u_current[1][local[1]+1], 1, local_vertical_edge, east, 0, MPI_COMM_WORLD, &status);
        }

        if(west != MPI_PROC_NULL) {
            MPI_Sendrecv(&u_current[1][1], 1, local_vertical_edge, west, 0, 
                        &u_current[1][0], 1, local_vertical_edge, west, 0, MPI_COMM_WORLD, &status);
        }

        gettimeofday(&tcommf, NULL);

        tcomm+=(tcommf.tv_sec-tcomms.tv_sec)+(tcommf.tv_usec-tcomms.tv_usec)*0.000001;

        gettimeofday(&tcomps, NULL);

        for(i = i_min; i <= i_max; i++) {
            for(j = j_min; j <= j_max; j+=2) {
                 if ((i+j)%2==1)
                     u_current[i][j] = u_previous[i][j] + (omega/4.0) * (u_current[i-1][j] + u_current[i+1][j] + u_current[i][j-1] + u_current[i][j+1] - 4*u_previous[i][j]);
            }
        }

        gettimeofday(&tcompf, NULL);

        tcomp+=(tcompf.tv_sec-tcomps.tv_sec)+(tcompf.tv_usec-tcomps.tv_usec)*0.000001;

        #ifdef TEST_CONV
        if (t%C==0) {
                        //*************TODO**************//
                        /*Test convergence*/
            converged = converge(u_previous, u_current, i_min, i_max, j_min, j_max);

            MPI_Reduce(&converged, &global_converged, 1, MPI_INT, MPI_MIN, 0, MPI_COMM_WORLD);
            MPI_Bcast(&global_converged, 1, MPI_INT, 0, MPI_COMM_WORLD);    

        }
        #endif

                //************************************//



    }
    gettimeofday(&ttf,NULL);

    ttotal=(ttf.tv_sec-tts.tv_sec)+(ttf.tv_usec-tts.tv_usec)*0.000001;

    MPI_Reduce(&ttotal,&total_time,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);
    MPI_Reduce(&tcomp,&comp_time,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);
    MPI_Reduce(&tcomm,&comm_time,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);



    //----Rank 0 gathers local matrices back to the global matrix----//

    if (rank==0) {
            U=allocate2d(global_padded[0],global_padded[1]);
    }
        //*************TODO*******************//

        /*Fill your code here*/

    MPI_Gather(&u_current[1][1], 1, local_block, &U[0][0], 1, global_block, 0, MPI_COMM_WORLD);

     //************************************//


        //----Printing results----//

        //**************TODO: Change "Jacobi" to "GaussSeidelSOR" or "RedBlackSOR" for appropriate printing****************//
    if (rank==0) {
        printf("RedBlackSOR X %d Y %d Px %d Py %d Iter %d ComputationTime %lf CommunicationTime %lf TotalTime %lf midpoint %lf\n",global[0],global[1],grid[0],grid[1],t,comp_time,comm_time,total_time,U[global[0]/2][global[1]/2]);

        #ifdef PRINT_RESULTS
        char * s=malloc(50*sizeof(char));
        sprintf(s,"resJacobiMPI_%dx%d_%dx%d",global[0],global[1],grid[0],grid[1]);
        fprint2d(s,U,global[0],global[1]);
        free(s);
        #endif

    }
    MPI_Finalize();
    return 0;
}

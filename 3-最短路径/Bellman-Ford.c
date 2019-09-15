#include <stdio.h>

#define EDGES 7
#define INF 999

void Print(int (*p)[50],int cow,int col){
    
    int i,j;
    for(i=0;i<cow;i++){
        for(j=0;j<col;j++){
            printf("%-5d",p[i][j]);
        }
        printf("\n");
    }
}

int main(){

int edge[EDGES][3]={{0,1,100},{0,2,30},{0,4,10},{4,3,50},{3,1,10},{2,1,60},{2,3,60}};

struct graph{
    int vertex;
    int edge;
    int a[50][50];
    int distance[50][50];
};
struct graph GR;
struct graph *G = &GR;

int i,j,k, from;
int vertex = 5;

//创建地图
G->vertex = vertex;
for(i=0;i<vertex;i++){
    for(j=0;j<vertex;j++){
        G->a[i][j] = INF;
        G->distance[i][j] = INF;
    }
}

G->edge = EDGES;
for(i=0;i<EDGES;i++){
    G->a[edge[i][0]][edge[i][1]] = edge[i][2];
    //G->edge++;
}


//核心算法代码
/*主要的思想：最短路径无非是直达或者通过另一个顶点转车一下。
扫描所有能够转车的顶点，比较路劲大小，就可以找到最短的路径
*/
/*算法流程：


*/

/*
时间复杂度o(N*M) N 为城市数量，M为边的数量
空间复杂度o(N)
*/
//从
from = 0;
G->distance[from][from] = 0;
for(k=0; k < vertex; k++)
    for(i=0; i < G->edge; i++)
            if(G->distance[from][edge[i][1]] > G->distance[from][edge[i][0]] + edge[i][2])
                G->distance[from][edge[i][1]] = G->distance[from][edge[i][0]] + edge[i][2];

printf("graph\n");
Print(G->a,vertex,vertex);
printf("distance\n");
Print(G->distance,vertex,vertex);
}



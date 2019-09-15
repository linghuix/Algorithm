#include <stdio.h>

#define EDGES 9
#define INF 999
int stack[50],top=0;
//输出二维数组
void Print(int (*p)[50],int cow,int col){
    
    int i,j;
    for(i=0;i<cow;i++){
        for(j=0;j<col;j++){
            printf("%-5d",p[i][j]);
        }
        printf("\n");
    }
}

//打印其中一条路径
int PS(int i, int (*p),int from){
    
    if(p[i] == from){
        printf("%d->",from);
        return i;
    }
    int m = PS(p[i],p,from);
    printf("%d->",m);
    return i;
}


int main(){
    
//边结构
int edge[EDGES][3]={{0,1,30},{0,2,30},{0,4,10},{4,3,50},{3,1,10},{2,1,50},{2,3,60},{4,2,10},{4,0,30}};

//图结构
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

//添加边
G->edge = EDGES;
for(i=0;i<EDGES;i++){
    G->a[edge[i][0]][edge[i][1]] = edge[i][2];
    G->distance[edge[i][0]][edge[i][1]] = edge[i][2];
    //G->edge++;
}



//核心算法代码
/*主要的思想：
(0,4)的最短路径为 = (0,4)||(0,2)+min(2,4)||(0,1)+min(1,4)
*/
/*算法流程：


*/

/*
时间复杂度o(N^2) N 为城市数量，M为边的数量
空间复杂度o(N)
*/
//从
from = 4;

//已经找到最短距离的点
int complete[5] = {0};
complete[from] = 1;

//记录最短路径中，某顶点的前一个顶点，可以存储多种路径。
int pre[5];
//一开始，每个顶点的上一个顶点都被设为是起点。也就是没有转车直达每个顶点的距离。
for(j=0;j<5;j++){
    pre[j] = from;
}

G->distance[from][from] = 0;


//寻找当前离起点最小的顶点
int min,v;
v = from;
for(j =1; j < vertex; j++){
    
    min=INF;
    for(i=0;i<vertex;i++){
        if(complete[i] != 1){
            if(min >  G->distance[from][i]){
                min = G->distance[from][i];
                v = i;
            }
            // printf("i=%d\n",i);
        }
    }
    // printf("v=%d\n",v);
    complete[v] = 1;
    
    for(i=0;i<vertex;i++){
        if(G->distance[v][i] != INF && complete[i] != 1){
            printf("%d  %d  %d  %d\n",G->distance[from][i],G->distance[from][v],G->distance[v][i],i);
            
            if(G->distance[from][i] > G->distance[from][v] + G->distance[v][i]){
                G->distance[from][i] = G->distance[from][v] + G->distance[v][i];
                pre[i] = v;
            }
        }
    }
    
    // for(i=0;i<5;i++)
        // printf("%-5d",complete[i]);
}

printf("graph\n");
Print(G->a,vertex,vertex);
printf("distance\n");
Print(G->distance,vertex,vertex);
printf("pre\n");
for(j=0;j<5;j++){
    printf("%-5d",pre[j]);
}
printf("\n");


for(i=0;i<vertex;i++){
    printf("from %d to %d = %d\n", from,i,G->distance[from][i]);
    printf("路径：");
    printf("%d\n", PS(i,pre,from));
}

}



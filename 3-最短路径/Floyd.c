#include <stdio.h>

#define EDGES 7
#define INF 999

typedef struct graph *MGraph;

struct graph{
    int vertex;
    int edge;
    int a[50][50];
    int distance[50][50];
    int path[50][50];           //记录路径
};

void Print(int (*p)[50],int cow,int col){
    
    int i,j;
    for(i=0;i<cow;i++){
        for(j=0;j<col;j++){
            printf("%-5d",p[i][j]);
        }
        printf("\n");
    }
}


//核心算法代码
/*主要的思想：最短路径无非是直达或者通过另一个顶点转车一下。
扫描所有能够转车的顶点，比较路劲大小，就可以找到最短的路径
*/
/*算法流程：
首先存储直达的距离，无法到达顶点距离用inf表示。
然后，限制只能从顶点0转车，与直达比较获取最短路径.结果是转车和从0转这两种情况的最短路径
随后，限制只能从顶点1转车，由于此时最短路径已经根据从顶点0转车更新过了，所以这次迭代，比较最短路径时后的结果其实是，直达或者从顶点0或者顶点1或者从0和1转车的最短路径。
依次迭代，直到所有顶点都扫描一遍，得到每个点之间的最短路径。无法到达的点距离为inf
*/

/*
时间复杂度o(N^3)
空间复杂度o(N^2)
*/
int Floyd(MGraph G){
    int k,i,j;
    for(k=0;k<G->vertex;k++){
        for(i=0;i<G->vertex;i++){
            for(j=0;j<G->vertex;j++){
                if(G->distance[i][j] > G->distance[i][k]+G->distance[k][j]){
                    
                    G->distance[i][j] = G->distance[i][k]+G->distance[k][j];
                    G->path[i][j] = k;                                          //记录ij之间需要中转的顶点k，可以使用递归打印路径
                    if(i==j && G->distance[i][j]<0){
                        printf("地图存在负值圈！\n");
                        return 0;
                    }
                }
            }
        }
    }
    return 1;
}

//打印路径
void Path(MGraph G,int i,int j){
    
    int k = G->path[i][j];
    if(k != -1 && k!=-INF){
        Path(G,i,k);
        // printf("%-5d",k);
        Path(G,k,j);
    }
    else if(k==-1)          //无中间节点
    {
        printf("%d->%d ",i,j);
    }
    else if(k == -INF){
        printf("\n%d->%d无法到达\n",i,j);
    }
}

int main(){

    int edge[EDGES][3]={{0,1,100},{0,2,30},{0,4,10},{4,3,50},{3,1,10},{2,1,60},{2,3,60}};

    struct graph GR;
    struct graph *G = &GR;

    int i,j,k;
    int vertex = 5;

    //创建地图
    G->vertex = vertex;
    for(i=0;i<vertex;i++){
        for(j=0;j<vertex;j++){
            G->a[i][j] = INF;
            G->distance[i][j] = INF;
            G->path[i][j] = -INF;//表明两点无法到达
            if(i==j) G->path[i][j] = -1;
        }
    }

    //添加边
    G->edge = 0;
    for(i=0;i<EDGES;i++){
        G->a[edge[i][0]][edge[i][1]] = edge[i][2];
        G->distance[edge[i][0]][edge[i][1]] = edge[i][2];
        G->path[edge[i][0]][edge[i][1]] = -1;       //表明无中间转点
        G->edge++;
    }

    //初始化最短距离
    for(i=0;i<vertex;i++)
        for(j=0;j<vertex;j++)
            G->distance[i][j] = G->a[i][j];

    if(Floyd(G)){
        
        printf("graph\n");
        Print(G->a,vertex,vertex);
        printf("distance\n");
        Print(G->distance,vertex,vertex);
        printf("path\n");
        Print(G->path,vertex,vertex);
    }
    
    printf("打印i到j的路径：\n");
    Path(G,1,4);
}



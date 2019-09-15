#include <stdio.h>
#include <stdlib.h>
//-------------------------------------------------------------------------------
#define StackSize 50 

//类型定义 

typedef char ElementType;

typedef struct stack* Stack;
struct stack{
    
    ElementType data[StackSize];    //数组data用于存放表结点，结点中的元素的类型设定为int 
    int top;                        //满栈顶，指向数据 
};

int Contain(ElementType d,Stack L){
    int i;
    
    for(i=0;i<=L->top;i++){
        if(d==L->data[i])
            return 1;
    }
    return 0;
}

//初始化将表的长度设置为0
Stack CreateStack(){
    
    Stack s = (Stack)malloc(sizeof(struct stack));
    s->top = -1; 
    return s;
} 

//清空堆栈
void Clear(Stack L){
    L->top = -1; 
    
}

//清空堆栈
void Delete(Stack L){
    if (L != NULL) 
        free(L); 
    L = NULL;
}

//判断栈是否空 
int IsEmpty (Stack L){
    
    return L->top == -1;
}


//判断栈是否满,  true为满
int IsFull(Stack L ){
    
    return L->top == StackSize - 1;
} 


//进栈 
void Push(ElementType x, Stack L){
    
    if(IsFull(L)) printf("Stack full\n");
    L->data[++ L->top] = x; 
} 


//退栈
ElementType Pop(Stack L){
    
    if(IsEmpty(L)) printf("Stack empty\n");
    return L->data[ L->top--];
}


//取栈顶元素 
ElementType StackTop(Stack L){
    
    if(IsEmpty(L)) printf("Stack empty\n");
    return L->data[L->top];
}

Stack Copy(Stack L){
    int i;
    Stack n = CreateStack();
    
    for(i=0;i<=L->top;i++){
        n->data[i] = L->data[i];
    }
    n->top = L->top;
    
    return n;
}

void print(Stack L,int flag){
    
    int i;
    //flag = 1
    if(flag){
        for(i=0;i<=L->top;i++){
            printf("%-5d",L->data[i]);
        }
        //printf("\n");
    }
    else{
        for(i=L->top;i>=0;i--){
            printf("%-5d",L->data[i]);
        }
    }
    
}

//-----------------------------
#define Vertex 6
#define EDGES 13
#define INF 999

//图结构
struct graph{
    // int Vertex;
    int edge;
    int a[50][50];
    int distance[50][50];
};

//打印从%d到%d的所有可能的路径
//算法复杂度 vertex^vertex
/*算法原理

从初始点，扫描相邻的可到达的点，将点压入堆栈，如果点为目标点，那么直接打印堆栈内容即为路径。如果不是目标点，并且该点不在堆栈中(为了防止重复的顶点1-0-1-0-1-0这样扫描)，那么以该点为初始点进行递归。 
注意，为了实现，路径随着顶点的变化而自动的更新，stack数据结构是当做参数传递进去的，而且每次传入的都是stack的拷贝

所以该算法无论是空间还是时间都是十分昂贵的
*/

void PrintRoute(int (*p)[50],int from, int to,Stack stack){
    
    int i;
    
    Push(to,stack);
    //printf("from = %d\n",from);
    
    for(i=0;p[to][i]!=-1;i++){
        if(!Contain(i,stack)){
            
            if(p[to][i] == from){
                Push(from,stack);
                print(stack,0);
                printf("\n");
            }
            else{
                PrintRoute(p,from,p[to][i],Copy(stack));
            }
        }
    }
    Delete(stack);
}
//---------------------------------------------------


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
int PS(int i, int (*p)[50],int from){
    
    if(p[i][0]==from){
        printf("%d->",from);
        return i;
    }
    int m = PS(p[i][0],p,from);
    printf("%d->",m);
    return i;
}


int main(){
    
    //边结构
    int edge[EDGES][3]={{0,1,30},{0,2,30},{0,4,10},{4,3,50},{3,1,10},{2,1,50},{2,3,60},{4,2,10},{4,0,30},{4,1,60},{5,1,20},{2,5,30},{4,5,40}};

    struct graph GR;
    struct graph *G = &GR;

    int i,j,k, from;
    // int Vertex = 6;

    //创建地图
    // G->Vertex = Vertex;
    for(i=0;i<Vertex;i++){
        for(j=0;j<Vertex;j++){
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
    首先从起点0开始选择直达的其他顶点
    (0,4)的最短路径为 = (0,4)||(0,2)+min(2,4)||(0,1)+min(1,4)||(0,3)+min(3,4)||(0,5)+min(5,4)||...
    只要(0,4)<(0,1)&&(0,2)&&(0,3)&&... 就可以确定(0,4)的最短路径必为(0,4)
    然后利用(0,4)去查看，仅通过4转车能否缩短(0,1),(0,2),(0,3),(0,5)...的路径，并更新
    
    然后同理查找剩余的顶点。(0,6) = (0,6)||(0,1)+min(1,6)||...||(0,4)+min(4,6)...
    因为上一步的更新，(0,x)已经是(0,4)+(4,x)和(0,x)的最小值了,所以(0,4)+min(4,6)>=(0,x)+min(x,6),(0,6)>=(0,4)+(4,6),不管min(4,6)不管中途转不转车，都是逃不出上面的两个等式的。所以当(0,6)<(0,1)&&(0,2)&&(0,3)&&(0,5)...(不许要小于(0,4))就可以确定(0,6)最短路径必为当前的(0,6)
    
    */
    /*算法流程：
    有上述思想可知：
    首先建立一个数组，保存从起点到其余点的直达距离，无法直达的用inf表示
    从数组中找出最小直达距离，必为到该点的最短距离。
    
    然后，根据图更新其余距离
    
    随后重复从数组中找到最小距离(除了上述确定最短距离的点)，必为到该点的最短距离

    */

    /*
    时间复杂度o(N^2) N 为城市数量
    空间复杂度o(N)
    */
    //从
    from = 4;

    //已经找到最短距离的点
    int complete[Vertex] = {0};
    complete[from] = 1;

    //记录最短路径中，某顶点的前一个顶点，可以存储多种路径。
    int pre[Vertex][50];
    for (i=0;i<Vertex;i++){
        for(j=0;j<50;j++){
            pre[i][j] = -1;
        }
    }
    //一开始，每个顶点的上一个顶点都被设为是起点。也就是没有转车直达每个顶点的距离。
    for(j=0;j<Vertex;j++){
        pre[j][0] = from;
    }

    G->distance[from][from] = 0;


    //寻找当前离起点最小的顶点
    int min,v;
    v = from;
    
    
    //到达每个顶点的路径数目
    int flag[Vertex]={0};
    // int flag = 0;

    for(j =1; j < Vertex; j++){
        
        min=INF;
        for(i=0;i<Vertex;i++){
            if(complete[i] != 1){
                if(min >  G->distance[from][i]){
                    min = G->distance[from][i];
                    // pre[v][flag] = i;
                    v = i;
                }
                // printf("i=%d\n",i);
            }
        }
        // printf("v=%d\n",v);
        complete[v] = 1;
        
        for(i=0;i<Vertex;i++){
            // printf("f=%d\n",flag);
            // if(G->distance[v][i] != INF && complete[i] != 1) 确定最短路径的也有可能还有相同的最短路径
            if(G->distance[v][i] != INF){
                printf("%d  %d  %d  %d\n",G->distance[from][i],G->distance[from][v],G->distance[v][i],i);
                //由于算法的特性，每次路径更新，v必定是i顶点的前一个顶点，所以记录下来
                if(G->distance[from][i] > G->distance[from][v] + G->distance[v][i]){
                    G->distance[from][i] = G->distance[from][v] + G->distance[v][i];
                    pre[i][flag[i]] = v;
                    flag[i] = 0;
                    while(pre[i][++flag[i]] != -1){pre[i][++flag[i]] = -1;}
                    flag[i] = 0;
                }
                //相同长度的路径，记录前一个顶点到另一个维度
                else if(G->distance[from][i] == G->distance[from][v] + G->distance[v][i] && v!=from && v!=i){
                    pre[i][++flag[i]] = v;
                }
            }
        }
        
        // for(i=0;i<5;i++)
            // printf("%-5d",complete[i]);
    }

    printf("graph\n");
    Print(G->a,Vertex,Vertex);
    printf("distance\n");
    Print(G->distance,Vertex,Vertex);
    printf("pre\n");
    Print(pre,Vertex,6);

// int route[]
// for(i=0;i<Vertex;i++)
    // route[i] = pre[i][0];
        printf("达到每个顶点的前顶点可选择数目：");
        for(i=0;i<Vertex;i++)
            printf("%-5d",flag[i]+1);

    int to;
    for(to=0;to<Vertex;to++){
        j = 0;
        printf("from %d to %d = %d\n", from,to,G->distance[from][to]);
        
        printf("路径：");
        printf("%d\n", PS(to,pre,from));
        
        while(pre[to][++j] != -1){
            pre[to][0] = pre[to][j];
            printf("路径：");
            printf("%d\n", PS(to,pre,from));
            j++;
        }
    }
}



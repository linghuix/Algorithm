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



//------------------------------------------------------------------------//


#define EDGES 9
#define INF 999
int stack[50],top=0;

//图结构
struct graph{
    int vertex;
    int edge;
    int a[50][50];
    int distance[50][50];
    int IsVisited[50];
};


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

//打印从%d到%d的所有可能的路径
//算法复杂度 vertex^vertex
/*算法原理

从初始点，扫描相邻的可到达的点，将点压入堆栈，如果点为目标点，那么直接打印堆栈内容即为路径。如果不是目标点，并且该点不在堆栈中(为了防止重复的顶点1-0-1-0-1-0这样扫描)，那么以该点为初始点进行递归。 
注意，为了实现，路径随着顶点的变化而自动的更新，stack数据结构是当做参数传递进去的，而且每次传入的都是stack的拷贝

所以该算法无论是空间还是时间都是十分昂贵的
*/

void PrintRoute(struct graph *G,int from, int to,Stack stack){
    
    int i;
    
    Push(from,stack);
    //printf("from = %d\n",from);
    
    for(i=0;i<G->vertex;i++){
        if(G->a[from][i] != INF && !Contain(i,stack)){
            
            if(i == to){
                print(stack,1);
                printf("%-5d",to);
                printf("\n");
            }
            else{
                PrintRoute(G,i,to,Copy(stack));
            }
        }
    }
    Delete(stack);
}


int main(){
    
    //边结构
    // int edge[EDGES][3]={{0,1,30},{0,2,30},{0,4,10},{4,3,50},{3,1,10},{2,1,50},{2,3,60},{4,2,10},{4,0,30}};
    int edge[EDGES][3]={{0,1,30},{1,2,10},{1,3,50},{3,2,10},{3,4,50}};


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
        }
    }

    //添加边
    G->edge = EDGES;
    for(i=0;i<EDGES;i++){
        G->a[edge[i][0]][edge[i][1]] = edge[i][2];
        G->a[edge[i][1]][edge[i][0]] = edge[i][2];
        G->distance[edge[i][0]][edge[i][1]] = edge[i][2];
        //G->edge++;
    }
    
    for(i=0;i<vertex;i++){
        G->IsVisited[i] = 0;
    }

    int from = 0, to = 4;


    printf("graph\n");
    Print(G->a,vertex,vertex);
    printf("distance\n");
    Print(G->distance,vertex,vertex);


    Stack route;
    route = CreateStack();
    
    
    printf("\n\n");
    printf("打印从%d到%d的所有可能的路径\n",from,to);
    PrintRoute( G, from, to, route);
    printf("\n\n");

    
    return 0;
}



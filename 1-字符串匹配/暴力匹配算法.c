#include "stdio.h"
#include "string.h"
#include "time.h"

int next[50];

//暴力
int ViolentMatch(const char* s, const char* p)
{

    int sLen = strlen(s);
    int pLen = strlen(p);

    int count = 0;
    int i = 0;
    int j = 0;
    while (i < sLen && j < pLen)
    {
        if (s[i] == p[j])
        {
            //①如果当前字符匹配成功（即S[i] == P[j]），则i++，j++    
            i++;
            j++;
        }
        else
        {
            //②如果失配（即S[i]! = P[j]），令i = i - (j - 1)，j = 0    
            i = i - j + 1;
            j = 0;
        }
        // printf("%d\n",i);
        count++;
    }
    
    printf("暴力匹配次数：%5d\n", count);
    //匹配成功，返回模式串p在文本串s中的位置,从0开始，否则返回-1
    if (j == pLen)
        return i - j;
    else
        return -1;
}


//reference:https://blog.csdn.net/v_july_v/article/details/7041827
int KmpSearch(const char* s, const char* p)
{
    int i = 0;  //s字符串的指针
    int j = 0;  //p字符串的指针
    int count = 0;
    
    int sLen = strlen(s);
    int pLen = strlen(p);
    // printf("count = %d\n",count);
    while (i < sLen && j < pLen)
    {
        //①如果j = -1，或者当前字符匹配成功（即S[i] == P[j]），都令i++，j++    
        if (j == -1 || s[i] == p[j])
        {
            i++;
            j++;
        }else
        {
            //②如果j != -1，且当前字符匹配失败（即S[i] != P[j]），则令 i 不变，j = next[j]    
            //next[j]即为j所对应的next值      
            j = next[j];
        }
        // printf("%d  %d\n",i,j);
        count++;
    }
    
    printf("Kmp匹配次数：%5d\n", count);
    
    if (j == pLen)
        return i - j;
    else
        return -1;
}


//递归思想 - 从已知的结果去如何去推断未知的结果
//nest数组表示，
void GetNext_1(const char *p,int next[])
{
    int pLen = strlen(p);
    next[0] = -1;
    int k = -1;             //该字母之前，表示前缀和后缀相同的个数
    int j = 0;              //s字符串,扫描指针
    
    while (j < pLen - 1)
    {
        // printf("%c, %c\n",p[k],p[j]);
        //p[k]表示前缀，p[j]表示后缀
        if (k == -1 || p[j] == p[k]) 
        {
            //k = -1 表示next中的数值为0
            //同样的，next[0]=-1
            ++k, ++j;                       //扫描指针下移，继续匹配下一个字符；
            next[j] = k;
        }
        else                                //如果k不是-1，并且当前选定的字符串部分不匹配。那么递归
        {
            k = next[k];
        }
        // printf("k = %d %d\n",k,j);
    }
    
    // for(int i =0;i<pLen;i++)
        // printf("%-4d",next[i]);
    // printf("\n");
}

//优化过后的next 数组求法
void GetNext_2(const char* p, int next[])
{
    int pLen = strlen(p);
    next[0] = -1;
    int k = -1;
    int j = 0;
    while (j < pLen - 1)
    {
        //p[k]表示前缀，p[j]表示后缀
        //k = -1 表示next中的数值为0
        //同样的，next[0]=-1
        if (k == -1 || p[j] == p[k])
        {
            ++j;
            ++k;
            //较之前next数组求法，改动在下面4行
            if (p[j] != p[k])
                next[j] = k;   //之前只有这一行
            else
                //因为不能出现p[j] = p[ next[j ]]，所以当出现时需要继续递归，k = next[k] = next[next[k]]
                next[j] = next[k];
        }
        else
        {
            k = next[k];
        }
    }
    
    for(j =0;j<pLen;j++)
        printf("%-4d",next[j]);
    printf("\n");
}



int main(){
    

    clock_t start, finish;
    double  duration;
    int i;
   
    int index,kmp_index;
    
    const char *s = "BBC ABCDAB ABCDABCDABDEABCAB";
    const char *p = "ABCAB";

    start = clock();
    for(i=0;i<100;i++)
        index = ViolentMatch(s,p);
    finish = clock();
    duration = (double)(finish - start) / CLOCKS_PER_SEC/100.0;
    printf( "%.10f seconds\n", duration );
    
    start = clock();
    for(i=0;i<100;i++){
        GetNext_2(p, next);
        kmp_index = KmpSearch(s,p);
    }
    finish = clock();
    duration = (double)(finish - start) / CLOCKS_PER_SEC/100.0;
    printf( "%.10f seconds\n", duration );

   
    printf("%-5d%-5d\n",index,kmp_index);
    
    return 0;
}
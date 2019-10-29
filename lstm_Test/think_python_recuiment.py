def factorial(n):
    space=' '*(4*n)
    print(space,'factorial',n)
    if n==0:
        print(space,'returning1')
        return 1
    else:
        recurse=factorial(n-1)
        result=n*recurse
        print(space,'returning',result)
    return result
 
if __name__ == "__main__":   
    g=factorial(4)
    print("resulting = ",g)
#include <stdio.h>
#include <cs50.h>

int main(void){
    // char answer[30];
    // printf("Enter your first name: ");
    // scanf("%s", answer);
    string answer = get_string("Enter you name: ");
    printf("hello, %s\n", answer);
    return 0;
}

#include <stdio.h>

int main() {
    int branch;
    
    printf("Enter a number (1-4) ");
    scanf("%d", &branch);
    switch(branch) {
        case 1:
            printf("Btect CSE\n");
            break;
	case 2:
            printf("Btech AIML\n");
            break;
	case 3:
            printf("Btech ECE\n");
            break;
        case 4:
            printf("Btech Mechanic\n");
            break;
       default:
            printf("Invalid input! Please enter a number between 1 and 4.\n");
    }
    
    return 0;
}

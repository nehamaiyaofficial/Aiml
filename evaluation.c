#include <stdio.h>

int main() {
    int branch;
    
    printf("Enter a number (1-4) ");
    scanf("%d", &branch);
    switch(branch) {
        case 1:
            printf("Btect CSE College Amity University\n");
            break;
	case 2:
            printf("Btech AIML\n");
            break;
	case 3:
            printf("Btech ECE\n");
            break;
        case 4:
            printf("Btech Mechanics\n");
            break;
       default:
            printf("Invalid input!`\n");
    }
    
    return 0;
}

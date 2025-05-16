#include <stdio.h>

int main() {
    int branch;
    
    printf("Enter a number (1-4) ");
    scanf("%d", &branch);
    switch(branch) {
        case 1:
            printf("Btect aiml College Amity University\n");
            break;
	case 2:
            printf("Btech cse\n");
            break;
	case 3:
            printf("Btech ECE\n");
            break;
        case 4:
            printf("Btech biotic\n");
            break;
       default:
            printf("Invalid input!\n");
=======
            printf("Btech Mechanics\n");
            break;
       default:
            printf("Invalid input!`\n");
    }
    
    return 0;
}

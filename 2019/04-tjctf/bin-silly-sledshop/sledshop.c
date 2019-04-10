#include <stdio.h>
#include <stdlib.h>

void shop_setup() {
    gid_t gid = getegid();
    setresgid(gid, gid, gid);
    setbuf(stdout, NULL);
}

void shop_list() {
    printf("The following products are available:\n");
    printf("|  Saucer  | $1 |\n");
    printf("| Kicksled | $2 |\n");
    printf("| Airboard | $3 |\n");
    printf("| Toboggan | $4 |\n");
}

void shop_order() {
    int canary = 0;
    char product_name[64];

    printf("Which product would you like?\n");
    gets(product_name);

    if (canary){
        printf("Sorry, we are closed.\n");
    }else{
        printf("Sorry, we don't currently have the product %s in stock. Try again later!\n", product_name);
    }
}

int main(int argc, char **argv) {
    shop_setup();
    shop_list();
    shop_order();
    return 0;
}

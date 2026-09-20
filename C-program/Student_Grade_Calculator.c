#include <stdio.h>


int main(){
    char name[50] = "";
    printf("Enter students name = ");
    scanf("%49s",name);

    long roll_id ;
    printf("Enter student's ID = ");
    scanf("%ld",&roll_id);

    char branch[50] = "";
    printf("Enter student's branch = ");
    scanf("%49s",branch);

    int math , sci , marathi , hindi , eng , sst ;

    printf("Enter marks of respective subjects given below :\n "); // out of 100 

    printf("Mathematics = ");
    scanf("%d",&math);

    printf("Science = ");
    scanf("%d",&sci);

    printf("Marathi = ");
    scanf("%d",&marathi);

    printf("Hindi = ");
    scanf("%d",&hindi);

    printf("English = ");
    scanf("%d",&eng);

    printf("Social Studies = ");
    scanf("%d",&sst);


    int total_marks = math + eng + sci + sst + marathi + hindi ;
    float per = (float)total_marks/6 ;

    printf("------------------- Welcome to XYZ School of Engineering -------------------\n\n");
    printf("Name = %s\n",name);
    printf("Branch = %s\n",branch);
    printf("Roll No. = %ld\n\n",roll_id);

    printf("Mathematics = %d\n",math);
    printf("English = %d\n",eng);
    printf("Science = %d\n",sci);
    printf("Social Studies = %d\n",sst);
    printf("Marathi = %d\n",marathi);
    printf("Hindi = %d\n\n\n",hindi);


    if((per >=90)&&(per <=100)){
        printf("Grade = O\n");
    }else if((per >= 80) && (per <= 89)){
        printf("Grade = A+\n");
    }else if((per >=70)&&(per <=79)){
        printf("Grade = A\n");
    }else if((per >= 60) && (per <= 69)){
        printf("Grade = B+\n");
    }else if((per >=50)&&(per <=59)){
        printf("Grade = B\n");
    }else if((per >= 40) && (per <= 49)){
        printf("Grade = C\n");
    }else{
        printf("Grade = F\n");
    }
    printf("Total Marks = %d\n",total_marks);
    printf("Percentage = %2.f%%\n",per);
    printf("Congratulations !!");

    return 0;
}
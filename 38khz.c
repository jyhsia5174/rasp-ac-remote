#include <stdio.h>
#include <pigpiod_if2.h> 
#include <time.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

void udelay(int us){
  struct timespec st_t, ed_t;
  clock_gettime(CLOCK_REALTIME, &st_t);
  st_t.tv_sec += (st_t.tv_nsec + 1000 * us) / 1000000000;
  st_t.tv_nsec = (st_t.tv_nsec + 1000 * us) % 1000000000;

  while(1){
    clock_gettime(CLOCK_REALTIME, &ed_t);
    if( ed_t.tv_sec >= st_t.tv_sec && ed_t.tv_nsec >= st_t.tv_nsec )
      break;
  }
  
  //printf("nanotime: %10jd.%09ld\n", (intmax_t) ed_t.tv_sec, ed_t.tv_nsec);
}

#define GPIO3 3
#define GPIO4 4
#define PI_OFF 0
#define PI_ON 1

#define SHIFT 400
#define P3370 3380
#define P1640 1640
#define P400 400
#define P500 500
#define P1280 1280


void pulse(int pi, int on_t, int off_t){
  hardware_clock(pi, GPIO4, 38000);
  udelay(on_t);
  hardware_clock(pi, GPIO4, 0);
  udelay(off_t-SHIFT);
}

int main(int argc, char **argv){
  if(argc < 2){
    perror("Usage: ./38khz file");
    exit(1);
  }

  char *fname = argv[1];
  int pi;
  if ( (pi = pigpio_start(NULL, NULL)) < 0)
  {
     // pigpio initialisation failed.
     printf("init failed.\n");
     return 1;
  }
  else
  {
    FILE *fp = fopen(fname, "r");

    if( fp != NULL ){
      int bit[344];
      for(int i = 0; i < 344; i++)
        fscanf(fp, "%d", bit+i);
        //bit[i] = 0;

      pulse(pi, P3370, P1640);
      for(int i = 0; i < 344; i++){
        if( bit[i] )
          pulse(pi, P400, P1280);
        else
          pulse(pi, P400, P500);
      }
      pulse(pi, P400, P500);
      fclose(fp);
    }
    hardware_clock(pi, GPIO4, 0);
  }
  return 0;
}

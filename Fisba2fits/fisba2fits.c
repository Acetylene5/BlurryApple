/*
 * fisba2fits.c
 * Neil Zimmerman
 * 30 Nov 2012
 * Adapted from Stefan Hippler's fisba.c;
 * fixes the nonconforming FITS header and row reversal problem.
 * tested with uShape 6.1 data
 *
 * This program depends on the cfitsio library, and local copies of the cfitsio .h files: fitsio2.h, fitsio.h, and longnam.h
 * To compile, do: gcc fisba2fits.c -lm -lcfitsio -o fisba2fits
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "fitsio2.h"

#define   MAX_FILE_NAME_LENGTH 160

int main (int argc, char *argv[])
{
  char    dat_fname[MAX_FILE_NAME_LENGTH], fits_fname[MAX_FILE_NAME_LENGTH], ow_fits_fname[MAX_FILE_NAME_LENGTH];
  char    data_id;
  int     row,col;
  int     comment_length;
  char    comment_string[1024];
  int     nonaperture_id;
  FILE    *fp1;
  fitsfile *fp2;  
  int     *iptr;

#ifdef DEBUG
  printf("%d, %s\n", argc, argv[1]);
#endif /* DEBUG */

  if (argc < 2){
    printf("uPhase input file (*.dat): ");
    scanf("%s", dat_fname);
  }
  else{
    strcpy(dat_fname, argv[1]);
  }
/*----- open input file (.dat) -----*/
  if ((fp1 = fopen(dat_fname,"rb")) == NULL) exit(1);
/*----- read uPhase header -----*/
  fread(&data_id,sizeof(char),1,fp1);
  fread(&row,sizeof(int),1,fp1);
  fread(&col,sizeof(int),1,fp1);
  fread(&nonaperture_id,sizeof(int),1,fp1);
  fread(&comment_length,sizeof(int),1,fp1);
  fread(comment_string,comment_length,1,fp1);

  printf("Header data: %2d %4d %4d %d %d\n", data_id, row, col, nonaperture_id, comment_length);
  comment_string[comment_length]=0;
  printf("Comment: %s\n", comment_string);

  if (data_id == 1){
    printf("Data set contains a FISBA/uPhase_2_HR surface deviations map in Angstroems\n");
  } else if (data_id == 2){
    printf("Data set contains a FISBA/uPhase_2_HR wave aberration map in Angstroems\n");
  } else if (data_id == 3){
    printf("Data set contains a FISBA/uPhase_2_HR raw phase map in 2PI/1024 units\n");
  } else if (data_id == 4){
    printf("Data set contains a FISBA/uPhase_2_HR intensity map in gray values\n");
  } else if (data_id == 21){
    printf("Data set contains a FISBA/uPhase_2_HR MTF map with double precision float values \n");
    printf("This is not yet implemented\n");
  } else {
    printf("No valid data ID found\n");
  }
/*----- read data -----*/
  iptr = (int*)malloc(row*col*sizeof(int));
  if (iptr == NULL) {
    printf("Error openiing output file\n");
  }
  if ( fread((void*)iptr,sizeof(int),row*col,fp1) != row*col ){
    printf("Error reading data\n");
  }
  reverse_rows(iptr, row, col);
/*----- open FITS output file -----*/
  long  firstpix = 1, naxis = 2;
  long naxes[2] = { col, row };
  long nelements = naxes[0] * naxes[1];
  int status = 0;         /* initialize status before calling fitsio routines */
  if (replace_substr(dat_fname, fits_fname, ".dat", ".fits") != 0)
  {
      printf("Error: \".dat\" substring not found in input file name %s", dat_fname);
      exit(1);
  }
  sprintf(ow_fits_fname, "!%s", fits_fname); /* Prepend exclamation point to overwrite an existing .fits file */
  fits_create_file(&fp2, ow_fits_fname, &status);
  fits_create_img(fp2, LONG_IMG, naxis, naxes, &status);
/*----- write data -----*/
  fits_write_img(fp2, TINT, firstpix, nelements, iptr, &status);
/*----- write uPhase-specific header keywords -----*/
  fits_write_key(fp2, TBYTE, "DATA_ID", &data_id, "uPhase/uShape data ID (1,2,3,4,21)", &status); 
  fits_write_key(fp2, TINT, "NONAPVAL", &nonaperture_id, "uPhase/uShape non-aperture value", &status); 
  fits_write_key(fp2, TSTRING, "ORIGIN", "AL Lab @ MPIA", "MPIA AO Lab", &status); 
  fits_write_key(fp2, TSTRING, "INSTRUME", "FISBA INTERFEROMETER", "uPhase 2 HR Interferometer", &status); 
/*----- close files -----*/
  fclose(fp1);
  fits_close_file(fp2, &status);
  fits_report_error(stderr, status);
  exit(0);
}

int reverse_rows(int *array, int Nrows, int Ncols)
{
  int r;
  int *array_cpy = (int *)malloc(Nrows*Ncols*sizeof(int));
  memcpy(array_cpy, array, Nrows*Ncols*sizeof(int));

  for(r = 0; r < Nrows; r++)
  {
    memcpy(&array[r*Ncols], &array_cpy[(Nrows - 1 - r)*Ncols], Ncols*sizeof(int)); 
  }

  free(array_cpy);
  return 0;
}

int replace_substr(char *old_str, char *new_str, char *old_substr, char *new_substr)
{
  char *p;

  if(!(p = strstr(old_str, old_substr)))  // Is 'old_substr' even in 'old_str'?
    return - 1;

  strncpy(new_str, old_str, p - old_str); // Copy old_str characters up to start of 'old_substr'
  new_str[p - old_str] = '\0';

  sprintf(new_str + (p - old_str), "%s%s", new_substr, p + strlen(old_substr));

  return 0;
}

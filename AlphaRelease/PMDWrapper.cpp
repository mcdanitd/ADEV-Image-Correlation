#include "PMDWrapper.h"

#include <stdio.h>
#include <string.h>

PMDWrapper::PMDWrapper() :
    initData(false),
    sourceData(0),
    dist(0),
    distCpy(0)
{

}

PMDWrapper::~PMDWrapper()
{
    if(sourceData != 0)
    {
        delete [] sourceData;
    }

    if(dist != 0)
    {
        delete [] dist;
    }

    if(distCpy != 0)
    {
        delete [] distCpy;
    }
}

int PMDWrapper::init()
{
    int res = 0;

    res = pmdOpenSourcePlugin(&dHnd,
                              SOURCE_PLUGIN,
                              SOURCE_PARAM);

    if(res != PMD_OK)
    {
        pmdGetLastError(0, err, 128);
        fprintf(stderr,
                "PMDWrapper::init()->Could not connect: %s\n",
                err);
        return false;
    }

    //printf("Opened sensor\n");

    res = pmdOpenProcessingPlugin (&pHnd, PROC_PLUGIN, PROC_PARAM);
    if (res != PMD_OK)
    {
        pmdGetLastError (0, err, 128);
        fprintf (stderr, "PMDWrapper::init()->Could not open processing plugin: %s\n", err);
        return false;
    }

    return true;
}

bool PMDWrapper::getData()
{
    int res = pmdUpdate(dHnd);

    if(res != PMD_OK)
    {
        pmdGetLastError(dHnd, err, 128);
        fprintf(stderr,
                "PMDWrapper::getData()->Could not transfer data: %s\n",
                err);
        pmdClose(dHnd);
        return false;
    }

    //printf("acquired image\n");

    res = pmdGetSourceDataDescription(dHnd,
                                      &dd);

    //printf("numRows: %d   numCols: %d\n", dd.img.numRows, dd.img.numColumns);

    if(res != PMD_OK)
    {
        pmdGetLastError(dHnd, err, 128);
        fprintf(stderr,
                "PMDWrapper::getData()->Could not get data description: %s\n",
                err);
        pmdClose(dHnd);
        return false;
    }

    //printf ("retrieved source data description\n");

    if(dd.subHeaderType != PMD_IMAGE_DATA)
    {
        fprintf(stderr, "PMDWrapper::getData()->Source data is not an image!\n");
        pmdClose(dHnd);
        return false;
    }

    if(initData == false)
    {
        dist = new float [dd.img.numRows * dd.img.numColumns];
        printf(" PMDWrapper::getData()->Created dist data!\n");

        distCpy = new float [dd.img.numRows * dd.img.numColumns];
        printf(" PMDWrapper::getData()->Created distCpy data!\n");

        sourceData = new char[dd.size];
        printf(" PMDWrapper::getData()->Created sourceData!\n");

        initData = true;
    }


    res = pmdGetSourceData(dHnd, sourceData, dd.size);
    if (res != PMD_OK)
    {
        pmdGetLastError(dHnd, err, 128);
        fprintf(stderr, "PMDWrapper::getData()->Could not get source data: %s\n", err);
        pmdClose(dHnd);
        return false;
    }

    return true;
}

int PMDWrapper::calcDistance()
{
    int res;

    res = pmdCalcDistances(pHnd,
                           dist,
                           dd.img.numColumns * dd.img.numRows * sizeof (float),
                           dd,
                           sourceData);

    if (res != PMD_OK)
    {
        pmdGetLastError(pHnd, err, 128);
        fprintf(stderr, "PMDWrapper::calcDistance()->Could not calculate distances: %s\n", err);
        pmdClose(pHnd);
        return false;
    }

    // Make a copy of this structure so other people have a chance...
    // Don't really want to hold up the sensor, want it to freewheel as
    // fast as it can
    memcpy(distCpy, dist, dd.img.numRows * dd.img.numColumns * sizeof(float));

//    printf ("PMDWrapper::calcDistance()->Middle distance: %f m\n",
//            distCpy[ (dd.img.numRows / 2) * dd.img.numColumns + dd.img.numColumns / 2]);



    return true;
}

bool PMDWrapper::close()
{
    pmdClose(dHnd);
    pmdClose(pHnd);

    return true;
}



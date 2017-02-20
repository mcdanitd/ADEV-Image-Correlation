#ifndef PMDWRAPPER_H
#define PMDWRAPPER_H


#include <pmdsdk2.h>

#define SOURCE_PLUGIN "C:\\PMD\\bin\\camboardpico"
#define SOURCE_PARAM ""
#define PROC_PLUGIN "C:\\PMD\\bin\\camboardpicoproc"
#define PROC_PARAM ""


class PMDWrapper
{

public:
    PMDWrapper();
    ~PMDWrapper();

    bool getData();
    int calcDistance();
    int init();
    bool close();

    float* getDist() { return distCpy; }
    char* getSourceData() { return sourceData; }
    PMDDataDescription* getDD() { return &dd; }

private:
    bool initData;
    char err[128];
    PMDDataDescription dd;
    char *sourceData;
    PMDHandle dHnd;
    PMDHandle pHnd;
    float *dist;
    float *distCpy;

};

#endif // PMDWRAPPER_H

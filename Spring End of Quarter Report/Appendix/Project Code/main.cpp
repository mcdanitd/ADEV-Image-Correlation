#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <csignal>


#include "PMDWrapper.h"

#include <QtNetwork/QUdpSocket>
#include <QByteArray>
#include <QDataStream>


PMDWrapper *p;

int main()
{

    auto lam = [] (int i)
    {
        if(p != 0) p->close();
        std::cout << "Exiting... " << i << std::endl;
        exit(0);
    };

    signal(SIGINT, lam);    // ^c
    signal(SIGABRT, lam);   // abort
    signal(SIGTERM, lam);   // sent by the 'kill' command
    //signal(SIGTSTP, lam);   // ^z

    p = new PMDWrapper();


    if(p->init() == false)
    {
        printf("Error grabbing data. Exiting."); // TODO add more debug
        exit(-1);
    }
    if(p->getData() == false) printf("Error grabbing data."); // TODO add more debug
    if(p->calcDistance() == false) printf("Error calculating distances."); // TODO add more debug



    PMDDataDescription *dd = p->getDD();
    float* imgData = p->getDist();
    char *sourceData = p->getSourceData();
    int numPix = dd->img.numColumns * dd->img.numRows;
    printf("col: %d  row: %d\n", dd->img.numColumns, dd->img.numRows);
//(dd.img.numRows / 2) * dd.img.numColumns + dd.img.numColumns / 2


    QUdpSocket udpSocket;
    QByteArray datagram;


    int ret;

    printf("Collecting... Press Control-C to quit and close camera...\n");
    while(1)
    {
        if(p->getData() == false) printf("Error grabbing data."); // TODO add more debug
        if(p->calcDistance() == false) printf("Error calculating distances."); // TODO add more debug


        dd = p->getDD(); // info about the image
        imgData = p->getDist(); // returns pointer to float image of distances

        //printf("%f\n", imgData[ 120*176/2 ]);

        // Set the first half of the image
        datagram.setRawData((const char*)imgData,
                            sizeof(float) * numPix / 2);
        if(datagram.size() < 1) printf("Problem setting datagram 1 data.\n");
        //printf("d1: %d\n", datagram.size());
        datagram[0]=1;

        ret = udpSocket.writeDatagram(datagram, QHostAddress::LocalHost, 12345);
        if(ret < 0) qDebug("ERROR dg1");


        // Set the second half of the image
        datagram.setRawData((const char*)(imgData + (numPix / 2)),
                            sizeof(float) * numPix / 2);
        if(datagram.size() < 1) printf("Problem setting datagram 2 data.\n");


        //printf("d2: %d\n", datagram.size());
        datagram[0]=2;


        ret = udpSocket.writeDatagram(datagram, QHostAddress::LocalHost, 12345);
        if(ret < 0) qDebug("ERROR dg2");
    }

}











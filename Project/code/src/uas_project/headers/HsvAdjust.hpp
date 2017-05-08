/*
*   Class for visually adjusting and finding the appropiate HSV segmentation values
*/

#ifndef _HSVADJUST_H_
#define _HSVADJUST_H_
#include <iostream>
#include "opencv2/opencv.hpp"
#include <string>

using namespace std;
using namespace cv;

class HsvAdjust
{
    public:
        HsvAdjust();
        void guiSegmentation(Mat img);
        Mat findContours(Mat img);
        Point2f getBallPosition(Mat img);
        void printValues();
    private:
        //slider values
        const int hSlider = 180;
        int hSliderMin;
        int hSliderMax;

        const int sSlider = 255;
        int sSliderMin;
        int sSliderMax;

        const int vSlider = 255;
        int vSliderMin;
        int vSliderMax;

        double hue;

        const int threshSlider = 1000;
        int areaThresh;
        int compactThresh;

        Point2f Center;
        float Radius;

        cv::Mat dst;
        cv::Mat imghsv;

        void on_trackbar( int);
        static void on_trackbar( int, void* );

};

#endif
